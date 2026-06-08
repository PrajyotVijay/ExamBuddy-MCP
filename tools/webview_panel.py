import os, json

PROGRESS_FILE = r"C:\Projects\ExamBuddy-MCP\storage\progress.json"
SCORE_FILE = r"C:\Projects\ExamBuddy-MCP\storage\quiz_scores.json"
CACHE_FILE = r"C:\Projects\ExamBuddy-MCP\storage\cache.json"
SUBJECTS_FILE = r"C:\Projects\ExamBuddy-MCP\storage\subjects.json"

def open_dashboard() -> str:
    """Generate an HTML dashboard for ExamBuddy — paste the output into a .html file to view."""

    # Load all data
    cache = {}
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

    subjects = {}
    if os.path.exists(SUBJECTS_FILE):
        with open(SUBJECTS_FILE, "r") as f:
            subjects = json.load(f)

    progress = {}
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            progress = json.load(f)

    scores = {"total": 0, "correct": 0, "history": []}
    if os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "r") as f:
            scores = json.load(f)

    active_subject = cache.get("active_subject", "None")
    subject_progress = progress.get(active_subject, {})
    completed_topics = [t for t, v in subject_progress.items() if v["status"] == "completed"]
    accuracy = round((scores["correct"] / scores["total"]) * 100) if scores["total"] > 0 else 0

    # Build subjects list HTML
    subjects_html = ""
    for name, info in subjects.items():
        active_badge = '<span style="background:#4CAF50;color:white;padding:2px 8px;border-radius:10px;font-size:11px;margin-left:8px;">active</span>' if name == active_subject else ""
        subjects_html += f'<div class="subject-item">{name} — {info["pages"]} pages{active_badge}</div>'

    # Build topics HTML
    topics_html = ""
    for topic in completed_topics:
        date = subject_progress[topic]["date"]
        topics_html += f'<div class="topic-item"><span class="check">✓</span>{topic}<span class="date">{date}</span></div>'
    if not topics_html:
        topics_html = '<div class="empty">No topics marked yet.</div>'

    # Build quiz history HTML
    history_html = ""
    for item in scores["history"][-5:]:
        color = "#4CAF50" if item["verdict"] == "Correct" else "#FF5722" if item["verdict"] == "Incorrect" else "#FF9800"
        history_html += f'<div class="history-item"><span class="verdict" style="color:{color}">{item["verdict"]}</span>{item["question"][:70]}...</div>'
    if not history_html:
        history_html = '<div class="empty">No quiz history yet.</div>'

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>ExamBuddy Dashboard</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: 'Segoe UI', sans-serif; background: #1e1e2e; color: #cdd6f4; min-height: 100vh; padding: 24px; }}
  h1 {{ font-size: 24px; color: #89b4fa; margin-bottom: 4px; }}
  .subtitle {{ font-size: 13px; color: #6c7086; margin-bottom: 24px; }}
  .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .card {{ background: #313244; border-radius: 12px; padding: 20px; }}
  .card h2 {{ font-size: 13px; text-transform: uppercase; letter-spacing: 1px; color: #6c7086; margin-bottom: 16px; }}
  .stat-row {{ display: flex; gap: 16px; margin-bottom: 16px; }}
  .stat {{ background: #1e1e2e; border-radius: 8px; padding: 12px 16px; flex: 1; }}
  .stat .value {{ font-size: 28px; font-weight: bold; color: #89b4fa; }}
  .stat .label {{ font-size: 11px; color: #6c7086; margin-top: 2px; }}
  .subject-item {{ padding: 8px 12px; background: #1e1e2e; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }}
  .topic-item {{ display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: #1e1e2e; border-radius: 6px; margin-bottom: 8px; font-size: 13px; }}
  .check {{ color: #a6e3a1; font-weight: bold; }}
  .date {{ margin-left: auto; color: #6c7086; font-size: 11px; }}
  .history-item {{ padding: 8px 12px; background: #1e1e2e; border-radius: 6px; margin-bottom: 8px; font-size: 12px; }}
  .verdict {{ font-weight: bold; margin-right: 8px; }}
  .empty {{ color: #6c7086; font-size: 13px; padding: 8px; }}
  .accuracy-bar {{ background: #1e1e2e; border-radius: 20px; height: 8px; margin-top: 8px; }}
  .accuracy-fill {{ background: #a6e3a1; border-radius: 20px; height: 8px; width: {accuracy}%; }}
  .full-width {{ grid-column: 1 / -1; }}
</style>
</head>
<body>
<h1>ExamBuddy</h1>
<p class="subtitle">Study Intelligence Dashboard — {active_subject}</p>

<div class="grid">
  <div class="card">
    <h2>Overview</h2>
    <div class="stat-row">
      <div class="stat"><div class="value">{len(completed_topics)}</div><div class="label">Topics Done</div></div>
      <div class="stat"><div class="value">{scores["total"]}</div><div class="label">Questions Attempted</div></div>
      <div class="stat"><div class="value">{accuracy}%</div><div class="label">Quiz Accuracy</div></div>
    </div>
    <div class="accuracy-bar"><div class="accuracy-fill"></div></div>
  </div>

  <div class="card">
    <h2>Loaded Subjects</h2>
    {subjects_html if subjects_html else '<div class="empty">No subjects loaded.</div>'}
  </div>

  <div class="card">
    <h2>Completed Topics</h2>
    {topics_html}
  </div>

  <div class="card">
    <h2>Recent Quiz History</h2>
    {history_html}
  </div>
</div>
</body>
</html>"""

    # Save to storage
    output_path = r"C:\Projects\ExamBuddy-MCP\storage\dashboard.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return f"Dashboard generated at: {output_path}\n\nOpen this file in your browser to view the ExamBuddy dashboard."