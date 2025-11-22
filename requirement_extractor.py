"""
Requirement Extraction Module
Extracts requirements from user stories using NLP and pattern matching
"""

import re
from text_preprocessor import TextPreprocessor
import config

class RequirementExtractor:
    """
    Extracts requirement sentences from user stories
    """
    
    def __init__(self):
        """Initialize the requirement extractor"""
        self.preprocessor = TextPreprocessor()
    
    def is_requirement_sentence(self, sentence):
        """
        Determine if a sentence contains a requirement
        
        Args:
            sentence (str): Input sentence
            
        Returns:
            bool: True if sentence contains requirement
        """
        sentence_lower = sentence.lower()
        
        # Check for requirement indicators
        for indicator in config.REQUIREMENT_INDICATORS:
            if indicator in sentence_lower:
                return True
        
        # Check for user story patterns
        for pattern in config.USER_STORY_PATTERNS:
            if re.search(pattern, sentence_lower):
                return True
        
        return False
    
    def extract_requirement_from_user_story(self, sentence):
        """
        Extract the core requirement from a user story format
        
        Args:
            sentence (str): User story sentence
            
        Returns:
            str: Extracted requirement
        """
        sentence_lower = sentence.lower()
        
        # Pattern: "As a X, I want to Y"
        match = re.search(r'i (?:want|need|would like) (?:to )?(.*?)(?:\.|so that|$)', sentence_lower)
        if match:
            return match.group(1).strip()
        
        # Pattern: "The system should/must/shall X"
        match = re.search(r'(?:system|application) (?:should|must|shall|will) (.*?)(?:\.|$)', sentence_lower)
        if match:
            return match.group(1).strip()
        
        # Pattern: "should/must/shall X"
        match = re.search(r'(?:should|must|shall|will) (.*?)(?:\.|$)', sentence_lower)
        if match:
            return match.group(1).strip()
        
        # If no pattern matched, return the sentence as-is
        return sentence.strip()
    
    def extract_requirements_from_text(self, text):
        """
        Extract all requirements from text
        
        Args:
            text (str): Input text containing user stories
            
        Returns:
            list: List of extracted requirements
        """
        # Preprocess text
        preprocessed = self.preprocessor.preprocess_full_pipeline(text)
        
        requirements = []
        
        for sent_data in preprocessed['processed_sentences']:
            sentence = sent_data['sentence']
            
            # Check if it's a requirement sentence
            if self.is_requirement_sentence(sentence):
                # Extract the core requirement
                requirement = self.extract_requirement_from_user_story(sentence)
                
                if requirement:
                    requirements.append({
                        'original_sentence': sentence,
                        'extracted_requirement': requirement,
                        'tokens': sent_data['tokens'],
                        'verbs': sent_data['verbs'],
                        'nouns': sent_data['nouns'],
                        'lemmatized_tokens': sent_data['lemmatized_tokens']
                    })
        
        return requirements
    
    def extract_key_phrases(self, requirement_data):
        """
        Extract key phrases from requirement
        
        Args:
            requirement_data (dict): Requirement data dictionary
            
        Returns:
            list: List of key phrases
        """
        key_phrases = []
        
        # Combine verbs and nouns as key phrases
        verbs = requirement_data['verbs']
        nouns = requirement_data['nouns']
        
        # Verb-noun pairs
        for verb in verbs:
            for noun in nouns:
                key_phrases.append(f"{verb} {noun}")
        
        # Individual verbs and nouns
        key_phrases.extend(verbs)
        key_phrases.extend(nouns)
        
        return list(set(key_phrases))  # Remove duplicates


if __name__ == "__main__":
    # Test the extractor
    extractor = RequirementExtractor()
    
    test_text = """
    As a user, I want to register an account so that I can access the system.
    As a customer, I want to view my order history.
    The system should load within 2 seconds.
    The application must be secure and protect user data.
    As an admin, I need to manage user permissions.
    The system shall be available 99.9% of the time.
    """
    
    requirements = extractor.extract_requirements_from_text(test_text)
    
    print("=== Extracted Requirements ===\n")
    for i, req in enumerate(requirements, 1):
        print(f"\n{i}. Original: {req['original_sentence']}")
        print(f"   Extracted: {req['extracted_requirement']}")
        print(f"   Verbs: {req['verbs']}")
        print(f"   Nouns: {req['nouns']}")
        print(f"   Key Phrases: {extractor.extract_key_phrases(req)}")
