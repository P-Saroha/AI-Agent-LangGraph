# AI-Agent Using LangGraph

An end-to-end AI chatbot built with LangGraph and LangChain. This project includes tool routing, RAG over local documents, structured memory (short-term and long-term), and a Streamlit UI. It is designed to show practical agent engineering with clear tool selection and reliable formatting.

## What I Built

- A production-style chatbot with deterministic routing + LLM gating
- RAG over local documents with per-thread indexes
- Long-term memory (Postgres) + short-term memory (summary + last-N)
- Real-time tools for weather, news, stock prices, and time
- Structured answers with sources for tool-based responses
- HITL approval for low-confidence document answers
- A full collection of LangGraph workflow patterns (sequential, parallel, conditional, iterative)
- Short-term memory experiments (persistence, trimming, summarization, deletion)
- LangSmith tracing demos and RAG chatbot variants

## Key Features

- **Hybrid tool selection**: rule-based routing first, then LLM tool gate, then LLM router
- **Weather tool**: OpenWeather API with clean formatted output
- **Search tool**: DuckDuckGo search with structured results + sources
- **Stock tool**: Yahoo Finance via `yfinance`
- **Time tool**: local system time
- **Memory**:
	- STM (summary of older chat + last-N recent messages)
	- LTM (Postgres structured facts)
	- Explicit remember support for user requests
- **RAG**:
	- Upload PDFs/TXT/MD to `knowledge_base/`
	- Per-thread FAISS index
	- Citations for retrieved context
- **Streamlit UI**:
	- Conversation threads
	- Tool trace
	- RAG controls

## What I Learned

- How to design tool routing that avoids tool loops
- How to use RAG only when it is relevant
- How to structure memory into STM/LTM and avoid noise
- How to format tool answers with consistent sources
- How to add fallback logic when tools fail
- How to manage multi-thread chat history in a UI
- How to build sequential, parallel, conditional, and iterative graphs
- How to experiment with STM: persistence, trimming, summarization, deletion
- How to trace and evaluate runs with LangSmith

## Project Structure

```
AI-Agent-LangGraph/
	Chatbot/
		chatbotBackend.py       # Agent logic and routing
		chatbotFrontend.py      # Streamlit UI
		chatbot_memory.py       # LTM + STM memory logic
		chatbot_rag.py          # RAG retrieval and index helpers
		chatbot_tools.py        # Tool routing and tool helpers
		knowledge_base/         # Uploaded docs for RAG
		faiss_index/            # Per-thread FAISS indexes
		docker-compose.yml      # Postgres for long-term memory
	ConditionalWorkflows/     # Conditional graphs (notebooks)
	IterativeWorkflows/       # Iterative loops (notebooks)
	ParallelWorkflows/        # Parallel graph patterns (notebooks)
	SequentialWorkflows/      # Sequential chains (notebooks)
	ShotTermMemeoryLLM/       # Short-term memory experiments (notebooks)
	LangSmith/                # LangSmith tracing examples
	requirements.txt
	README.md
```

## Learning Modules (Notebooks)

- **ConditionalWorkflows**: decision-based flows (e.g., review or quadratic logic)
- **IterativeWorkflows**: looped generation workflows (e.g., post refinement)
- **ParallelWorkflows**: parallel execution patterns (e.g., essay + batsman tasks)
- **SequentialWorkflows**: step-by-step chains (prompt chaining, BMI, basic flow)
- **ShotTermMemeoryLLM**: STM experiments (persistence, deletion, summarization, trimming)
- **LangSmith**: tracing demos and RAG chatbot variants

## Setup

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Configure environment

Create or update `.env` in the project root:

```
GOOGLE_API_KEY=your_gemini_key
OPENWEATHER_API_KEY=your_openweather_key
LTM_POSTGRES_URI=postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable
```

### 3) Start Postgres (for long-term memory)

```bash
cd Chatbot
docker compose up -d
```

### 4) Run the app

```bash
cd Chatbot
streamlit run chatbotFrontend.py
```

## Example Queries

- Weather: "today weather of Delhi"
- News: "latest tech news"
- Stock: "stock price of ORCL"
- Time: "what is the time now"
- RAG: "summarize the PDF I uploaded"
- Memory: "tell me about myself"

## Notes

- The main production agent is inside [Chatbot/](Chatbot/).
- For full chatbot workflow details, see [Chatbot/README.md](Chatbot/README.md).
