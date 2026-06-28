from langchain_core.messages import SystemMessage, HumanMessage
from tools.yahoo_finance import get_stock_data
from tools.news_fetcher import get_stock_news
from llm_config import get_llm

def analyse_stock(ticker: str) -> str:
    """
    Core agent logic — orchestrates tools and calls LLM.
    Java analogy: @Service method with proper exception 
    handling at each layer, like a service calling 
    multiple @Components with try/catch around each.
    """

    # Step 1: Fetch stock data — fail fast if ticker is invalid
    # Java analogy: throwing early like @Valid on a DTO
    try:
        print(f"📊 Fetching stock data for {ticker}...")
        stock_data = get_stock_data(ticker)
    except ValueError as e:
        return f"❌ Invalid ticker: {e}"
    except ConnectionError as e:
        return f"❌ Network error fetching stock data: {e}"

    # Step 2: Fetch news — non fatal, agent continues without it
    # Java analogy: Optional dependency — service works without it
    try:
        print(f"📰 Fetching news for {stock_data['company_name']}...")
        news = get_stock_news(stock_data["company_name"])
    except Exception as e:
        print(f"⚠️  News fetch failed: {e}. Continuing without news.")
        news = []

    # Step 3: Format news or use fallback message
    if news:
        news_text = "\n".join([
            f"- {a['title']} ({a['published_at']})"
            for a in news
        ])
    else:
        news_text = "No recent news available."

    # Step 4: Build the prompt
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

    # Step 5: Call LLM — catch any API failures cleanly
    try:
        print("🤖 Calling LLM for analysis...")
        llm = get_llm()
        response = llm.invoke([
            SystemMessage(system_prompt),
            HumanMessage(user_prompt)
        ])
        return response.content

    except Exception as e:
        return f"❌ LLM call failed: {e}"