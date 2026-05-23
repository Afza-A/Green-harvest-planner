import joblib
import pandas as pd
import plotly.express as px
import streamlit as st

from src.climate_risk import get_climate_condition
from src.data_loader import load_crop_dataset
from src.harvest_info import estimate_harvest_duration
from src.recommendation import (
    calculate_sustainability_score,
    get_recommendations,
    get_score_message,
    get_yield_category,
)

st.set_page_config(page_title="Green Harvest Planner", layout="wide")


@st.cache_data
def get_data():
    train_df, test_df = load_crop_dataset()
    full_df = pd.concat([train_df, test_df], ignore_index=True)
    return train_df, test_df, full_df


@st.cache_resource
def get_model():
    return joblib.load("models/crop_yield_model.pkl")


@st.cache_data
def get_metrics():
    try:
        return pd.read_csv("models/model_evaluation_results.csv")
    except FileNotFoundError:
        return pd.DataFrame()


@st.cache_data
def get_confusion_matrix():
    try:
        return pd.read_csv("models/confusion_matrix.csv", index_col=0)
    except FileNotFoundError:
        return pd.DataFrame()


train_df, test_df, df = get_data()
model = get_model()
metrics_df = get_metrics()
cm_df = get_confusion_matrix()


with st.sidebar:
    st.header("Farm Details")

    crop_search = st.text_input("Search crop", placeholder="Type crop name...")
    all_crops = sorted(df["Crop"].unique())

    if crop_search:
        crop_options = [
            crop_name for crop_name in all_crops
            if crop_search.lower() in crop_name.lower()
        ]
    else:
        crop_options = all_crops

    if not crop_options:
        st.warning("No crop found. Showing all crops again.")
        crop_options = all_crops

    crop = st.selectbox("Choose Crop", crop_options)
    state = st.selectbox("Choose State", sorted(df["State"].unique()))
    season = st.selectbox("Choose Season", sorted(df["Season"].unique()))

    year = st.number_input(
        "Cultivation Year",
        min_value=int(df["Year"].min()),
        max_value=2030,
        value=2024,
        step=1,
    )

    area = st.number_input(
        "Cultivated Area (hectares)",
        min_value=1.0,
        value=1000.0,
        step=100.0,
    )

    rainfall = st.slider(
        "Annual Rainfall (mm)",
        min_value=0.0,
        max_value=3000.0,
        value=800.0,
    )

    fertilizer = st.slider(
        "Fertilizer Input (kg)",
        min_value=0.0,
        max_value=10000.0,
        value=150.0,
    )

    pesticide = st.slider(
        "Pesticide Input (L)",
        min_value=0.0,
        max_value=1000.0,
        value=20.0,
    )


input_data = pd.DataFrame([{
    "Year": year,
    "State": state,
    "Crop": crop,
    "Season": season,
    "Area": area,
    "Annual_Rainfall": rainfall,
    "Fertilizer": fertilizer,
    "Pesticide": pesticide,
}])

prediction = model.predict(input_data)[0]
yield_category = get_yield_category(prediction)
green_score = calculate_sustainability_score(rainfall, fertilizer, pesticide, area)
score_message = get_score_message(green_score)

climate_status, climate_message = get_climate_condition(rainfall)

harvest_info = estimate_harvest_duration(
    crop,
    rainfall,
    fertilizer,
    pesticide,
    area,
    prediction,
)

harvest_months = harvest_info["estimated_months"]
harvest_status = harvest_info["status"]
harvest_message = harvest_info["message"]
harvest_risks = harvest_info["risks"]


if green_score >= 80 and prediction >= 3:
    mood = "Flourishing Field"
    dark = "#0F2A1D"
    mid = "#2F6B3F"
    soft = "#7B967A"
    light = "#BED4C2"
elif green_score >= 50:
    mood = "Growing Steady"
    dark = "#1E3A2A"
    mid = "#6B4028"
    soft = "#7B967A"
    light = "#ECE6D8"
else:
    mood = "Needs Gentle Care"
    dark = "#26351F"
    mid = "#8A5A35"
    soft = "#A3B18A"
    light = "#ECE6D8"


st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Nunito:wght@400;600;700;800;900&display=swap');

.stApp {{
    background:
        radial-gradient(circle at 12% 10%, rgba(190,212,194,.35), transparent 18%),
        radial-gradient(circle at 86% 18%, rgba(123,150,122,.28), transparent 16%),
        linear-gradient(rgba(15,42,29,.88), rgba(15,42,29,.90)),
        url("assets/leaf_pattern.jpg");
    background-size: auto, auto, auto, 360px;
    color: #ECE6D8;
    font-family: Nunito, sans-serif;
}}

.block-container {{
    max-width: 1320px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(rgba(15,42,29,.94), rgba(47,107,63,.88));
    border-right: 2px solid rgba(190,212,194,.35);
}}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {{
    color: #ECE6D8 !important;
    font-weight: 900 !important;
}}

[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background-color: #ECE6D8 !important;
    color: #340B01 !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
}}

.hero {{
    background: linear-gradient(135deg, {dark}, {mid});
    border: 2px solid rgba(190,212,194,.42);
    box-shadow: 0 24px 60px rgba(0,0,0,.35);
    border-radius: 32px;
    padding: 44px;
    position: relative;
    overflow: hidden;
}}

.hero:after {{
    content: "";
    position: absolute;
    right: -50px;
    bottom: -60px;
    width: 260px;
    height: 180px;
    background: {light};
    opacity: .28;
    border-radius: 70% 30% 60% 40%;
    transform: rotate(-12deg);
}}

.hero-title {{
    font-family: 'DM Serif Display', serif;
    font-size: 68px;
    line-height: 1;
    color: #ECE6D8;
}}

.hero-text {{
    font-size: 22px;
    line-height: 1.55;
    color: #DDEDD6;
    font-weight: 800;
    max-width: 980px;
}}

.mood {{
    display: inline-block;
    margin-top: 18px;
    background: linear-gradient(135deg, {light}, #ECE6D8);
    color: #340B01;
    padding: 12px 18px;
    border-radius: 999px;
    font-weight: 900;
    font-size: 18px;
}}

.card {{
    background: linear-gradient(145deg, #ECE6D8, {light});
    color: #340B01;
    border-left: 9px solid {soft};
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 16px 36px rgba(0,0,0,.25);
    min-height: 175px;
}}

.card-label {{
    color: {mid};
    font-weight: 900;
    font-size: 16px;
}}

.card-value {{
    font-size: clamp(24px, 2.1vw, 34px);
    line-height: 1.15;
    font-weight: 900;
    margin-top: 8px;
    word-break: normal;
    overflow-wrap: normal;
}}

.card-small {{
    font-weight: 900;
    color: {mid};
    margin-top: 8px;
    font-size: 15px;
    line-height: 1.35;
}}

.advice {{
    background: linear-gradient(135deg, #ECE6D8, {light});
    color: #340B01;
    border-left: 9px solid {mid};
    border-radius: 22px;
    padding: 18px 22px;
    margin-bottom: 14px;
    font-size: 18px;
    font-weight: 850;
    box-shadow: 0 12px 28px rgba(0,0,0,.20);
}}

.note {{
    background: linear-gradient(135deg, {mid}, {dark});
    color: #ECE6D8;
    border: 2px dashed rgba(236,230,216,.5);
    border-radius: 22px;
    padding: 20px;
    font-size: 19px;
    font-weight: 900;
}}

.stTabs [data-baseweb="tab"] {{
    background: #ECE6D8;
    color: #340B01;
    border-radius: 16px;
    padding: 12px 20px;
    font-weight: 900;
}}

.stTabs [aria-selected="true"] {{
    background: {light};
    border-bottom: 5px solid {mid};
}}

.js-plotly-plot {{
    border-radius: 20px;
    overflow: hidden;
}}
</style>
""", unsafe_allow_html=True)


st.markdown(f"""
<div class="hero">
    <div class="hero-title">Green Harvest Planner</div>
    <div class="hero-text">
        Plan your crop like a tiny green adventure. Choose a crop, set the season,
        rainfall in mm, fertilizer in kg, and pesticide in liters. This app estimates yield,
        harvest outlook, climate risk, and field care tips. The ML model learns from Indian crop data,
        while climate notes help spot drought, heavy-rain, and input-stress risks.
    </div>
    <div class="mood">{mood}</div>
</div>
""", unsafe_allow_html=True)

st.write("")

c1, c2, c3, c4, c5 = st.columns([1.1, 1.3, 1.1, 1.3, 1.4])

with c1:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Predicted Yield</div>
        <div class="card-value">{prediction:.2f}</div>
        <div class="card-small">estimated yield in tonnes per hectare (t/ha)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Yield Category</div>
        <div class="card-value">{yield_category}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Green Score</div>
        <div class="card-value">{green_score}/100</div>
        <div class="card-small">rainfall + input-use warning score</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Harvest Outlook</div>
        <div class="card-value">{harvest_months} months</div>
        <div class="card-small">{harvest_status}</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="card">
        <div class="card-label">Climate Condition</div>
        <div class="card-value">{climate_status}</div>
        <div class="card-small">{climate_message}</div>
    </div>
    """, unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Prediction",
    "Model Evaluation",
    "Confusion Matrix",
    "What-If Analysis",
    "Dataset"
])


with tab1:
    st.subheader("Field Suggestions")

    st.markdown(
        '<div class="note">Green Score is not model accuracy. It is a sustainability warning score based on rainfall, fertilizer per hectare, and pesticide per hectare.</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(f'<div class="note">{harvest_message}</div>', unsafe_allow_html=True)

    if harvest_risks:
        st.write("")
        for risk in harvest_risks:
            st.markdown(
                f'<div class="advice">Growth note: {risk}.</div>',
                unsafe_allow_html=True,
            )

    st.write("")

    st.markdown(
        f'<div class="advice">Climate note: {climate_message}</div>',
        unsafe_allow_html=True,
    )

    for rec in get_recommendations(rainfall, fertilizer, pesticide, area, prediction):
        st.markdown(f'<div class="advice">{rec}</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="note">{score_message}</div>', unsafe_allow_html=True)


with tab2:
    st.subheader("Model Evaluation Metrics")

    if metrics_df.empty:
        st.warning("Run `python train_model.py` first to generate evaluation metrics.")
    else:
        st.dataframe(metrics_df, use_container_width=True)

        fig = px.bar(
            metrics_df,
            x="Model",
            y=["Train_R2", "Test_R2", "CV_R2_Mean"],
            barmode="group",
            title="Model R2 Comparison",
            color_discrete_sequence=["#1F5A3A", "#7B967A", "#6B4028"],
        )
        fig.update_layout(
            paper_bgcolor="#ECE6D8",
            plot_bgcolor="#BED4C2",
            font=dict(color="#340B01", size=14),
            title_font=dict(color="#340B01", size=22),
        )
        st.plotly_chart(fig, use_container_width=True)

        fig_error = px.bar(
            metrics_df,
            x="Model",
            y=["MAE", "RMSE", "Median_AE"],
            barmode="group",
            title="Model Error Comparison",
            color_discrete_sequence=["#2F6B3F", "#A3B18A", "#8A5A35"],
        )
        fig_error.update_layout(
            paper_bgcolor="#ECE6D8",
            plot_bgcolor="#BED4C2",
            font=dict(color="#340B01", size=14),
            title_font=dict(color="#340B01", size=22),
        )
        st.plotly_chart(fig_error, use_container_width=True)


with tab3:
    st.subheader("Confusion Matrix From Yield Categories")

    st.write(
        "Yield is a regression target, so the confusion matrix is created after grouping yield into Low, Medium, and High categories."
    )

    if cm_df.empty:
        st.warning("Run `python train_model.py` first to generate confusion matrix.")
    else:
        fig_cm = px.imshow(
            cm_df,
            text_auto=True,
            color_continuous_scale=["#ECE6D8", "#7B967A", "#1F5A3A"],
            title="Yield Category Confusion Matrix",
        )
        fig_cm.update_layout(
            paper_bgcolor="#ECE6D8",
            plot_bgcolor="#ECE6D8",
            font=dict(color="#340B01", size=14),
            title_font=dict(color="#340B01", size=22),
        )
        st.plotly_chart(fig_cm, use_container_width=True)
        st.dataframe(cm_df, use_container_width=True)


with tab4:
    st.subheader("What-If Analysis")

    w1, w2, w3 = st.columns(3)

    with w1:
        new_rainfall = st.slider("Try Rainfall (mm)", 0.0, 3000.0, float(rainfall))

    with w2:
        new_fertilizer = st.slider("Try Fertilizer Input (kg)", 0.0, 10000.0, float(fertilizer))

    with w3:
        new_pesticide = st.slider("Try Pesticide Input (L)", 0.0, 1000.0, float(pesticide))

    scenario_data = input_data.copy()
    scenario_data["Annual_Rainfall"] = new_rainfall
    scenario_data["Fertilizer"] = new_fertilizer
    scenario_data["Pesticide"] = new_pesticide

    scenario_prediction = model.predict(scenario_data)[0]
    scenario_climate_status, scenario_climate_message = get_climate_condition(new_rainfall)

    scenario_harvest = estimate_harvest_duration(
        crop,
        new_rainfall,
        new_fertilizer,
        new_pesticide,
        area,
        scenario_prediction,
    )

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Current Yield", f"{prediction:.2f} t/ha")
    s2.metric("New Yield", f"{scenario_prediction:.2f} t/ha", f"{scenario_prediction - prediction:.2f}")
    s3.metric("New Harvest Time", f"{scenario_harvest['estimated_months']} months")
    s4.metric("New Climate", scenario_climate_status)

    st.markdown(
        f'<div class="note">{scenario_harvest["message"]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="advice">Scenario climate note: {scenario_climate_message}</div>',
        unsafe_allow_html=True,
    )


with tab5:
    st.subheader("Dataset Overview")

    d1, d2, d3 = st.columns(3)
    d1.metric("Training Rows", f"{train_df.shape[0]:,}")
    d2.metric("Testing Rows", f"{test_df.shape[0]:,}")
    d3.metric("Features Used", "8")

    st.markdown(
        '<div class="note">In this project, area is treated as hectares, rainfall as millimeters, fertilizer as kilograms, pesticide as liters, and yield as tonnes per hectare. The model uses crop, state, season, year, area, rainfall, fertilizer, and pesticide. Humidity, temperature, soil moisture, and flood data are not present in this dataset, so they are not used as model features.</div>',
        unsafe_allow_html=True,
    )

    st.write("")

    st.dataframe(df.head(100), use_container_width=True)

    fig_rain = px.scatter(
        df,
        x="Annual_Rainfall",
        y="Yield",
        color="Season",
        title="Rainfall vs Yield",
        color_discrete_sequence=["#1F5A3A", "#7B967A", "#6B4028", "#A3B18A", "#D4A373"],
    )
    fig_rain.update_layout(
        paper_bgcolor="#ECE6D8",
        plot_bgcolor="#BED4C2",
        font=dict(color="#340B01", size=14),
        title_font=dict(color="#340B01", size=22),
    )
    st.plotly_chart(fig_rain, use_container_width=True) 