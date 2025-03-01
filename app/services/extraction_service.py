from app.models.extraction_model import Section
from app.models.document_model import Document  # Add this import
from app.utils.pdf_utils import get_index_sections, extract_section_by_name, extract_item1_financial_statements
import os

class ExtractionService:
    @staticmethod
    def save_section(code_name, section_name, content_information):
        section = Section(code_name, section_name, content_information)
        section.save()
        return {"message": "Section saved successfully"}

    @staticmethod
    def list_sections(code_name):
        # Find the document by code_name to get the filename
        doc = Document.find_by_code_name(code_name)
        if not doc or "filename" not in doc:
            return {"error": "Document not found or filename missing"}

        pdf_path = os.path.join("uploads", doc["filename"])
        if not os.path.exists(pdf_path):
            return {"error": f"PDF file not found at {pdf_path}"}

        # Extract all section names from the PDF
        sections = get_index_sections(pdf_path)
        
        # Store section names in sections collection
        for section in sections:
            section_data = {
                "code_name": code_name,
                "section_name": section["section_name"],
                "content_information": ""  # Initially empty, filled later
            }
            Section(code_name, section["section_name"], "").save()

        return [{"section_name": section["section_name"]} for section in sections]

    @staticmethod
    def get_section_content(code_name, section_name):
        # Find the document by code_name to get the filename
        doc = Document.find_by_code_name(code_name)
        if not doc or "filename" not in doc:
            return {"error": "Document not found or filename missing"}

        pdf_path = os.path.join("uploads", doc["filename"])
        if not os.path.exists(pdf_path):
            return {"error": f"PDF file not found at {pdf_path}"}

        # Extract section content based on section_name
        if section_name.lower() == "item 1. financial statements":
            section_data = extract_item1_financial_statements(pdf_path)
        else:
            section_data = extract_section_by_name(pdf_path, section_name)

        if "error" in section_data:
            return section_data

        ExtractionService.save_section(code_name, section_name, section_data["content"])

        return {
            "section_name": section_name,
            "content": section_data["content"]
        }