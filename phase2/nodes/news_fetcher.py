from state import StockAnalysisState
from tools.news_fetcher import get_stock_news

def news_fetcher_node(state: StockAnalysisState) -> dict:
    """
    Node 2: Fetches news using company name from state.

    Java analogy: A Spring Batch Tasklet that:
    - Reads stock_data from JobExecutionContext (set by Node 1)
    - Calls a @Component (get_stock_news tool)
    - Writes news back to JobExecutionContext

    Notice: we get company_name from stock_data in state —
    this is nodes communicating via State, not directly
    calling each other. Like steps sharing JobExecutionContext.
    """

    stock_data = state["stock_data"]

    # Guard check — if Node 1 failed, skip this node gracefully
    # Java analogy: checking JobExecutionContext for null before proceeding
    if not stock_data:
        print("⚠️  [Node 2] No stock data in state, skipping news fetch.")
        return {"news": []}

    company_name = stock_data["company_name"]
    print(f"📰 [Node 2] Fetching news for {company_name}...")

    try:
        news = get_stock_news(company_name)
        print(f"✅ [Node 2] Got {len(news)} articles")
        return {"news": news}

    except Exception as e:
        print(f"⚠️  [Node 2] News fetch failed: {e}. Continuing without news.")
        return {"news": []}