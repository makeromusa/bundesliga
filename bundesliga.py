import streamlit as st
import requests

st.set_page_config(page_title="Football Wrapped ⚽", layout="wide")

# -------------------------
# 🔐 API KEYS
# -------------------------
FOOTBALL_API_KEY = st.secrets["FOOTBALL_API_KEY"]
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
HEADERS = {"X-Auth-Token": FOOTBALL_API_KEY}

# -------------------------
# 🌍 LEAGUES
# -------------------------
LEAGUES = {
    "Bundesliga 🇩🇪": "BL1",
    "Premier League 🏴": "PL",
    "La Liga 🇪🇸": "PD",
    "Ligue 1 🇫🇷": "FL1",
    "Serie A 🇮🇹": "SA"
}

# -------------------------
# ⚡ CACHED FETCH FUNCTIONS
# -------------------------
@st.cache_data(ttl=600)
def fetch_data(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return r.json()
    except:
        return {}

# -------------------------
# 🎯 SIDEBAR NAVIGATION
# -------------------------
st.sidebar.title("⚽ Football Wrapped")

selected_league = st.sidebar.selectbox("Select League", list(LEAGUES.keys()))
LEAGUE_CODE = LEAGUES[selected_league]

page = st.sidebar.radio("Navigate", ["Dashboard", "Matches", "Standings", "Top Scorers"])

# -------------------------
# 📡 API URLS
# -------------------------
MATCHES_URL = f"https://api.football-data.org/v4/competitions/{LEAGUE_CODE}/matches"
TEAMS_URL = f"https://api.football-data.org/v4/competitions/{LEAGUE_CODE}/teams"
STANDINGS_URL = f"https://api.football-data.org/v4/competitions/{LEAGUE_CODE}/standings"
SCORERS_URL = f"https://api.football-data.org/v4/competitions/{LEAGUE_CODE}/scorers"

matches = fetch_data(MATCHES_URL).get("matches", [])
teams_data = fetch_data(TEAMS_URL).get("teams", [])

if not teams_data:
    st.error("⚠️ API failed. Check your key.")
    st.stop()

teams_list = [t["name"] for t in teams_data]
team_name = st.sidebar.selectbox("Select Team", teams_list)

# -------------------------
# 🛡️ LOGO FIX FUNCTION
# -------------------------
def get_logo(team_name):
    t = next((x for x in teams_data if x["name"] == team_name), {})
    logo = t.get("crest")
    if not
