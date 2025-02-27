import re
import pdfplumber

def extract_company_name(text):
    match = re.search(r"(.*?)\n(?=\(?Exact name of registrant as specified in its charter\)?)", text, re.IGNORECASE)
    return match.group(1).strip() if match else None

def extract_filing_date(text):
    match = re.search(r"For the quarterly period ended\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})", text)
    return match.group(1).strip() if match else None

def determine_file_type(text):
    if re.search(r"FORM 10-Q", text, re.IGNORECASE):
        return "10-Q"
    elif re.search(r"FORM 10-K", text, re.IGNORECASE):
        return "10-K"
    return None

def extract_10q_info(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        if text:
            company_name = extract_company_name(text)
            filing_date = extract_filing_date(text)
            filing_type = determine_file_type(text)
            if not filing_type:
                return {"Error": "Could not determine filing type (10-Q or 10-K)"}
            return {
                "Company_Name": company_name,
                "Filing_Date": filing_date,
                "Filing_Type": filing_type
            }
        else:
            return {"Error": "Could not extract text from the first page"}

def find_section_pages(pdf_path, section_name):
    """Find the start and next section's page number from the index."""
    with pdfplumber.open(pdf_path) as pdf:
        index_page = pdf.pages[1]  # Assuming index is on page 2
        index_text = index_page.extract_text()

        matches = re.findall(r"(Item\s+\d+\..*?)\s+(\d+)", index_text, re.IGNORECASE)
        sections = [(match[0], int(match[1])) for match in matches]

        for i, (sec, page) in enumerate(sections):
            if section_name.lower() in sec.lower():
                next_section = sections[i + 1] if i + 1 < len(sections) else None
                next_section_name = next_section[0] if next_section else None
                next_section_page = next_section[1] if next_section else None
                
                print(f"Section '{sec}' starts on page {page}.")
                if next_section:
                    print(f"Next section '{next_section_name}' starts on page {next_section_page}.")
                
                return page, next_section_name, next_section_page

        print(f"Section '{section_name}' not found in the index.")
        return None, None, None

def extract_section_by_name(pdf_path, section_name):
    """Extract only the relevant section text from its start page until the next section starts."""
    start_page, next_section_name, next_section_page = find_section_pages(pdf_path, section_name)
    if start_page is None:
        return {"error": f"Section '{section_name}' not found in the index."}

    with pdfplumber.open(pdf_path) as pdf:
        extracted_text = []
        found_section = False

        for i in range(start_page - 2, len(pdf.pages)):
            page = pdf.pages[i]
            text = page.extract_text()

            if text:
                if found_section:
                    if next_section_name and re.search(fr"({next_section_name})", text, re.IGNORECASE):
                        extracted_text.append(text[:re.search(fr"({next_section_name})", text, re.IGNORECASE).start()])
                        break
                    extracted_text.append(text)
                    if next_section_page and i + 1 == next_section_page - 1:
                        break
                else:
                    match = re.search(fr"({section_name})", text, re.IGNORECASE)
                    if match:
                        found_section = True
                        section_text = text[match.start():]
                        if next_section_name:
                            next_match = re.search(fr"({next_section_name})", section_text, re.IGNORECASE)
                            if next_match:
                                section_text = section_text[:next_match.start()]
                                found_section = False
                        extracted_text.append(section_text)

        if extracted_text:
            section_content = "\n".join(extracted_text)
            print(f"\nExtracted Section '{section_name}':\n{section_content}")
            return {
                "section_name": section_name,
                "start_page": start_page,
                "end_page": next_section_page,
                "content": section_content
            }
    return {"error": f"Section '{section_name}' not found on the expected pages."}