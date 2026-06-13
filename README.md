# ExamBuddy — AI Study Assistant

ExamBuddy turns any university syllabus PDF into a personal AI-powered study assistant. Built as both a web application and a VS Code MCP server, it integrates with GitHub Copilot and uses Work IQ to deliver intelligent, context-aware study support.

> **Live Demo:** [exambuddy-mcp.onrender.com](https://exambuddy-mcp.onrender.com) | **Repo:** [PrajyotVijay/ExamBuddy-MCP](https://github.com/PrajyotVijay/ExamBuddy-MCP)
---

## The Problem

Every engineering student receives a syllabus PDF on the first day and is left alone to figure out how to study it. No structure, no guidance, no personalization — just a PDF and an exam date looming ahead.

## The Solution

ExamBuddy reads your syllabus and becomes your personal study assistant. Load your PDF, set your exam date, and get a tailored study plan, topic explanations, practice questions, and an interactive quiz — all powered by AI.

---

## Features

| Feature | Description |
|---------|-------------|
| Smart Study Plans | Day-by-day plans auto-calculated from your exam date |
| Topic Explanations | Exam-focused explanations with key formulas |
| Question Generator | MCQ, short answer, and long answer questions |
| Interactive Quiz | AI-graded quiz with persistent score tracking |
| Progress Tracker | Track completed topics per subject |
| Multi-Subject Support | Load and switch between multiple syllabi |
| Performance Analytics | Identify strong and weak areas |
| Study Streak | Track consecutive study days |
| Smart Recommendations | Work IQ powered next-step suggestions |
| Dashboard | Complete study session overview |

---

## Tech Stack

- **Frontend:** Flask web app with responsive dark UI
- **Backend:** Python + FastMCP server
- **AI:** GitHub Models API (GPT-4o-mini) via Azure AI Inference
- **Microsoft IQ:** Work IQ — session context and workspace intelligence
- **PDF Parsing:** pypdf
- **Deployment:** Render

---

## How It Works

```
Student uploads syllabus PDF
         ↓
ExamBuddy parses and indexes content
         ↓
Work IQ builds session context from progress + quiz history
         ↓
AI tools deliver personalized study assistance
         ↓
Dashboard shows complete study intelligence
```

---

## Quick Start

### Web App (Recommended)
Visit [exambuddy-mcp.onrender.com](https://exambuddy-mcp.onrender.com)

1. Click **Get Started**
2. Upload your syllabus PDF
3. Enter subject name and click **Load Syllabus**
4. Use Study Plan, Quiz Me, and other tools

### Local Setup

```bash
git clone https://github.com/PrajyotVijay/ExamBuddy-MCP.git
cd ExamBuddy-MCP
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`:

GITHUB_TOKEN=your_github_personal_access_token

Run:
```bash
python app.py
```

Open `localhost:5000` in your browser.

### VS Code MCP Server

Create `.vscode/mcp.json`:
```json
{
  "servers": {
    "ExamBuddy": {
      "type": "stdio",
      "command": "path/to/.venv/Scripts/python.exe",
      "args": ["server.py"],
      "cwd": "path/to/ExamBuddy-MCP"
    }
  }
}
```

Open GitHub Copilot Chat in Agent mode and use ExamBuddy tools directly.

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `load_syllabus` | Parse syllabus PDF and set active subject |
| `switch_subject` | Switch between loaded subjects |
| `list_subjects` | List all loaded subjects |
| `explain_topic` | Exam-focused topic explanation |
| `generate_questions` | Generate exam-style questions |
| `study_plan` | Day-wise study plan with exam countdown |
| `quiz_me` | Interactive quiz with answer grading |
| `mark_topic_done` | Mark topic as studied |
| `show_progress` | View study progress |
| `get_dashboard_data` | Full study session dashboard |
| `get_smart_recommendation` | Work IQ powered recommendations |
| `get_streak` | View study streak |

---

## Microsoft IQ Integration

ExamBuddy integrates **Work IQ** — the intelligence layer that builds context from the student's study session, quiz history, completed topics, and active subject to deliver personalized recommendations that adapt as the student progresses.

The AI inference runs on `models.inference.ai.azure.com` — Azure AI Foundry infrastructure — making ExamBuddy directly compatible with enterprise Foundry IQ deployment.

---

## Built For

Microsoft Agents League Hackathon 2026 — Creative Apps Track
