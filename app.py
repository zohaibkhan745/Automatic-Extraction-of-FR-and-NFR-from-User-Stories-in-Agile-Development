"""
Flask Web Application for FR/NFR Extraction System
Provides a web interface for the system
"""

from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
from requirement_classifier import RequirementClassifier

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize classifier
classifier = RequirementClassifier()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze user stories and return classification results"""
    try:
        # Get input text
        text = request.form.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No input text provided'}), 400
        
        # Classify requirements
        results = classifier.classify_text(text)
        
        # Format for JSON response
        response = {
            'success': True,
            'total_requirements': results['total_requirements'],
            'fr_count': results['fr_count'],
            'nfr_count': results['nfr_count'],
            'functional_requirements': [
                {
                    'requirement': fr['requirement'],
                    'original': fr['original_sentence'],
                    'confidence': f"{fr['confidence']:.0%}",
                    'verbs': fr['verbs'],
                    'nouns': fr['nouns']
                }
                for fr in results['functional_requirements']
            ],
            'non_functional_requirements': [
                {
                    'requirement': nfr['requirement'],
                    'original': nfr['original_sentence'],
                    'category': nfr['nfr_category'],
                    'confidence': f"{nfr['confidence']:.0%}",
                    'verbs': nfr['verbs'],
                    'nouns': nfr['nouns']
                }
                for nfr in results['non_functional_requirements']
            ]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_file', methods=['POST'])
def analyze_file():
    """Analyze user stories from uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Read file content
        if file.filename.endswith('.txt'):
            text = file.read().decode('utf-8')
        elif file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            # Assume first column contains user stories
            text = '\n'.join(df.iloc[:, 0].astype(str).tolist())
        else:
            return jsonify({'error': 'Unsupported file format. Use .txt or .csv'}), 400
        
        if not text.strip():
            return jsonify({'error': 'File is empty'}), 400
        
        # Classify requirements
        results = classifier.classify_text(text)
        
        # Format for JSON response
        response = {
            'success': True,
            'total_requirements': results['total_requirements'],
            'fr_count': results['fr_count'],
            'nfr_count': results['nfr_count'],
            'functional_requirements': [
                {
                    'requirement': fr['requirement'],
                    'original': fr['original_sentence'],
                    'confidence': f"{fr['confidence']:.0%}",
                    'verbs': fr['verbs'],
                    'nouns': fr['nouns']
                }
                for fr in results['functional_requirements']
            ],
            'non_functional_requirements': [
                {
                    'requirement': nfr['requirement'],
                    'original': nfr['original_sentence'],
                    'category': nfr['nfr_category'],
                    'confidence': f"{nfr['confidence']:.0%}",
                    'verbs': nfr['verbs'],
                    'nouns': nfr['nouns']
                }
                for nfr in results['non_functional_requirements']
            ]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("\n" + "=" * 60)
    print("FR/NFR EXTRACTION SYSTEM - Web Interface")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    app.run(debug=False, host='127.0.0.1', port=5000)
