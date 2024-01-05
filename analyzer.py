import spacy
import textblob
from textblob import TextBlob
import nltk
from nltk.tokenize import word_tokenize
import re
import os


class DataAnalyzer:
    def __init__(self, stop_words_folder, positive_words_path, negative_words_path):
        # Load the English language model for spaCy
        self.nlp = spacy.load("en_core_web_sm")
        nltk.download('punkt')

        # Load Stop Words List from multiple files in the specified folder
        self.stop_words = set()
        for filename in os.listdir(stop_words_folder):
            if filename.endswith(".txt"):
                file_path = os.path.join(stop_words_folder, filename)
                with open(file_path, 'r') as file:
                    self.stop_words.update(set(file.read().splitlines()))

        # Load Positive and Negative words
        with open(positive_words_path, 'r') as file:
            self.positive_words = set(file.read().splitlines())

        with open(negative_words_path, 'r') as file:
            self.negative_words = set(file.read().splitlines())

    def clean_text(self, article_text):
        # Cleaning using Stop Words Lists
        cleaned_tokens = [word.lower() for word in word_tokenize(article_text) if word.isalpha() and word.lower() not in self.stop_words]
        cleaned_text = ' '.join(cleaned_tokens)
        return cleaned_text

    def analyze_text(self, article_text):
        # Sentiment Analysis using TextBlob
        cleaned_text = self.clean_text(article_text)
        sentiment_analysis = TextBlob(cleaned_text)
        positive_score = sum(1 for word in sentiment_analysis.words if word in self.positive_words)
        negative_score = sum(1 for word in sentiment_analysis.words if word in self.negative_words)
        polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
        subjectivity_score = (positive_score + negative_score) / ((len(cleaned_text.split()) + 0.000001))

        # Tokenize the text using spaCy
        doc = self.nlp(article_text)

        # Calculate variables for readability analysis
        num_sentences = len(list(doc.sents))
        avg_sentence_length = len(doc) / num_sentences
        word_count = len(re.findall(r'\b\w+\b', cleaned_text))
        avg_words_per_sentence = word_count / num_sentences
        complex_word_count = sum(1 for token in doc if token.is_alpha and len(token.text) > 2)
        percentage_of_complex_words = (complex_word_count / word_count) * 100
        fog_index = 0.4 * (avg_sentence_length + percentage_of_complex_words)

        return [positive_score, negative_score, polarity_score, subjectivity_score,
                avg_sentence_length, percentage_of_complex_words, fog_index,
                avg_words_per_sentence, complex_word_count, word_count]


