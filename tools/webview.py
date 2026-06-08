import os, json

PROGRESS_FILE = r"C:\Projects\ExamBuddy-MCP\storage\progress.json"
SCORE_FILE = r"C:\Projects\ExamBuddy-MCP\storage\quiz_scores.json"
CACHE_FILE = r"C:\Projects\ExamBuddy-MCP\storage\cache.json"
SUBJECTS_FILE = r"C:\Projects\ExamBuddy-MCP\storage\subjects.json"

def get_dashboard_data() -> str:
    """Get a full dashboard summary of active subject, progress, and quiz scores."""
    
    # Active subject
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
    
    active_subject = cache.get("active_subject", "None")

    # Subjects
    subjects = {}
    if os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, "r") as f:
            subjects = json.load(f)

    # Progress
    progress = {}
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)

    subject_progress = progress.get(active_subject, {})
    completed_topics = [t for t, v in subject_progress.items() if v["status"] == "completed"]

    # Quiz scores
    scores = {"total": 0, "correct": 0, "history": []}
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            scores = json.load(f)

    accuracy = round((scores["correct"] / scores["total"]) * 100) if scores["total"] > 0 else 0

    result = f"""
EXAMBUDDY DASHBOARD
===================
Active Subject: {active_subject}
Loaded Subjects: {", ".join(subjects.keys()) if subjects else "none"}

STUDY PROGRESS
--------------
Topics completed: {len(completed_topics)}
{chr(10).join(f"  - {t}" for t in completed_topics) if completed_topics else "  No topics marked yet."}

QUIZ PERFORMANCE
----------------
Total questions attempted: {scores["total"]}
Correct answers: {scores["correct"]}
Accuracy: {accuracy}%

RECENT QUIZ HISTORY
-------------------"""

    if scores["history"]:
        for item in scores["history"][-5:]:
            result += f"\n  [{item['verdict']}] {item['question'][:60]}..."
    else:
        result += "\n  No quiz history yet."

    return result