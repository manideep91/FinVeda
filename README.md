# 📈 FinVeda — AI Stock Analysis Agent

A multi-phase project to learn agentic AI concepts from scratch,
built with Python, LangChain, LangGraph, and Gemini (Vertex AI).

Each phase builds on the previous — showing clear progression
from basic scripting to true agentic AI.

---

## 🗂️ Phase Structure

### ✅ Phase 1 — Single Agent (Tools + LLM Calls)

> **Concept: How to call tools and LLM from code**

- Fetches stock data from Yahoo Finance
- Fetches news from NewsAPI
- Passes data to Gemini LLM for BUY/SELL/HOLD recommendation
- Configurable LLM via `.env` (swap providers without code change)

⚠️ Not truly agentic — developer controls the flow, LLM just answers.

📁 [Go to Phase 1](./phase1)

---

### ✅ Phase 2 — LangGraph Concepts (State, Nodes, Edges)

> **Concept: How to structure a graph-based pipeline**

- Introduces LangGraph — State, Nodes, Edges, Graph
- 3 nodes: Stock Fetcher → News Fetcher → Decision Agent
- Shared State flows between nodes (like Spring Batch JobExecutionContext)
- Clean separation of concerns — one responsibility per node

⚠️ Still not truly agentic — graph flow is hardcoded, LLM is still a passenger.

📁 [Go to Phase 2](./phase2)

---

### 🔜 Phase 3 — True Agentic AI (ReAct + ToolNode)

> **Concept: LLM drives the flow, not the developer**

- Introduces ReAct pattern — LLM Reasons then Acts
- LLM decides which tools to call and when
- LLM decides when it has enough information to answer
- Uses LangGraph ToolNode — tools are registered, LLM calls them dynamically

✅ First truly agentic phase — LLM is in control.

📁 [Go to Phase 3](./phase3) ← 🚧 In progress

---

### 🔜 Phase 4 — Memory + Ledger (Persistence)

> **Concept: Agent remembers across runs**

- Persistent state across sessions
- Portfolio tracking with SQLite
- Agent recalls past recommendations and adjusts

📁 [Go to Phase 4](./phase4) ← Coming soon

---

### 🔜 Phase 5 — Scheduling + MCP (Autonomous Ops)

> **Concept: Agent runs itself**

- APScheduler for local scheduling
- 7:30 AM IST daily analysis
- MCP integration for autonomous operations

📁 [Go to Phase 5](./phase5) ← Coming soon

---

## 🛠️ Tech Stack

| Tool                         | Purpose                    |
| ---------------------------- | -------------------------- |
| Python + uv                  | Language + package manager |
| LangChain                    | LLM abstraction layer      |
| LangGraph                    | Agent graph framework      |
| Gemini 2.5 Flash (Vertex AI) | LLM via GCP                |
| Yahoo Finance (`yfinance`)   | Stock price + fundamentals |
| NewsAPI                      | Company news headlines     |

---

## 🚀 Long Term Goal

FinVeda is being built toward a **consumer-facing app/website**
for individual investors — real-time stock analysis powered by AI.
