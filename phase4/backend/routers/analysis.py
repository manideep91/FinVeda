from fastapi import APIRouter, HTTPException
from kiteconnect import KiteConnect
from backend.agent import analyse_stock
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/analysis", tags=["Analysis"])
kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

@router.get("/portfolio")
def analyse_portfolio(access_token: str, limit: int = 5):
    """
    Fetches ALL holdings from Kite but analyses
    only first `limit` stocks through AI agent.
    Default limit is 5 to save LLM tokens.
    """
    try:
        kite.set_access_token(access_token)
        
        # Step 1: Fetch ALL holdings from Kite
        all_holdings = kite.holdings()

        if not all_holdings:
            return {"message": "No holdings found", "results": []}

        print(f"📊 Total holdings in portfolio: {len(all_holdings)}")
        print(f"🤖 Will analyse first {limit} stocks via AI")

        # Step 2: Pass only first `limit` to AI agent
        # Fetch all from Zerodha, limit LLM calls
        holdings_to_analyse = all_holdings[:limit]

        results = []
        for holding in holdings_to_analyse:
            ticker = holding["tradingsymbol"] + ".NS"
            print(f"🤖 Analysing {ticker}...")

            try:
                analysis = analyse_stock(ticker)
                analysis["quantity"] = holding["quantity"]
                analysis["avg_price"] = holding["average_price"]
                analysis["current_price"] = holding["last_price"]
                analysis["pnl"] = holding["pnl"]
                results.append(analysis)

            except Exception as e:
                results.append({
                    "ticker": ticker,
                    "error": str(e)
                })

        return {
            "total_holdings": len(all_holdings),   # all from Zerodha
            "analysed": len(results),               # LLM analysed
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))