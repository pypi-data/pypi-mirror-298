import pytest

from datasets_plus import process_dataset_name


@pytest.mark.parametrize(
    "input_name, expected_output",
    [
        ("dataset", ("dataset", None, None)),
        ("dataset:split", ("dataset", None, "split")),
        ("dataset::split", ("dataset", None, "split")),
        ("dataset:config:split", ("dataset", "config", "split")),
    ],
)
def test_process_dataset_name(input_name, expected_output):
    assert process_dataset_name(input_name) == expected_output


def test_process_dataset_name_invalid():
    with pytest.raises(ValueError, match="Invalid dataset name format"):
        process_dataset_name("dataset:config:split:extra")
