from typing import Optional


def process_dataset_name(name: str) -> tuple[str, Optional[str], Optional[str]]:
    """
    Process a dataset name string and extract dataset name, config name, and split name.

    The function handles various formats of dataset name strings:
    - "{dataset_name}"
    - "{dataset_name}:{config_name}"
    - "{dataset_name}:{config_name}:{split_name}"
    - "{dataset_name}::{split_name}" (empty config name)

    Args:
        name (str): The dataset name string to process.

    Returns:
        tuple[str, Optional[str], Optional[str]]: A tuple containing:
            - dataset_name (str): The name of the dataset.
            - config_name (Optional[str]): The name of the configuration, if provided.
            - split_name (Optional[str]): The name of the split, if provided.

    Raises:
        ValueError: If the input string format is invalid.

    Examples:
        >>> process_dataset_name("mnist")
        ('mnist', None, None)
        >>> process_dataset_name("glue:mrpc")
        ('glue', None, 'mrpc')
        >>> process_dataset_name("glue:cola:train")
        ('glue', 'cola', 'train')
        >>> process_dataset_name("squad::validation")
        ('squad', None, 'validation')
    """
    parts = name.split(":")
    if len(parts) == 1:
        return parts[0], None, None
    elif len(parts) == 2:
        return parts[0], None, parts[1]
    elif len(parts) == 3:
        if parts[1] == "":
            return parts[0], None, parts[2]
        return parts[0], parts[1], parts[2]
    else:
        raise ValueError(
            f"Invalid dataset name format: {name}. "
            "Allowed formats are {dataset_name} or {dataset_name}:{config_name} "
            "or {dataset_name}:{config_name}:{split_name}"
        )
