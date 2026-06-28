import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_stock_news(company_name: str, max_articles: int = 5) -> list:
    """
    Fetches recent news headlines for a company.
    Java analogy: @Component using RestTemplate with
    proper try/catch, validation and fallback handling.
    """
    api_key = os.getenv("NEWS_API_KEY")

    # Missing API key check
    # Java analogy: @PostConstruct validation of @Value fields
    if not api_key:
        raise EnvironmentError("NEWS_API_KEY is missing from .env file.")

    try:
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": company_name,
            "sortBy": "publishedAt",
            "pageSize": max_articles,
            "language": "en",
            "apiKey": api_key
        }

        response = requests.get(url, params=params, timeout=10)  # timeout like RestTemplate.setConnectTimeout()
        response.raise_for_status()  # throws on 4xx/5xx

        articles = response.json().get("articles", [])

        # No articles found — not an error, just return a friendly fallback
        # Java analogy: returning Optional.empty() instead of throwing
        if not articles:
            print(f"⚠️  No news articles found for '{company_name}'. Proceeding without news.")
            return []

        return [
            {
                "title": a["title"],
                "description": a.get("description", ""),
                "published_at": a["publishedAt"][:10],
            }
            for a in articles
            if a.get("title")  # skip articles with no title
        ]

    except requests.exceptions.ConnectionError:
        raise ConnectionError("Failed to reach NewsAPI. Check your internet connection.")

    except requests.exceptions.Timeout:
        raise TimeoutError("NewsAPI request timed out. Try again in a moment.")

    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"NewsAPI returned an error: {e}")