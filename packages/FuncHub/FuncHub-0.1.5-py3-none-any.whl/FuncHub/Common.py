import json
import yaml
import sys
import os
import torch
import numpy as np
from typing import List, Dict, Any
import tiktoken
import csv
from typing import Optional
tokenizer = tiktoken.get_encoding('cl100k_base')

#### File Operations

def open_yaml(path: str, key: str = '') -> Dict[str, Any]:
    """Load YAML file and optionally return a specific key."""
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    return config[key] if key else config

def open_json(path: str) -> Dict[str, Any]:
    """Load JSON file."""
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # logger.error(f"Error: JSON file not found at {path}. Aborting.")
        print(f"Error: JSON file not found at {path}. Aborting.")
        sys.exit(1)

def dump_to_json(path: str, data: Any) -> None:
    """Save data to JSON file."""
    with open(path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def dump_to_text(text: str, path: str) -> None:
    """Save text to file, creating directories if needed."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Text successfully written to {path}")

#### Text Processing

def tokenize(text: str) -> List[int]:
    """Tokenize text using tiktoken."""
    return tokenizer.encode(text=text)

def ends_with(text: str, format_list: List[str]) -> bool:
    """Check if text ends with any of the given formats."""
    return text.endswith(tuple(format_list))

def normalize_text(text: str) -> str:
    """Normalize text by lowercasing and removing extra whitespace."""
    return ' '.join(text.lower().split())

def remove_stopwords(text: str, stopwords: List[str]) -> str:
    """Remove stopwords from text."""
    return ' '.join([word for word in text.split() if word.lower() not in stopwords])

#### AI and Machine Learning

def get_device() -> torch.device:
    """Determine the available device for PyTorch."""
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")

def compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings."""
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))

#### Utility Functions

def safe_divide(numerator: float, denominator: float) -> float:
    """Safely divide two numbers, returning 0 if denominator is 0."""
    return numerator / denominator if denominator != 0 else 0

def moving_average(data: List[float], window_size: int) -> List[float]:
    """Calculate moving average of a list of numbers."""
    return [sum(data[i:i+window_size]) / window_size for i in range(len(data) - window_size + 1)]

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """Flatten a nested dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """Split a list into chunks of specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def open_text(path: str) -> str:
    """Open text file and return content."""
    with open(path, 'r', encoding='utf-8') as file:
        return file.read()
    
def save_text(text: str, path: str) -> None:
    """Save text to file."""
    with open(path, 'w', encoding='utf-8') as file:
        file.write(text)
    
def dumpt_to_text(text: str, path: str) -> None:
    """Append text to file."""
    with open(path, 'a', encoding='utf-8') as file:
        file.write(text)


def dumpt_to_csv(data: Dict[str, Any], path: str) -> None:
    """Add data to CSV file."""
    if os.path.exists(path):
        with open(path, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writerow(data)
    else:
        with open(path, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data.keys())
            writer.writeheader()
            writer.writerow(data)