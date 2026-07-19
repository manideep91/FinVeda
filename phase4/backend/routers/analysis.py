from fastapi import APIRouter, HTTPException
from kiteconnect import KiteConnect
from backend.agent import analyse_stock
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/analysis", tags=["Analysis"])
kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

@router.get("/portfolio")
def get_portfolio(access_token: str):
    """
    Fetches ALL holdings from Kite.
    No AI analysis — just raw holdings for sidebar.
    Analysis happens on demand via /analysis/stock.

    Java analogy: @GetMapping("/portfolio") that just
    calls a Feign client and maps to DTO — no business logic.
    """
    try:
        kite.set_access_token(access_token)
        all_holdings = kite.holdings()

        if not all_holdings:
            return {"total_holdings": 0, "holdings": []}

        return {
            "total_holdings": len(all_holdings),
            "holdings": [
                {
                    "ticker": h["tradingsymbol"] + ".NS",
                    "quantity": h["quantity"],
                    "avg_price": h["average_price"],
                    "current_price": h["last_price"],
                    "pnl": h["pnl"]
                }
                for h in all_holdings
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@router.get("/stock")
def analyse_single_stock(ticker: str, access_token: str):
    try:
        kite.set_access_token(access_token)
        print(f"🤖 Analysing single stock: {ticker}")
        analysis = analyse_stock(ticker)

        # Check if analysis actually returned useful data
        # If all key fields are None — treat as error
        if not analysis.get("recommendation") and not analysis.get("technical_summary"):
            return {
                "ticker": ticker,
                "status": "error",
                "error_message": f"Could not fetch data for '{ticker}'. This stock may not be listed on NSE or Yahoo Finance does not have data for it."
            }

        return {
            "ticker": ticker,
            "status": "success",
            "recommendation": analysis.get("recommendation"),
            "confidence": analysis.get("confidence"),
            "technical_summary": analysis.get("technical_summary"),
            "news_sentiment": analysis.get("news_sentiment"),
            "key_risks": analysis.get("key_risks"),
        }

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Failed to analyse {ticker}: {error_msg}")
        return {
            "ticker": ticker,
            "status": "error",
            "error_message": error_msg[:200]
        }