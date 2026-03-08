from dataclasses import dataclass, field
from typing import List

@dataclass
class FootballTeam:
    name: str
    league: str
    wins: int
    draws: int
    losses: int
    goals_scored_avg: float
    goals_conceded_avg: float
    form: List[str]
    elo_rating: int

FOOTBALL_DB = {
    # Premier League
    "manchester city":    FootballTeam("Manchester City",    "Premier League", 19,4,1, 2.9,0.8, ["W","W","W","D","W"], 1980),
    "arsenal":            FootballTeam("Arsenal",            "Premier League", 18,5,2, 2.6,0.9, ["W","W","D","W","W"], 1940),
    "liverpool":          FootballTeam("Liverpool",          "Premier League", 17,4,3, 2.7,1.0, ["W","D","W","W","L"], 1930),
    "chelsea":            FootballTeam("Chelsea",            "Premier League", 13,6,5, 2.1,1.4, ["W","L","W","D","W"], 1820),
    "tottenham":          FootballTeam("Tottenham",          "Premier League", 11,5,8, 1.9,1.7, ["L","W","D","L","W"], 1780),
    "manchester united":  FootballTeam("Manchester United",  "Premier League", 10,5,9, 1.6,1.9, ["L","D","W","L","D"], 1750),
    "newcastle":          FootballTeam("Newcastle",          "Premier League", 14,4,6, 2.0,1.3, ["W","W","L","W","D"], 1810),
    "aston villa":        FootballTeam("Aston Villa",        "Premier League", 14,3,7, 2.1,1.5, ["W","D","W","L","W"], 1800),
    "brighton":           FootballTeam("Brighton",           "Premier League", 12,6,6, 1.8,1.5, ["D","W","D","W","L"], 1780),
    "west ham":           FootballTeam("West Ham",           "Premier League", 10,4,10,1.5,1.8, ["L","W","L","D","W"], 1720),
    # La Liga
    "real madrid":        FootballTeam("Real Madrid",        "La Liga",        20,3,1, 3.0,0.7, ["W","W","W","W","D"], 2010),
    "barcelona":          FootballTeam("Barcelona",          "La Liga",        18,3,3, 2.8,1.0, ["W","W","D","W","W"], 1960),
    "atletico madrid":    FootballTeam("Atletico Madrid",    "La Liga",        16,5,3, 1.9,0.8, ["W","D","W","W","D"], 1880),
    "real sociedad":      FootballTeam("Real Sociedad",      "La Liga",        13,5,6, 1.7,1.3, ["W","D","L","W","W"], 1790),
    "villarreal":         FootballTeam("Villarreal",         "La Liga",        12,6,6, 1.6,1.4, ["D","W","D","L","W"], 1770),
    # Bundesliga
    "bayern munich":      FootballTeam("Bayern Munich",      "Bundesliga",     21,2,1, 3.2,0.9, ["W","W","W","W","W"], 2020),
    "borussia dortmund":  FootballTeam("Borussia Dortmund",  "Bundesliga",     15,4,5, 2.4,1.5, ["W","D","W","L","W"], 1850),
    "rb leipzig":         FootballTeam("RB Leipzig",         "Bundesliga",     14,5,5, 2.1,1.3, ["W","W","D","W","L"], 1830),
    "bayer leverkusen":   FootballTeam("Bayer Leverkusen",   "Bundesliga",     17,6,1, 2.5,0.9, ["W","W","W","D","W"], 1920),
    # Serie A
    "inter milan":        FootballTeam("Inter Milan",        "Serie A",        19,4,1, 2.6,0.8, ["W","W","D","W","W"], 1970),
    "juventus":           FootballTeam("Juventus",           "Serie A",        15,5,4, 1.9,1.0, ["D","W","W","D","W"], 1860),
    "ac milan":           FootballTeam("AC Milan",           "Serie A",        14,5,5, 2.0,1.2, ["W","L","W","D","W"], 1840),
    "napoli":             FootballTeam("Napoli",             "Serie A",        16,4,4, 2.3,1.1, ["W","W","D","W","L"], 1890),
    "roma":               FootballTeam("Roma",               "Serie A",        13,4,7, 1.8,1.4, ["L","W","D","W","W"], 1800),
    # Ligue 1
    "psg":                FootballTeam("Paris Saint-Germain","Ligue 1",        20,3,1, 3.1,0.8, ["W","W","W","W","D"], 2000),
    "marseille":          FootballTeam("Marseille",          "Ligue 1",        14,5,5, 2.0,1.3, ["W","D","W","L","W"], 1820),
    "monaco":             FootballTeam("Monaco",             "Ligue 1",        14,4,6, 2.1,1.4, ["W","W","L","D","W"], 1810),
    # Others
    "porto":              FootballTeam("Porto",              "Primeira Liga",  16,5,3, 2.2,1.0, ["W","W","D","W","W"], 1870),
    "benfica":            FootballTeam("Benfica",            "Primeira Liga",  17,4,3, 2.3,1.0, ["W","W","W","D","L"], 1880),
    "ajax":               FootballTeam("Ajax",               "Eredivisie",     18,3,3, 2.7,1.1, ["W","D","W","W","W"], 1900),
}

@dataclass
class BasketballTeam:
    name: str
    conference: str
    wins: int
    losses: int
    ppg: float
    opp_ppg: float
    off_rtg: float
    def_rtg: float
    form: List[str]

NBA_DB = {
    "boston celtics":         BasketballTeam("Boston Celtics",         "East", 47,12, 120.5,107.8, 122.1,108.5, ["W","W","W","W","W"]),
    "cleveland cavaliers":    BasketballTeam("Cleveland Cavaliers",    "East", 45,14, 116.9,108.2, 119.5,109.8, ["W","W","D","W","W"]),
    "new york knicks":        BasketballTeam("New York Knicks",        "East", 38,21, 113.5,110.2, 116.2,111.4, ["W","D","W","L","W"]),
    "miami heat":             BasketballTeam("Miami Heat",             "East", 32,27, 111.3,110.8, 113.8,111.9, ["D","W","L","W","D"]),
    "philadelphia 76ers":     BasketballTeam("Philadelphia 76ers",     "East", 24,35, 108.9,113.5, 111.2,114.8, ["L","D","W","L","L"]),
    "oklahoma city thunder":  BasketballTeam("Oklahoma City Thunder",  "West", 46,13, 119.8,109.5, 121.5,110.2, ["W","W","W","D","W"]),
    "denver nuggets":         BasketballTeam("Denver Nuggets",         "West", 42,17, 117.3,110.5, 119.8,111.5, ["W","D","W","W","L"]),
    "golden state warriors":  BasketballTeam("Golden State Warriors",  "West", 33,26, 115.6,113.2, 118.2,114.8, ["W","L","W","L","D"]),
    "la clippers":            BasketballTeam("LA Clippers",            "West", 35,24, 114.2,111.8, 116.5,112.5, ["W","W","D","L","W"]),
    "la lakers":              BasketballTeam("LA Lakers",              "West", 31,28, 114.5,114.8, 116.8,115.5, ["L","W","D","W","L"]),
    "memphis grizzlies":      BasketballTeam("Memphis Grizzlies",      "West", 28,31, 111.8,113.5, 114.2,114.8, ["D","L","W","D","L"]),
    "san antonio spurs":      BasketballTeam("San Antonio Spurs",      "West", 17,42, 108.5,118.2, 111.2,119.5, ["L","L","D","L","L"]),
}

@dataclass
class TennisPlayer:
    name: str
    country: str
    rank: int
    win_pct: float
    hard: float
    clay: float
    grass: float
    ace_avg: float
    first_serve: float
    bp_save: float

ATP_DB = {
    "novak djokovic":     TennisPlayer("Novak Djokovic",     "SRB",  1, 0.851, 0.862, 0.875, 0.895,  9.2, 64.5, 66.8),
    "carlos alcaraz":     TennisPlayer("Carlos Alcaraz",     "ESP",  2, 0.832, 0.838, 0.872, 0.845,  7.8, 62.1, 65.2),
    "jannik sinner":      TennisPlayer("Jannik Sinner",      "ITA",  3, 0.818, 0.855, 0.801, 0.782,  8.5, 65.2, 64.8),
    "daniil medvedev":    TennisPlayer("Daniil Medvedev",    "RUS",  4, 0.762, 0.818, 0.682, 0.718, 10.1, 63.8, 63.5),
    "alexander zverev":   TennisPlayer("Alexander Zverev",   "GER",  5, 0.742, 0.752, 0.778, 0.701, 11.2, 61.5, 62.1),
    "andrey rublev":      TennisPlayer("Andrey Rublev",      "RUS",  6, 0.712, 0.718, 0.728, 0.685,  8.8, 60.5, 61.8),
    "holger rune":        TennisPlayer("Holger Rune",        "DEN",  7, 0.692, 0.698, 0.712, 0.668,  9.5, 59.8, 60.5),
    "stefanos tsitsipas": TennisPlayer("Stefanos Tsitsipas", "GRE",  8, 0.702, 0.698, 0.745, 0.671,  9.8, 60.2, 61.2),
    "casper ruud":        TennisPlayer("Casper Ruud",        "NOR",  9, 0.678, 0.672, 0.712, 0.645,  7.5, 59.5, 60.8),
    "taylor fritz":       TennisPlayer("Taylor Fritz",       "USA", 10, 0.668, 0.692, 0.641, 0.658, 12.1, 61.8, 61.5),
    "tommy paul":         TennisPlayer("Tommy Paul",         "USA", 11, 0.645, 0.668, 0.621, 0.638, 10.5, 60.5, 60.2),
    "grigor dimitrov":    TennisPlayer("Grigor Dimitrov",    "BUL", 12, 0.651, 0.658, 0.645, 0.668,  9.2, 60.8, 61.2),
    "alex de minaur":     TennisPlayer("Alex De Minaur",     "AUS", 13, 0.648, 0.661, 0.641, 0.658,  8.1, 63.5, 60.8),
    "ben shelton":        TennisPlayer("Ben Shelton",        "USA", 15, 0.632, 0.648, 0.612, 0.635, 14.5, 58.5, 59.5),
}

WTA_DB = {
    "aryna sabalenka":    TennisPlayer("Aryna Sabalenka",    "BLR",  1, 0.832, 0.848, 0.818, 0.802,  8.5, 62.5, 65.1),
    "iga swiatek":        TennisPlayer("Iga Swiatek",        "POL",  2, 0.845, 0.835, 0.892, 0.795,  5.8, 68.5, 66.8),
    "coco gauff":         TennisPlayer("Coco Gauff",         "USA",  3, 0.798, 0.812, 0.785, 0.778,  6.2, 63.8, 64.2),
    "jessica pegula":     TennisPlayer("Jessica Pegula",     "USA",  4, 0.762, 0.778, 0.745, 0.735,  5.5, 65.2, 63.5),
    "elena rybakina":     TennisPlayer("Elena Rybakina",     "KAZ",  5, 0.772, 0.775, 0.758, 0.795,  9.8, 61.5, 64.8),
    "barbora krejcikova": TennisPlayer("Barbora Krejcikova", "CZE",  6, 0.725, 0.718, 0.738, 0.755,  5.8, 62.8, 63.1),
    "qinwen zheng":       TennisPlayer("Qinwen Zheng",       "CHN",  7, 0.718, 0.732, 0.705, 0.701,  7.2, 61.2, 62.5),
}
