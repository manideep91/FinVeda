from typing import TypedDict, Optional

class StockAnalysisState(TypedDict):
    """
    Shared state that flows through all nodes.
    
    Java analogy: JobExecutionContext in Spring Batch —
    every node reads from and writes to this object.
    
    TypedDict = like a Java DTO/POJO with typed fields.
    Optional  = like @Nullable in Java
    """
    ticker: str                        # input — set by user
    stock_data: Optional[dict]         # written by stock_fetcher_node
    news: Optional[list]               # written by news_fetcher_node
    recommendation: Optional[str]      # written by decision_agent_node