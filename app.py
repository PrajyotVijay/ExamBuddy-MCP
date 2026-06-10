from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv
import os, json

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

app = Flask(__name__)

UPLOAD_FOLDER = r"C:\Projects\ExamBuddy-MCP\storage"

HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>ExamBuddy</title>
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
.stat-row { display: flex; gap: 8px; margin-bottom: 12px; }
.stat { background: #1e1e2e; border-radius: 8px; padding: 10px; flex: 1; text-align: center; }
.stat .value { font-size: 22px; font-weight: bold; color: #89b4fa; }
.stat .label { font-size: 10px; color: #6c7086; }
.subject-badge { display: inline-block; padding: 3px 10px; background: #45475a; border-radius: 10px; font-size: 11px; margin: 2px; cursor: pointer; }
.subject-badge.active { background: #89b4fa; color: #1e1e2e; font-weight: 600; }
.tag { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-bottom: 4px; }
.tag-correct { background: #a6e3a1; color: #1e1e2e; }
.tag-incorrect { background: #f38ba8; color: #1e1e2e; }
</style>
</head>
<body>
<div class="header">
  <h1>ExamBuddy</h1>
  <span>AI Study Assistant powered by GitHub Copilot + Work IQ</span>
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
      </div>

      <div class="card" id="quizAnswerCard" style="display:none">
        <h2>Submit Answer</h2>
        <textarea id="quizAnswer" rows="3" placeholder="Type your answer here..."></textarea>
        <button class="btn btn-green" onclick="submitAnswer()">Submit Answer</button>
      </div>

    </div>

    <div class="output">
      <h2>Output</h2>
      <div class="result" id="result">Welcome to ExamBuddy. Load a syllabus PDF to get started.</div>
    </div>
  </div>
</div>

<script>
async function api(endpoint, data) {
  document.getElementById('result').innerHTML = '<span class="loading">Processing...</span>';
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  const json = await res.json();
  document.getElementById('result').textContent = json.result || json.error;
  return json;
}

async function loadSyllabus() {
  const file = document.getElementById('syllabusFile').files[0];
  const subject = document.getElementById('subjectName').value || file?.name.replace('.pdf','');
  if (!file) { alert('Please select a PDF file'); return; }
  const formData = new FormData();
  formData.append('file', file);
  formData.append('subject_name', subject);
  document.getElementById('result').innerHTML = '<span class="loading">Loading syllabus...</span>';
  const res = await fetch('/load_syllabus', {method: 'POST', body: formData});
  const json = await res.json();
  document.getElementById('result').textContent = json.result || json.error;
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
  const res = await api('/quiz_me', {topic});
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
    result = quiz_me(topic=data.get('topic','random'), answer=data.get('answer',''))
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)