from flask import Blueprint

# Create a Blueprint for processing routes
processing_bp = Blueprint('processing', __name__, url_prefix='/processing')

# Route 1: Segmentation
@processing_bp.route('/segmentation', methods=['GET'])
def segmentation():
    return "segmentation"

# Route 2: Tokenization
@processing_bp.route('/tokenization', methods=['GET'])
def tokenization():
    return "tokenization"

# Route 3: Removing Stopwords
@processing_bp.route('/removing_stopwords', methods=['GET'])
def removing_stopwords():
    return "removing_stopwords"

# Route 4: Stemming
@processing_bp.route('/stemming', methods=['GET'])
def stemming():
    return "stemming"

# Route 5: Lemmatization
@processing_bp.route('/lemmatization', methods=['GET'])
def lemmatization():
    return "lemmatization"

# Route 6: POS Tagging
@processing_bp.route('/POStagging', methods=['GET'])
def pos_tagging():
    return "POStagging"

# Route 7: NE Tagging
@processing_bp.route('/NEtagging', methods=['GET'])
def ne_tagging():
    return "NEtagging"