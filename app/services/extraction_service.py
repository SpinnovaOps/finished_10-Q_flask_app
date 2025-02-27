from app.models.extraction_model import Section

class ExtractionService:
    @staticmethod
    def save_section(code_name, section_name, content_information):
        section = Section(code_name, section_name, content_information)
        section.save()
        return {"message": "Section saved successfully"}

    @staticmethod
    def list_sections(code_name):
        sections = Section.list_sections_by_code_name(code_name)
        return [{"section_name": s["section_name"]} for s in sections]

    @staticmethod
    def get_section_content(code_name, section_name):
        section = Section.find_section_content(code_name, section_name)
        if section:
            return {"section_name": section_name, "content": section["content_information"]}
        return {"error": f"Section '{section_name}' not found for code_name '{code_name}'"}