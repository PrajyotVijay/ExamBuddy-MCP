import os, json
from openai import OpenAI
from dotenv import load_dotenv
from tools.syllabus import _load_cache

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

SCORE_FILE = r"C:\Projects\ExamBuddy-MCP\storage\quiz_scores.json"
STATE_FILE = r"C:\Projects\ExamBuddy-MCP\storage\quiz_state.json"

def _load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}

def _save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def _load_scores():
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, ValueError):
            return {"total": 0, "correct": 0, "history": []}
    return {"total": 0, "correct": 0, "history": []}

def _save_scores(scores):
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f, indent=2)

def quiz_me(topic: str = "random", answer: str = "", question_type: str = "general") -> str:
    """Interactive quiz — call with no answer to get a question, call with your answer to check it."""
    client = OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=os.getenv("GITHUB_TOKEN"),
        timeout=30.0
    )
    context = _load_cache().get("content", "")
    scores = _load_scores()
    _quiz_state = _load_state()

    if answer and _quiz_state.get("last_question"):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a strict but fair university examiner. Reply in this exact format:\nVERDICT: Correct | Partially Correct | Incorrect\nEXPLANATION: <your explanation>"},
                {"role": "user", "content": f"""Question: {_quiz_state['last_question']}
Correct answer: {_quiz_state.get('last_answer', 'unknown')}
Student answered: {answer}"""}
            ],
            max_tokens=400
        )
        result = response.choices[0].message.content
        verdict = "Incorrect"
        if "VERDICT: Correct" in result:
            verdict = "Correct"
        elif "VERDICT: Partially Correct" in result:
            verdict = "Partially Correct"

        scores["total"] += 1
        if verdict == "Correct":
            scores["correct"] += 1
        scores["history"].append({
            "question": _quiz_state["last_question"],
            "your_answer": answer,
            "verdict": verdict
        })
        _save_scores(scores)
        _save_state({})
        # Auto mark topic as done if correct
        if verdict == "Correct":
            try:
                from tools.progress import mark_topic_done
                from tools.syllabus import _load_cache as get_cache
                active_subject = get_cache().get("active_subject", "General")
                mark_topic_done(f"Quiz session — {active_subject}", active_subject)
            except:
                pass

        accuracy = round((scores["correct"] / scores["total"]) * 100)
        return f"{result}\n\n---\nScore: {scores['correct']}/{scores['total']} ({accuracy}% accuracy)"

    else:
        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a university exam question generator. You MUST follow the exact format given by the user."},
            {"role": "user", "content": f"""Generate 1 exam question on: {topic}
    Context: {context[:1500]}

    IMPORTANT: Return ONLY the following format, nothing else:

    QUESTION: [write question here]
    A) [option 1]
    B) [option 2]
    C) [option 3]
    D) [option 4]
    ANSWER: [correct option letter and text]

    Do not add any intro text. Start directly with QUESTION:""" if question_type == "mcq" else f"""Generate 1 descriptive exam question on: {topic}
    Context: {context[:1500]}

    Return ONLY:
    QUESTION: [question text]
    ANSWER: [model answer]"""}
        ],
        max_tokens=300
    )
    raw = response.choices[0].message.content.strip()

    # Parse question and answer
    q, a = "", ""
    if "QUESTION:" in raw and "ANSWER:" in raw:
        parts = raw.split("ANSWER:")
        q = parts[0].replace("QUESTION:", "").strip()
        a = parts[1].strip()
    else:
        lines = raw.split("\n")
        q = lines[0] if lines else raw
        a = lines[-1] if len(lines) > 1 else ""

    _save_state({"last_question": q, "last_answer": a})

    accuracy = round((scores["correct"] / scores["total"]) * 100) if scores["total"] > 0 else 0
    return f"Question: {q}\n\nSession score: {scores['correct']}/{scores['total']} ({accuracy}% accuracy)"