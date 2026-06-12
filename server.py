from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv(r"C:\Projects\ExamBuddy-MCP\.env")

mcp = FastMCP("ExamBuddy")

from tools.syllabus import load_syllabus, switch_subject, list_subjects
from tools.explain import explain_topic
from tools.questions import generate_questions
from tools.planner import study_plan
from tools.quiz import quiz_me
from tools.progress import mark_topic_done, show_progress, reset_progress
from tools.webview import get_dashboard_data
from tools.workiq import get_smart_recommendation
from tools.webview_panel import open_dashboard
mcp.tool()(open_dashboard)

from tools.streak import get_streak
mcp.tool()(get_streak)

mcp.tool()(get_smart_recommendation)
mcp.tool()(get_dashboard_data)

mcp.tool()(mark_topic_done)
mcp.tool()(show_progress)
mcp.tool()(reset_progress)

mcp.tool()(load_syllabus)
mcp.tool()(switch_subject)
mcp.tool()(list_subjects)
mcp.tool()(explain_topic)
mcp.tool()(generate_questions)
mcp.tool()(study_plan)
mcp.tool()(quiz_me)

if __name__ == "__main__":
    mcp.run(transport="stdio")