from app.models.document_model import Document
from app.utils.pdf_utils import extract_10q_info, extract_section_by_name
from app.services.extraction_service import ExtractionService
import os
import uuid

class FileService:
    @staticmethod
    def save_document(file, username):
        # Generate unique temporary filename
        temp_filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join("uploads", temp_filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)

        # Extract metadata including filing type
        metadata = extract_10q_info(file_path)
        if "Error" in metadata:
            raise ValueError(metadata["Error"])

        company_name = metadata["Company_Name"]
        filing_date = metadata["Filing_Date"]
        filing_type = metadata.get("Filing_Type")  # Default to 10-Q if not found

        # Assume quarter/annual and year based on filing date or defaults
        quarter_annual = "Q1"  # Adjust based on filing date or logic if needed
        year = filing_date.split(",")[-1].strip() if filing_date else "2025"
        form = filing_type  # Use extracted filing type (10-Q or 10-K)

        # Create Document instance
        doc = Document(company_name, filing_date, quarter_annual, year, form, username)
        
        # Save document with filename included
        doc_data = {
            "company_name": doc.company_name,
            "filing_date": doc.filing_date,
            "quarter_annual": doc.quarter_annual,
            "year": doc.year,
            "form": doc.form,
            "username": doc.username,
            "code_name": doc.code_name,
            "filename": temp_filename  # Use unique temporary filename
        }
        doc.save_with_filename(doc_data)

        return {"code": doc.code_name}

    @staticmethod
    def list_uploaded_files():
        return Document.list_all()