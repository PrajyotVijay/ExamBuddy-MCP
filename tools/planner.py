import os
from openai import OpenAI
from dotenv import load_dotenv
from tools.syllabus import _load_cache

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")


def study_plan(days_available: int, exam_focus: str = "all units") -> str:
    """Generate a day-by-day study plan based on the loaded syllabus."""
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN")
    )
    
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
    return response.choices[0].message.content