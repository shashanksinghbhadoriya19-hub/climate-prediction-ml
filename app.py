import streamlit as st
import numpy as np
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Climate Prediction",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- LOAD MODEL ----------------
model = joblib.load("climate_model.pkl")
scaler = joblib.load("scaler.pkl")

# ---------------- CUSTOM DARK THEME CSS ----------------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
.block-container {
    padding-top: 2rem;
}
.card {
    background-color: #161b22;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 0 12px rgba(0,0,0,0.4);
}
.result {
    font-size: 48px;
    font-weight: bold;
    color: #00ffcc;
    text-align: center;
}
.subtext {
    text-align: center;
    color: #9ba3b4;
}
hr {
    border: 1px solid #30363d;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center;'>🌍 Climate Prediction Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#9ba3b4;'>Machine Learning based temperature prediction</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- LAYOUT ----------------
col1, col2 = st.columns(2)

# -------- INPUT CARD --------
with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🔧 Input Weather Parameters")

    precipitation = st.number_input("🌧 Precipitation (mm)", min_value=0.0, max_value=50.0, value=2.0)
    temp_min = st.number_input("🌡 Minimum Temperature (°C)", min_value=-10.0, max_value=30.0, value=10.0)
    wind = st.number_input("💨 Wind Speed (m/s)", min_value=0.0, max_value=20.0, value=3.0)

    predict_btn = st.button("🔮 Predict Temperature")
    st.markdown("</div>", unsafe_allow_html=True)

# -------- RESULT CARD --------
with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📊 Prediction Result")

    if predict_btn:
        input_data = np.array([[precipitation, temp_min, wind]])
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)

        st.markdown(f"<div class='result'>{prediction[0]:.2f} °C</div>", unsafe_allow_html=True)
        st.markdown("<p class='subtext'>Predicted Maximum Temperature</p>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='subtext'>Enter values and click Predict</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- EXPLANATION ----------------
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("ℹ How this prediction works"):
    st.write("""
    - This system uses **Random Forest Regression**
    - Trained on **historical weather data**
    - Input features are scaled using **StandardScaler**
    - The model predicts **maximum temperature** based on similar past patterns
    """)

# ---------------- FOOTER ----------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#9ba3b4;'>Streamlit</p>", unsafe_allow_html=True)
