from langchain_core.tools import tool
from tools.yahoo_finance import get_stock_data
from tools.news_fetcher import get_stock_news

@tool
def fetch_stock_data(ticker: str) -> str:
    """
    Fetches stock price and fundamentals from Yahoo Finance.
    Use this tool when you need current price, PE ratio,
    52-week high/low, market cap, or sector for a stock.

    Args:
        ticker: Stock ticker symbol e.g. TCS.NS, RELIANCE.NS, AAPL
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
    Use this tool when you need to analyse news sentiment
    or recent events affecting a stock.

    Args:
        company_name: Full company name e.g. Tata Consultancy Services
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