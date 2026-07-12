import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()


# Initialize Kite with your api_key
# Java analogy: @Bean that creates a pre-configured RestTemplate
kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

def get_login_url() -> str:
    """
    Generates the Zerodha login URL.
    
    Java analogy: Like Spring Security's OAuth2 authorization URL
    e.g. https://accounts.google.com/oauth/authorize?client_id=xxx
    
    User visits this URL → logs in → Zerodha redirects back
    to our callback URL with request_token
    """
    return kite.login_url()

def generate_access_token(request_token: str) -> str:
    """
    Exchanges request_token for access_token.
    
    Java analogy: Like Spring Security exchanging
    authorization_code for access_token in OAuth2 flow.
    
    request_token = short lived (one time use)
    access_token  = used for all API calls that session
    """
    api_secret = os.getenv("KITE_API_SECRET")
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    
    # Set token on kite instance for subsequent API calls
    kite.set_access_token(access_token)
    
    return access_token

def get_kite_client(access_token: str) -> KiteConnect:
    """
    Returns an authenticated Kite client.
    
    Java analogy: Like getting an authenticated RestTemplate
    with Bearer token already set in headers.
    """
    kite.set_access_token(access_token)
    return kite