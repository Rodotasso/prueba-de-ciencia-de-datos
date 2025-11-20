import streamlit as st

st.set_page_config(page_title="AI Epidemiology & Public Health Agent", page_icon="🏥", layout="wide")

# ===== CSS - Diseño Profesional de Salud Pública =====
st.markdown("""
    <style>
    /* Fondo con tema médico profesional */
    .stApp {
        background: linear-gradient(to bottom, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Header con barra superior */
    .header-bar {
        background: linear-gradient(135deg, #2c5f2d 0%, #97cc04 100%);
        padding: 20px;
        border-radius: 0 0 15px 15px;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-title {
        text-align: center;
        font-size: 2.8em;
        color: white;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.1em;
        color: #f0f0f0;
        margin-top: 10px;
        font-weight: 300;
    }
    
    /* Contenedor de workflow */
    .workflow-container {
        max-width: 1200px;
        margin: 40px auto;
        padding: 0 20px;
    }
    
    .workflow-title {
        text-align: center;
        font-size: 1.8em;
        color: #2c5f2d;
        font-weight: 600;
        margin-bottom: 30px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Grid de tarjetas estilo moderno */
    .cards-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 20px;
        margin-top: 20px;
    }
    
    .step-card {
        background: white;
        border-left: 5px solid #2c5f2d;
        border-radius: 12px;
        padding: 25px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .step-card:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 20px rgba(44,95,45,0.15);
        border-left-color: #97cc04;
    }
    
    .step-card::before {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: linear-gradient(135deg, transparent 60%, rgba(151,204,4,0.1) 100%);
        border-radius: 0 12px 0 100%;
    }
    
    .step-number {
        display: inline-block;
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #2c5f2d, #97cc04);
        color: white;
        border-radius: 50%;
        text-align: center;
        line-height: 40px;
        font-weight: bold;
        font-size: 1.2em;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(44,95,45,0.3);
    }
    
    .step-title {
        font-size: 1.3em;
        font-weight: 600;
        color: #2c5f2d;
        margin: 10px 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .step-icon {
        font-size: 2em;
        float: right;
        margin-top: -35px;
        opacity: 0.7;
    }
    
    .step-desc {
        color: #555;
        font-size: 0.95em;
        line-height: 1.5;
        margin-top: 10px;
    }
    
    .step-link {
        display: inline-block;
        margin-top: 15px;
        color: #2c5f2d;
        font-weight: 600;
        text-decoration: none;
        font-size: 0.9em;
        transition: color 0.3s;
    }
    
    .step-link:hover {
        color: #97cc04;
    }
    
    /* Botón de inicio con nuevo diseño */
    .cta-section {
        text-align: center;
        margin: 50px auto;
        padding: 40px;
        background: white;
        border-radius: 15px;
        max-width: 600px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .cta-button {
        display: inline-block;
        background: linear-gradient(135deg, #2c5f2d 0%, #97cc04 100%);
        color: white;
        padding: 18px 45px;
        border-radius: 8px;
        font-size: 1.2em;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(44,95,45,0.3);
        border: none;
        cursor: pointer;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(44,95,45,0.4);
    }
    
    /* Badge de características */
    .features-badge {
        display: inline-block;
        background: #e8f5e9;
        color: #2c5f2d;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        margin: 5px 5px 5px 0;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown("""
<div class="header-bar">
    <h1 class="main-title">🏥 AI Epidemiology & Public Health Agent</h1>
    <p class="subtitle">Advanced Biostatistical Analysis & Epidemiological Modeling for Doctoral Research</p>
</div>
""", unsafe_allow_html=True)

# ===== Workflow Section =====
st.markdown('<h2 class="workflow-title">📋 Analysis Workflow</h2>', unsafe_allow_html=True)

workflow_html = """
<div class="workflow-container">
    <div class="cards-grid">
        <div class="step-card">
            <span class="step-number">1</span>
            <span class="step-icon">📂</span>
            <h3 class="step-title">Upload Data</h3>
            <p class="step-desc">Load epidemiological datasets in multiple formats: CSV, Excel, JSON, Parquet. Handle multiple files simultaneously.</p>
            <span class="features-badge">Multi-format</span>
            <span class="features-badge">Batch upload</span>
            <a href="?page=01_📂_Upload_and_Schema" class="step-link">Start uploading →</a>
        </div>
        
        <div class="step-card">
            <span class="step-number">2</span>
            <span class="step-icon">🧹</span>
            <h3 class="step-title">Data Cleaning</h3>
            <p class="step-desc">Handle missing values, outliers detection (IQR, Z-score), smart imputation, and data quality assessment.</p>
            <span class="features-badge">Outlier detection</span>
            <span class="features-badge">Smart imputation</span>
            <a href="?page=02_🧹_Clean_Data" class="step-link">Clean data →</a>
        </div>
        
        <div class="step-card">
            <span class="step-number">3</span>
            <span class="step-icon">📊</span>
            <h3 class="step-title">Epi Visualizations</h3>
            <p class="step-desc">Population pyramids, epidemic curves, survival plots, geographic heat maps, and advanced epidemiological charts.</p>
            <span class="features-badge">Kaplan-Meier</span>
            <span class="features-badge">Epi curves</span>
            <a href="?page=03_📊_Data_Visualization" class="step-link">Visualize →</a>
        </div>
        
        <div class="step-card">
            <span class="step-number">4</span>
            <span class="step-icon">🤖</span>
            <h3 class="step-title">ML Predictive Models</h3>
            <p class="step-desc">Train and evaluate machine learning models: XGBoost, Random Forest, SVM with cross-validation and hyperparameter tuning.</p>
            <span class="features-badge">15 algorithms</span>
            <span class="features-badge">Auto-tuning</span>
            <a href="?page=04_🤖_Modeling_and_Evaluation" class="step-link">Build models →</a>
        </div>
        
        <div class="step-card">
            <span class="step-number">5</span>
            <span class="step-icon">🏥</span>
            <h3 class="step-title">Epidemiological Models</h3>
            <p class="step-desc">Cox Proportional Hazards, Kaplan-Meier survival analysis, Poisson regression, OR/RR/HR calculations, SMR analysis.</p>
            <span class="features-badge">Survival analysis</span>
            <span class="features-badge">Cox PH</span>
            <a href="?page=04b_🏥_Epidemiological_Models" class="step-link">Analyze →</a>
        </div>
        
        <div class="step-card">
            <span class="step-number">6</span>
            <span class="step-icon">📑</span>
            <h3 class="step-title">Generate Reports</h3>
            <p class="step-desc">Create professional epidemiological reports with statistics, visualizations, and model results in PDF or HTML format.</p>
            <span class="features-badge">PDF export</span>
            <span class="features-badge">HTML reports</span>
            <a href="?page=05_📑_Report" class="step-link">Create report →</a>
        </div>
    </div>
</div>
"""

st.markdown(workflow_html, unsafe_allow_html=True)

# ===== CTA Section =====
st.markdown("""
<div class="cta-section">
    <h3 style="color: #2c5f2d; margin-bottom: 15px;">Ready to analyze your epidemiological data?</h3>
    <p style="color: #666; margin-bottom: 25px;">Start with uploading your dataset and let AI guide you through the analysis</p>
    <a href="?page=01_📂_Upload_and_Schema" class="cta-button">🚀 Begin Analysis</a>
</div>
""", unsafe_allow_html=True)

# ===== Handle Navigation =====
query_params = st.query_params
if "page" in query_params:
    st.switch_page(f"pages/{query_params['page']}.py")
