from fastapi import APIRouter, Query
from app.models.predictor import predict_basketball
from app.models.database import NBA_DB

router = APIRouter()

FIXTURES = [
    ("Boston Celtics","LA Lakers"), ("Oklahoma City Thunder","Denver Nuggets"),
    ("Golden State Warriors","New York Knicks"), ("Cleveland Cavaliers","Miami Heat"),
    ("LA Clippers","Memphis Grizzlies"),
]

@router.get("/predict", summary="Predict an NBA match")
def predict(
    home_team: str = Query(..., example="Boston Celtics"),
    away_team: str = Query(..., example="LA Lakers"),
):
    """Predict NBA match outcome with spread and over/under."""
    return predict_basketball(home_team, away_team)

@router.get("/todays-predictions", summary="Today's NBA predictions")
def today():
    results = []
    for h, a in FIXTURES:
        p = predict_basketball(h, a)
        results.append({
            "match": p["match"], "prediction": p["prediction"],
            "confidence": p["confidence"],
            "spread": p["spread"],
            "over_under": f'{p["over_under"]["line"]} → {p["over_under"]["prediction"]}',
            "expected_total": p["expected_total"],
        })
    return {"total": len(results), "predictions": results}

@router.get("/teams", summary="List NBA teams")
def teams():
    by_conf: dict = {}
    for t in NBA_DB.values():
        by_conf.setdefault(t.conference, []).append({
            "name": t.name, "record": f"{t.wins}-{t.losses}",
            "ppg": t.ppg, "net_rtg": round(t.off_rtg-t.def_rtg,1)
        })
    return {"total": len(NBA_DB), "by_conference": by_conf}
