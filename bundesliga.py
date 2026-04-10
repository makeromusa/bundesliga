import streamlit as st
import requests

st.set_page_config(page_title="Football Wrapped ⚽", layout="wide")

st.title("Football Wrapped ⚽")

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
# ⚡ CACHED FETCH
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
# 🎯 SIDEBAR
# -------------------------
st.sidebar.title("⚽ Football Wrapped")

selected_league = st.sidebar.selectbox("Select League", list(LEAGUES.keys()))
LEAGUE_CODE = LEAGUES[selected_league]

page = st.sidebar.radio("Navigate", ["Dashboard", "Matches", "Standings", "Top Scorers", "Highlights"])

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
# 🛡️ LOGO FIX
# -------------------------
def get_logo(team_name):
    t = next((x for x in teams_data if x["name"] == team_name), {})
    logo = t.get("crest")

    if not logo or "null" in str(logo):
        logo = f"https://crests.football-data.org/{t.get('id', 0)}.png"

    return logo


# -------------------------
# 📊 DASHBOARD
# -------------------------
if page == "Dashboard":

    st.header(f"{team_name} Overview")

    st.image(get_logo(team_name), width=120)

    wins = draws = losses = goals_for = goals_against = matches_played = 0
    goal_list = []

    for m in matches:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        if team_name not in [home, away]:
            continue

        matches_played += 1

        score = m["score"]["fullTime"]
        winner = m["score"]["winner"]

        hg = score["home"] or 0
        ag = score["away"] or 0

        if home == team_name:
            gf, ga = hg, ag
        else:
            gf, ga = ag, hg

        goal_list.append(gf)
        goals_for += gf
        goals_against += ga

        if winner == "DRAW":
            draws += 1
        elif (winner == "HOME_TEAM" and home == team_name) or (winner == "AWAY_TEAM" and away == team_name):
            wins += 1
        else:
            losses += 1

    points = wins * 3 + draws
    avg_goals = round(sum(goal_list)/matches_played,2) if matches_played else 0

    cols = st.columns(6)
    cols[0].metric("Matches", matches_played)
    cols[1].metric("Wins", wins)
    cols[2].metric("Draws", draws)
    cols[3].metric("Losses", losses)
    cols[4].metric("Points", points)
    cols[5].metric("Avg Goals/Game", avg_goals)


# -------------------------
# ⚽ MATCHES
# -------------------------
elif page == "Matches":

    st.header("Matches")

    for m in matches:
        home = m["homeTeam"]["name"]
        away = m["awayTeam"]["name"]

        if team_name not in [home, away]:
            continue

        score = m["score"]["fullTime"]
        winner = m["score"]["winner"]

        hg = score["home"] or 0
        ag = score["away"] or 0

        if home == team_name:
            gf, ga, venue = hg, ag, "Home"
        else:
            gf, ga, venue = ag, hg, "Away"

        if winner == "DRAW":
            result = f"{gf}-{ga} (Draw)"
        elif (winner == "HOME_TEAM" and home == team_name) or (winner == "AWAY_TEAM" and away == team_name):
            result = f"{gf}-{ga} (Win)"
        else:
            result = f"{gf}-{ga} (Loss)"

        st.markdown(f"""
        <div>
        <img src='{get_logo(home)}' width='25'/> <b>{home}</b> vs 
        <img src='{get_logo(away)}' width='25'/> <b>{away}</b>
        | {venue} | {result}
        </div>
        """, unsafe_allow_html=True)


# -------------------------
# 🏆 STANDINGS
# -------------------------
elif page == "Standings":

    st.header("League Table")

    standings = fetch_data(STANDINGS_URL).get("standings", [])

    if standings:
        table = standings[0]["table"]

        for team in table:
            st.markdown(f"""
            <div>
            {team['position']}. 
            <img src='{get_logo(team["team"]["name"])}' width='25'/> 
            <b>{team["team"]["name"]}</b> 
            - {team["points"]} pts
            </div>
            """, unsafe_allow_html=True)


# -------------------------
# ⚽ TOP SCORERS
# -------------------------
elif page == "Top Scorers":

    st.header("Top Scorers")

    scorers = fetch_data(SCORERS_URL).get("scorers", [])

    for s in scorers[:10]:
        st.markdown(f"""
        <div>
        <img src='{get_logo(s["team"]["name"])}' width='25'/>
        <b>{s["player"]["name"]}</b> ({s["team"]["name"]}) - ⚽ {s["goals"]}
        </div>
        """, unsafe_allow_html=True)


# -------------------------
# 🎥 HIGHLIGHTS
# -------------------------
elif page == "Highlights":

    st.header("Top 10 Highlights")

    def fetch_highlights(team):
        try:
            url = "https://www.googleapis.com/youtube/v3/search"

            params = {
                "part": "snippet",
                "q": f"{team} 2024 2025 highlights",
                "key": YOUTUBE_API_KEY,
                "maxResults": 25,
                "type": "video",
                "videoEmbeddable": "true"
            }

            data = requests.get(url, params=params, timeout=10).json()

            vids = []

            for item in data.get("items", []):
                title = item["snippet"]["title"].lower()

                if team.lower() in title and not any(x in title for x in ["fifa", "career", "gameplay"]):
                    vids.append(item["id"]["videoId"])

                if len(vids) == 10:
                    break

            return vids

        except:
            return []

    videos = fetch_highlights(team_name)

    if not videos:
        st.warning("No good highlights found.")
    else:
        for v in videos:
            st.video(f"https://www.youtube.com/watch?v={v}")
