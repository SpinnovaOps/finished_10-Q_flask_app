from app.models.document_model import Document
from app.utils.pdf_utils import extract_10q_info, get_quarter_from_date
import os
import uuid

class FileService:
    @staticmethod
    def save_document(file_path, username, original_filename):
        # Extract company information
        metadata = extract_10q_info(file_path)
        if "Error" in metadata:
            raise ValueError(metadata["Error"])

        company_name = metadata["Company_Name"]
        filing_date = metadata["Filing_Date"]
        filing_type = metadata["Filing_Type"]

        if not filing_type:
            raise ValueError("Unable to determine filing type (10-Q or 10-K)")

        # Determine quarter from filing date
        quarter_annual = get_quarter_from_date(filing_date) if filing_date else "Invalid Date"
        if quarter_annual == "Invalid Date":
            raise ValueError("Invalid filing date format")

        year = filing_date.split(",")[-1].strip() if filing_date else "2025"
        filename = original_filename  # Store original filename

        # Generate unique temporary filename
        temp_filename = f"{uuid.uuid4().hex}_{filename}"
        temp_file_path = os.path.join("uploads", temp_filename)

        # Create Document instance and generate code_name
        doc = Document(company_name, filing_date, quarter_annual, year, filing_type, username)

        # Save document metadata with original filename
        doc_data = {
            "company_name": doc.company_name,
            "filing_date": doc.filing_date,
            "quarter_annual": doc.quarter_annual,
            "year": doc.year,
            "form": doc.form,  # Now filing_type
            "username": doc.username,
            "code_name": doc.code_name,
            "filename": temp_filename  # Store temporary filename
        }
        doc.save_with_filename(doc_data)

        # Move file to uploads with unique name
        os.rename(file_path, temp_file_path)

        return {"code": doc.code_name}

    @staticmethod
    def list_uploaded_files():
        return Document.list_all()