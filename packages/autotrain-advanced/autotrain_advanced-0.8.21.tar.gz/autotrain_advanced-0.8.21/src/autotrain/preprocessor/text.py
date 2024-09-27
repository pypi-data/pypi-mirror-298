import ast
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from datasets import ClassLabel, Dataset, DatasetDict, Sequence
from sklearn.model_selection import train_test_split

from autotrain import logger


RESERVED_COLUMNS = ["autotrain_text", "autotrain_label", "autotrain_question", "autotrain_answer"]
LLM_RESERVED_COLUMNS = [
    "autotrain_prompt",
    "autotrain_context",
    "autotrain_rejected_text",
    "autotrain_prompt_start",
]


@dataclass
class TextBinaryClassificationPreprocessor:
    train_data: pd.DataFrame
    text_column: str
    label_column: str
    username: str
    project_name: str
    token: str
    valid_data: Optional[pd.DataFrame] = None
    test_size: Optional[float] = 0.2
    seed: Optional[int] = 42
    convert_to_class_label: Optional[bool] = False
    local: Optional[bool] = False

    def __post_init__(self):
        # check if text_column and label_column are in train_data
        if self.text_column not in self.train_data.columns:
            raise ValueError(f"{self.text_column} not in train data")
        if self.label_column not in self.train_data.columns:
            raise ValueError(f"{self.label_column} not in train data")
        # check if text_column and label_column are in valid_data
        if self.valid_data is not None:
            if self.text_column not in self.valid_data.columns:
                raise ValueError(f"{self.text_column} not in valid data")
            if self.label_column not in self.valid_data.columns:
                raise ValueError(f"{self.label_column} not in valid data")

        # make sure no reserved columns are in train_data or valid_data
        for column in RESERVED_COLUMNS:
            if column in self.train_data.columns:
                raise ValueError(f"{column} is a reserved column name")
            if self.valid_data is not None:
                if column in self.valid_data.columns:
                    raise ValueError(f"{column} is a reserved column name")

    def split(self):
        if self.valid_data is not None:
            return self.train_data, self.valid_data
        else:
            train_df, valid_df = train_test_split(
                self.train_data,
                test_size=self.test_size,
                random_state=self.seed,
                stratify=self.train_data[self.label_column],
            )
            train_df = train_df.reset_index(drop=True)
            valid_df = valid_df.reset_index(drop=True)
            return train_df, valid_df

    def prepare_columns(self, train_df, valid_df):
        train_df.loc[:, "autotrain_text"] = train_df[self.text_column]
        train_df.loc[:, "autotrain_label"] = train_df[self.label_column]
        valid_df.loc[:, "autotrain_text"] = valid_df[self.text_column]
        valid_df.loc[:, "autotrain_label"] = valid_df[self.label_column]

        # drop text_column and label_column
        train_df = train_df.drop(columns=[self.text_column, self.label_column])
        valid_df = valid_df.drop(columns=[self.text_column, self.label_column])
        return train_df, valid_df

    def prepare(self):
        train_df, valid_df = self.split()
        train_df, valid_df = self.prepare_columns(train_df, valid_df)

        train_df.loc[:, "autotrain_label"] = train_df["autotrain_label"].astype(str)
        valid_df.loc[:, "autotrain_label"] = valid_df["autotrain_label"].astype(str)

        label_names = sorted(set(train_df["autotrain_label"].unique().tolist()))

        train_df = Dataset.from_pandas(train_df)
        valid_df = Dataset.from_pandas(valid_df)

        if self.convert_to_class_label:
            train_df = train_df.cast_column("autotrain_label", ClassLabel(names=label_names))
            valid_df = valid_df.cast_column("autotrain_label", ClassLabel(names=label_names))

        if self.local:
            dataset = DatasetDict(
                {
                    "train": train_df,
                    "validation": valid_df,
                }
            )
            dataset.save_to_disk(f"{self.project_name}/autotrain-data")
        else:
            train_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="train",
                private=True,
                token=self.token,
            )
            valid_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="validation",
                private=True,
                token=self.token,
            )

        if self.local:
            return f"{self.project_name}/autotrain-data"
        return f"{self.username}/autotrain-data-{self.project_name}"


class TextMultiClassClassificationPreprocessor(TextBinaryClassificationPreprocessor):
    pass


class TextSingleColumnRegressionPreprocessor(TextBinaryClassificationPreprocessor):
    def split(self):
        if self.valid_data is not None:
            return self.train_data, self.valid_data
        else:
            train_df, valid_df = train_test_split(
                self.train_data,
                test_size=self.test_size,
                random_state=self.seed,
            )
            train_df = train_df.reset_index(drop=True)
            valid_df = valid_df.reset_index(drop=True)
            return train_df, valid_df

    def prepare(self):
        train_df, valid_df = self.split()
        train_df, valid_df = self.prepare_columns(train_df, valid_df)

        train_df = Dataset.from_pandas(train_df)
        valid_df = Dataset.from_pandas(valid_df)

        if self.local:
            dataset = DatasetDict(
                {
                    "train": train_df,
                    "validation": valid_df,
                }
            )
            dataset.save_to_disk(f"{self.project_name}/autotrain-data")
        else:
            train_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="train",
                private=True,
                token=self.token,
            )
            valid_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="validation",
                private=True,
                token=self.token,
            )

        if self.local:
            return f"{self.project_name}/autotrain-data"
        return f"{self.username}/autotrain-data-{self.project_name}"


class TextTokenClassificationPreprocessor(TextBinaryClassificationPreprocessor):
    def split(self):
        if self.valid_data is not None:
            return self.train_data, self.valid_data
        else:
            train_df, valid_df = train_test_split(
                self.train_data,
                test_size=self.test_size,
                random_state=self.seed,
            )
            train_df = train_df.reset_index(drop=True)
            valid_df = valid_df.reset_index(drop=True)
            return train_df, valid_df

    def prepare(self):
        train_df, valid_df = self.split()
        train_df, valid_df = self.prepare_columns(train_df, valid_df)
        try:
            train_df.loc[:, "autotrain_text"] = train_df["autotrain_text"].apply(lambda x: ast.literal_eval(x))
            valid_df.loc[:, "autotrain_text"] = valid_df["autotrain_text"].apply(lambda x: ast.literal_eval(x))
        except ValueError:
            logger.warning("Unable to do ast.literal_eval on train_df['autotrain_text']")
            logger.warning("assuming autotrain_text is already a list")
        try:
            train_df.loc[:, "autotrain_label"] = train_df["autotrain_label"].apply(lambda x: ast.literal_eval(x))
            valid_df.loc[:, "autotrain_label"] = valid_df["autotrain_label"].apply(lambda x: ast.literal_eval(x))
        except ValueError:
            logger.warning("Unable to do ast.literal_eval on train_df['autotrain_label']")
            logger.warning("assuming autotrain_label is already a list")

        label_names_train = sorted(set(train_df["autotrain_label"].explode().unique().tolist()))
        label_names_valid = sorted(set(valid_df["autotrain_label"].explode().unique().tolist()))
        label_names = sorted(set(label_names_train + label_names_valid))

        train_df = Dataset.from_pandas(train_df)
        valid_df = Dataset.from_pandas(valid_df)

        if self.convert_to_class_label:
            train_df = train_df.cast_column("autotrain_label", Sequence(ClassLabel(names=label_names)))
            valid_df = valid_df.cast_column("autotrain_label", Sequence(ClassLabel(names=label_names)))

        if self.local:
            dataset = DatasetDict(
                {
                    "train": train_df,
                    "validation": valid_df,
                }
            )
            dataset.save_to_disk(f"{self.project_name}/autotrain-data")
        else:
            train_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="train",
                private=True,
                token=self.token,
            )
            valid_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="validation",
                private=True,
                token=self.token,
            )

        if self.local:
            return f"{self.project_name}/autotrain-data"
        return f"{self.username}/autotrain-data-{self.project_name}"


@dataclass
class LLMPreprocessor:
    train_data: pd.DataFrame
    username: str
    project_name: str
    token: str
    valid_data: Optional[pd.DataFrame] = None
    test_size: Optional[float] = 0.2
    seed: Optional[int] = 42
    text_column: Optional[str] = None
    prompt_column: Optional[str] = None
    rejected_text_column: Optional[str] = None
    local: Optional[bool] = False

    def __post_init__(self):
        if self.text_column is None:
            raise ValueError("text_column must be provided")

        # check if text_column and rejected_text_column are in train_data
        if self.prompt_column is not None and self.prompt_column not in self.train_data.columns:
            self.prompt_column = None
        if self.rejected_text_column is not None and self.rejected_text_column not in self.train_data.columns:
            self.rejected_text_column = None

        # make sure no reserved columns are in train_data or valid_data
        for column in RESERVED_COLUMNS + LLM_RESERVED_COLUMNS:
            if column in self.train_data.columns:
                raise ValueError(f"{column} is a reserved column name")
            if self.valid_data is not None:
                if column in self.valid_data.columns:
                    raise ValueError(f"{column} is a reserved column name")

    def split(self):
        if self.valid_data is not None:
            return self.train_data, self.valid_data
        # no validation is done in llm training if validation data is not provided
        return self.train_data, self.train_data
        # else:
        #     train_df, valid_df = train_test_split(
        #         self.train_data,
        #         test_size=self.test_size,
        #         random_state=self.seed,
        #     )
        #     train_df = train_df.reset_index(drop=True)
        #     valid_df = valid_df.reset_index(drop=True)
        #     return train_df, valid_df

    def prepare_columns(self, train_df, valid_df):
        drop_cols = [self.text_column]
        train_df.loc[:, "autotrain_text"] = train_df[self.text_column]
        valid_df.loc[:, "autotrain_text"] = valid_df[self.text_column]
        if self.prompt_column is not None:
            drop_cols.append(self.prompt_column)
            train_df.loc[:, "autotrain_prompt"] = train_df[self.prompt_column]
            valid_df.loc[:, "autotrain_prompt"] = valid_df[self.prompt_column]
        if self.rejected_text_column is not None:
            drop_cols.append(self.rejected_text_column)
            train_df.loc[:, "autotrain_rejected_text"] = train_df[self.rejected_text_column]
            valid_df.loc[:, "autotrain_rejected_text"] = valid_df[self.rejected_text_column]

        # drop drop_cols
        train_df = train_df.drop(columns=drop_cols)
        valid_df = valid_df.drop(columns=drop_cols)
        return train_df, valid_df

    def prepare(self):
        train_df, valid_df = self.split()
        train_df, valid_df = self.prepare_columns(train_df, valid_df)
        train_df = Dataset.from_pandas(train_df)
        valid_df = Dataset.from_pandas(valid_df)
        if self.local:
            dataset = DatasetDict(
                {
                    "train": train_df,
                    "validation": valid_df,
                }
            )
            dataset.save_to_disk(f"{self.project_name}/autotrain-data")
        else:
            train_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="train",
                private=True,
                token=self.token,
            )
            valid_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="validation",
                private=True,
                token=self.token,
            )
        if self.local:
            return f"{self.project_name}/autotrain-data"
        return f"{self.username}/autotrain-data-{self.project_name}"


@dataclass
class Seq2SeqPreprocessor:
    train_data: pd.DataFrame
    text_column: str
    label_column: str
    username: str
    project_name: str
    token: str
    valid_data: Optional[pd.DataFrame] = None
    test_size: Optional[float] = 0.2
    seed: Optional[int] = 42
    local: Optional[bool] = False

    def __post_init__(self):
        # check if text_column and label_column are in train_data
        if self.text_column not in self.train_data.columns:
            raise ValueError(f"{self.text_column} not in train data")
        if self.label_column not in self.train_data.columns:
            raise ValueError(f"{self.label_column} not in train data")
        # check if text_column and label_column are in valid_data
        if self.valid_data is not None:
            if self.text_column not in self.valid_data.columns:
                raise ValueError(f"{self.text_column} not in valid data")
            if self.label_column not in self.valid_data.columns:
                raise ValueError(f"{self.label_column} not in valid data")

        # make sure no reserved columns are in train_data or valid_data
        for column in RESERVED_COLUMNS:
            if column in self.train_data.columns:
                raise ValueError(f"{column} is a reserved column name")
            if self.valid_data is not None:
                if column in self.valid_data.columns:
                    raise ValueError(f"{column} is a reserved column name")

    def split(self):
        if self.valid_data is not None:
            return self.train_data, self.valid_data
        else:
            train_df, valid_df = train_test_split(
                self.train_data,
                test_size=self.test_size,
                random_state=self.seed,
            )
            train_df = train_df.reset_index(drop=True)
            valid_df = valid_df.reset_index(drop=True)
            return train_df, valid_df

    def prepare_columns(self, train_df, valid_df):
        train_df.loc[:, "autotrain_text"] = train_df[self.text_column]
        train_df.loc[:, "autotrain_label"] = train_df[self.label_column]
        valid_df.loc[:, "autotrain_text"] = valid_df[self.text_column]
        valid_df.loc[:, "autotrain_label"] = valid_df[self.label_column]

        # drop text_column and label_column
        train_df = train_df.drop(columns=[self.text_column, self.label_column])
        valid_df = valid_df.drop(columns=[self.text_column, self.label_column])
        return train_df, valid_df

    def prepare(self):
        train_df, valid_df = self.split()
        train_df, valid_df = self.prepare_columns(train_df, valid_df)

        train_df = Dataset.from_pandas(train_df)
        valid_df = Dataset.from_pandas(valid_df)

        if self.local:
            dataset = DatasetDict(
                {
                    "train": train_df,
                    "validation": valid_df,
                }
            )
            dataset.save_to_disk(f"{self.project_name}/autotrain-data")
        else:
            train_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="train",
                private=True,
                token=self.token,
            )
            valid_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="validation",
                private=True,
                token=self.token,
            )
        if self.local:
            return f"{self.project_name}/autotrain-data"
        return f"{self.username}/autotrain-data-{self.project_name}"


@dataclass
class SentenceTransformersPreprocessor:
    train_data: pd.DataFrame
    username: str
    project_name: str
    token: str
    valid_data: Optional[pd.DataFrame] = None
    test_size: Optional[float] = 0.2
    seed: Optional[int] = 42
    local: Optional[bool] = False
    sentence1_column: Optional[str] = "sentence1"
    sentence2_column: Optional[str] = "sentence2"
    sentence3_column: Optional[str] = "sentence3"
    target_column: Optional[str] = "target"
    convert_to_class_label: Optional[bool] = False

    def __post_init__(self):
        # make sure no reserved columns are in train_data or valid_data
        for column in RESERVED_COLUMNS + LLM_RESERVED_COLUMNS:
            if column in self.train_data.columns:
                raise ValueError(f"{column} is a reserved column name")
            if self.valid_data is not None:
                if column in self.valid_data.columns:
                    raise ValueError(f"{column} is a reserved column name")

    def split(self):
        if self.valid_data is not None:
            return self.train_data, self.valid_data
        else:
            train_df, valid_df = train_test_split(
                self.train_data,
                test_size=self.test_size,
                random_state=self.seed,
            )
            train_df = train_df.reset_index(drop=True)
            valid_df = valid_df.reset_index(drop=True)
            return train_df, valid_df

    def prepare_columns(self, train_df, valid_df):
        train_df.loc[:, "autotrain_sentence1"] = train_df[self.sentence1_column]
        train_df.loc[:, "autotrain_sentence2"] = train_df[self.sentence2_column]
        valid_df.loc[:, "autotrain_sentence1"] = valid_df[self.sentence1_column]
        valid_df.loc[:, "autotrain_sentence2"] = valid_df[self.sentence2_column]
        keep_cols = ["autotrain_sentence1", "autotrain_sentence2"]

        if self.sentence3_column is not None:
            train_df.loc[:, "autotrain_sentence3"] = train_df[self.sentence3_column]
            valid_df.loc[:, "autotrain_sentence3"] = valid_df[self.sentence3_column]
            keep_cols.append("autotrain_sentence3")

        if self.target_column is not None:
            train_df.loc[:, "autotrain_target"] = train_df[self.target_column]
            valid_df.loc[:, "autotrain_target"] = valid_df[self.target_column]
            keep_cols.append("autotrain_target")

        train_df = train_df[keep_cols]
        valid_df = valid_df[keep_cols]

        return train_df, valid_df

    def prepare(self):
        train_df, valid_df = self.split()
        train_df, valid_df = self.prepare_columns(train_df, valid_df)

        if self.convert_to_class_label:
            label_names = sorted(set(train_df["autotrain_target"].unique().tolist()))

        train_df = Dataset.from_pandas(train_df)
        valid_df = Dataset.from_pandas(valid_df)

        if self.convert_to_class_label:
            train_df = train_df.cast_column("autotrain_target", ClassLabel(names=label_names))
            valid_df = valid_df.cast_column("autotrain_target", ClassLabel(names=label_names))

        if self.local:
            dataset = DatasetDict(
                {
                    "train": train_df,
                    "validation": valid_df,
                }
            )
            dataset.save_to_disk(f"{self.project_name}/autotrain-data")
        else:
            train_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="train",
                private=True,
                token=self.token,
            )
            valid_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="validation",
                private=True,
                token=self.token,
            )
        if self.local:
            return f"{self.project_name}/autotrain-data"
        return f"{self.username}/autotrain-data-{self.project_name}"


@dataclass
class TextExtractiveQuestionAnsweringPreprocessor:
    train_data: pd.DataFrame
    text_column: str
    question_column: str
    answer_column: str
    username: str
    project_name: str
    token: str
    valid_data: Optional[pd.DataFrame] = None
    test_size: Optional[float] = 0.2
    seed: Optional[int] = 42
    local: Optional[bool] = False

    def __post_init__(self):
        # check if text_column, question_column, and answer_column are in train_data
        if self.text_column not in self.train_data.columns:
            raise ValueError(f"{self.text_column} not in train data")
        if self.question_column not in self.train_data.columns:
            raise ValueError(f"{self.question_column} not in train data")
        if self.answer_column not in self.train_data.columns:
            raise ValueError(f"{self.answer_column} not in train data")
        # check if text_column, question_column, and answer_column are in valid_data
        if self.valid_data is not None:
            if self.text_column not in self.valid_data.columns:
                raise ValueError(f"{self.text_column} not in valid data")
            if self.question_column not in self.valid_data.columns:
                raise ValueError(f"{self.question_column} not in valid data")
            if self.answer_column not in self.valid_data.columns:
                raise ValueError(f"{self.answer_column} not in valid data")

        # make sure no reserved columns are in train_data or valid_data
        for column in RESERVED_COLUMNS:
            if column in self.train_data.columns:
                raise ValueError(f"{column} is a reserved column name")
            if self.valid_data is not None:
                if column in self.valid_data.columns:
                    raise ValueError(f"{column} is a reserved column name")

        # convert answer_column to dict
        try:
            self.train_data.loc[:, self.answer_column] = self.train_data[self.answer_column].apply(
                lambda x: ast.literal_eval(x)
            )
        except ValueError:
            logger.warning("Unable to do ast.literal_eval on train_data[answer_column]")
            logger.warning("assuming answer_column is already a dict")

        if self.valid_data is not None:
            try:
                self.valid_data.loc[:, self.answer_column] = self.valid_data[self.answer_column].apply(
                    lambda x: ast.literal_eval(x)
                )
            except ValueError:
                logger.warning("Unable to do ast.literal_eval on valid_data[answer_column]")
                logger.warning("assuming answer_column is already a dict")

    def split(self):
        if self.valid_data is not None:
            return self.train_data, self.valid_data
        else:
            train_df, valid_df = train_test_split(
                self.train_data,
                test_size=self.test_size,
                random_state=self.seed,
            )
            train_df = train_df.reset_index(drop=True)
            valid_df = valid_df.reset_index(drop=True)
            return train_df, valid_df

    def prepare_columns(self, train_df, valid_df):
        train_df.loc[:, "autotrain_text"] = train_df[self.text_column]
        train_df.loc[:, "autotrain_question"] = train_df[self.question_column]
        train_df.loc[:, "autotrain_answer"] = train_df[self.answer_column]
        valid_df.loc[:, "autotrain_text"] = valid_df[self.text_column]
        valid_df.loc[:, "autotrain_question"] = valid_df[self.question_column]
        valid_df.loc[:, "autotrain_answer"] = valid_df[self.answer_column]

        # drop all other columns
        train_df = train_df.drop(
            columns=[
                x for x in train_df.columns if x not in ["autotrain_text", "autotrain_question", "autotrain_answer"]
            ]
        )
        valid_df = valid_df.drop(
            columns=[
                x for x in valid_df.columns if x not in ["autotrain_text", "autotrain_question", "autotrain_answer"]
            ]
        )
        return train_df, valid_df

    def prepare(self):
        train_df, valid_df = self.split()
        train_df, valid_df = self.prepare_columns(train_df, valid_df)

        train_df = Dataset.from_pandas(train_df)
        valid_df = Dataset.from_pandas(valid_df)

        if self.local:
            dataset = DatasetDict(
                {
                    "train": train_df,
                    "validation": valid_df,
                }
            )
            dataset.save_to_disk(f"{self.project_name}/autotrain-data")
        else:
            train_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="train",
                private=True,
                token=self.token,
            )
            valid_df.push_to_hub(
                f"{self.username}/autotrain-data-{self.project_name}",
                split="validation",
                private=True,
                token=self.token,
            )
        if self.local:
            return f"{self.project_name}/autotrain-data"
        return f"{self.username}/autotrain-data-{self.project_name}"
