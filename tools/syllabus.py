import os, json
from pypdf import PdfReader

CACHE_FILE = r"C:\Projects\ExamBuddy-MCP\storage\cache.json"
SUBJECTS_FILE = r"C:\Projects\ExamBuddy-MCP\storage\subjects.json"

def _save_cache(text, path, subject):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({"content": text, "path": path, "active_subject": subject}, f)

def _load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}

def _load_subjects():
    if os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save_subjects(subjects):
    with open(SUBJECTS_FILE, "w", encoding="utf-8") as f:
        json.dump(subjects, f, indent=2)

def load_syllabus(pdf_path: str, subject_name: str = "") -> str:
    """Load a university syllabus PDF. Optionally provide subject_name to manage multiple subjects."""
    if not os.path.exists(pdf_path):
        return f"Error: File not found at {pdf_path}"

    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

    subject = subject_name if subject_name else os.path.basename(pdf_path).replace(".pdf", "")

    # Save to subjects registry
    subjects = _load_subjects()
    subjects[subject] = {"path": pdf_path, "pages": len(reader.pages)}
    _save_subjects(subjects)

    # Set as active subject
    _save_cache(text, pdf_path, subject)

    preview = text[:500] + "..." if len(text) > 500 else text
    return f"Syllabus loaded — Subject: {subject} ({len(reader.pages)} pages)\n\nPreview:\n{preview}"

def switch_subject(subject_name: str) -> str:
    """Switch the active subject to a previously loaded syllabus."""
    subjects = _load_subjects()

    if subject_name not in subjects:
        available = ", ".join(subjects.keys()) if subjects else "none loaded yet"
        return f"Subject '{subject_name}' not found. Available subjects: {available}"

    pdf_path = subjects[subject_name]["path"]
    if not os.path.exists(pdf_path):
        return f"Error: PDF file no longer exists at {pdf_path}. Please reload it."

    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
    _save_cache(text, pdf_path, subject_name)

    return f"Switched to subject: {subject_name} ({subjects[subject_name]['pages']} pages)"

def list_subjects() -> str:
    """List all loaded subjects and show the currently active one."""
    subjects = _load_subjects()
    cache = _load_cache()
    active = cache.get("active_subject", "none")

    if not subjects:
        return "No subjects loaded yet. Use load_syllabus to load a PDF."

    result = f"Loaded subjects (active: {active}):\n"
    for name, info in subjects.items():
        marker = "-> " if name == active else "   "
        result += f"{marker}{name} — {info['pages']} pages\n"
    return result