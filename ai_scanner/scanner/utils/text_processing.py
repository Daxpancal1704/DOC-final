import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def split_sentences(text):

    sentences = nltk.sent_tokenize(text)

    return sentences


def clean_text(sentence):

    sentence = sentence.lower()

    sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    return sentence


def tokenize_text(sentence):

    tokens = word_tokenize(sentence)

    return tokens

def remove_stopwords(tokens):

    stop_words = set(stopwords.words('english'))

    filtered_words = []

    for word in tokens:

        if word not in stop_words:

            filtered_words.append(word)

    return filtered_words

def normalize_text(words):

    normalized_sentence = " ".join(words)

    return normalized_sentence


def process_text(sentences):

    processed_sentences = []

    for sentence in sentences:

        cleaned = clean_text(sentence)

        tokens = tokenize_text(cleaned)

        filtered = remove_stopwords(tokens)

        normalized = normalize_text(filtered)

        processed_sentences.append(normalized)

    return processed_sentences
