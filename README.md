# 📈 Stock Analysis Agent

A multi-phase project to learn agentic AI concepts, built with Python, LangChain, and Gemini (Vertex AI).

## Learning Phases

### ✅ Phase 1 — Single Agent (Tools + LLM calls)

- Single agent that fetches stock data (Yahoo Finance) and news (NewsAPI)
- Calls Gemini LLM for BUY/SELL/HOLD recommendation
- Configurable LLM via `.env`
- [Go to Phase 1](./phase1)

### 🔜 Phase 2 — Multi-Agent (LangGraph)

- Orchestrator agent delegates to specialist agents
- Technical, Fundamental, News, and Decision agents
- LLM decides which tools to call and when
- [Go to Phase 2](./phase2)

### 🔜 Phase 3 — Memory + Ledger

- Persistent state across runs
- Portfolio tracking with SQLite

### 🔜 Phase 4 — Scheduling + MCP

- Autonomous scheduled runs
- 7:30 AM IST daily analysis

## Tech Stack

- Python + uv
- LangChain + LangGraph
- Gemini (Vertex AI / GCP)
- Yahoo Finance, NewsAPI
