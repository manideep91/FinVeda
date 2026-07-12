import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from backend.routers.portfolio import router as portfolio_router
from backend.routers.analysis import router as analysis_router

load_dotenv()

app = FastAPI(title="FinVeda API", version="1.0.0")
app.include_router(portfolio_router)
app.include_router(analysis_router)

# CORS — allows Angular (localhost:4200) to call this API
# Java analogy: @CrossOrigin in Spring Boot controllers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory token store for now
# Java analogy: a simple HashMap acting as a session store
# We'll move this to DB in a later step
token_store = {}

kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

@app.get("/")
def health_check():
    """
    Health check endpoint.
    Java analogy: Spring Actuator /health endpoint
    """
    return {"status": "FinVeda API is running!"}

@app.get("/auth/login")
def login():
    """
    Returns Zerodha login URL.
    Angular will redirect user to this URL.
    
    Java analogy: @GetMapping("/auth/login") that returns
    OAuth2 authorization URL
    """
    login_url = kite.login_url()
    return {"login_url": login_url}

@app.get("/auth/callback")
def auth_callback(request_token: str):
    """
    Zerodha redirects here after user logs in.
    Exchanges request_token for access_token.
    
    Java analogy: Spring Security OAuth2 callback handler
    @GetMapping("/login/oauth2/code/kite")
    """
    api_secret = os.getenv("KITE_API_SECRET")
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    
    # Store token in memory (keyed by user_id)
    user_id = data["user_id"]
    token_store[user_id] = access_token
    
    return {
        "message": "Login successful!",
        "user_id": user_id,
        "user_name": data["user_name"],
        "access_token": access_token  # Angular will store this
    }