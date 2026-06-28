from langchain_core.messages import SystemMessage, HumanMessage
from state import StockAnalysisState
from llm_config import get_llm

def decision_agent_node(state: StockAnalysisState) -> dict:
    """
    Node 3: LLM-powered decision agent.

    Java analogy: A Spring Batch Tasklet that:
    - Reads stock_data and news from JobExecutionContext
    - Calls an external AI microservice (LLM)
    - Writes recommendation back to JobExecutionContext

    This is the ONLY node with an LLM — the others are
    just plain data fetchers. Like how only one Spring
    service has complex business logic, others are just
    repositories.
    """

    stock_data = state["stock_data"]
    news = state["news"]

    # Guard check — no point calling LLM without stock data
    if not stock_data:
        print("❌ [Node 3] No stock data available, cannot make recommendation.")
        return {"recommendation": "❌ Analysis failed — invalid ticker or network error."}

    # Format news or fallback
    if news:
        news_text = "\n".join([
            f"- {a['title']} ({a['published_at']})"
            for a in news
        ])
    else:
        news_text = "No recent news available."

    print(f"🤖 [Node 3] Calling LLM for {stock_data['ticker']} analysis...")

    system_prompt = """You are a stock market analyst for Indian markets.
Analyse the data provided and give a structured recommendation.
Always respond in this exact format:

TECHNICAL SUMMARY: (2-3 sentences on price vs 52w range)
NEWS SENTIMENT: (Positive / Neutral / Negative with one reason)
RECOMMENDATION: (BUY / SELL / HOLD)
CONFIDENCE: (score out of 10)
KEY RISKS: (2 bullet points)
"""

    user_prompt = f"""
Analyse this stock:

Ticker: {stock_data['ticker']}
Company: {stock_data['company_name']}
Current Price: {stock_data['current_price']}
Previous Close: {stock_data['previous_close']}
P/E Ratio: {stock_data['pe_ratio']}
52-Week High: {stock_data['52w_high']}
52-Week Low: {stock_data['52w_low']}
Sector: {stock_data['sector']}

Recent News:
{news_text}
"""

    try:
        llm = get_llm()
        response = llm.invoke([
            SystemMessage(system_prompt),
            HumanMessage(user_prompt)
        ])
        print(f"✅ [Node 3] LLM analysis complete")
        return {"recommendation": response.content}

    except Exception as e:
        print(f"❌ [Node 3] LLM call failed: {e}")
        return {"recommendation": f"❌ LLM call failed: {e}"}