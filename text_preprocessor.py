"""
Text Preprocessing Module
Handles all NLP preprocessing tasks using NLTK
"""

import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import config

class TextPreprocessor:
    """
    Preprocesses text using NLTK techniques
    """
    
    def __init__(self):
        """Initialize preprocessor and download required NLTK data"""
        self.lemmatizer = WordNetLemmatizer()
        self._download_nltk_resources()
        self.stop_words = set(stopwords.words('english'))
        # Remove requirement indicators from stopwords
        for word in config.REQUIREMENT_INDICATORS:
            for w in word.split():
                if w in self.stop_words:
                    self.stop_words.remove(w)
    
    def _download_nltk_resources(self):
        """Download necessary NLTK resources if not already present"""
        resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'omw-1.4']
        for resource in resources:
            try:
                nltk.data.find(f'tokenizers/{resource}')
            except LookupError:
                try:
                    nltk.download(resource, quiet=True)
                except:
                    pass
    
    def clean_text(self, text):
        """
        Clean and normalize text
        
        Args:
            text (str): Raw input text
            
        Returns:
            str: Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep periods and commas
        text = re.sub(r'[^\w\s\.\,\-]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def tokenize_sentences(self, text):
        """
        Split text into sentences
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of sentences
        """
        return sent_tokenize(text)
    
    def tokenize_words(self, text):
        """
        Split text into words
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of words
        """
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        """
        Remove stopwords from token list
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Filtered tokens
        """
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def lemmatize(self, tokens):
        """
        Apply lemmatization to tokens
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: Lemmatized tokens
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def pos_tagging(self, tokens):
        """
        Perform Part-of-Speech tagging
        
        Args:
            tokens (list): List of tokens
            
        Returns:
            list: List of (token, pos_tag) tuples
        """
        return pos_tag(tokens)
    
    def extract_verbs(self, pos_tags):
        """
        Extract verbs from POS tagged tokens
        
        Args:
            pos_tags (list): List of (token, pos_tag) tuples
            
        Returns:
            list: List of verbs
        """
        return [token for token, tag in pos_tags if tag.startswith('VB')]
    
    def extract_nouns(self, pos_tags):
        """
        Extract nouns from POS tagged tokens
        
        Args:
            pos_tags (list): List of (token, pos_tag) tuples
            
        Returns:
            list: List of nouns
        """
        return [token for token, tag in pos_tags if tag.startswith('NN')]
    
    def preprocess_full_pipeline(self, text):
        """
        Complete preprocessing pipeline
        
        Args:
            text (str): Raw input text
            
        Returns:
            dict: Dictionary containing all preprocessing results
        """
        # Clean text
        cleaned_text = self.clean_text(text)
        
        # Tokenize into sentences
        sentences = self.tokenize_sentences(cleaned_text)
        
        results = {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'sentences': sentences,
            'processed_sentences': []
        }
        
        # Process each sentence
        for sentence in sentences:
            # Word tokenization
            tokens = self.tokenize_words(sentence)
            
            # POS tagging (before removing stopwords to maintain context)
            pos_tags = self.pos_tagging(tokens)
            
            # Extract verbs and nouns
            verbs = self.extract_verbs(pos_tags)
            nouns = self.extract_nouns(pos_tags)
            
            # Remove stopwords
            filtered_tokens = self.remove_stopwords(tokens)
            
            # Lemmatization
            lemmatized_tokens = self.lemmatize(filtered_tokens)
            
            sentence_data = {
                'sentence': sentence,
                'tokens': tokens,
                'pos_tags': pos_tags,
                'verbs': verbs,
                'nouns': nouns,
                'filtered_tokens': filtered_tokens,
                'lemmatized_tokens': lemmatized_tokens
            }
            
            results['processed_sentences'].append(sentence_data)
        
        return results


if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = TextPreprocessor()
    
    test_text = """
    As a user, I want to register an account.
    The system should load within 2 seconds.
    The application must be secure.
    """
    
    results = preprocessor.preprocess_full_pipeline(test_text)
    
    print("=== Preprocessing Results ===\n")
    print(f"Original Text: {results['original_text']}\n")
    print(f"Cleaned Text: {results['cleaned_text']}\n")
    print(f"Sentences: {results['sentences']}\n")
    
    for i, sent_data in enumerate(results['processed_sentences'], 1):
        print(f"\n--- Sentence {i}: {sent_data['sentence']} ---")
        print(f"Tokens: {sent_data['tokens']}")
        print(f"POS Tags: {sent_data['pos_tags']}")
        print(f"Verbs: {sent_data['verbs']}")
        print(f"Nouns: {sent_data['nouns']}")
        print(f"Filtered Tokens: {sent_data['filtered_tokens']}")
        print(f"Lemmatized: {sent_data['lemmatized_tokens']}")
