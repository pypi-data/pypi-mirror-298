# Random English Word Generator

🎉 **Random English Word Generator** is a Python package that generates random English words based on the length and number of words you specify! 🎉

This package leverages the `nltk` corpus to generate real English words, making it perfect for tasks like text augmentation, random text generation, and adding random noise to datasets.

## Features

- **Custom Word Length**: You can specify the word length for each word generated.
- **Generate Multiple Words**: Generate a list of random words by specifying how many you need.
- **Lightweight & Easy to Use**: No external dependencies other than `nltk`, and easy to set up.

## Installation

Install the package using pip:

```bash
pip install random-english-word-generator
```

## Usage

```python
from random_english_word_generator import generate_words

# Generate 5 random words of length 6
words = generate_words(word_length=6, num_words=5)
print(words)
# Output: ['planet', 'system', 'orange', 'monkey', 'banana']
```

## Contributing

If you have any suggestions for improving this package, feel free to open an issue or submit a pull request on GitHub. We appreciate your contributions!

## Links

For more tools and features, visit our website: 👉 [randomgenerator.ai](https://randomgenerator.ai)