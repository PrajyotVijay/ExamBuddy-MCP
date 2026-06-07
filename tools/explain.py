import os
from openai import OpenAI
from dotenv import load_dotenv
from tools.syllabus import _load_cache

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

def explain_topic(topic: str) -> str:
    """Explain a syllabus topic in exam-focused detail with key points and formulas."""
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN")
    )
    
    context = _load_cache.get("content", "No syllabus loaded yet.")
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert university exam tutor."},
            {"role": "user", "content": f"""Syllabus context:\n{context[:3000]}

Explain this topic for exam preparation: {topic}

Include:
- Core concept (2-3 sentences)
- Key formulas or definitions (if applicable)
- Common exam question angles
- 1 quick example or analogy

Be concise and exam-focused."""}
        ],
        max_tokens=800
    )
    return response.choices[0].message.content