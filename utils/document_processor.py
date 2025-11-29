import PyPDF2
import docx
from io import BytesIO

def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split('.')[-1].lower()
    
    try:
        if file_type == 'pdf':
            return extract_text_from_pdf(uploaded_file)
        elif file_type == 'docx':
            return extract_text_from_docx(uploaded_file)
        elif file_type == 'txt':
            return uploaded_file.read().decode('utf-8')
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    except Exception as e:
        raise Exception(f"Error extracting text from {file_type}: {str(e)}")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(docx_file):
    doc = docx.Document(BytesIO(docx_file.read()))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()
