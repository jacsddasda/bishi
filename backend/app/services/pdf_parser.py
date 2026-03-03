import PyPDF2
import os

def parse_pdf(filepath):
    """
    Parse PDF file and extract text content
    """
    text = ""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n\n'
        
        # Clean up the extracted text
        text = clean_text(text)
        return text
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")

def clean_text(text):
    """
    Clean and normalize extracted text
    """
    # Remove excessive whitespace
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Strip whitespace and remove empty lines
        cleaned_line = line.strip()
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    
    # Join lines with proper spacing
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Remove any special characters that might cause issues
    cleaned_text = cleaned_text.replace('\r', '')
    
    return cleaned_text
