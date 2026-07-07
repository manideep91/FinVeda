from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from llm_config import get_llm
from tools.stock_tool import fetch_stock_data, fetch_stock_news

def build_agent():
    """
    Builds a ReAct agent — LLM + Tools.

    Java analogy: This is your @Configuration class that:
    - Takes a @Bean (LLM)
    - Registers @Components (tools)
    - Returns a dynamic JobExecutionDecider that decides
      which tool to call at runtime

    create_react_agent() does the heavy lifting:
    - Binds tools to LLM
    - Creates the ReAct loop (Reason → Act → Observe → Repeat)
    - Adds ToolNode automatically (no manual wiring needed!)
    - Adds conditional edges automatically
    """

    llm = get_llm()
    tools = [fetch_stock_data, fetch_stock_news]

    system_prompt = """You are an expert stock market analyst for Indian markets.

You have access to two tools:
- fetch_stock_data: gets price, PE ratio, 52w high/low for a stock
- fetch_stock_news: gets recent news headlines for a company

Follow these steps:
1. First fetch the stock data using the ticker provided
2. Then fetch news using the company name from stock data
3. Analyse both and give recommendation in this exact format:

TECHNICAL SUMMARY: (2-3 sentences on price vs 52w range)
NEWS SENTIMENT: (Positive / Neutral / Negative with one reason)
RECOMMENDATION: (BUY / SELL / HOLD)
CONFIDENCE: (score out of 10)
KEY RISKS: (2 bullet points)
"""

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=SystemMessage(system_prompt)
    )

    return agent