import os
from typing import Any, Optional, Union

import datasets

from . import parsing


def load_hf_dataset(
    name_or_path: str,
    name: Optional[str] = None,
    split: Optional[str] = None,
    **kwargs: Any,
) -> Union[datasets.Dataset, datasets.DatasetDict]:
    """
    Load a Hugging Face dataset from various sources.

    Args:
        name_or_path (str): The name or path of the dataset to load.
        name (Optional[str]): The name of the dataset configuration.
        split (Optional[str]): The split of the dataset to load.
        **kwargs: Additional keyword arguments to pass to the underlying loader.

    Returns:
        Union[Dataset, DatasetDict]: The loaded dataset.

    Raises:
        ValueError: If incompatible arguments are provided for the given input.
    """
    if name_or_path.endswith((".json", ".jsonl")):
        if name is not None:
            raise ValueError("Cannot specify config name when loading from JSON file.")
        if split is not None:
            raise ValueError("Cannot specify split when loading from JSON file.")
        return datasets.load_dataset("json", data_files=name_or_path)["train"]

    if os.path.isdir(name_or_path):
        if name is not None:
            raise ValueError("Cannot specify config name when loading from disk.")
        ds = datasets.load_from_disk(name_or_path)
        if split is not None:
            if not isinstance(ds, datasets.DatasetDict):
                raise TypeError(f"Cannot split non-DatasetDict. Got {type(ds)}.")
            ds = ds[split]
        return ds

    return datasets.load_dataset(name_or_path, name=name, split=split, **kwargs)


def load_dataset(
    name_or_path: str, **kwargs: Any
) -> Union[datasets.Dataset, datasets.DatasetDict]:
    """
    Load a Hugging Face dataset using a complex string format.

    Args:
        name_or_path (str): A string in the format "dataset_name:config:split".
        **kwargs: Additional keyword arguments to pass to load_hf_dataset.

    Returns:
        Union[Dataset, DatasetDict]: The loaded dataset.
    """
    dataset_name, config_name, split_name = parsing.process_dataset_name(name_or_path)
    return load_hf_dataset(dataset_name, config_name, split_name, **kwargs)
