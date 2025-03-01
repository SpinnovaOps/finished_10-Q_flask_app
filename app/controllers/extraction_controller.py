from flask import request, jsonify, session
from app.services.extraction_service import ExtractionService

def list_sections():
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data:
        return jsonify({"error": "Missing or invalid JSON payload: code_name is required"}), 400

    code_name = data["code_name"]
    if not isinstance(code_name, str) or not code_name.strip():
        return jsonify({"error": "code_name must be a non-empty string"}), 400

    sections = ExtractionService.list_sections(code_name)
    if "error" in sections:
        return jsonify(sections), 404
    return jsonify(sections), 200

def extract_section_content():
    if "username" not in session:
        return jsonify({"error": "User not logged in"}), 401

    data = request.get_json()
    if not data or "code_name" not in data or "section_name" not in data:
        return jsonify({"error": "Missing or invalid JSON payload: code_name and section_name are required"}), 400

    code_name = data["code_name"]
    section_name = data["section_name"]

    if not isinstance(code_name, str) or not code_name.strip():
        return jsonify({"error": "code_name must be a non-empty string"}), 400
    if not isinstance(section_name, str) or not section_name.strip():
        return jsonify({"error": "section_name must be a non-empty string"}), 400

    content = ExtractionService.get_section_content(code_name, section_name)
    if "error" in content:
        return jsonify(content), 404
    return jsonify(content), 200