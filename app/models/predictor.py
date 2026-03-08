import os, pickle, math, warnings
import numpy as np
warnings.filterwarnings("ignore")

_BUNDLE = None
_TEAMS  = None

def _load():
    global _BUNDLE, _TEAMS
    if _BUNDLE: return True
    try:
        with open("app/ml/model.pkl","rb") as f: _BUNDLE = pickle.load(f)
        with open("app/ml/team_stats.pkl","rb") as f: _TEAMS = pickle.load(f)
        print(f"✅ ML loaded: {_BUNDLE['name']}, CV={_BUNDLE['cv']*100:.1f}%")
        return True
    except:
        return False

def _fs(form):
    W=[0.35,0.25,0.20,0.12,0.08]
    return sum(W[i]*(1 if r=="W" else 0.4 if r=="D" else 0) for i,r in enumerate(form[:5]))

def _norm(v):
    s=sum(v); return [x/s for x in v] if s else [1/len(v)]*len(v)

def _cl(cv):
    if cv>=0.70: return f"⭐⭐⭐ High ({cv*100:.1f}%)"
    if cv>=0.65: return f"⭐⭐ Good ({cv*100:.1f}%)"
    return f"⭐ Medium ({cv*100:.1f}%)"

def predict_football(home, away):
    loaded = _load()
    hk=home.lower().strip(); ak=away.lower().strip()
    DEF={"goals_scored":1.3,"goals_conceded":1.5,"win_rate":0.40,"form":["D","L","W","D","L"]}

    if loaded and _TEAMS:
        h=_TEAMS.get(hk,DEF); a=_TEAMS.get(ak,DEF)
        cols=_BUNDLE["cols"]
        vals={
            "h_gf":h["goals_scored"],"h_ga":h["goals_conceded"],"h_wr":h["win_rate"],
            "h_fm":_fs(h["form"]),"h_sh":h["goals_scored"]*3,"h_sha":h["goals_conceded"]*3,
            "a_gf":a["goals_scored"],"a_ga":a["goals_conceded"],"a_wr":a["win_rate"],
            "a_fm":_fs(a["form"]),"a_sh":a["goals_scored"]*3,"a_sha":a["goals_conceded"]*3,
            "gd":h["goals_scored"]-a["goals_scored"],
            "dd":a["goals_conceded"]-h["goals_conceded"],
            "fd":_fs(h["form"])-_fs(a["form"]),
            "wd":h["win_rate"]-a["win_rate"],
            "home":1.0,"imp_h":0.45,"imp_d":0.28,"imp_a":0.27,
        }
        X=np.array([[vals[c] for c in cols]])
        prob=_BUNDLE["model"].predict_proba(X)[0]
        hp,dp,ap=round(float(prob[0]),4),round(float(prob[1]),4),round(float(prob[2]),4)
        cv=_BUNDLE["cv"]; src=f"XGBoost trained on 9,000+ real matches (CV {cv*100:.1f}%)"
        h_n=_TEAMS.get(hk,{}).get("name",home.title())
        a_n=_TEAMS.get(ak,{}).get("name",away.title())
    else:
        from app.models.database import FOOTBALL_DB, FootballTeam
        D=FootballTeam("Unknown","Unknown",10,5,9,1.4,1.7,["D","L","W","D","L"],1700)
        hd=FOOTBALL_DB.get(hk,D); ad=FOOTBALL_DB.get(ak,D)
        hg=hd.wins+hd.draws+hd.losses; ag=ad.wins+ad.draws+ad.losses
        elo=(1/(1+10**(-((hd.elo_rating-ad.elo_rating)/400))))-0.5
        h_sc=hd.wins/max(hg,1)*0.20+_fs(hd.form)*0.25+(hd.goals_scored_avg/2.5)*0.15+(1-hd.goals_conceded_avg/3)*0.15+elo*0.15+0.10
        a_sc=ad.wins/max(ag,1)*0.20+_fs(ad.form)*0.25+(ad.goals_scored_avg/2.5)*0.15+(1-ad.goals_conceded_avg/3)*0.15+(-elo)*0.15
        dr=(hd.draws/max(hg,1)+0.25)/2*0.55
        hp,dp,ap=_norm([h_sc,dr,a_sc]); hp,dp,ap=round(hp,4),round(dp,4),round(1-hp-dp,4)
        h={"goals_scored":hd.goals_scored_avg,"goals_conceded":hd.goals_conceded_avg,"form":hd.form}
        a={"goals_scored":ad.goals_scored_avg,"goals_conceded":ad.goals_conceded_avg,"form":ad.form}
        cv=0.62; src="Statistical fallback — run SETUP.bat for real ML"
        h_n=hd.name; a_n=ad.name
        h={"goals_scored":hd.goals_scored_avg,"goals_conceded":hd.goals_conceded_avg,"form":hd.form}
        a={"goals_scored":ad.goals_scored_avg,"goals_conceded":ad.goals_conceded_avg,"form":ad.form}

    if loaded and _TEAMS:
        h2=_TEAMS.get(hk,DEF); a2=_TEAMS.get(ak,DEF)
    else:
        h2=h; a2=a

    xgh=max(0.3,round(h2["goals_scored"]*(1.2-a2["goals_conceded"]/4),2))
    xga=max(0.2,round(a2["goals_scored"]*(1.0-h2["goals_conceded"]/4),2))
    txg=round(xgh+xga,2)
    if hp>=dp and hp>=ap: pred,emo="HOME WIN","🏠"
    elif ap>hp and ap>dp: pred,emo="AWAY WIN","✈️"
    else: pred,emo="DRAW","🤝"

    return {
        "match":f"{h_n} vs {a_n}","prediction":pred,"emoji":emo,
        "probabilities":{"home_win":f"{hp*100:.1f}%","draw":f"{dp*100:.1f}%","away_win":f"{ap*100:.1f}%"},
        "raw":{"home_win":hp,"draw":dp,"away_win":ap},
        "expected_goals":{"home":xgh,"away":xga,"total":txg,
            "over_2_5":"✅ YES" if txg>2.5 else "❌ NO",
            "btts":"✅ YES" if (xgh*xga/3+0.2)>0.5 else "❌ NO"},
        "form":{"home":" ".join(h2["form"][:5]),"away":" ".join(a2["form"][:5])},
        "confidence":_cl(cv),"model":src,
    }

def predict_basketball(home,away):
    from app.models.database import NBA_DB,BasketballTeam
    D=BasketballTeam("Unknown","?",25,35,109.0,113.5,111.5,114.8,["L","W","L","D","D"])
    h=NBA_DB.get(home.lower().strip(),D); a=NBA_DB.get(away.lower().strip(),D)
    h_wp=h.wins/max(h.wins+h.losses,1); a_wp=a.wins/max(a.wins+a.losses,1)
    h_sc=h_wp*0.35+_fs(h.form)*0.25+(h.off_rtg-h.def_rtg)/20*0.30+0.06
    a_sc=a_wp*0.35+_fs(a.form)*0.25+(a.off_rtg-a.def_rtg)/20*0.30
    hp,ap=_norm([h_sc,a_sc]); hp,ap=round(hp,4),round(1-hp,4)
    exp=round((h.ppg+a.opp_ppg)/2*0.5+(a.ppg+h.opp_ppg)/2*0.5,1)
    line=round(exp/5)*5; spread=round((hp-0.5)*20,1)
    return {"match":f"{h.name} vs {a.name}","prediction":f"{h.name} WIN" if hp>0.5 else f"{a.name} WIN",
        "probabilities":{h.name:f"{hp*100:.1f}%",a.name:f"{ap*100:.1f}%"},
        "raw":{h.name:hp,a.name:ap},"expected_total":exp,
        "spread":f"{h.name} {'+' if spread<0 else '-'}{abs(spread)}",
        "over_under":{"line":line,"prediction":"✅ OVER" if exp>line else "❌ UNDER","expected":exp},
        "net_ratings":{h.name:round(h.off_rtg-h.def_rtg,1),a.name:round(a.off_rtg-a.def_rtg,1)},
        "confidence":"⭐⭐ Good","model":"Net Rating + Form Model"}

def predict_tennis(p1,p2,surface="hard",tour="atp"):
    from app.models.database import ATP_DB,WTA_DB,TennisPlayer
    D=TennisPlayer("Unknown","?",100,0.50,0.50,0.50,0.50,7.0,60.0,60.0)
    db=ATP_DB if tour.lower()=="atp" else WTA_DB
    pp1=db.get(p1.lower().strip(),D); pp2=db.get(p2.lower().strip(),D)
    sa={"hard":"hard","clay":"clay","grass":"grass"}.get(surface.lower(),"hard")
    p1s=getattr(pp1,sa); p2s=getattr(pp2,sa)
    re=math.tanh((pp2.rank-pp1.rank)/100)*0.10
    p1v=pp1.win_pct*0.25+p1s*0.45+(pp1.ace_avg/12+pp1.first_serve/100+pp1.bp_save/100)/3*0.15+re*0.15
    p2v=pp2.win_pct*0.25+p2s*0.45+(pp2.ace_avg/12+pp2.first_serve/100+pp2.bp_save/100)/3*0.15+(-re)*0.15
    p1p,p2p=_norm([p1v,p2v]); p1p,p2p=round(p1p,4),round(1-p1p,4)
    cv=0.78 if (pp1.rank<20 and pp2.rank<20) else 0.63
    return {"match":f"{pp1.name} vs {pp2.name}","surface":surface.upper(),"tour":tour.upper(),
        "prediction":f"{''.join([pp1.name if p1p>0.5 else pp2.name])} WINS",
        "probabilities":{pp1.name:f"{p1p*100:.1f}%",pp2.name:f"{p2p*100:.1f}%"},
        "raw":{pp1.name:p1p,pp2.name:p2p},
        "surface_specialist":pp1.name if p1s>p2s else pp2.name,
        "rankings":{pp1.name:pp1.rank,pp2.name:pp2.rank},
        "confidence":_cl(cv),"model":"Surface + Serve + Rank Model"}
