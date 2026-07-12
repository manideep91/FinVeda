from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from backend.tools.yahoo_finance import get_stock_data
from backend.tools.news_fetcher import get_stock_news
from backend.llm_config import get_llm

@tool
def fetch_stock_data(ticker: str) -> str:
    """
    Fetches stock price and fundamentals from Yahoo Finance.
    Use this when you need current price, PE ratio,
    52-week high/low, market cap or sector for a stock.
    """
    try:
        data = get_stock_data(ticker)
        return f"""
Company: {data['company_name']}
Ticker: {data['ticker']}
Current Price: {data['current_price']}
Previous Close: {data['previous_close']}
PE Ratio: {data['pe_ratio']}
52-Week High: {data['52w_high']}
52-Week Low: {data['52w_low']}
Sector: {data['sector']}
"""
    except Exception as e:
        return f"Error fetching stock data: {e}"


@tool
def fetch_stock_news(company_name: str) -> str:
    """
    Fetches recent news headlines for a company.
    Use this when you need to analyse news sentiment
    or recent events affecting a stock.
    """
    try:
        news = get_stock_news(company_name)
        if not news:
            return "No recent news found."
        return "\n".join([
            f"- {a['title']} ({a['published_at']})"
            for a in news
        ])
    except Exception as e:
        return f"Error fetching news: {e}"


def build_agent():
    """
    Builds ReAct agent — same as Phase 3.
    Java analogy: @Bean factory method returning
    a configured service.
    """
    llm = get_llm()
    tools = [fetch_stock_data, fetch_stock_news]

    system_prompt = """You are an expert stock market analyst for Indian markets.
You have access to two tools:
- fetch_stock_data: gets price, PE ratio, 52w high/low
- fetch_stock_news: gets recent news headlines

Follow these steps:
1. Fetch stock data using the ticker
2. Fetch news using company name from stock data
3. Analyse both and respond in this EXACT format:

RECOMMENDATION: (BUY / SELL / HOLD)
CONFIDENCE: (score out of 10)
TECHNICAL_SUMMARY: (one sentence)
NEWS_SENTIMENT: (Positive / Neutral / Negative)
KEY_RISKS: (one sentence)
"""

    return create_react_agent(
        model=llm,
        tools=tools,
        prompt=SystemMessage(system_prompt)
    )


def analyse_stock(ticker: str) -> dict:
    """
    Analyses a single stock and returns structured result.
    Java analogy: @Service method called by @RestController
    """
    agent = build_agent()

    response = agent.invoke({
        "messages": [
            {"role": "user", "content": f"Analyse this stock: {ticker}"}
        ]
    })

    raw = response["messages"][-1].content

    # Parse structured response into dict
    # Java analogy: mapping response string to DTO fields
    result = {"ticker": ticker, "raw": raw}

    for line in raw.split("\n"):
        if line.startswith("RECOMMENDATION:"):
            result["recommendation"] = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            result["confidence"] = line.split(":", 1)[1].strip()
        elif line.startswith("TECHNICAL_SUMMARY:"):
            result["technical_summary"] = line.split(":", 1)[1].strip()
        elif line.startswith("NEWS_SENTIMENT:"):
            result["news_sentiment"] = line.split(":", 1)[1].strip()
        elif line.startswith("KEY_RISKS:"):
            result["key_risks"] = line.split(":", 1)[1].strip()

    return result