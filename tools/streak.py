import os, json
from datetime import date, timedelta

STREAK_FILE = r"C:\Projects\ExamBuddy-MCP\storage\streak.json"

def _load_streak():
    if os.path.exists(STREAK_FILE):
        try:
            with open(STREAK_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {"current_streak": 0, "longest_streak": 0, "last_study_date": "", "total_days": 0}
    return {"current_streak": 0, "longest_streak": 0, "last_study_date": "", "total_days": 0}

def _save_streak(streak):
    with open(STREAK_FILE, "w") as f:
        json.dump(streak, f, indent=2)

def update_streak() -> dict:
    """Update study streak — call this whenever user studies."""
    streak = _load_streak()
    today = str(date.today())
    yesterday = str(date.today() - timedelta(days=1))

    if streak["last_study_date"] == today:
        return streak
    elif streak["last_study_date"] == yesterday:
        streak["current_streak"] += 1
    else:
        streak["current_streak"] = 1

    streak["last_study_date"] = today
    streak["total_days"] += 1
    streak["longest_streak"] = max(streak["longest_streak"], streak["current_streak"])
    _save_streak(streak)
    return streak

def get_streak() -> str:
    """Get current study streak information."""
    streak = _load_streak()
    update_streak()
    return f"Current streak: {streak['current_streak']} days\nLongest streak: {streak['longest_streak']} days\nTotal study days: {streak['total_days']}"