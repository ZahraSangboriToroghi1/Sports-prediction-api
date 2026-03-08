from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import football, basketball, tennis, ev_scanner

app = FastAPI(
    title="⚽🏀🎾 Sports Prediction API — Powered by Real ML",
    description="""
## Real ML Model trained on 9,000+ actual matches

### Sports:
- ⚽ **Football** — Premier League, La Liga, Bundesliga, Serie A, Ligue 1
- 🏀 **Basketball** — NBA
- 🎾 **Tennis** — ATP & WTA

### Unique Features:
- 📊 **EV Scanner** — +Expected Value bets
- 🔄 **Arbitrage Finder** — Risk-free profit

### Plans:
| Plan | Price | Calls/Day |
|------|-------|-----------|
| Basic | FREE | 10 |
| Pro | $19/mo | 1,000 |
| Ultra | $49/mo | 10,000 |
| Mega | $99/mo | Unlimited |
    """,
    version="3.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(football.router,   prefix="/football",   tags=["⚽ Football"])
app.include_router(basketball.router, prefix="/basketball", tags=["🏀 Basketball"])
app.include_router(tennis.router,     prefix="/tennis",     tags=["🎾 Tennis"])
app.include_router(ev_scanner.router, prefix="/ev",         tags=["📊 EV & Arbitrage"])

@app.get("/", tags=["🏠 Info"])
def root():
    from app.models.predictor import _MODEL_BUNDLE
    ml_status = f"✅ ML Active ({_MODEL_BUNDLE['model_name']}, {_MODEL_BUNDLE['cv_mean']*100:.1f}% accuracy)" if _MODEL_BUNDLE else "⚠️ Run SETUP.bat first"
    return {
        "name": "Sports Prediction API v3.0",
        "ml_status": ml_status,
        "status": "✅ Online",
        "docs": "http://localhost:8000/docs",
        "quick_test": {
            "football":   "/football/predict?home_team=Arsenal&away_team=Chelsea",
            "basketball": "/basketball/predict?home_team=Boston Celtics&away_team=LA Lakers",
            "tennis":     "/tennis/predict?player1=Novak Djokovic&player2=Carlos Alcaraz&surface=clay",
            "ev_scan":    "/ev/scan",
        }
    }

@app.get("/health", tags=["🏠 Info"])
def health():
    return {"status":"healthy"}
