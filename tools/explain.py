import os
from openai import OpenAI
from dotenv import load_dotenv
from tools.syllabus import _load_cache

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

def explain_topic(topic: str) -> str:
    """Explain a syllabus topic in exam-focused detail with key points and formulas."""
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
        timeout=30.0
    )

    context = _load_cache().get("content", "No syllabus loaded yet.")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert university exam tutor. Be concise and exam-focused."},
            {"role": "user", "content": f"""Syllabus context:\n{context[:2000]}

Explain this topic for exam preparation: {topic}

Include:
- Core concept (2-3 sentences)
- Key formulas or definitions
- Common exam question angles
- 1 quick example

Keep it under 200 words."""}
        ],
        max_tokens=400
    )
    return response.choices[0].message.content