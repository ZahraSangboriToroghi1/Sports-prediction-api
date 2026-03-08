from fastapi import APIRouter
from app.models.predictor import predict_football

router = APIRouter()

ODDS_DATA = [
    {"match":("Arsenal","Chelsea"),        "bk":{"Bet365":{"home":2.10,"draw":3.40,"away":3.20},"William Hill":{"home":2.05,"draw":3.50,"away":3.30},"Betway":{"home":2.15,"draw":3.35,"away":3.15},"1xBet":{"home":2.20,"draw":3.30,"away":3.10},"Pinnacle":{"home":2.18,"draw":3.38,"away":3.18}}},
    {"match":("Real Madrid","Barcelona"),  "bk":{"Bet365":{"home":2.30,"draw":3.20,"away":3.10},"William Hill":{"home":2.25,"draw":3.30,"away":3.20},"Betway":{"home":2.35,"draw":3.15,"away":3.05},"1xBet":{"home":2.40,"draw":3.10,"away":3.00},"Pinnacle":{"home":2.36,"draw":3.22,"away":3.08}}},
    {"match":("Bayern Munich","Borussia Dortmund"),"bk":{"Bet365":{"home":1.80,"draw":3.60,"away":4.20},"William Hill":{"home":1.85,"draw":3.50,"away":4.10},"Betway":{"home":1.78,"draw":3.65,"away":4.25},"1xBet":{"home":1.90,"draw":3.45,"away":4.05},"Pinnacle":{"home":1.88,"draw":3.55,"away":4.18}}},
    {"match":("Inter Milan","Juventus"),   "bk":{"Bet365":{"home":2.00,"draw":3.30,"away":3.80},"William Hill":{"home":1.98,"draw":3.35,"away":3.90},"Betway":{"home":2.02,"draw":3.28,"away":3.75},"1xBet":{"home":2.05,"draw":3.25,"away":3.70},"Pinnacle":{"home":2.04,"draw":3.30,"away":3.78}}},
    {"match":("Liverpool","Manchester City"),"bk":{"Bet365":{"home":2.45,"draw":3.25,"away":2.85},"William Hill":{"home":2.40,"draw":3.30,"away":2.90},"Betway":{"home":2.50,"draw":3.20,"away":2.80},"1xBet":{"home":2.55,"draw":3.15,"away":2.78},"Pinnacle":{"home":2.48,"draw":3.22,"away":2.84}}},
    {"match":("PSG","Marseille"),          "bk":{"Bet365":{"home":1.60,"draw":3.80,"away":5.50},"William Hill":{"home":1.62,"draw":3.75,"away":5.40},"Betway":{"home":1.58,"draw":3.85,"away":5.60},"1xBet":{"home":1.65,"draw":3.70,"away":5.30},"Pinnacle":{"home":1.63,"draw":3.78,"away":5.48}}},
]

def _best(bk, out):
    b = max(bk, key=lambda x: bk[x][out])
    return b, bk[b][out]

def _ev(prob, odds):
    return round(prob*odds - 1, 5)

def _kelly(prob, odds):
    b = odds-1; q = 1-prob
    k = max(0, min((b*prob-q)/b*0.25, 0.05))
    return f"{k*100:.2f}% of bankroll"

@router.get("/scan", summary="📊 Find +EV betting opportunities")
def scan():
    """
    Find bets where our ML probability > bookmaker implied probability.
    Positive EV = profitable long-term strategy.
    """
    opps = []
    for data in ODDS_DATA:
        h, a = data["match"]
        pred = predict_football(h, a)
        probs = pred["raw"]
        for out, our_p in [("home",probs["home_win"]),("draw",probs["draw"]),("away",probs["away_win"])]:
            bb, bo = _best(data["bk"], out)
            imp = 1/bo
            ev = _ev(our_p, bo)
            edge = round((our_p-imp)*100,2)
            if ev > 0:
                opps.append({
                    "match": pred["match"],
                    "bet": {"home":"Home Win 🏠","draw":"Draw 🤝","away":"Away Win ✈️"}[out],
                    "bookmaker": bb, "odds": bo,
                    "our_prob": f"{our_p*100:.1f}%",
                    "implied_prob": f"{imp*100:.1f}%",
                    "edge": f"+{edge}%",
                    "ev": f"+{ev*100:.2f}%",
                    "rating": "🔥🔥 HOT" if ev>0.08 else "🔥 GOOD" if ev>0.04 else "✅ EDGE",
                    "kelly": _kelly(our_p, bo),
                })
    opps.sort(key=lambda x: float(x["ev"].replace("+","").replace("%","")), reverse=True)
    return {"total": len(opps), "opportunities": opps, "disclaimer": "Bet responsibly."}

@router.get("/arbitrage", summary="🔄 Find risk-free arbitrage")
def arbitrage():
    """
    Find guaranteed profit by backing all outcomes across different bookmakers.
    Total implied probability < 100% = guaranteed profit.
    """
    arbs = []
    for data in ODDS_DATA:
        h, a = data["match"]
        bk = data["bk"]
        bh_b, bh = _best(bk,"home")
        bd_b, bd = _best(bk,"draw")
        ba_b, ba = _best(bk,"away")
        total_imp = (1/bh + 1/bd + 1/ba)*100
        profit = round(100-total_imp, 3)
        if profit > 0:
            stake = 1000.0
            denom = 1/bh + 1/bd + 1/ba
            hs = round(stake*(1/bh)/denom, 2)
            ds = round(stake*(1/bd)/denom, 2)
            as_ = round(stake-hs-ds, 2)
            arbs.append({
                "match": f"{h} vs {a}",
                "profit_pct": f"+{profit:.3f}%",
                "profit_per_$1000": f"${round(stake*profit/100,2)}",
                "total_implied": f"{total_imp:.2f}%",
                "bets": {
                    "home_win":  {"book":bh_b,"odds":bh,"stake":f"${hs}"},
                    "draw":      {"book":bd_b,"odds":bd,"stake":f"${ds}"},
                    "away_win":  {"book":ba_b,"odds":ba,"stake":f"${as_}"},
                },
                "risk": "✅ ZERO RISK",
            })
    arbs.sort(key=lambda x: float(x["profit_pct"].replace("+","").replace("%","")), reverse=True)
    return {
        "total": len(arbs),
        "arbs": arbs if arbs else [{"msg":"No arbs right now. Check again soon."}],
        "tip": "Arbs disappear in minutes — act fast!",
    }

@router.get("/value-bets/today", summary="⭐ Today's top value bets")
def value_bets():
    """Top 5 value bets for today selected by our ML model."""
    result = scan()
    return {"date":"today","top_picks": result["opportunities"][:5],"total_found":result["total"]}
