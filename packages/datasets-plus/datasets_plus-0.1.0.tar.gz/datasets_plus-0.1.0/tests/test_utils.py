import json

import datasets
import pytest
from pytest_mock import MockerFixture

from datasets_plus import load_dataset, load_hf_dataset


class TestLoadHFDataset:
    @pytest.fixture(scope="class")
    def temp_dataset_dir(self, tmp_path_factory):
        temp_dir = tmp_path_factory.mktemp("dataset")

        # Create a JSON dataset
        json_data = [{"id": 1, "text": "Hello"}, {"id": 2, "text": "World"}]
        json_path = temp_dir / "data.json"
        with open(json_path, "w") as f:
            json.dump(json_data, f)

        # Create a Parquet dataset
        ds = datasets.Dataset.from_dict({"id": [3, 4], "text": ["Foo", "Bar"]})
        ds.save_to_disk(temp_dir / "disk_dataset")

        ds_dict = datasets.DatasetDict({"train": ds, "test": ds})
        ds_dict.save_to_disk(temp_dir / "dataset_dict")

        return temp_dir

    def test_load_hf_dataset_json(self, temp_dataset_dir):
        json_path = temp_dataset_dir / "data.json"
        result = load_hf_dataset(str(json_path))
        assert isinstance(result, datasets.Dataset)
        assert len(result) == 2
        assert result[0] == {"id": 1, "text": "Hello"}

        with pytest.raises(ValueError):
            load_hf_dataset(str(json_path), name="config")

        with pytest.raises(ValueError):
            load_hf_dataset(str(json_path), split="train")

    def test_load_hf_dataset_directory(self, temp_dataset_dir):
        disk_dataset_path = temp_dataset_dir / "disk_dataset"
        result = load_hf_dataset(str(disk_dataset_path))
        assert isinstance(result, datasets.Dataset)

    def test_load_hf_dataset_directory_split(self, temp_dataset_dir):
        disk_dataset_path = temp_dataset_dir / "dataset_dict"
        result = load_hf_dataset(str(disk_dataset_path))
        assert isinstance(result, datasets.DatasetDict)

        result_split = load_hf_dataset(str(disk_dataset_path), split="train")
        assert isinstance(result_split, datasets.Dataset)

        with pytest.raises(ValueError):
            load_hf_dataset(str(temp_dataset_dir), name="config")

    def test_load_hf_dataset_huggingface(self, mocker):
        mock_load_dataset = mocker.patch("datasets.load_dataset")
        mock_load_dataset.return_value = datasets.Dataset.from_dict({"text": ["test"]})

        result = load_hf_dataset("dataset_name", name="config", split="train")
        mock_load_dataset.assert_called_with(
            "dataset_name", name="config", split="train"
        )
        assert isinstance(result, datasets.Dataset)

    def test_load_hf_dataset_errors(self, temp_dataset_dir):
        with pytest.raises(TypeError):
            load_hf_dataset(
                str(temp_dataset_dir / "disk_dataset"), split="non_existent_split"
            )

    def test_load_hf_dataset_disk_bad_split(self, temp_dataset_dir):
        with pytest.raises(KeyError):
            load_hf_dataset(
                str(temp_dataset_dir / "dataset_dict"), split="non_existent_split"
            )


class TestLoadDataset:
    @pytest.mark.parametrize(
        "input_name, expected_args",
        [
            ("dataset_path", ("dataset_path", None, None)),
            ("dataset_path:split", ("dataset_path", None, "split")),
            ("dataset_path::split", ("dataset_path", None, "split")),
            ("dataset:config:split", ("dataset", "config", "split")),
        ],
    )
    def test_load_dataset(self, mocker: MockerFixture, input_name, expected_args):
        mock_load_hf_dataset = mocker.patch("datasets_plus.utils.load_hf_dataset")
        load_dataset(input_name)
        mock_load_hf_dataset.assert_called_with(*expected_args)

    def test_load_dataset_json(self, mocker: MockerFixture):
        mock_load_hf_dataset = mocker.patch("datasets_plus.utils.load_hf_dataset")
        load_dataset("test.json")
        mock_load_hf_dataset.assert_called_with("test.json", None, None)

        load_dataset("test.jsonl")
        mock_load_hf_dataset.assert_called_with("test.jsonl", None, None)

    def test_load_dataset_invalid(self):
        with pytest.raises(ValueError):
            load_dataset("dataset:config:split:extra")
