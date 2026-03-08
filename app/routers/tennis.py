from fastapi import APIRouter, Query
from app.models.predictor import predict_tennis
from app.models.database import ATP_DB, WTA_DB

router = APIRouter()

@router.get("/predict", summary="Predict a tennis match")
def predict(
    player1: str = Query(..., example="Novak Djokovic"),
    player2: str = Query(..., example="Carlos Alcaraz"),
    surface: str = Query("hard", description="hard / clay / grass"),
    tour:    str = Query("atp",  description="atp / wta"),
):
    """Predict tennis match with surface, serve stats, and ranking analysis."""
    return predict_tennis(player1, player2, surface, tour)

@router.get("/todays-predictions", summary="Today's tennis predictions")
def today():
    matches = [
        ("Novak Djokovic","Carlos Alcaraz","clay","atp"),
        ("Jannik Sinner","Daniil Medvedev","hard","atp"),
        ("Alexander Zverev","Holger Rune","clay","atp"),
        ("Aryna Sabalenka","Iga Swiatek","hard","wta"),
        ("Coco Gauff","Elena Rybakina","grass","wta"),
    ]
    results = []
    for p1,p2,surf,tour in matches:
        p = predict_tennis(p1,p2,surf,tour)
        results.append({"match":p["match"],"surface":p["surface"],"prediction":p["prediction"],"confidence":p["confidence"]})
    return {"total": len(results), "predictions": results}

@router.get("/players", summary="List all players")
def players():
    atp = sorted([{"name":p.name,"rank":p.rank,"country":p.country} for p in ATP_DB.values()], key=lambda x: x["rank"])
    wta = sorted([{"name":p.name,"rank":p.rank,"country":p.country} for p in WTA_DB.values()], key=lambda x: x["rank"])
    return {"surfaces":["hard","clay","grass"],"atp":atp,"wta":wta}
