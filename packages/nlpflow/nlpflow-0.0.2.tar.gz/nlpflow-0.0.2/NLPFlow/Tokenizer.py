from abc import ABC, abstractmethod
from typing import List, Union
import spacy
from transformers import BertTokenizer
from preprocessing import SpacyModelPicker

class BaseTokenizer(ABC):
    @abstractmethod
    def tokenize(self, text: str):
        pass
    
    def detokenize(self, text: str):
        pass

class Tokenizer(SpacyModelPicker):
    def __init__(self, tokenizer_type="word", model='large'):
        self.tokenizer_type = tokenizer_type
        super().__init__(model)
        if (tokenizer_type == "subword" and model is not None):
            raise ValueError("")

class WordTokenizer:
    def __init__(self, model: str = 'en_core_web_lg'):
        self.nlp = spacy.load(model)

    def tokenize(self, text: str):
        return [token.text for token in self.nlp(text)]

    def detokenize(self, tokens: list):
        return ' '.join(tokens)

class SentenceTokenizer:
    def __init__(self, model: str = 'en_core_web_lg'):
        self.nlp = spacy.load(model)

    def tokenize(self, text: str):
        return [sent.text for sent in self.nlp(text).sents]

    def detokenize(self, tokens: list):
        return ' '.join(tokens)
    
        
class TokenizerFactory:
    @staticmethod
    def get_tokenizer(tokenizer_type: str, model: str):
        if tokenizer_type == "word":
            return WordTokenizer(model)
        elif tokenizer_type == "sentence":
            return SentenceTokenizer(model)
        else:
            raise ValueError(f"Unknown tokenizer type: {tokenizer_type}")
        
class Tokenizer(SpacyModelPicker):
    def __init__(self, model: str = "en_core_web_lg", tokenizer_type: str = 'word'):
        # Use the factory to get the appropriate tokenizer
        self.tokenizer = TokenizerFactory.get_tokenizer(tokenizer_type, model)

    def tokenize(self, text: str):
        return self.tokenizer.tokenize(text)

    def detokenize(self, tokens: list):
        return self.tokenizer.detokenize(tokens)