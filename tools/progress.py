import os, json
from datetime import date
from tools.syllabus import _load_cache

PROGRESS_FILE = r"C:\Projects\ExamBuddy-MCP\storage\progress.json"

def _load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def _save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def mark_topic_done(topic: str, subject: str = "") -> str:
    """Mark a topic as studied/completed for tracking progress."""
    progress = _load_progress()
    cache = _load_cache()
    active_subject = subject if subject else cache.get("active_subject", "General")

    if active_subject not in progress:
        progress[active_subject] = {}

    progress[active_subject][topic] = {
        "status": "completed",
        "date": str(date.today())
    }
    _save_progress(progress)

    total = len(progress[active_subject])
    return f"Marked as done: {topic} ({active_subject})\nTopics completed in this subject: {total}"

def show_progress(subject: str = "") -> str:
    """Show study progress — completed topics, pending topics, and overall completion."""
    progress = _load_progress()
    cache = _load_cache()
    active_subject = subject if subject else cache.get("active_subject", "General")

    if active_subject not in progress or not progress[active_subject]:
        return f"No progress recorded yet for {active_subject}. Use mark_topic_done to track studied topics."

    topics = progress[active_subject]
    completed = [t for t, v in topics.items() if v["status"] == "completed"]

    result = f"Progress report — {active_subject}\n"
    result += f"Completed: {len(completed)} topics\n\n"
    for topic, info in topics.items():
        result += f"[done] {topic} — studied on {info['date']}\n"

    return result

def reset_progress(subject: str = "") -> str:
    """Reset progress for a subject."""
    progress = _load_progress()
    cache = _load_cache()
    active_subject = subject if subject else cache.get("active_subject", "General")

    if active_subject in progress:
        progress[active_subject] = {}
        _save_progress(progress)
        return f"Progress reset for {active_subject}."
    return f"No progress found for {active_subject}."