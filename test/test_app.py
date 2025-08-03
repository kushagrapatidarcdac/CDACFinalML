import streamlit as st
import requests

# Set your endpoints
# Live Server URL
PREDICTOR_URL = "https://cdacfinalml.onrender.com/predictor/"
RECOMMENDER_URL = "https://cdacfinalml.onrender.com/recommender/"
INCREMENTPRED_URL = "https://cdacfinalml.onrender.com/incrementpredictor/"

# Local Machine URL
# PREDICTOR_URL = "http://localhost:8000/predictor/"
# RECOMMENDER_URL = "http://localhost:8000/recommender/"
# INCREMENTPRED_URL = "http://localhost:8000/incrementpredictor/"

headers = {
    "Content-Type": "application/json"
}

st.title("ML Server Test UI")

tabs = st.tabs(["Prediction", "Recommendation", "Incremental Predictor"])

# Prediction Tab
with tabs[0]:
    st.header("Run Prediction Endpoint")
    segment = st.text_input("Segment", "esports", key="seg1")
    game = st.text_input("Game", "valorant", key="game1")
    total_rounds = st.number_input("Total Rounds", min_value=1, value=500, key="tr1")
    kd = st.number_input("K/D", value=1.2, key="kd1")

    if st.button("Run Prediction"):
        payload = {
            "segment": segment,
            "game": game,
            "total_rounds": total_rounds,
            "kd": kd
        }
        try:
            resp = requests.post(PREDICTOR_URL, json=payload, headers=headers)
            st.text_area("Predicted Rating:", resp.json()['rating'])
            # st.write("Status code:", resp.status_code)
            # st.json(resp.json())
        except Exception as e:
            st.error(str(e))

# Recommendation Tab
with tabs[1]:
    st.header("Run Recommendation Endpoint")
    segment = st.text_input("Segment", "esports", key="seg2")
    game = st.text_input("Game", "csgo", key="game2")
    player_name = st.text_input("Player Name", "ZywOo")
    k = st.number_input("Number of Recommendations (k)", min_value=1, value=5, key="k")

    if st.button("Run Recommendation"):
        payload = {
            "segment": segment,
            "game": game,
            "player_name": player_name,
            "k": k
        }
        try:
            resp = requests.post(RECOMMENDER_URL, json=payload, headers=headers)
            for _ in range(len(resp.json()['player_name'])):
                st.text_area(f"Recommended Player {_}:", resp.json()['player_name'][_])
            
            # st.write("Status code:", resp.status_code)
            # st.json(resp.json())
        except Exception as e:
            st.error(str(e))

# Incremental Predictor Tab
with tabs[2]:
    st.header("Run Incremental Predictor Endpoint")
    segment = st.text_input("Segment", "esports", key="seg3")
    game = st.text_input("Game", "dota2", key="game3")
    player_name = st.text_input("Player Name", "kappsdark", key="pn3")
    country = st.text_input("Country", "india")
    team = st.text_input("Team", "prx")
    total_rounds = st.number_input("Total Rounds", min_value=1, value=500, key="tr3")
    kd = st.number_input("K/D", value=1.2, key="kd3")
    rating = st.number_input("Rating", value=1.13, key="rt3")

    if st.button("Run Incremental Prediction"):
        payload = {
            "segment": segment,
            "game": game,
            "player_name": player_name,
            "country": country,
            "team": team,
            "total_rounds": total_rounds,
            "kd": kd,
            "rating": rating
        }
        try:
            resp = requests.post(INCREMENTPRED_URL, json=payload, headers=headers)
            st.text_area("Status", resp.json()['status'])
            # st.write("Status code:", resp.status_code)
            # st.json(resp.json())
        except Exception as e:
            st.error(str(e))
