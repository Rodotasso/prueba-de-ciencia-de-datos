import streamlit as st

st.set_page_config(page_title="AI Epidemiology & Public Health Agent", page_icon="🏥", layout="wide")

# ===== CSS =====
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #89f7fe, #66a6ff);
    }
    .main-title {
        text-align: center;
        font-size: 3em;
        color: white;
        font-weight: bold;
        margin-bottom: 0.3em;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #f0f0f0;
        margin-bottom: 2em;
    }
    .cards-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 25px;
        margin-top: 30px;
    }
    .card {
        background-color: white;
        width: 260px;
        height: 180px;
        border-radius: 20px;
        box-shadow: 0px 6px 20px rgba(0,0,0,0.15);
        text-align: center;
        padding: 20px;
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        cursor: pointer;
        text-decoration: none;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0px 10px 30px rgba(0,0,0,0.25);
    }
    .card-icon {
        font-size: 2.5em;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 6px;
        color: #333;
    }
    .card-desc {
        font-size: 0.9em;
        color: #666;
    }
    .center-btn {
        text-align: center;
        margin-top: 40px;
    }
    .get-started-btn {
        background-color: #ff6b6b;
        color: white;
        padding: 14px 40px;
        border-radius: 30px;
        font-size: 1.2em;
        font-weight: bold;
        text-decoration: none;
        transition: background 0.3s ease-in-out;
    }
    .get-started-btn:hover {
        background-color: #ff4757;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Title =====
st.markdown("<h1 class='main-title'>🏥 AI Epidemiology & Public Health Agent</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Advanced Biostatistical Analysis & Epidemiological Modeling for Doctoral Research 📊</p>", unsafe_allow_html=True)

# ===== Cards =====
cards_html = """
<div class="cards-container">
    <a href="?page=01_📂_Upload_and_Schema" class="card">
        <div class="card-icon">📂</div>
        <div class="card-title">Step-1: Upload Data</div>
        <div class="card-desc">Load epidemiological datasets (CSV, Excel, JSON, Parquet)</div>
    </a>
    <a href="?page=02_🧹_Clean_Data" class="card">
        <div class="card-icon">🧹</div>
        <div class="card-title">Step-2: Data Cleaning</div>
        <div class="card-desc">Handle missing values, outliers & data quality issues</div>
    </a>
    <a href="?page=03_📊_Data_Visualization" class="card">
        <div class="card-icon">📊</div>
        <div class="card-title">Step-3: Epi Visualizations</div>
        <div class="card-desc">Pyramids, epi curves, survival plots & heat maps</div>
    </a>
    <a href="?page=04_🤖_Modeling_and_Evaluation" class="card">
        <div class="card-icon">🤖</div>
        <div class="card-title">Step-4: ML Models</div>
        <div class="card-desc">Predictive modeling with XGBoost, Random Forest & more</div>
    </a>
    <a href="?page=04b_🏥_Epidemiological_Models" class="card">
        <div class="card-icon">🏥</div>
        <div class="card-title">Step-4b: Epi Models</div>
        <div class="card-desc">Cox, Kaplan-Meier, Poisson, OR/RR/HR analysis</div>
    </a>
    <a href="?page=05_📑_Report" class="card">
        <div class="card-icon">📑</div>
        <div class="card-title">Step-5: Report</div>
        <div class="card-desc">Generate professional epidemiological reports</div>
    </a>
</div>
"""

st.markdown(cards_html, unsafe_allow_html=True)

# ===== Get Started Button =====
st.markdown("""
<div class="center-btn">
    <a href="?page=01_📂_Upload_and_Schema" class="get-started-btn">✨ Get Started</a>
</div>
""", unsafe_allow_html=True)

# ===== Handle Navigation =====
query_params = st.query_params
if "page" in query_params:
    st.switch_page(f"pages/{query_params['page']}.py")
