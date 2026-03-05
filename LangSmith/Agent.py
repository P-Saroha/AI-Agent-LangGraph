import requests
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# LLM
from langchain_google_genai import ChatGoogleGenerativeAI

# Tools
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

# Agent
from langchain.agents import create_react_agent
from langchain.agents import AgentExecutor

# Prompt hub
from langchain import hub


# -------------------------
# Search Tool
# -------------------------
search_tool = DuckDuckGoSearchRun()


# -------------------------
# Weather Tool
# -------------------------
@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""
    url = f"https://wttr.in/{city}?format=3"
    return requests.get(url).text


# -------------------------
# Gemini LLM
# -------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)


# -------------------------
# Tools list
# -------------------------
tools = [search_tool, get_weather]


# -------------------------
# Prompt
# -------------------------
prompt = hub.pull("hwchase17/react")


# -------------------------
# Create Agent
# -------------------------
agent = create_react_agent(
    llm,
    tools,
    prompt
)


# -------------------------
# Agent Executor
# -------------------------
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# -------------------------
# Chat Loop
# -------------------------
while True:
    q = input("\nAsk: ")

    if q.lower() in ["exit", "quit"]:
        break

    result = agent_executor.invoke({"input": q})

    print("\nAnswer:", result["output"])