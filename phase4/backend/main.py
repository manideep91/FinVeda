import os
import json
import tempfile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from kiteconnect import KiteConnect

load_dotenv()

# ── GCP Auth ──────────────────────────────────────────────────
# On cloud: GCP credentials come as JSON string in env variable
# On local: GOOGLE_APPLICATION_CREDENTIALS points to file directly
# Java analogy: @PostConstruct loading external config at startup
gcp_creds_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
if gcp_creds_json:
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(json.loads(gcp_creds_json), f)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = f.name
        print("✅ GCP credentials loaded from environment variable")

# ── App setup ─────────────────────────────────────────────────
app = FastAPI(title="FinVeda API", version="1.0.0")

# CORS — allows Angular to call this API
# Java analogy: @CrossOrigin in Spring Boot
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",      # local dev
        "https://fin-veda-ten.vercel.app",       # Vercel deployment
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory token store
token_store = {}
kite = KiteConnect(api_key=os.getenv("KITE_API_KEY"))

# ── Routers ───────────────────────────────────────────────────
from backend.routers.portfolio import router as portfolio_router
from backend.routers.analysis import router as analysis_router

app.include_router(portfolio_router)
app.include_router(analysis_router)

# ── Core endpoints ────────────────────────────────────────────
@app.get("/")
def health_check():
    """
    Health check — also returns app status.
    Java analogy: Spring Actuator /health endpoint
    """
    app_enabled = os.getenv("APP_ENABLED", "true").lower() == "true"
    return {
        "status": "FinVeda API is running!",
        "analysis_enabled": app_enabled
    }

@app.get("/app/status")
def app_status():
    """
    Angular calls this on load to check if analysis is enabled.
    Java analogy: @GetMapping("/status") returning app config
    """
    app_enabled = os.getenv("APP_ENABLED", "true").lower() == "true"
    return {
        "analysis_enabled": app_enabled,
        "message": "hello" if app_enabled else "AI analysis is currently disabled. Portfolio viewing is still available. ABC"
    }

@app.get("/auth/login")
def login():
    login_url = kite.login_url()
    return {"login_url": login_url}

@app.get("/auth/callback")
def auth_callback(request_token: str):
    api_secret = os.getenv("KITE_API_SECRET")
    data = kite.generate_session(request_token, api_secret=api_secret)
    access_token = data["access_token"]
    user_id = data["user_id"]
    token_store[user_id] = access_token

    return {
        "message": "Login successful!",
        "user_id": user_id,
        "user_name": data["user_name"],
        "access_token": access_token
    }