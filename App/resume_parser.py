import hashlib
import io

from pypdf import PdfReader
from docx import Document

SUPPORTED_TYPES = ["pdf", "docx", "txt"]


def extract_resume_text(uploaded_file) -> str:
    """Extract plain text from a Streamlit-uploaded resume (PDF, DOCX, or TXT)."""
    data = uploaded_file.getvalue()
    name = uploaded_file.name.lower()

    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(data))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    elif name.endswith(".docx"):
        doc = Document(io.BytesIO(data))
        text = "\n".join(p.text for p in doc.paragraphs)
    elif name.endswith(".txt"):
        text = data.decode("utf-8", errors="ignore")
    else:
        raise ValueError(
            f"Unsupported file type: {uploaded_file.name}. "
            f"Supported types: {', '.join(SUPPORTED_TYPES)}."
        )

    text = text.strip()
    if not text:
        raise ValueError(
            "Could not extract any text from the resume. "
            "If it is a scanned PDF, please upload a text-based version."
        )
    return text


def content_hash(uploaded_file) -> str:
    """Stable id for a given uploaded file so the same resume isn't re-ingested."""
    return hashlib.sha256(uploaded_file.getvalue()).hexdigest()[:16]
