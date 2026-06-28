from state import StockAnalysisState
from tools.yahoo_finance import get_stock_data

def stock_fetcher_node(state: StockAnalysisState) -> dict:
    """
    Node 1: Fetches stock data from Yahoo Finance.

    Java analogy: A Spring Batch Tasklet that:
    - Reads ticker from JobExecutionContext (state)
    - Calls a @Component (get_stock_data tool)
    - Writes result back to JobExecutionContext (state)

    Returns ONLY the fields it updates — LangGraph
    automatically merges this into the full state.
    Like updating only specific fields in JobExecutionContext.
    """
    ticker = state["ticker"]
    print(f"📊 [Node 1] Fetching stock data for {ticker}...")

    try:
        stock_data = get_stock_data(ticker)
        print(f"✅ [Node 1] Got data for {stock_data['company_name']}")
        return {"stock_data": stock_data}

    except ValueError as e:
        print(f"❌ [Node 1] Invalid ticker: {e}")
        return {"stock_data": None}

    except ConnectionError as e:
        print(f"❌ [Node 1] Network error: {e}")
        return {"stock_data": None}