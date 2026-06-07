import os, json
from pypdf import PdfReader

CACHE_FILE = r"C:\Projects\ExamBuddy-MCP\storage\cache.json"

def _save_cache(text, path):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"content": text, "path": path}, f)

def _load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

_syllabus_cache = _load_cache()

def load_syllabus(pdf_path: str) -> str:
    """Load a university syllabus PDF and extract its topics for study."""
    global _syllabus_cache
    if not os.path.exists(pdf_path):
        return f"Error: File not found at {pdf_path}"
    
    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    
    _syllabus_cache = {"content": text, "path": pdf_path}
    _save_cache(text, pdf_path)
    
    preview = text[:500] + "..." if len(text) > 500 else text
    return f"✅ Syllabus loaded ({len(reader.pages)} pages).\n\nPreview:\n{preview}"