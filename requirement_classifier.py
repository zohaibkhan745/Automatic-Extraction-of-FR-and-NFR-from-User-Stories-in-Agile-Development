"""
Requirement Classification Module
Classifies requirements as Functional (FR) or Non-Functional (NFR)
"""

import re
from requirement_extractor import RequirementExtractor
import config

class RequirementClassifier:
    """
    Classifies requirements into Functional and Non-Functional categories
    """
    
    def __init__(self):
        """Initialize the classifier"""
        self.extractor = RequirementExtractor()
        self.functional_keywords = set([kw.lower() for kw in config.FUNCTIONAL_KEYWORDS])
        self.nfr_keywords = set([kw.lower() for kw in config.NON_FUNCTIONAL_KEYWORDS])
    
    def calculate_keyword_score(self, text, keywords):
        """
        Calculate score based on keyword matches
        
        Args:
            text (str): Text to analyze
            keywords (set): Set of keywords to match
            
        Returns:
            int: Number of keyword matches
        """
        text_lower = text.lower()
        score = 0
        
        for keyword in keywords:
            if keyword in text_lower:
                score += 1
        
        return score
    
    def has_performance_indicators(self, text):
        """
        Check if text contains performance-related indicators
        
        Args:
            text (str): Text to analyze
            
        Returns:
            bool: True if performance indicators found
        """
        performance_patterns = [
            r'\d+\s*(millisecond|second|minute|ms|s|min)',
            r'within\s+\d+',
            r'(fast|quick|speed|performance|load time|response time)',
            r'concurrent\s+users?',
            r'\d+%\s*(uptime|availability)'
        ]
        
        text_lower = text.lower()
        for pattern in performance_patterns:
            if re.search(pattern, text_lower):
                return True
        
        return False
    
    def has_quality_attributes(self, text):
        """
        Check if text contains quality attributes (NFR indicators)
        
        Args:
            text (str): Text to analyze
            
        Returns:
            bool: True if quality attributes found
        """
        quality_words = [
            'secure', 'security', 'reliable', 'available', 'scalable',
            'maintainable', 'usable', 'portable', 'efficient', 'stable',
            'robust', 'user-friendly', 'intuitive', 'compatible'
        ]
        
        text_lower = text.lower()
        for word in quality_words:
            if word in text_lower:
                return True
        
        return False
    
    def classify_requirement(self, requirement_data):
        """
        Classify a single requirement as FR or NFR
        
        Args:
            requirement_data (dict): Requirement data from extractor
            
        Returns:
            dict: Classification result
        """
        requirement = requirement_data['extracted_requirement']
        original = requirement_data['original_sentence']
        
        # Calculate scores
        fr_score = self.calculate_keyword_score(requirement, self.functional_keywords)
        nfr_score = self.calculate_keyword_score(requirement, self.nfr_keywords)
        
        # Check for NFR indicators
        has_performance = self.has_performance_indicators(requirement)
        has_quality = self.has_quality_attributes(requirement)
        
        # Add bonus scores for NFR indicators
        if has_performance:
            nfr_score += 3
        if has_quality:
            nfr_score += 2
        
        # Determine classification
        if nfr_score > fr_score:
            classification = 'NFR'
            confidence = nfr_score / (fr_score + nfr_score + 1)  # +1 to avoid division by zero
        elif fr_score > nfr_score:
            classification = 'FR'
            confidence = fr_score / (fr_score + nfr_score + 1)
        else:
            # If tied, default to FR (functional requirements are more common)
            classification = 'FR'
            confidence = 0.5
        
        # Determine NFR subcategory if classified as NFR
        nfr_category = None
        if classification == 'NFR':
            nfr_category = self.identify_nfr_category(requirement)
        
        return {
            'original_sentence': original,
            'requirement': requirement,
            'classification': classification,
            'confidence': round(confidence, 2),
            'fr_score': fr_score,
            'nfr_score': nfr_score,
            'nfr_category': nfr_category,
            'verbs': requirement_data['verbs'],
            'nouns': requirement_data['nouns']
        }
    
    def identify_nfr_category(self, text):
        """
        Identify the specific NFR category
        
        Args:
            text (str): Requirement text
            
        Returns:
            str: NFR category name
        """
        text_lower = text.lower()
        
        category_scores = {}
        
        for category, keywords in config.NFR_CATEGORIES.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    score += 1
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            # Return category with highest score
            return max(category_scores, key=category_scores.get)
        
        return 'general'
    
    def classify_text(self, text):
        """
        Extract and classify all requirements from text
        
        Args:
            text (str): Input text containing user stories
            
        Returns:
            dict: Classification results with FR and NFR lists
        """
        # Extract requirements
        requirements = self.extractor.extract_requirements_from_text(text)
        
        # Classify each requirement
        functional_requirements = []
        non_functional_requirements = []
        
        for req_data in requirements:
            classification = self.classify_requirement(req_data)
            
            if classification['classification'] == 'FR':
                functional_requirements.append(classification)
            else:
                non_functional_requirements.append(classification)
        
        return {
            'functional_requirements': functional_requirements,
            'non_functional_requirements': non_functional_requirements,
            'total_requirements': len(requirements),
            'fr_count': len(functional_requirements),
            'nfr_count': len(non_functional_requirements)
        }
    
    def format_output(self, results):
        """
        Format classification results for display
        
        Args:
            results (dict): Classification results
            
        Returns:
            str: Formatted output string
        """
        output = []
        output.append("=" * 60)
        output.append("REQUIREMENT CLASSIFICATION RESULTS")
        output.append("=" * 60)
        output.append(f"\nTotal Requirements Found: {results['total_requirements']}")
        output.append(f"Functional Requirements: {results['fr_count']}")
        output.append(f"Non-Functional Requirements: {results['nfr_count']}")
        output.append("\n")
        
        # Functional Requirements
        output.append("─" * 60)
        output.append("FUNCTIONAL REQUIREMENTS (FR)")
        output.append("─" * 60)
        
        if results['functional_requirements']:
            for i, fr in enumerate(results['functional_requirements'], 1):
                output.append(f"\n{i}. {fr['requirement']}")
                output.append(f"   Confidence: {fr['confidence']:.0%}")
                output.append(f"   Original: {fr['original_sentence']}")
        else:
            output.append("\nNo functional requirements found.")
        
        # Non-Functional Requirements
        output.append("\n")
        output.append("─" * 60)
        output.append("NON-FUNCTIONAL REQUIREMENTS (NFR)")
        output.append("─" * 60)
        
        if results['non_functional_requirements']:
            for i, nfr in enumerate(results['non_functional_requirements'], 1):
                output.append(f"\n{i}. {nfr['requirement']}")
                output.append(f"   Category: {nfr['nfr_category'].upper()}")
                output.append(f"   Confidence: {nfr['confidence']:.0%}")
                output.append(f"   Original: {nfr['original_sentence']}")
        else:
            output.append("\nNo non-functional requirements found.")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)


if __name__ == "__main__":
    # Test the classifier
    classifier = RequirementClassifier()
    
    test_text = """
    As a user, I want to register an account.
    The system should load within 2 seconds.
    The application must be secure.
    As a customer, I want to view my order history.
    The system must handle 1000 concurrent users.
    As an admin, I need to delete user accounts.
    The interface should be user-friendly and intuitive.
    I want to search for products by name.
    The system shall be available 99.9% of the time.
    """
    
    results = classifier.classify_text(test_text)
    print(classifier.format_output(results))
