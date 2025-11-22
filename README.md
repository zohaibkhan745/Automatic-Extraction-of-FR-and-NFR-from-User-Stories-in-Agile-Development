# 🎯 Automatic Extraction of Functional and Non-Functional Requirements from User Stories

An intelligent NLP-based system that automatically extracts and classifies **Functional Requirements (FR)** and **Non-Functional Requirements (NFR)** from Agile user stories using Python and NLTK.

## 🌟 Features

- ✅ **Automatic Requirement Extraction** - Extracts requirements from natural language text
- ✅ **FR/NFR Classification** - Intelligently classifies requirements using NLP
- ✅ **Web Interface** - User-friendly Flask-based web application
- ✅ **File Upload Support** - Process `.txt` and `.csv` files
- ✅ **Real-time Analysis** - Instant results with confidence scores
- ✅ **Detailed Insights** - Shows verbs, nouns, and NFR categories

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/zohaibkhan745/Automatic-Extraction-of-FR-and-NFR-from-User-Stories-in-Agile-Development.git
cd Automatic-Extraction-of-FR-and-NFR-from-User-Stories-in-Agile-Development
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download NLTK data**
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('punkt_tab')"
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

## 📖 Usage

### Text Input
1. Enter user stories in the text area
2. Click "Analyze Text"
3. View classified requirements

### File Upload
1. Click "Upload File"
2. Select a `.txt` or `.csv` file
3. View extracted requirements

### Example Input
```
As a user, I want to register an account.
As a user, I want to search for products.
The system must load within 2 seconds.
The application must be secure.
```

### Example Output
**Functional Requirements:**
- register an account (Confidence: 85%)
- search for products (Confidence: 85%)

**Non-Functional Requirements:**
- load within 2 seconds (Performance, Confidence: 90%)
- be secure (Security, Confidence: 80%)

## 🏗️ Project Structure

```
├── app.py                      # Flask web application
├── requirement_classifier.py   # Core NLP classification logic
├── text_preprocessor.py       # Text preprocessing utilities
├── sample_user_stories.csv    # Sample dataset
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Web interface
└── README.md                 # This file
```

## 🧠 NLP Techniques Used

| Technique | Purpose |
|-----------|---------|
| **Tokenization** | Split text into sentences and words |
| **Stop Word Removal** | Remove common words |
| **Lemmatization** | Convert words to base form |
| **POS Tagging** | Identify parts of speech |
| **Pattern Matching** | Detect NFR patterns |
| **Keyword Matching** | Identify requirement types |

## 📊 Classification Logic

The system uses a rule-based approach:

1. **Pattern Detection** - Matches regex patterns for NFRs (e.g., "within X seconds")
2. **Keyword Analysis** - Identifies NFR keywords (secure, fast, reliable, etc.)
3. **Verb Analysis** - Detects action verbs for FRs (create, add, search, etc.)
4. **Confidence Scoring** - Assigns confidence levels to classifications

## 🎯 NFR Categories

- **Performance** - Speed, response time, load time
- **Security** - Authentication, encryption, authorization
- **Usability** - User-friendliness, ease of use
- **Reliability** - Uptime, availability
- **Scalability** - Concurrent users, capacity
- **Maintainability** - Code quality, updates

## 🛠️ Technologies

- **Python 3.12** - Programming language
- **NLTK** - Natural Language Processing
- **Flask** - Web framework
- **Pandas** - Data handling
- **Scikit-learn** - Machine learning utilities

## 📝 Requirements

See `requirements.txt`:
```
flask
pandas
nltk
scikit-learn
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Zohaib Malik**
- GitHub: [@zohaibkhan745](https://github.com/zohaibkhan745)

## 🙏 Acknowledgments

- NLTK Team for the excellent NLP library
- Flask Team for the web framework
- Agile community for user story best practices

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**⭐ If you find this project helpful, please give it a star!**
