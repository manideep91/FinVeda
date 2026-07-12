import yfinance as yf

def get_stock_data(ticker: str) -> dict:
    """
    Fetches price and basic fundamentals for a stock.
    Java analogy: @Component wrapping a RestTemplate call,
    with proper try/catch and validation.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # Invalid ticker check — Yahoo returns minimal dict with no price
        # Java analogy: validating response body before mapping to DTO
        if not info or info.get("currentPrice") is None and info.get("regularMarketPrice") is None:
            raise ValueError(f"Ticker '{ticker}' not found or has no price data. Check the ticker symbol.")

        return {
            "ticker": ticker,
            "company_name": info.get("longName") or info.get("shortName") or ticker,
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice", "N/A"),
            "previous_close": info.get("previousClose", "N/A"),
            "pe_ratio": info.get("trailingPE", "N/A"),
            "52w_high": info.get("fiftyTwoWeekHigh", "N/A"),
            "52w_low": info.get("fiftyTwoWeekLow", "N/A"),
            "market_cap": info.get("marketCap", "N/A"),
            "sector": info.get("sector", "N/A"),
        }

    except ValueError:
        raise  # let our own validation bubble up as-is

    except Exception as e:
        raise ConnectionError(f"Failed to fetch data for '{ticker}'. Check your internet connection. Details: {e}")