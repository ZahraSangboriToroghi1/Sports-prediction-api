from fastapi import APIRouter, Query
from app.models.predictor import predict_football
from app.models.database import FOOTBALL_DB

router = APIRouter()

FIXTURES = [
    ("Arsenal","Chelsea"), ("Real Madrid","Barcelona"),
    ("Bayern Munich","Borussia Dortmund"), ("Inter Milan","Juventus"),
    ("Liverpool","Manchester City"), ("PSG","Marseille"),
    ("Napoli","AC Milan"), ("Atletico Madrid","Real Sociedad"),
]

@router.get("/predict", summary="Predict a match outcome")
def predict(
    home_team: str = Query(..., example="Arsenal"),
    away_team: str = Query(..., example="Chelsea"),
):
    """Predict win/draw probabilities, xG, BTTS, Over 2.5 for any match."""
    return predict_football(home_team, away_team)

@router.get("/todays-predictions", summary="Today's top predictions")
def today():
    results = []
    for h, a in FIXTURES:
        p = predict_football(h, a)
        results.append({
            "match": p["match"], "league": p["league"],
            "prediction": p["prediction"], "confidence": p["confidence_pct"],
            "home_win": p["probabilities"]["home_win"],
            "draw": p["probabilities"]["draw"],
            "away_win": p["probabilities"]["away_win"],
            "over_2_5": p["expected_goals"]["over_2_5"],
            "btts": p["expected_goals"]["btts"],
            "xg": f'{p["expected_goals"]["home"]} - {p["expected_goals"]["away"]}',
        })
    return {"total": len(results), "predictions": results}

@router.get("/head-to-head", summary="Both home/away scenarios")
def h2h(team1: str = Query(..., example="Arsenal"), team2: str = Query(..., example="Chelsea")):
    return {
        f"{team1} at HOME": predict_football(team1, team2),
        f"{team2} at HOME": predict_football(team2, team1),
    }

@router.get("/teams", summary="List all available teams")
def teams():
    by_league: dict = {}
    for t in FOOTBALL_DB.values():
        by_league.setdefault(t.league, []).append({"name": t.name, "elo": t.elo_rating})
    return {"total": len(FOOTBALL_DB), "by_league": by_league}
