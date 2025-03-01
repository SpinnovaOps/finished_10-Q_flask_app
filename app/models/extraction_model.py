from app.utils.mongo_utils import sections_collection

class Section:
    def __init__(self, code_name, section_name, content_information):
        self.code_name = code_name
        self.section_name = section_name
        self.content_information = content_information

    def save(self):
        section_data = {
            "code_name": self.code_name,
            "section_name": self.section_name,
            "content_information": self.content_information
        }
        sections_collection.insert_one(section_data)

    @staticmethod
    def find_by_code_name(code_name):
        return list(sections_collection.find({"code_name": code_name}, {"section_name": 1}))

    @staticmethod
    def find_section_content(code_name, section_name):
        return sections_collection.find_one({"code_name": code_name, "section_name": section_name})