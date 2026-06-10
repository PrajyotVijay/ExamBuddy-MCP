import os, json
from openai import OpenAI
from dotenv import load_dotenv
from tools.syllabus import _load_cache
from tools.progress import _load_progress
from tools.quiz import _load_scores

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

CONTEXT_FILE = r"C:\Projects\ExamBuddy-MCP\storage\work_context.json"

def _load_context():
    if os.path.exists(CONTEXT_FILE):
        with open(CONTEXT_FILE, "r") as f:
            return json.load(f)
    return {"session_history": [], "workspace_insights": []}

def _save_context(context):
    with open(CONTEXT_FILE, "w") as f:
        json.dump(context, f, indent=2)

def get_smart_recommendation() -> str:
    """Work IQ powered recommendation — analyzes your study session context, progress, and quiz performance to suggest what to study next."""
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
        timeout=30.0
    )

    # Gather full workspace context — Work IQ pattern
    syllabus = _load_cache()
    progress = _load_progress()
    scores = _load_scores()
    context = _load_context()

    active_subject = syllabus.get("active_subject", "Unknown")
    subject_progress = progress.get(active_subject, {})
    completed_topics = [t for t, v in subject_progress.items() if v["status"] == "completed"]
    accuracy = round((scores["correct"] / scores["total"]) * 100) if scores["total"] > 0 else 0

    # Build workspace intelligence summary
    workspace_summary = f"""
Student workspace context (Work IQ):
- Active subject: {active_subject}
- Topics completed: {", ".join(completed_topics) if completed_topics else "none yet"}
- Quiz accuracy: {accuracy}% ({scores["correct"]}/{scores["total"]} correct)
- Recent quiz topics: {", ".join([h["question"][:40] for h in scores.get("history", [])[-3:]]) if scores.get("history") else "none"}
- Syllabus content available: {"yes" if syllabus.get("content") else "no"}
"""

    # Save context for session memory
    context["session_history"].append({
        "subject": active_subject,
        "completed": len(completed_topics),
        "accuracy": accuracy
    })
    _save_context(context)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an intelligent study advisor with full context of the student's workspace, progress, and performance. Give specific, actionable recommendations."},
            {"role": "user", "content": f"""{workspace_summary}

Based on this student's complete workspace context, provide:
1. The single most important topic they should study right now and why
2. A specific study technique based on their quiz performance
3. A realistic target for their next study session

Be specific, direct, and encouraging. Max 150 words."""}
        ],
        max_tokens=300
    )

    return f"Work IQ Recommendation for {active_subject}:\n\n{response.choices[0].message.content}"