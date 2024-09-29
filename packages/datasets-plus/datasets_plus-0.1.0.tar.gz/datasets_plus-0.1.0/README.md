# 🤗 datasets-plus

A wrapper for Hugging Face datasets with extra utilities! 🚀

## 🌟 Features

- 🔧 Simplified dataset loading
- 🔀 Easy splitting and configuration
- 📁 Support for local and remote datasets
- 🧰 Additional utility functions

## 🚀 Installation

Install datasets-plus using pip:

```bash
pip install datasets-plus
```

## 📚 Usage

Here's a quick example of how to use datasets-plus:

```python
from datasets_plus import load_dataset

# Load validation fold of TriviaQA's unfiltered subset
dataset = load_dataset("mandarjoshi/trivia_qa:unfiltered:validation")

# Print dataset info
print(f"Loaded dataset with {len(dataset)} examples")
print("First example:", dataset[0])

# Load the train fold of the local hf dataset saved at /path/to/dataset
dataset = load_dataset("/path/to/dataset:train")
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgements

- [Hugging Face Datasets](https://github.com/huggingface/datasets) for the amazing foundation
- All our contributors and users!

Happy data loading! 🎉