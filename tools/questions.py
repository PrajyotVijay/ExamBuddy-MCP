import os
from openai import OpenAI
from dotenv import load_dotenv
from tools.syllabus import _load_cache

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

def generate_questions(topic: str, count: int = 5, question_type: str = "mixed") -> str:
    """Generate exam-style questions for a topic. Types: mcq, short, long, mixed."""
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
        timeout=30.0
    )
    
    context = _load_cache().get("content", "")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a university exam paper setter."},
            {"role": "user", "content": f"""Generate {count} {question_type} exam questions on: {topic}
Syllabus context: {context[:2000]}

Format each question clearly numbered. For MCQ include 4 options and mark the answer.
Match difficulty to university end-semester exam level."""}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content