# AI-Agent Using LangGraph

An end-to-end AI chatbot built with LangGraph and LangChain. This project includes tool routing, RAG over local documents, structured memory (short-term and long-term), and a Streamlit UI. It is designed to show practical agent engineering with clear tool selection and reliable formatting.

## What I Built

- A production-style chatbot with deterministic routing + LLM gating
- RAG over local documents with per-thread indexes
- Long-term memory (Postgres) + short-term memory (session context)
- Real-time tools for weather, news, stock prices, and time
- Structured answers with sources for tool-based responses
- HITL approval for low-confidence document answers

## Key Features

- **Hybrid tool selection**: rule-based routing first, then LLM tool gate, then LLM router
- **Weather tool**: OpenWeather API with clean formatted output
- **Search tool**: DuckDuckGo search with structured results + sources
- **Stock tool**: Yahoo Finance via `yfinance`
- **Time tool**: local system time
- **Memory**:
	- STM (recent messages)
	- LTM (Postgres structured facts)
	- Auto-memory for stable facts
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

## Project Structure

```
AI-Agent-LangGraph/
	Chatbot/
		chatbotBackend.py       # Agent logic, tools, memory, RAG
		chatbotFrontend.py      # Streamlit UI
		knowledge_base/         # Uploaded docs for RAG
		faiss_index/            # Per-thread FAISS indexes
		docker-compose.yml      # Postgres for long-term memory
	requirements.txt
	README.md
```

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

- The main agent is inside [Chatbot/](Chatbot/).
- If you want full workflow details, see [Chatbot/README.md](Chatbot/README.md).
