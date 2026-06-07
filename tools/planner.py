import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import date
from tools.syllabus import _load_cache

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

def study_plan(days_available: int = 0, exam_focus: str = "all units", exam_date: str = "") -> str:
    """Generate a day-by-day study plan. Optionally provide exam_date as DD-MM-YYYY to auto-calculate days remaining."""
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN")
    )

    if exam_date:
        try:
            day, month, year = map(int, exam_date.split("-"))
            exam = date(year, month, day)
            today = date.today()
            days_available = (exam - today).days
            if days_available <= 0:
                return "Exam date has already passed. Please provide a future date."
        except ValueError:
            return "Invalid date format. Please use DD-MM-YYYY."

    if days_available <= 0:
        return "Please provide either days_available or a valid exam_date in DD-MM-YYYY format."

    context = _load_cache().get("content", "No syllabus loaded. Please run load_syllabus first.")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert academic study planner."},
            {"role": "user", "content": f"""Create a {days_available}-day study plan for a university exam.
Focus: {exam_focus}
Syllabus: {context[:3000]}

Output a day-wise schedule. Each day: topic, study approach (theory/numericals/revision), estimated hours.
End with a 1-day revision buffer. Keep it realistic and exam-pressure-aware."""}
        ],
        max_tokens=1000
    )

    days_info = f"Exam date: {exam_date} | Days remaining: {days_available}" if exam_date else f"Days available: {days_available}"
    return f"{days_info}\n\n{response.choices[0].message.content}"