from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("ExamBuddy")

from tools.syllabus import load_syllabus
from tools.explain import explain_topic
from tools.questions import generate_questions
from tools.planner import study_plan
from tools.quiz import quiz_me

mcp.tool()(load_syllabus)
mcp.tool()(explain_topic)
mcp.tool()(generate_questions)
mcp.tool()(study_plan)
mcp.tool()(quiz_me)

if __name__ == "__main__":
    mcp.run(transport="stdio")