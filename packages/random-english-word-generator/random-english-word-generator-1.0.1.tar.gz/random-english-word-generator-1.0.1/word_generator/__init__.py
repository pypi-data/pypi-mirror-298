import random
from nltk.corpus import words
import nltk

# Download the word corpus, only needed once
nltk.download('words')

def generate_words(word_length, num_words):
    """
    Generate a list of random English words based on the given length and number.
    
    :param word_length: Length of each word
    :param num_words: Number of words to generate
    :return: List of generated words
    """
    english_words = [word for word in words.words() if len(word) == word_length]
    
    if len(english_words) < num_words:
        raise ValueError(f"Not enough words with length {word_length}. Only found {len(english_words)} words.")
    
    return random.sample(english_words, num_words)
