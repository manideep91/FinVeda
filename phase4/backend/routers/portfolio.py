from fastapi import APIRouter, HTTPException
from kiteconnect import KiteConnect
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

# Java analogy: @RestController with @RequestMapping("/portfolio")
kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

@router.get("/holdings")
def get_holdings(access_token: str):
    """
    Fetches user's actual holdings from Zerodha.
    
    Java analogy: @GetMapping("/holdings") in a
    @RestController — calls Kite API like a Feign client
    and returns the response.

    Args:
        access_token: token received after Kite login
    """
    try:
        # Set access token for this request
        kite.set_access_token(access_token)

        # Fetch holdings from Kite API
        holdings = kite.holdings()

        if not holdings:
            return {"message": "No holdings found", "holdings": []}

        # Clean up response — only return what we need
        # Java analogy: mapping Entity to DTO
        return {
            "total_holdings": len(holdings),
            "holdings": [
                {
                    "ticker": h["tradingsymbol"] + ".NS",  # add .NS for Yahoo Finance
                    "company": h["exchange"],
                    "quantity": h["quantity"],
                    "avg_price": h["average_price"],
                    "current_price": h["last_price"],
                    "pnl": h["pnl"]
                }
                for h in holdings
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch holdings: {e}")