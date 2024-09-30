# NLPFlow
from NLPFlow.utils.decorators import convert_input_to_string
from NLPFlow.utils.exceptions import InvalidModelException

# Misc 
import re
import spacy
import warnings
warnings.simplefilter("ignore", FutureWarning)
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np

class SpacyModelPicker:
    """Base class for handling spaCy model selection."""
    
    def __init__(self, model='large'):
        if model in ['large', 'lg']:
            self.nlp = spacy.load("en_core_web_lg")
            self.model_name = 'Large spaCy English model'
        elif model in ['medium', 'md']:
            self.nlp = spacy.load("en_core_web_md")
            self.model_name = 'Medium spaCy English model'
        elif model in ['small', 'sm']:
            self.nlp = spacy.load("en_core_web_sm")
            self.model_name = 'Small spaCy English model'
        else:
            raise InvalidModelException("Invalid spaCy model. Valid options: ['large', 'medium', 'small']")
    
    def model_name_(self):
        return self.model_name

class Preprocessor(SpacyModelPicker):
    """Class to handle text preprocessing and noise removal tasks using spaCy NLP models."""
    
    @convert_input_to_string
    def remove_html_tags(self, text):
        """Remove HTML tags from the text."""
        return re.sub(r'<[^>]+>', '', text)
    
    @convert_input_to_string
    def remove_mentions(self, text):
        """Remove mentions (e.g., @user) from the text."""
        return re.sub(r'@\w+', '', text).strip()

    @convert_input_to_string
    def remove_hashtags(self, text):
        """Remove hashtags (e.g., #hashtag) from the text."""
        return re.sub(r'#\w+', '', text).strip()

    @convert_input_to_string
    def remove_urls(self, text):
        """Remove URLs from the text using spaCy."""
        doc = self.nlp(text)
        return " ".join(token.text for token in doc if not token.like_url)

    @convert_input_to_string
    def remove_emails(self, text):
        """Remove emails from the text."""
        regex_sub = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '', text, flags=re.MULTILINE)
        doc = self.nlp(regex_sub)
        return " ".join(token.text for token in doc if not token.like_email)

    @convert_input_to_string
    def remove_special_characters(self, text):
        """Remove special characters from the text."""
        return re.sub(r'[^a-zA-Z0-9\s]', '', text)

    @convert_input_to_string
    def remove_numbers(self, text):
        """Remove numbers from the text."""
        return re.sub(r'\d+', '', text)
    
    @convert_input_to_string
    def remove_whitespace(self, text):
        """Remove extra whitespace from the text."""
        return re.sub(r'\s+', ' ', text).strip()

    @convert_input_to_string
    def remove_stopwords(self, text):
        """Remove stopwords using spaCy NLP model."""
        doc = self.nlp(text)
        return " ".join([token.text for token in doc if not token.is_stop])

    @convert_input_to_string
    def remove_punctuation(self, text):
        """Remove punctuation using spaCy NLP model."""
        doc = self.nlp(text)
        return " ".join([token.text for token in doc if not token.is_punct])

    @convert_input_to_string
    def lemmatize(self, text):
        """Lemmatize the text using spaCy."""
        doc = self.nlp(text)
        return " ".join([token.lemma_ for token in doc])

    @convert_input_to_string
    def remove_accented_chars(self, text):
        """Remove accented characters from the text."""
        return "".join([c for c in text if ord(c) < 128])

    @convert_input_to_string
    def remove_successive_characters(self, text, max_repeats=2):
        """Remove excessive repeated characters, reducing to a specified maximum."""
        return re.sub(r'(.)\1{'+str(max_repeats)+',}', r'\1' * max_repeats, text)

    @convert_input_to_string
    def preprocess(self, text, steps=None):
        """
        Apply multiple preprocessing steps to the input text.
        If steps is None, apply default steps in a logical order.
        """
        default_steps = [
            self.remove_html_tags,
            self.remove_emails,
            self.remove_mentions,
            self.remove_hashtags,
            self.remove_urls,
            self.remove_special_characters,
            self.remove_numbers,
            self.remove_stopwords,
            self.remove_punctuation,
            self.remove_accented_chars,
            self.remove_successive_characters,
            self.remove_whitespace,
            self.lemmatize
        ]
        
        steps = steps or default_steps
        
        for step in steps:
            text = step(text)
        return text


class Vectorizer:
    def __init__(self, method='tfidf', ngram_range=(1, 1), max_features=None, model='large'):
        self.method = method
        self.ngram_range = ngram_range
        self.max_features = max_features
        
        if self.method == 'tfidf':
            self.vectorizer = TfidfVectorizer(ngram_range=self.ngram_range, max_features=self.max_features)
        elif self.method == 'count':
            self.vectorizer = CountVectorizer(ngram_range=self.ngram_range, max_features=self.max_features)
        elif self.method == 'word_embeddings':
            self.nlp = SpacyModelPicker(model).nlp
        else:
            raise ValueError("Invalid method. Choose between 'tfidf', 'count', or 'word_embeddings'.")
    
    def fit(self, text_data):
        """Fit the vectorizer to the text data."""
        if self.method in ['tfidf', 'count']:
            self.vectorizer.fit(text_data)
            
    def transform(self, text_data):
        """Transform text data into numerical vectors."""
        if self.method == 'tfidf' or self.method == 'count':
            return self.vectorizer.transform(text_data)

        elif self.method == 'word_embeddings':
            return np.array([self.get_word_embeddings(text) for text in text_data])

    def fit_transform(self, text_data):
        """Fit the vectorizer and then transform the text data."""
        if self.method == 'tfidf' or self.method == 'count':
            return self.vectorizer.fit_transform(text_data)

        elif self.method == 'word_embeddings':
            return np.array([self.get_word_embeddings(text) for text in text_data])

    def get_word_embeddings(self, text):
        """Generate word embeddings using spaCy."""
        doc = self.nlp(text)
        return doc.vector

    def get_feature_names(self):
        """Get feature names from the vectorizer (only for tfidf and count)."""
        if self.method in ['tfidf', 'count']:
            return self.vectorizer.get_feature_names_out()
        else:
            raise ValueError("Feature names not available for word embeddings.")