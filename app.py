import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AQI Predictor",
    page_icon="🌍",
    layout="centered"
)

# ===============================
# FUTURISTIC + GLASS UI CSS
# ===============================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0f2027 0%, #000000 65%);
    color: white;
}
section.main { background: transparent !important; }

.title {
    font-size: 52px;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00f5ff, #00ff87);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #9ee7ff;
    margin-bottom: 30px;
}

.glass {
    background: rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: 25px;
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.18);
    box-shadow: 0 12px 40px rgba(0,0,0,0.7);
    margin-bottom: 30px;
}

.stButton>button {
    width: 100%;
    height: 55px;
    border-radius: 16px;
    font-size: 18px;
    font-weight: 800;
    background: linear-gradient(90deg, #00ffcc, #00c6ff);
    color: black;
}

.aqi-box {
    background: linear-gradient(135deg, #00c6ff, #0072ff);
    padding: 30px;
    border-radius: 24px;
    text-align: center;
    font-size: 32px;
    font-weight: 900;
    box-shadow: 0 0 40px rgba(0,255,255,0.6);
}
</style>
""", unsafe_allow_html=True)

# ===============================
# LOAD MODEL
# ===============================
@st.cache_resource
def load_model():
    with open("aqi_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ===============================
# WORLD MAP OUTLINE (TOP UI)
# ===============================
fig_map = go.Figure(go.Scattergeo())
fig_map.update_layout(
    geo=dict(
        showcountries=True,
        countrycolor="rgba(0,255,255,0.4)",
        showland=True,
        landcolor="rgba(0,0,0,0)",
        bgcolor="rgba(0,0,0,0)",
        projection_type="natural earth"
    ),
    height=260,
    margin=dict(l=0, r=0, t=0, b=0),
    paper_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig_map, use_container_width=True)

# ===============================
# HEADER
# ===============================
st.markdown("<div class='title'>🌍 AQI Prediction System</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Futuristic ML‑Based Air Quality Intelligence</div>", unsafe_allow_html=True)

# ===============================
# INPUT CARD
# ===============================
st.markdown("<div class='glass'>", unsafe_allow_html=True)
st.subheader("🧪 Pollutant Inputs (µg/m³)")

c1, c2 = st.columns(2)
with c1:
    pm25 = st.number_input("PM2.5", 0.0, 500.0, 80.0)
    no2  = st.number_input("NO₂", 0.0, 300.0, 40.0)
with c2:
    pm10 = st.number_input("PM10", 0.0, 600.0, 140.0)
    so2  = st.number_input("SO₂", 0.0, 200.0, 15.0)

st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# HEALTH ADVISORY FUNCTION
# ===============================
def health_advisory(aqi):
    if aqi <= 50:
        return "✅ Excellent Air Quality", [
            "🌿 Safe for everyone",
            "🏃 Ideal for outdoor exercise",
            "👶 Safe for children & elderly"
        ], "#00ff87"
    elif aqi <= 100:
        return "🙂 Acceptable Air Quality", [
            "⚠️ Mild discomfort for sensitive groups",
            "🫁 Asthma patients should monitor symptoms",
            "🚴 Outdoor activity allowed with breaks"
        ], "#7dd3fc"
    elif aqi <= 200:
        return "😐 Moderate Pollution", [
            "👶 Children & elderly should stay indoors",
            "😷 Wear masks outdoors",
            "🏃 Avoid heavy exercise"
        ], "#ffd166"
    elif aqi <= 300:
        return "🚨 Poor Air Quality", [
            "❌ Avoid outdoor activities",
            "😷 Masks mandatory",
            "🏠 Use air purifiers",
            "🚫 Outdoor work not recommended"
        ], "#ff9f1c"
    else:
        return "☠️ Severe Air Emergency", [
            "🚫 Everyone must stay indoors",
            "🏥 High risk for heart & lung patients",
            "❌ No outdoor exposure",
            "📞 Follow government health advisories"
        ], "#ff4d4d"

# ===============================
# PREDICTION
# ===============================
if st.button("🚀 Predict AQI"):

    input_df = pd.DataFrame([{
        "pm25": pm25,
        "pm10": pm10,
        "no2": no2,
        "so2": so2
    }])

    prediction = int(model.predict(input_df)[0])

    # AQI RESULT
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.markdown(f"<div class='aqi-box'>Predicted AQI: {prediction}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # HEALTH ADVISORY (ABOVE GRAPHS)
    title, points, color = health_advisory(prediction)
    st.markdown(f"""
    <div class='glass' style='border-left:6px solid {color};'>
        <h3 style='color:{color};'>🩺 Health Advisory</h3>
        <h4>{title}</h4>
        <ul style='font-size:17px; line-height:1.7;'>
            {''.join(f"<li>{p}</li>" for p in points)}
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # AQI GAUGE
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prediction,
        gauge={
            "axis": {"range": [0, 500]},
            "bar": {"color": "#00ffff"},
            "steps": [
                {"range": [0,50], "color": "#00e400"},
                {"range": [51,100], "color": "#ffff00"},
                {"range": [101,200], "color": "#ff7e00"},
                {"range": [201,300], "color": "#ff0000"},
                {"range": [301,500], "color": "#7e0023"},
            ],
        },
        title={"text": "AQI Severity Gauge"}
    ))
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # POLLUTANT BAR CHART
    poll_df = pd.DataFrame({
        "Pollutant": ["PM2.5", "PM10", "NO₂", "SO₂"],
        "Value": [pm25, pm10, no2, so2]
    })
    fig_bar = px.bar(
        poll_df, x="Pollutant", y="Value",
        color="Value", color_continuous_scale="Turbo",
        title="Pollutant Concentration Levels"
    )
    st.markdown("<div class='glass'>", unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown(
    "<center style='color:#7dd3fc;'>ML Project • Futuristic AQI Analytics 🌱</center>",
    unsafe_allow_html=True
)
