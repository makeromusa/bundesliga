# ⚽ Football Wrapped ("Bundesliga Wrapped")

An interactive, multi-league football analytics dashboard and video highlight aggregator built with Python and Streamlit.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bundesligawrapped.streamlit.app)
[![Live Site](https://img.shields.io/badge/Live_App-bundesligawrapped.streamlit.app-FF4B4B?style=flat&logo=streamlit)](https://bundesligawrapped.streamlit.app)
[![Author](https://img.shields.io/badge/Author-Asman_Makero_Musa-blue)](https://makeromusa.me)

---

## 🌟 Key Features

- **Team Performance Dashboard:** Instant overview of matches played, wins, draws, losses, total points, and average goals per game.
- **Match Results & Form Tracker:** Full fixture history displaying home/away splits, scorelines, and match outcome tags (Win, Draw, Loss).
- **Live League Standings:** Real-time league table rankings with official club crests and accumulated points.
- **Top Scorers Leaderboard:** Golden boot race tracker showing top 10 goalscorers per league.
- **Top 10 Video Highlights:** Embedded match recap videos dynamically curated for any selected club.
- **Multi-League Coverage:** Supports Bundesliga (BL1), Premier League (PL), La Liga (PD), Serie A (SA), and Ligue 1 (FL1).

---

## 🔌 API Integrations

### 1. Football-Data.org API (v4)
- **Endpoints Used:**
  - `/v4/competitions/{LEAGUE}/matches` — Full-time scorelines and fixture schedules.
  - `/v4/competitions/{LEAGUE}/teams` — Club names, IDs, and official crest vectors.
  - `/v4/competitions/{LEAGUE}/standings` — Up-to-date league table metrics.
  - `/v4/competitions/{LEAGUE}/scorers` — Top player scoring statistics.
- **Performance:** Optimized with Streamlit's `@st.cache_data(ttl=600)` to minimize API consumption and accelerate page load times.

### 2. YouTube Data API (v3)
- **Endpoint Used:**
  - `/youtube/v3/search` — Queries embeddable video recaps matching `{team} 2024 2025 highlights`.
- **Heuristic Filtering:** Strips gaming and simulation videos (e.g., *FIFA*, *Career Mode*, *Gameplay*) to guarantee official match recaps and broadcast footage.

---

## 🛠️ Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/makeromusa/bundesliga.git
   cd bundesliga
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Secrets:**
   Create a `.streamlit/secrets.toml` file in the root directory:
   ```toml
   FOOTBALL_API_KEY = "your_football_data_api_key"
   YOUTUBE_API_KEY = "your_google_youtube_api_key"
   ```

4. **Run the Streamlit application:**
   ```bash
   streamlit run bundesliga.py
   ```

---

## 🚀 Deployment

The production app is deployed on **Streamlit Community Cloud** with continuous deployment from this repository:  
👉 **[https://bundesligawrapped.streamlit.app](https://bundesligawrapped.streamlit.app)**
