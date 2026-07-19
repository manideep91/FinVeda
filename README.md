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

**Run:**

```bash
cd phase1
uv run python main.py
```

---

### ✅ Phase 2 — LangGraph Concepts (State, Nodes, Edges)

> **Concept: How to structure a graph-based pipeline**

- Introduces LangGraph — State, Nodes, Edges, Graph
- 3 nodes: Stock Fetcher → News Fetcher → Decision Agent
- Shared State flows between nodes (like Spring Batch JobExecutionContext)
- Clean separation of concerns — one responsibility per node

⚠️ Still not truly agentic — graph flow is hardcoded, LLM is still a passenger.

📁 [Go to Phase 2](./phase2)

**Run:**

```bash
cd phase2
uv run python main.py
```

---

### ✅ Phase 3 — True Agentic AI (ReAct + ToolNode)

> **Concept: LLM drives the flow, not the developer**

- Introduces ReAct pattern — LLM Reasons then Acts
- LLM decides which tools to call and when
- LLM decides when it has enough information to answer
- Uses LangGraph ToolNode — tools are registered, LLM calls them dynamically

✅ First truly agentic phase — LLM is in control.

📁 [Go to Phase 3](./phase3)

**Run:**

```bash
cd phase3
uv run python main.py
```

---

### ✅ Phase 4 — Full Stack App (FastAPI + Angular + Kite Integration)

> **Concept: Production-grade agentic AI with real portfolio data**

- FastAPI backend with Kite/Zerodha OAuth integration
- Fetches real portfolio holdings from Zerodha
- Loops each stock through Phase 3 ReAct AI agent
- Angular 20 dashboard — select stocks, analyse on demand
- Live BUY/SELL/HOLD recommendations with confidence score
- Daily scheduler + WhatsApp notification (UI ready, backend coming soon)

✅ Consumer-facing app — real broker data + real AI analysis.

📁 [Go to Phase 4](./phase4)

**Run Backend:**

```bash
cd phase4
uv run uvicorn backend.main:app --reload --port 8000
```

**Run Frontend** (in a separate terminal):

```bash
cd phase4/frontend
ng serve
```

**Open:** http://localhost:4200

---

### 🔜 Phase 5 — WhatsApp + Scheduler (Autonomous Ops)

> **Concept: Agent runs itself and notifies you**

- APScheduler for daily analysis at 7:30 AM IST
- WhatsApp integration via Twilio/WhatsApp Business API
- Runs every business day automatically
- Sends portfolio summary with BUY/SELL/HOLD per stock

📁 [Go to Phase 5](./phase5) ← Coming soon

---

## 🛠️ Tech Stack

| Tool                              | Purpose                           |
| --------------------------------- | --------------------------------- |
| Python + uv                       | Language + package manager        |
| LangChain                         | LLM abstraction layer             |
| LangGraph                         | Agent graph framework             |
| Gemini 2.5 Flash Lite (Vertex AI) | LLM via GCP                       |
| Yahoo Finance (`yfinance`)        | Stock price + fundamentals        |
| NewsAPI                           | Company news headlines            |
| FastAPI + uvicorn                 | Backend REST API                  |
| Kite Connect (Zerodha)            | Real portfolio holdings via OAuth |
| Angular 20                        | Frontend dashboard                |

---

## ⚙️ Setup

**1. Clone the repo:**

```bash
git clone https://github.com/manideep91/FinVeda.git
cd FinVeda
```

**2. Create root `.env`:**
GOOGLE_CLOUD_PROJECT=your_gcp_project
NEWS_API_KEY=your_newsapi_key
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash-lite
KITE_API_KEY=your_kite_api_key
KITE_API_SECRET=your_kite_api_secret

**3. Each phase has its own virtual environment:**

```bash
cd phase1  # or phase2, phase3, phase4
uv sync    # installs dependencies
```

---

## 🚀 Long Term Goal

FinVeda is being built toward a **consumer-facing app/website**
for individual investors — real-time AI stock analysis powered by
Gemini, connected directly to your broker portfolio.
