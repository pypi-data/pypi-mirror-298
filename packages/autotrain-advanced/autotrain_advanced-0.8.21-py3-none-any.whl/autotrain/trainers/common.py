"""
Common classes and functions for all trainers.
"""

import json
import os
import shutil
import time
import traceback

import requests
from accelerate import PartialState
from huggingface_hub import HfApi
from pydantic import BaseModel
from transformers import TrainerCallback, TrainerControl, TrainerState, TrainingArguments

from autotrain import is_colab, logger


ALLOW_REMOTE_CODE = os.environ.get("ALLOW_REMOTE_CODE", "true").lower() == "true"


def get_file_sizes(directory):
    file_sizes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_size_gb = file_size / (1024**3)  # Convert bytes to GB
            file_sizes[file_path] = file_size_gb
    return file_sizes


def remove_global_step(directory):
    for root, dirs, _ in os.walk(directory, topdown=False):
        for name in dirs:
            if name.startswith("global_step"):
                folder_path = os.path.join(root, name)
                print(f"Removing folder: {folder_path}")
                shutil.rmtree(folder_path)


def remove_autotrain_data(config):
    os.system(f"rm -rf {config.project_name}/autotrain-data")
    remove_global_step(config.project_name)


def save_training_params(config):
    if os.path.exists(f"{config.project_name}/training_params.json"):
        training_params = json.load(open(f"{config.project_name}/training_params.json"))
        if "token" in training_params:
            training_params.pop("token")
            json.dump(
                training_params,
                open(f"{config.project_name}/training_params.json", "w"),
                indent=4,
            )


def pause_endpoint(params):
    if isinstance(params, dict):
        token = params["token"]
    else:
        token = params.token
    endpoint_id = os.environ["ENDPOINT_ID"]
    username = endpoint_id.split("/")[0]
    project_name = endpoint_id.split("/")[1]
    api_url = f"https://api.endpoints.huggingface.cloud/v2/endpoint/{username}/{project_name}/pause"
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.post(api_url, headers=headers, timeout=120)
    return r.json()


def pause_space(params, is_failure=False):
    if "SPACE_ID" in os.environ:
        # shut down the space
        logger.info("Pausing space...")
        api = HfApi(token=params.token)

        if is_failure:
            msg = "Your training run has failed! Please check the logs for more details"
            title = "Your training has failed ❌"
        else:
            msg = "Your training run was successful! [Check out your trained model here]"
            msg += f"(https://huggingface.co/{params.username}/{params.project_name})"
            title = "Your training has finished successfully ✅"

        if not params.token.startswith("hf_oauth_"):
            try:
                api.create_discussion(
                    repo_id=os.environ["SPACE_ID"],
                    title=title,
                    description=msg,
                    repo_type="space",
                )
            except Exception as e:
                logger.warning(f"Failed to create discussion: {e}")
                if is_failure:
                    logger.error("Model failed to train and discussion was not created.")
                else:
                    logger.warning("Model trained successfully but discussion was not created.")

        api.pause_space(repo_id=os.environ["SPACE_ID"])
    if "ENDPOINT_ID" in os.environ:
        # shut down the endpoint
        logger.info("Pausing endpoint...")
        pause_endpoint(params)


def monitor(func):
    def wrapper(*args, **kwargs):
        config = kwargs.get("config", None)
        if config is None and len(args) > 0:
            config = args[0]

        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_message = f"""{func.__name__} has failed due to an exception: {traceback.format_exc()}"""
            logger.error(error_message)
            logger.error(str(e))
            if int(os.environ.get("PAUSE_ON_FAILURE", 1)) == 1:
                pause_space(config, is_failure=True)

    return wrapper


class AutoTrainParams(BaseModel):
    """
    Base class for all AutoTrain parameters.
    """

    class Config:
        protected_namespaces = ()

    def save(self, output_dir):
        """
        Save parameters to a json file.
        """
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, "training_params.json")
        # save formatted json
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.model_dump_json(indent=4))

    def __str__(self):
        """
        String representation of the parameters.
        """
        data = self.model_dump()
        data["token"] = "*****" if data.get("token") else None
        return str(data)

    def __init__(self, **data):
        """
        Initialize the parameters, check for unused/extra parameters and warn the user.
        """
        super().__init__(**data)

        if len(self.project_name) > 0:
            # make sure project_name is always alphanumeric but can have hyphens. if not, raise ValueError
            if not self.project_name.replace("-", "").isalnum():
                raise ValueError("project_name must be alphanumeric but can contain hyphens")

        # project name cannot be more than 50 characters
        if len(self.project_name) > 50:
            raise ValueError("project_name cannot be more than 50 characters")

        # Parameters not supplied by the user
        defaults = set(self.model_fields.keys())
        supplied = set(data.keys())
        not_supplied = defaults - supplied
        if not_supplied and not is_colab:
            logger.warning(f"Parameters not supplied by user and set to default: {', '.join(not_supplied)}")

        # Parameters that were supplied but not used
        # This is a naive implementation. It might catch some internal Pydantic params.
        unused = supplied - set(self.model_fields)
        if unused:
            logger.warning(f"Parameters supplied but not used: {', '.join(unused)}")


class UploadLogs(TrainerCallback):
    def __init__(self, config):
        self.config = config
        self.api = None
        self.last_upload_time = 0

        if self.config.push_to_hub:
            if PartialState().process_index == 0:
                self.api = HfApi(token=config.token)
                self.api.create_repo(
                    repo_id=f"{self.config.username}/{self.config.project_name}", repo_type="model", private=True
                )

    def on_step_end(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        if self.config.push_to_hub is False:
            return control

        if not os.path.exists(os.path.join(self.config.project_name, "runs")):
            return control

        if (state.global_step + 1) % self.config.logging_steps == 0 and self.config.log == "tensorboard":
            if PartialState().process_index == 0:
                current_time = time.time()
                if current_time - self.last_upload_time >= 600:
                    try:
                        self.api.upload_folder(
                            folder_path=os.path.join(self.config.project_name, "runs"),
                            repo_id=f"{self.config.username}/{self.config.project_name}",
                            path_in_repo="runs",
                        )
                    except Exception as e:
                        logger.warning(f"Failed to upload logs: {e}")
                        logger.warning("Continuing training...")

                    self.last_upload_time = current_time
        return control


class LossLoggingCallback(TrainerCallback):
    def on_log(self, args, state, control, logs=None, **kwargs):
        _ = logs.pop("total_flos", None)
        if state.is_local_process_zero:
            logger.info(logs)


class TrainStartCallback(TrainerCallback):
    def on_train_begin(self, args, state, control, **kwargs):
        logger.info("Starting to train...")
