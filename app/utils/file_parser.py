import fitz  # PyMuPDF
from docx import Document


def parse_pdf(file_path: str) -> str:
    text = ""
    doc = fitz.open(file_path)

    for page in doc:
        text += page.get_text()

    return text


def parse_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def extract_text(file_path: str, filename: str) -> str:
    if filename.endswith(".pdf"):
        return parse_pdf(file_path)

    elif filename.endswith(".docx"):
        return parse_docx(file_path)

    else:
        raise ValueError("Unsupported file format")