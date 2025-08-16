import os
import fitz  # PyMuPDF
import docx2txt

def extract_text_from_cv(file_path: str) -> str:
    """Extract raw text from CV file (PDF, DOCX, TXT)."""
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        text = []
        with fitz.open(file_path) as doc:
            for page in doc:
                page_text = page.get_text("text")
                if page_text:
                    text.append(page_text)
        return " ".join(text)

    elif ext in [".docx", ".doc"]:
        return docx2txt.process(file_path) or ""

    elif ext == ".txt":
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    else:
        raise ValueError("Unsupported file format. Please upload PDF, DOCX, or TXT.")
