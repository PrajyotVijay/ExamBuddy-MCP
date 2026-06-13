# ExamBuddy Skill

## Description
ExamBuddy is an AI-powered exam study assistant that turns university syllabus PDFs into personalized study tools.

## When to use this skill
Use ExamBuddy when the user wants to:
- Study for an upcoming exam
- Generate a study plan based on their syllabus
- Practice with quiz questions
- Get topic explanations
- Track study progress

## How to use ExamBuddy tools

### Loading a syllabus
Always start by loading the syllabus PDF before using any other tool.
#load_syllabus pdf_path="path/to/syllabus.pdf" subject_name="Subject Name"

### Generating a study plan
After loading syllabus, generate a study plan with exam date:
#study_plan exam_date="DD-MM-YYYY" exam_focus="all units"

### Explaining a topic
#explain_topic topic="Topic Name"

### Generating questions
#generate_questions topic="Topic Name" count=5 question_type="mcq"

question_type options: mcq, short, long, mixed

### Interactive quiz
Step 1 — Get a question:
#quiz_me topic="Topic Name" question_type="mcq"

Step 2 — Submit your answer:
#quiz_me answer="Your answer here"

### Tracking progress
#mark_topic_done topic="Topic Name"

#show_progress

### Getting recommendations
#get_smart_recommendation

### Viewing dashboard

#get_dashboard_data

## Example workflow
1. Load syllabus: `#load_syllabus pdf_path="storage/ps_syllabus.pdf" subject_name="Probability and Statistics"`
2. Generate study plan: `#study_plan exam_date="20-06-2026"`
3. Explain a topic: `#explain_topic topic="Bayes Theorem"`
4. Quiz yourself: `#quiz_me topic="Bayes Theorem" question_type="mcq"`
5. Check progress: `#get_dashboard_data`

## Tips
- Always load syllabus first before using other tools
- Use exam_date parameter in study_plan for accurate countdown
- Quiz Me remembers your last question — answer it before asking a new one
- Use get_smart_recommendation after completing topics for personalized next steps
