# agentChef

agentChef is a powerful tool for collecting, processing, and generating datasets for AI training. It provides a set of agents that can fetch data from various sources including Hugging Face, GitHub, Wikipedia, and arXiv.

## Installation

You can install agentChef using pip:

```
pip install agentChef
```

## Usage

Here's a quick example of how to use agentChef:

```python
from agentchef import DatasetKitchen

# Initialize the DatasetKitchen
kitchen = DatasetKitchen(config_path='path/to/your/config.yaml')

# Prepare a dataset
dataset = kitchen.prepare_dataset(
    source="hf://dataset_name",
    template_name="your_template",
    num_samples=1000,
    augmentation_config={},
    output_file="output_dataset.parquet"
)

# Generate paraphrases
paraphrases = kitchen.generate_paraphrases(
    seed_file="seed_data.txt",
    num_samples=5
)

# Augment data
augmented_data = kitchen.augment_data(
    seed_parquet="seed_data.parquet",
    augmentation_config={}
)
```

For more detailed usage instructions, please refer to the documentation.

## Features

- Collect data from Hugging Face, GitHub, Wikipedia, and arXiv
- Process and structure data according to customizable templates
- Generate synthetic data and paraphrases
- Augment existing datasets
- Clean and validate data

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.