from flask import request, jsonify, session
from app.services.file_service import FileService
import os

def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    username = session.get("username")
    if not username:
        return jsonify({"error": "User not logged in"}), 401

    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    try:
        result = FileService.save_document(file_path, username, file.filename)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def list_uploaded_files():
    files = FileService.list_uploaded_files()
    return jsonify(files), 200