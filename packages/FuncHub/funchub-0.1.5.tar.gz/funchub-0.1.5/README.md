#  Utility Library

A collection of utility functions for file operations, text processing, AI, and machine learning, designed to streamline common tasks in PyTorch projects.

## Features

- Load and save JSON and YAML files.
- Text processing utilities including tokenization and normalization.
- Device management for PyTorch (CPU, CUDA, or MPS).
- Similarity computation for embeddings using cosine similarity.
- Utility functions for data manipulation such as moving averages, safe division, and flattening dictionaries.

## Installation

You can install the library via pip:

```bash
pip install FuncHub
```

## Usage

### File Operations

#### Load YAML File

```python
from pytorch_utility_library import open_yaml

config = open_yaml('config.yaml', key='model')
```

#### Load JSON File

```python
from pytorch_utility_library import open_json

data = open_json('data.json')
```

#### Save Data to JSON

```python
from pytorch_utility_library import dump_to_json

dump_to_json('output.json', data)
```

#### Save Text to File

```python
from pytorch_utility_library import dump_to_text

dump_to_text('Hello, World!', 'output/hello.txt')
```

### Text Processing

#### Tokenize Text

```python
from pytorch_utility_library import tokenize

tokens = tokenize("Hello, how are you?")
```

#### Normalize Text

```python
from pytorch_utility_library import normalize_text

normalized = normalize_text("  Hello,   How Are You?  ")
```

### AI and Machine Learning

#### Get Device

```python
from pytorch_utility_library import get_device

device = get_device()
print(f"Using device: {device}")
```

#### Compute Cosine Similarity

```python
from pytorch_utility_library import compute_similarity

similarity = compute_similarity(embedding1, embedding2)
```

### Utility Functions

#### Calculate Moving Average

```python
from pytorch_utility_library import moving_average

averages = moving_average([1, 2, 3, 4, 5], window_size=3)
```

#### Flatten a Nested Dictionary

```python
from pytorch_utility_library import flatten_dict

flat_dict = flatten_dict({'a': {'b': 1, 'c': 2}, 'd': 3})
```

## Logging

The library uses a custom logger for error and information logging. Make sure to configure the logger in your application as needed.

## Contributing

Contributions are welcome! 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

