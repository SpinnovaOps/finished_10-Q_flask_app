from flask import Blueprint, request, jsonify, session
from app.utils.mongo_utils import sections_collection
import os
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag
from nltk import ne_chunk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import ssl

# Ensure NLTK resources are downloaded
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('vader_lexicon')

# Create Blueprint
processing_bp = Blueprint('processing', __name__, url_prefix='/processing')

# Ensure output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '../../outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_to_file(filename, content):
    """Helper function to save content to a .txt file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def get_section_content(code_name, section_name):
    """Retrieve content_information from MongoDB."""
    section = sections_collection.find_one({"code_name": code_name, "section_name": section_name})
    if not section or "content_information" not in section or not section["content_information"]:
        raise ValueError("Section not found or content is empty")
    return section["content_information"]

@processing_bp.route('/segmentation', methods=['POST'])
def segmentation():
    """Segment text into sentences."""
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing code_name or section_name"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    try:
        content = get_section_content(code_name, section_name)
        sentences = sent_tokenize(content)
        result = "\n".join(sentences)
        save_to_file(f"{code_name}_{section_name}_segmentation.txt", result)
        return jsonify({"message": "Segmentation complete", "sentences": sentences}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@processing_bp.route('/tokenization', methods=['POST'])
def tokenization():
    """Tokenize segmented text into words."""
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing code_name or section_name"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    try:
        content = get_section_content(code_name, section_name)
        sentences = sent_tokenize(content)
        tokens = [word_tokenize(sentence) for sentence in sentences]
        result = "\n".join([" ".join(token_list) for token_list in tokens])
        save_to_file(f"{code_name}_{section_name}_tokenization.txt", result)
        return jsonify({"message": "Tokenization complete", "tokens": tokens}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@processing_bp.route('/stopwords', methods=['POST'])
def stopwords_removal():
    """Remove stopwords from tokenized text."""
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing code_name or section_name"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    try:
        content = get_section_content(code_name, section_name)
        sentences = sent_tokenize(content)
        tokens = [word_tokenize(sentence) for sentence in sentences]
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [[word for word in token_list if word.lower() not in stop_words] for token_list in tokens]
        result = "\n".join([" ".join(token_list) for token_list in filtered_tokens])
        save_to_file(f"{code_name}_{section_name}_stopwords.txt", result)
        return jsonify({"message": "Stopwords removed", "filtered_tokens": filtered_tokens}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@processing_bp.route('/lemmatization', methods=['POST'])
def lemmatization():
    """Lemmatize tokens after stopwords removal."""
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing code_name or section_name"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    try:
        content = get_section_content(code_name, section_name)
        sentences = sent_tokenize(content)
        tokens = [word_tokenize(sentence) for sentence in sentences]
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [[word for word in token_list if word.lower() not in stop_words] for token_list in tokens]
        lemmatizer = WordNetLemmatizer()
        lemmatized = [[lemmatizer.lemmatize(word) for word in token_list] for token_list in filtered_tokens]
        result = "\n".join([" ".join(token_list) for token_list in lemmatized])
        save_to_file(f"{code_name}_{section_name}_lemmatization.txt", result)
        return jsonify({"message": "Lemmatization complete", "lemmatized": lemmatized}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@processing_bp.route('/stemming', methods=['POST'])
def stemming():
    """Stem tokens after lemmatization."""
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing code_name or section_name"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    try:
        content = get_section_content(code_name, section_name)
        sentences = sent_tokenize(content)
        tokens = [word_tokenize(sentence) for sentence in sentences]
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [[word for word in token_list if word.lower() not in stop_words] for token_list in tokens]
        lemmatizer = WordNetLemmatizer()
        lemmatized = [[lemmatizer.lemmatize(word) for word in token_list] for token_list in filtered_tokens]
        stemmer = PorterStemmer()
        stemmed = [[stemmer.stem(word) for word in token_list] for token_list in lemmatized]
        result = "\n".join([" ".join(token_list) for token_list in stemmed])
        save_to_file(f"{code_name}_{section_name}_stemming.txt", result)
        return jsonify({"message": "Stemming complete", "stemmed": stemmed}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@processing_bp.route('/pos_tagging', methods=['POST'])
def pos_tagging():
    """Perform POS tagging on stemmed tokens."""
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing code_name or section_name"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    try:
        content = get_section_content(code_name, section_name)
        sentences = sent_tokenize(content)
        tokens = [word_tokenize(sentence) for sentence in sentences]
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [[word for word in token_list if word.lower() not in stop_words] for token_list in tokens]
        pos_tagged = [pos_tag(token_list) for token_list in filtered_tokens]
        result = "\n".join([str(tagged) for tagged in pos_tagged])
        save_to_file(f"{code_name}_{section_name}_pos_tagging.txt", result)
        return jsonify({"message": "POS tagging complete", "pos_tagged": [dict(tagged) for tagged in pos_tagged]}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@processing_bp.route('/ne_tagging', methods=['POST'])
def ne_tagging():
    """Perform Named Entity Recognition on POS-tagged tokens."""
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing code_name or section_name"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    try:
        content = get_section_content(code_name, section_name)
        sentences = sent_tokenize(content)
        tokens = [word_tokenize(sentence) for sentence in sentences]
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [[word for word in token_list if word.lower() not in stop_words] for token_list in tokens]
        pos_tagged = [pos_tag(token_list) for token_list in filtered_tokens]
        ne_tagged = [ne_chunk(tagged) for tagged in pos_tagged]
        result = "\n".join([str(tree) for tree in ne_tagged])
        save_to_file(f"{code_name}_{section_name}_ne_tagging.txt", result)
        # Convert tree to string for JSON serialization
        return jsonify({"message": "NE tagging complete", "ne_tagged": [str(tree) for tree in ne_tagged]}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@processing_bp.route('/sentiment_analysis', methods=['POST'])
def sentiment_analysis():
    """Perform sentiment analysis and return polarity scores."""
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing code_name or section_name"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    try:
        content = get_section_content(code_name, section_name)
        sid = SentimentIntensityAnalyzer()
        scores = sid.polarity_scores(content)
        result = f"Sentiment Scores: {scores}"
        save_to_file(f"{code_name}_{section_name}_sentiment.txt", result)
        return jsonify({"message": "Sentiment analysis complete", "polarity_scores": scores}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
