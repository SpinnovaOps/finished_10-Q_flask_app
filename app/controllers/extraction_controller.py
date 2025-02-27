from flask import request, jsonify
from app.services.extraction_service import ExtractionService

def list_sections():
    data = request.get_json()
    code_name = data["code_name"]
    sections = ExtractionService.list_sections(code_name)
    return jsonify(sections), 200

def extract_section_content():
    data = request.get_json()
    code_name = data["code_name"]
    section_name = data["section_name"]
    content = ExtractionService.get_section_content(code_name, section_name)
    return jsonify(content), 200