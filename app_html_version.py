import streamlit as st

st.set_page_config(
    page_title="EpiHealth AI Platform", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS - Diseño Dashboard Médico Moderno =====
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background: #0a0e27;
        background-image: 
            radial-gradient(at 47% 33%, hsl(162, 77%, 40%) 0, transparent 59%), 
            radial-gradient(at 82% 65%, hsl(198, 100%, 50%) 0, transparent 55%);
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 60px 20px 40px;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(34, 211, 238, 0.1);
        border: 1px solid rgba(34, 211, 238, 0.3);
        color: #22d3ee;
        padding: 8px 20px;
        border-radius: 30px;
        font-size: 0.85em;
        font-weight: 500;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    
    .hero-title {
        font-size: 3.5em;
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff 0%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.2em;
        color: rgba(255, 255, 255, 0.7);
        font-weight: 400;
        margin: 20px auto;
        max-width: 700px;
        line-height: 1.6;
    }
    
    /* Process Timeline - Diseño Único */
    .timeline-container {
        max-width: 1100px;
        margin: 60px auto;
        padding: 0 20px;
        position: relative;
    }
    
    .timeline-header {
        text-align: center;
        margin-bottom: 50px;
    }
    
    .timeline-title {
        font-size: 2em;
        color: white;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .timeline-desc {
        color: rgba(255, 255, 255, 0.6);
        font-size: 1em;
    }
    
    /* Process Steps - Layout Horizontal */
    .process-steps {
        display: flex;
        flex-direction: column;
        gap: 25px;
    }
    
    .process-step {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px;
        display: flex;
        align-items: center;
        gap: 25px;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .process-step::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #22d3ee, #06b6d4);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.4s ease;
    }
    
    .process-step:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(34, 211, 238, 0.4);
        transform: translateX(10px);
    }
    
    .process-step:hover::before {
        transform: scaleX(1);
    }
    
    .step-icon-wrapper {
        flex-shrink: 0;
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.2), rgba(6, 182, 212, 0.2));
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.5em;
        position: relative;
    }
    
    .step-number-badge {
        position: absolute;
        top: -8px;
        right: -8px;
        width: 28px;
        height: 28px;
        background: linear-gradient(135deg, #22d3ee, #06b6d4);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.4em;
        color: white;
        font-weight: 700;
        box-shadow: 0 4px 12px rgba(34, 211, 238, 0.4);
    }
    
    .step-content {
        flex: 1;
    }
    
    .step-name {
        font-size: 1.4em;
        color: white;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .step-description {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.95em;
        line-height: 1.6;
        margin-bottom: 12px;
    }
    
    .step-tags {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
    }
    
    .tag {
        background: rgba(34, 211, 238, 0.1);
        border: 1px solid rgba(34, 211, 238, 0.3);
        color: #22d3ee;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.8em;
        font-weight: 500;
    }
    
    .step-action {
        flex-shrink: 0;
        width: 120px;
        text-align: center;
    }
    
    .action-button {
        display: inline-block;
        background: linear-gradient(135deg, #22d3ee, #06b6d4);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9em;
        transition: all 0.3s ease;
        box-shadow: 0 4px 14px rgba(34, 211, 238, 0.3);
    }
    
    .action-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(34, 211, 238, 0.5);
    }
    
    /* CTA Section - Diseño Único */
    .cta-wrapper {
        max-width: 800px;
        margin: 80px auto 60px;
        padding: 0 20px;
    }
    
    .cta-card {
        background: linear-gradient(135deg, rgba(34, 211, 238, 0.1), rgba(6, 182, 212, 0.1));
        border: 1px solid rgba(34, 211, 238, 0.2);
        border-radius: 20px;
        padding: 50px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .cta-heading {
        font-size: 2em;
        color: white;
        font-weight: 700;
        margin-bottom: 15px;
    }
    
    .cta-text {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1em;
        margin-bottom: 35px;
    }
    
    .cta-main-button {
        display: inline-block;
        background: linear-gradient(135deg, #22d3ee, #06b6d4);
        color: white;
        padding: 18px 50px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1.15em;
        transition: all 0.3s ease;
        box-shadow: 0 8px 24px rgba(34, 211, 238, 0.4);
    }
    
    .cta-main-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(34, 211, 238, 0.6);
    }
    
    /* Features Grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 20px;
        max-width: 1100px;
        margin: 40px auto;
        padding: 0 20px;
    }
    
    .feature-box {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        background: rgba(255, 255, 255, 0.05);
        border-color: rgba(34, 211, 238, 0.3);
    }
    
    .feature-icon {
        font-size: 2.5em;
        margin-bottom: 15px;
    }
    
    .feature-title {
        color: white;
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .feature-text {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9em;
    }
    
    @media (max-width: 768px) {
        .hero-title { font-size: 2.2em; }
        .process-step { flex-direction: column; text-align: center; }
        .step-action { width: 100%; }
    }
    </style>
""", unsafe_allow_html=True)

# ===== Hero Section =====
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">🏥 DOCTORAL-LEVEL PLATFORM</div>
    <h1 class="hero-title">EpiHealth AI Platform</h1>
    <p class="hero-subtitle">
        Advanced biostatistical analysis and epidemiological modeling powered by artificial intelligence. 
        From data ingestion to publication-ready insights.
    </p>
</div>
""", unsafe_allow_html=True)

# ===== Features Grid =====
st.markdown("""
<div class="features-grid">
    <div class="feature-box">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">Lightning Fast</div>
        <div class="feature-text">Process millions of records in seconds</div>
    </div>
    <div class="feature-box">
        <div class="feature-icon">🔬</div>
        <div class="feature-title">PhD-Level Analysis</div>
        <div class="feature-text">Cox, Kaplan-Meier, Poisson regression</div>
    </div>
    <div class="feature-box">
        <div class="feature-icon">🤖</div>
        <div class="feature-title">AI-Powered</div>
        <div class="feature-text">Smart insights with Groq LLM</div>
    </div>
    <div class="feature-box">
        <div class="feature-icon">📊</div>
        <div class="feature-title">Interactive Viz</div>
        <div class="feature-text">Forest plots, survival curves, pyramids</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== Process Timeline =====
st.markdown("""
<div class="timeline-container">
    <div class="timeline-header">
        <h2 class="timeline-title">Complete Analysis Pipeline</h2>
        <p class="timeline-desc">6-step workflow from raw data to publication-ready results</p>
    </div>
    
    <div class="process-steps">
        <div class="process-step">
            <div class="step-icon-wrapper">
                <span>📂</span>
                <div class="step-number-badge">1</div>
            </div>
            <div class="step-content">
                <div class="step-name">Data Ingestion</div>
                <div class="step-description">
                    Load multiple epidemiological datasets simultaneously. Support for CSV, Excel, JSON, and Parquet formats with automatic encoding detection.
                </div>
                <div class="step-tags">
                    <span class="tag">Multi-format</span>
                    <span class="tag">Batch processing</span>
                    <span class="tag">Auto-detect</span>
                </div>
            </div>
            <div class="step-action">
                <a href="?page=01_📂_Upload_and_Schema" class="action-button">Upload</a>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-icon-wrapper">
                <span>🧹</span>
                <div class="step-number-badge">2</div>
            </div>
            <div class="step-content">
                <div class="step-name">Data Preprocessing</div>
                <div class="step-description">
                    Advanced cleaning pipeline with outlier detection (IQR, Z-score), intelligent imputation, and quality assessment metrics.
                </div>
                <div class="step-tags">
                    <span class="tag">IQR detection</span>
                    <span class="tag">Smart impute</span>
                    <span class="tag">QC metrics</span>
                </div>
            </div>
            <div class="step-action">
                <a href="?page=02_🧹_Clean_Data" class="action-button">Clean</a>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-icon-wrapper">
                <span>📊</span>
                <div class="step-number-badge">3</div>
            </div>
            <div class="step-content">
                <div class="step-name">Epidemiological Visualization</div>
                <div class="step-description">
                    Generate population pyramids, epidemic curves, survival plots, heat maps, and interactive dashboards for exploratory analysis.
                </div>
                <div class="step-tags">
                    <span class="tag">Plotly</span>
                    <span class="tag">Kaplan-Meier</span>
                    <span class="tag">Epi curves</span>
                </div>
            </div>
            <div class="step-action">
                <a href="?page=03_📊_Data_Visualization" class="action-button">Explore</a>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-icon-wrapper">
                <span>🤖</span>
                <div class="step-number-badge">4</div>
            </div>
            <div class="step-content">
                <div class="step-name">Machine Learning Models</div>
                <div class="step-description">
                    Train 15+ ML algorithms including XGBoost, Random Forest, and SVM. Automated hyperparameter tuning and cross-validation.
                </div>
                <div class="step-tags">
                    <span class="tag">XGBoost</span>
                    <span class="tag">GridSearch</span>
                    <span class="tag">CV</span>
                </div>
            </div>
            <div class="step-action">
                <a href="?page=04_🤖_Modeling_and_Evaluation" class="action-button">Train</a>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-icon-wrapper">
                <span>🏥</span>
                <div class="step-number-badge">5</div>
            </div>
            <div class="step-content">
                <div class="step-name">Biostatistical Analysis</div>
                <div class="step-description">
                    Cox proportional hazards, survival analysis, Poisson regression for rates, OR/RR/HR calculations with 95% CI and forest plots.
                </div>
                <div class="step-tags">
                    <span class="tag">Cox PH</span>
                    <span class="tag">Survival</span>
                    <span class="tag">Poisson</span>
                </div>
            </div>
            <div class="step-action">
                <a href="?page=04b_🏥_Epidemiological_Models" class="action-button">Analyze</a>
            </div>
        </div>
        
        <div class="process-step">
            <div class="step-icon-wrapper">
                <span>📑</span>
                <div class="step-number-badge">6</div>
            </div>
            <div class="step-content">
                <div class="step-name">Report Generation</div>
                <div class="step-description">
                    Export publication-ready reports with comprehensive statistics, visualizations, and model performance metrics in PDF or HTML.
                </div>
                <div class="step-tags">
                    <span class="tag">PDF</span>
                    <span class="tag">HTML</span>
                    <span class="tag">Charts</span>
                </div>
            </div>
            <div class="step-action">
                <a href="?page=05_📑_Report" class="action-button">Export</a>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== CTA Section =====
st.markdown("""
<div class="cta-wrapper">
    <div class="cta-card">
        <h2 class="cta-heading">Ready to Transform Your Research?</h2>
        <p class="cta-text">
            Start analyzing your epidemiological data with cutting-edge AI tools and biostatistical methods
        </p>
        <a href="?page=01_📂_Upload_and_Schema" class="cta-main-button">
            🚀 Launch Platform
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# ===== Handle Navigation =====
query_params = st.query_params
if "page" in query_params:
    st.switch_page(f"pages/{query_params['page']}.py")
