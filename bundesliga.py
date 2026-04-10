import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Football Wrapped ⚽", layout="wide")
st.title("Football Wrapped ⚽")

# 🔐 API KEYS
FOOTBALL_API_KEY = st.secrets["FOOTBALL_API_KEY"]
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]
HEADERS = {"X-Auth-Token": FOOTBALL_API_KEY}

# 🌍 LEAGUES
LEAGUES = {
    "Bundesliga 🇩🇪": "BL1",
    "Premier League 🏴": "PL",
    "La Liga 🇪🇸": "PD",
    "Ligue 1 🇫🇷": "FL1",
    "Serie A 🇮🇹": "SA"
}

# 🎯 SELECT LEAGUE
selected_league = st.selectbox("Select League", list(LEAGUES.keys()))
LEAGUE_CODE = LEAGUES[selected_league]

MATCHES_URL = f"https://api.football-data.org/v4/competitions/{LEAGUE_CODE}/matches"
TEAMS_URL = f"https://api.football-data.org/v4/competitions/{LEAGUE_CODE}/teams"


# 🔄 FETCH FUNCTIONS
def fetch_matches_safe():
    try:
        resp = requests.get(MATCHES_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.json().get("matches", [])
    except:
        st.warning("⚠️ Couldn't fetch live match data.")
        return []


def fetch_teams_safe():
    try:
        resp = requests.get(TEAMS_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.json().get("teams", [])
    except:
        st.warning("⚠️ Couldn't fetch live team data.")
        return []


matches = fetch_matches_safe()
teams_data = fetch_teams_safe()

if not teams_data:
    st.stop()

teams_list = [team["name"] for team in teams_data]

# 🎯 TEAM SELECT
team_name = st.selectbox("Select your team:", teams_list)

team_info = next((t for t in teams_data if t["name"] == team_name), {})
team_logo = team_info.get("crest", "")
coach = team_info.get("coach", {}).get("name", "N/A")

if team_logo:
    st.image(team_logo, width=120)

st.markdown(f"**Coach:** {coach}")

# 📊 STATS
wins = draws = losses = goals_for = goals_against = matches_played = 0
goal_list = []

for m in matches:
    home, away = m["homeTeam"]["name"], m["awayTeam"]["name"]
    score, winner = m["score"]["fullTime"], m["score"]["winner"]

    if team_name not in [home, away]:
        continue

    matches_played += 1

    home_goals = score["home"] or 0
    away_goals = score["away"] or 0

    if home == team_name:
        gf, ga = home_goals, away_goals
    else:
        gf, ga = away_goals, home_goals

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
avg_goals = round(sum(goal_list) / matches_played, 2) if matches_played > 0 else 0

cols = st.columns(6)
cols[0].metric("Matches", matches_played)
cols[1].metric("Wins", wins)
cols[2].metric("Draws", draws)
cols[3].metric("Losses", losses)
cols[4].metric("Points", points)
cols[5].metric("Avg Goals/Game", avg_goals)

st.markdown("---")

# ⚽ MATCHES
st.subheader("Matches Played")

for m in matches:
    home, away = m["homeTeam"]["name"], m["awayTeam"]["name"]

    if team_name not in [home, away]:
        continue

    score, winner = m["score"]["fullTime"], m["score"]["winner"]

    home_logo = next((t["crest"] for t in teams_data if t["name"] == home), "")
    away_logo = next((t["crest"] for t in teams_data if t["name"] == away), "")

    home_goals = score["home"] or 0
    away_goals = score["away"] or 0

    if home == team_name:
        gf, ga, venue = home_goals, away_goals, "Home"
    else:
        gf, ga, venue = away_goals, home_goals, "Away"

    if winner == "DRAW":
        result = f"{gf}-{ga} (Draw)"
    elif (winner == "HOME_TEAM" and home == team_name) or (winner == "AWAY_TEAM" and away == team_name):
        result = f"{gf}-{ga} (Win)"
    else:
        result = f"{gf}-{ga} (Loss)"

    st.markdown(f"""
    <div>
    <img src='{home_logo}' width='25'/> <b>{home}</b> vs 
    <img src='{away_logo}' width='25'/> <b>{away}</b> 
    | {venue} | {result}
    </div>
    """, unsafe_allow_html=True)


# ⭐ TOP PLAYERS (UNCHANGED)
def fetch_top_players(team_name):
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {"action": "query", "list": "search", "srsearch": f"{team_name} squad", "format": "json"}
        r = requests.get(search_url, params=params, timeout=10).json()

        if not r['query']['search']:
            return [], []

        page_title = r['query']['search'][0]['title']
        page_url = f"https://en.wikipedia.org/wiki/{page_title.replace(' ', '_')}"

        soup = BeautifulSoup(requests.get(page_url, timeout=10).content, 'html.parser')

        players, images = [], []
        table = soup.find('table', {'class': 'wikitable'})

        if not table:
            return [], []

        rows = table.find_all('tr')[1:]

        for row in rows[:3]:
            cols = row.find_all('td')
            if cols:
                name_tag = cols[0].find('a') or cols[0]
                players.append(name_tag.get_text(strip=True))

                img_tag = cols[0].find('img')
                images.append("https:" + img_tag['src'] if img_tag else "https://upload.wikimedia.org/wikipedia/commons/7/7c/Placeholder.png")

        return players, images

    except:
        return [], []


st.subheader("🌟 Top 3 Players")

top_players, top_player_images = fetch_top_players(team_name)

if not top_players:
    top_players = ["Player 1", "Player 2", "Player 3"]
    top_player_images = ["https://upload.wikimedia.org/wikipedia/commons/7/7c/Placeholder.png"] * 3

cols = st.columns(3)

for i, col in enumerate(cols):
    with col:
        st.image(top_player_images[i], width=150)
        st.caption(top_players[i])


# 🎥 YOUTUBE HIGHLIGHTS (UPDATED TO 10)
st.subheader("🎥 Top 10 Highlights")

try:
    query = f"{team_name} {selected_league} highlights"

    yt_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}&maxResults=10&type=video"

    yt_data = requests.get(yt_url, timeout=10).json()

    for item in yt_data.get("items", []):
        video_id = item["id"]["videoId"]
        st.video(f"https://www.youtube.com/watch?v={video_id}")

except:
    st.info("⚠️ Couldn't load YouTube highlights.")
