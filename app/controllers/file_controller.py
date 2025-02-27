from flask import request, jsonify, session
from app.services.file_service import FileService
import os

def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    username = session.get("username")
    if not username:
        return jsonify({"error": "Username required, please log in"}), 401

    # Input validation
    if not file.filename:
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    try:
        result = FileService.save_document(file, username)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def list_uploaded_files():
    files = FileService.list_uploaded_files()
    return jsonify(files), 200