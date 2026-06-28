from langgraph.graph import StateGraph, START, END
from state import StockAnalysisState
from nodes.stock_fetcher import stock_fetcher_node
from nodes.news_fetcher import news_fetcher_node
from nodes.decision_agent import decision_agent_node

def build_graph():
    """
    Wires all nodes and edges into a LangGraph graph.

    Java analogy: This is your Spring Batch Job @Bean —
    it defines the Steps and transitions between them.

    StateGraph  = Spring Batch Job
    add_node()  = registering a Step
    add_edge()  = defining Step transitions
    compile()   = building the Job (like ApplicationContext refresh)
    """

    # Step 1: Create the graph with our State
    # Java analogy: new JobBuilder("stockAnalysis")
    graph = StateGraph(StockAnalysisState)

    # Step 2: Register all nodes
    # Java analogy: registering Steps in a Job
    graph.add_node("stock_fetcher", stock_fetcher_node)
    graph.add_node("news_fetcher", news_fetcher_node)
    graph.add_node("decision_agent", decision_agent_node)

    # Step 3: Define edges (flow between nodes)
    # Java analogy: .start(step1).next(step2).next(step3)
    graph.add_edge(START, "stock_fetcher")
    graph.add_edge("stock_fetcher", "news_fetcher")
    graph.add_edge("news_fetcher", "decision_agent")
    graph.add_edge("decision_agent", END)

    # Step 4: Compile — locks the graph and makes it executable
    # Java analogy: applicationContext.refresh()
    return graph.compile()