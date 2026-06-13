from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
import os, json

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "storage")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>ExamBuddy — AI Study Assistant</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🎓</text></svg>">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Segoe UI', sans-serif; background: #1e1e2e; color: #cdd6f4; min-height: 100vh; }
.header { padding: 24px 40px; border-bottom: 1px solid #313244; display: flex; align-items: center; gap: 12px; }
.header h1 { font-size: 22px; color: #89b4fa; }
.header span { font-size: 13px; color: #6c7086; }
.container { max-width: 1100px; margin: 32px auto; padding: 0 24px; }
.grid { display: grid; grid-template-columns: 300px 1fr; gap: 24px; }
.sidebar { display: flex; flex-direction: column; gap: 16px; }
.card { background: #313244; border-radius: 12px; padding: 20px; }
.card h2 { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #6c7086; margin-bottom: 16px; }
.btn { width: 100%; padding: 10px 16px; border-radius: 8px; border: none; cursor: pointer; font-size: 13px; font-family: 'Segoe UI', sans-serif; margin-bottom: 8px; transition: opacity 0.2s; }
.btn:hover { opacity: 0.85; }
.btn-primary { background: #89b4fa; color: #1e1e2e; font-weight: 600; }
.btn-secondary { background: #45475a; color: #cdd6f4; }
.btn-green { background: #a6e3a1; color: #1e1e2e; font-weight: 600; }
.btn-yellow { background: #f9e2af; color: #1e1e2e; font-weight: 600; }
input, select, textarea { width: 100%; padding: 8px 12px; background: #1e1e2e; border: 1px solid #45475a; border-radius: 6px; color: #cdd6f4; font-size: 13px; font-family: 'Segoe UI', sans-serif; margin-bottom: 8px; }
input[type="file"] { padding: 6px; }
label { font-size: 12px; color: #6c7086; display: block; margin-bottom: 4px; }
.output { background: #313244; border-radius: 12px; padding: 24px; min-height: 400px; }
.output h2 { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #6c7086; margin-bottom: 16px; }
.result { background: #1e1e2e; border-radius: 8px; padding: 16px; white-space: pre-wrap; font-size: 13px; line-height: 1.6; min-height: 300px; }
.loading { color: #6c7086; font-style: italic; }
@keyframes spin { to { transform: rotate(360deg); } }
.spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid #45475a; border-top-color: #89b4fa; border-radius: 50%; animation: spin 0.8s linear infinite; margin-right: 8px; vertical-align: middle; }
@media (max-width: 768px) {
  .grid { grid-template-columns: 1fr; }
  .container { padding: 0 12px; }
  .header { padding: 16px 20px; }
  .header span { display: none; }
  .output { min-height: 300px; }
  .result { min-height: 200px; }
}
</style>
</head>
<body>
<div id="landing" style="display:block">
  <div style="min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px">
    <h1 style="font-size:48px;color:#89b4fa;margin-bottom:12px">ExamBuddy</h1>
    <p style="font-size:18px;color:#cdd6f4;margin-bottom:8px">Turn your syllabus PDF into a personal AI study assistant</p>
    <p style="font-size:14px;color:#6c7086;margin-bottom:48px">Powered by GitHub Copilot + Work IQ — built for engineering students</p>
    <div style="display:flex;gap:24px;margin-bottom:64px;flex-wrap:wrap;justify-content:center">
      <div style="background:#313244;border-radius:12px;padding:24px;width:200px">
        <div style="font-size:28px;font-weight:700;color:#89b4fa;margin-bottom:12px">01</div>
        <div style="font-weight:600;margin-bottom:8px;color:#cdd6f4">Smart Study Plans</div>
        <div style="font-size:13px;color:#6c7086">Day-by-day plans tailored to your syllabus and exam date</div>
      </div>
      <div style="background:#313244;border-radius:12px;padding:24px;width:200px">
        <div style="font-size:28px;font-weight:700;color:#a6e3a1;margin-bottom:12px">02</div>
        <div style="font-weight:600;margin-bottom:8px;color:#cdd6f4">Interactive Quiz</div>
        <div style="font-size:13px;color:#6c7086">Practice with AI-generated questions and instant grading</div>
      </div>
      <div style="background:#313244;border-radius:12px;padding:24px;width:200px">
        <div style="font-size:28px;font-weight:700;color:#f9e2af;margin-bottom:12px">03</div>
        <div style="font-weight:600;margin-bottom:8px;color:#cdd6f4">Progress Dashboard</div>
        <div style="font-size:13px;color:#6c7086">Track topics, quiz scores, and get smart recommendations</div>
      </div>
    </div>
    <button onclick="document.getElementById('landing').style.display='none';document.getElementById('app').style.display='block'" style="background:#89b4fa;color:#1e1e2e;border:none;padding:16px 48px;border-radius:8px;font-size:16px;font-weight:600;cursor:pointer">Get Started</button>
    <p style="margin-top:16px;font-size:12px;color:#6c7086">No signup required — just upload your syllabus PDF</p>
  </div>
</div>

<div id="app" style="display:none">
<div class="header">
  <h1>ExamBuddy</h1>
  <span id="activeSubject">AI Study Assistant powered by GitHub Copilot + Work IQ</span>
</div>
<div class="container">
  <div class="grid">
    <div class="sidebar">
      <div class="card">
        <h2>Load Syllabus</h2>
        <label>Subject Name</label>
        <input type="text" id="subjectName" placeholder="e.g. Probability and Statistics">
        <label>Syllabus PDF</label>
        <input type="file" id="syllabusFile" accept=".pdf">
        <button class="btn btn-primary" onclick="loadSyllabus()">Load Syllabus</button>
      </div>
      <div class="card">
        <h2>Study Plan</h2>
        <label>Exam Date (DD-MM-YYYY)</label>
        <input type="text" id="examDate" placeholder="e.g. 20-06-2026">
        <label>Focus Area</label>
        <input type="text" id="examFocus" placeholder="e.g. all units">
        <button class="btn btn-green" onclick="getStudyPlan()">Generate Study Plan</button>
      </div>
      <div class="card">
        <h2>Tools</h2>
        <label>Topic</label>
        <input type="text" id="topicInput" placeholder="e.g. Bayes Theorem">
        <button class="btn btn-secondary" onclick="explainTopic()">Explain Topic</button>
        <label>Question Type</label>
        <select id="questionType">
          <option value="mixed">Mixed</option>
          <option value="mcq">MCQ</option>
          <option value="short">Short Answer</option>
          <option value="long">Long Answer</option>
        </select>
        <button class="btn btn-secondary" onclick="generateQuestions()">Generate Questions</button>
        <button class="btn btn-yellow" onclick="quizMe()">Quiz Me</button>
        <button class="btn btn-secondary" onclick="getDashboard()">View Dashboard</button>
        <button class="btn btn-secondary" onclick="getRecommendation()">Smart Recommendation</button>
        <button class="btn btn-secondary" onclick="getStreak()">Study Streak</button>
        <button class="btn btn-secondary" onclick="getAnalytics()">Performance Analytics</button>
      </div>
      <div class="card" id="quizAnswerCard" style="display:none">
        <h2>Submit Answer</h2>
        <textarea id="quizAnswer" rows="3" placeholder="Type your answer here..."></textarea>
        <button class="btn btn-green" onclick="submitAnswer()">Submit Answer</button>
      </div>
    </div>
    <div class="output">
      <h2 id="outputTitle">Output</h2>
      <div class="result" id="result">Welcome to ExamBuddy. Load a syllabus PDF to get started.</div>
    </div>
  </div>
</div>


<script>
async function api(endpoint, data) {
  document.getElementById('outputTitle').textContent = 'Processing...';
  document.getElementById('result').innerHTML = '<span class="loading"><span class="spinner"></span>Processing...</span>';
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  const json = await res.json();
  document.getElementById('result').textContent = json.result || json.error;
  document.getElementById('outputTitle').textContent = 'Output';
  return json;
}

async function loadSyllabus() {
  const file = document.getElementById('syllabusFile').files[0];
  const subject = document.getElementById('subjectName').value || file?.name.replace('.pdf','');
  if (!file) { alert('Please select a PDF file'); return; }
  const formData = new FormData();
  formData.append('file', file);
  formData.append('subject_name', subject);
  document.getElementById('result').innerHTML = '<span class="loading"><span class="spinner"></span>Loading syllabus...</span>';
  const res = await fetch('/load_syllabus', {method: 'POST', body: formData});
  const json = await res.json();
  document.getElementById('result').textContent = json.result || json.error;
  document.getElementById('activeSubject').textContent = 'Active subject: ' + subject;
}

async function getStudyPlan() {
  await api('/study_plan', {
    exam_date: document.getElementById('examDate').value,
    exam_focus: document.getElementById('examFocus').value || 'all units'
  });
}

async function explainTopic() {
  const topic = document.getElementById('topicInput').value;
  if (!topic) { alert('Enter a topic'); return; }
  await api('/explain_topic', {topic});
}

async function generateQuestions() {
  const topic = document.getElementById('topicInput').value;
  if (!topic) { alert('Enter a topic'); return; }
  await api('/generate_questions', {topic, question_type: document.getElementById('questionType').value});
}

async function quizMe() {
  const topic = document.getElementById('topicInput').value || 'random';
  const question_type = document.getElementById('questionType').value;
  const res = await api('/quiz_me', {topic, question_type});
  if (res.result) document.getElementById('quizAnswerCard').style.display = 'block';
}

async function submitAnswer() {
  const answer = document.getElementById('quizAnswer').value;
  if (!answer) { alert('Enter your answer'); return; }
  await api('/quiz_me', {answer});
  document.getElementById('quizAnswer').value = '';
  document.getElementById('quizAnswerCard').style.display = 'none';
}

async function getDashboard() {
  await api('/dashboard', {});
}

async function getRecommendation() {
  await api('/recommendation', {});
}

async function getStreak() {
  await api('/streak', {});
}

async function getAnalytics() {
  await api('/analytics', {});
}
</script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/load_syllabus', methods=['POST'])
def load_syllabus_route():
    from tools.syllabus import load_syllabus
    file = request.files.get('file')
    subject_name = request.form.get('subject_name', '')
    if not file:
        return jsonify({'error': 'No file provided'})
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)
    result = load_syllabus(path, subject_name)
    return jsonify({'result': result})

@app.route('/study_plan', methods=['POST'])
def study_plan_route():
    from tools.planner import study_plan
    data = request.json
    result = study_plan(exam_date=data.get('exam_date',''), exam_focus=data.get('exam_focus','all units'))
    return jsonify({'result': result})

@app.route('/explain_topic', methods=['POST'])
def explain_topic_route():
    from tools.explain import explain_topic
    data = request.json
    result = explain_topic(data.get('topic',''))
    return jsonify({'result': result})

@app.route('/generate_questions', methods=['POST'])
def generate_questions_route():
    from tools.questions import generate_questions
    data = request.json
    result = generate_questions(data.get('topic',''), question_type=data.get('question_type','mixed'))
    return jsonify({'result': result})

@app.route('/quiz_me', methods=['POST'])
def quiz_me_route():
    from tools.quiz import quiz_me
    data = request.json
    result = quiz_me(
        topic=data.get('topic','random'),
        answer=data.get('answer',''),
        question_type=data.get('question_type','general')
    )
    return jsonify({'result': result})

@app.route('/dashboard', methods=['POST'])
def dashboard_route():
    from tools.webview import get_dashboard_data
    result = get_dashboard_data()
    return jsonify({'result': result})

@app.route('/recommendation', methods=['POST'])
def recommendation_route():
    from tools.workiq import get_smart_recommendation
    result = get_smart_recommendation()
    return jsonify({'result': result})

@app.route('/streak', methods=['POST'])
def streak_route():
    from tools.streak import get_streak
    result = get_streak()
    return jsonify({'result': result})

@app.route('/analytics', methods=['POST'])
def analytics_route():
    from tools.quiz import _load_scores
    from tools.progress import _load_progress
    from tools.syllabus import _load_cache
    
    scores = _load_scores()
    cache = _load_cache()
    progress = _load_progress()
    active_subject = cache.get("active_subject", "General")
    subject_progress = progress.get(active_subject, {})
    completed = list(subject_progress.keys())
    accuracy = round((scores["correct"] / scores["total"]) * 100) if scores["total"] > 0 else 0
    
    if scores["total"] < 2:
        return jsonify({'result': f'Answer at least 2 quiz questions to see analytics.\n\nCurrent: {scores["total"]} questions attempted.'})
    
    # Find weak topics from history
    topic_performance = {}
    for item in scores["history"]:
        q = item["question"][:40]
        if q not in topic_performance:
            topic_performance[q] = {"correct": 0, "total": 0}
        topic_performance[q]["total"] += 1
        if item["verdict"] == "Correct":
            topic_performance[q]["correct"] += 1
    
    weak = [t for t, v in topic_performance.items() if v["correct"] == 0]
    strong = [t for t, v in topic_performance.items() if v["correct"] == v["total"]]
    
    result = f"""PERFORMANCE ANALYTICS — {active_subject}

Overall Accuracy: {accuracy}%
Questions Attempted: {scores["total"]}
Correct Answers: {scores["correct"]}
Topics Completed: {len(completed)}

STRONG AREAS:
{chr(10).join(f'  + {t}...' for t in strong) if strong else '  Keep practicing to identify strong areas'}

WEAK AREAS (needs attention):
{chr(10).join(f'  - {t}...' for t in weak) if weak else '  No weak areas identified yet'}

RECOMMENDATION:
{"Focus on weak areas before exam." if weak else "Great performance! Keep practicing new topics."}"""
    
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)