from app.utils.mongo_utils import documents_collection

class Document:
    def __init__(self, company_name, filing_date, quarter_annual, year, form, username):
        self.company_name = company_name
        self.filing_date = filing_date
        self.quarter_annual = quarter_annual
        self.year = year
        self.form = form  # Now dynamic (10-Q or 10-K)
        self.username = username
        self.code_name = self.generate_code_name()

    def generate_code_name(self):
        return f"{self.company_name}_{self.year}_{self.quarter_annual}_{self.form}".replace(" ", "_").upper()

    def save(self):
        doc_data = {
            "company_name": self.company_name,
            "filing_date": self.filing_date,
            "quarter_annual": self.quarter_annual,
            "year": self.year,
            "form": self.form,
            "username": self.username,
            "code_name": self.code_name
        }
        documents_collection.insert_one(doc_data)

    def save_with_filename(self, doc_data):
        documents_collection.insert_one(doc_data)

    @staticmethod
    def find_by_code_name(code_name):
        return documents_collection.find_one({"code_name": code_name})

    @staticmethod
    def list_all():
        docs = documents_collection.find({}, {"_id": 0, "filename": 1, "code_name": 1})
        return [{"filename": doc.get("filename", ""), "code": doc["code_name"]} for doc in docs]