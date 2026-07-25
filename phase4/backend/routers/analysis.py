from fastapi import APIRouter, HTTPException
from kiteconnect import KiteConnect
from backend.agent import analyse_stock
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/analysis", tags=["Analysis"])
kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

def is_analysis_enabled() -> bool:
    """
    Checks APP_ENABLED flag.
    Java analogy: @ConditionalOnProperty check before
    executing expensive service method.
    """
    return os.getenv("APP_ENABLED", "true").lower() == "true"

@router.get("/portfolio")
def get_portfolio(access_token: str):
    """
    Fetches ALL holdings — always allowed regardless of flag.
    No LLM calls here — just Kite API.
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
    """
    Analyses a single stock via AI agent.
    GATED by APP_ENABLED flag — returns friendly error if disabled.
    Java analogy: @PreAuthorize checking a feature flag
    before executing business logic.
    """

    # ← Gate check — block LLM calls if flag is off
    if not is_analysis_enabled():
        return {
            "ticker": ticker,
            "status": "disabled",
            "error_message": "AI analysis is currently disabled. Please try again later."
        }

    try:
        kite.set_access_token(access_token)
        print(f"🤖 Analysing single stock: {ticker}")
        analysis = analyse_stock(ticker)

        if not analysis.get("recommendation") and not analysis.get("technical_summary"):
            return {
                "ticker": ticker,
                "status": "error",
                "error_message": f"Could not fetch data for '{ticker}'. This stock may not be listed on NSE."
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