import streamlit as st

st.set_page_config(
    page_title="EpiHealth AI Platform", 
    page_icon="🏥", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CSS Simplificado =====
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background: #0a0e27;
        background-image: 
            radial-gradient(at 47% 33%, hsl(162, 77%, 40%) 0, transparent 59%), 
            radial-gradient(at 82% 65%, hsl(198, 100%, 50%) 0, transparent 55%);
    }
    
    /* Títulos y texto */
    h1, h2, h3 {
        color: white !important;
    }
    
    p, div, span {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Botones personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #22d3ee, #06b6d4) !important;
        color: white !important;
        border: none !important;
        padding: 12px 30px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(34, 211, 238, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(34, 211, 238, 0.5) !important;
    }
    
    /* Cards personalizadas */
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    /* Métricas */
    .stMetric {
        background: rgba(255, 255, 255, 0.05) !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(34, 211, 238, 0.2) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #22d3ee !important;
        font-size: 2em !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ===== Header =====
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <div style='display: inline-block; background: rgba(34, 211, 238, 0.1); 
                        border: 1px solid rgba(34, 211, 238, 0.3); color: #22d3ee; 
                        padding: 8px 20px; border-radius: 30px; font-size: 0.85em; 
                        font-weight: 500; margin-bottom: 20px;'>
                🏥 DOCTORAL-LEVEL PLATFORM
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.title("🏥 EpiHealth AI Platform")
    st.markdown("""
        <div style='text-align: center; font-size: 1.2em; color: rgba(255, 255, 255, 0.7); 
                    margin: 20px auto; max-width: 700px; line-height: 1.6;'>
            Advanced biostatistical analysis and epidemiological modeling powered by artificial intelligence. 
            From data ingestion to publication-ready insights.
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ===== Features =====
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.03); 
                    border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px;'>
            <div style='font-size: 3em;'>⚡</div>
            <div style='color: white; font-size: 1.1em; font-weight: 600; margin: 10px 0;'>Lightning Fast</div>
            <div style='color: rgba(255, 255, 255, 0.6); font-size: 0.9em;'>Process millions of records</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.03); 
                    border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px;'>
            <div style='font-size: 3em;'>🔬</div>
            <div style='color: white; font-size: 1.1em; font-weight: 600; margin: 10px 0;'>PhD-Level Analysis</div>
            <div style='color: rgba(255, 255, 255, 0.6); font-size: 0.9em;'>Cox, Kaplan-Meier, Poisson</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.03); 
                    border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px;'>
            <div style='font-size: 3em;'>🤖</div>
            <div style='color: white; font-size: 1.1em; font-weight: 600; margin: 10px 0;'>AI-Powered</div>
            <div style='color: rgba(255, 255, 255, 0.6); font-size: 0.9em;'>Smart insights with LLM</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(255, 255, 255, 0.03); 
                    border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px;'>
            <div style='font-size: 3em;'>📊</div>
            <div style='color: white; font-size: 1.1em; font-weight: 600; margin: 10px 0;'>Interactive Viz</div>
            <div style='color: rgba(255, 255, 255, 0.6); font-size: 0.9em;'>Forest plots, survival curves</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ===== Workflow Title =====
st.markdown("""
    <div style='text-align: center; margin: 40px 0;'>
        <h2 style='color: white; font-size: 2em; font-weight: 600;'>Complete Analysis Pipeline</h2>
        <p style='color: rgba(255, 255, 255, 0.6);'>6-step workflow from raw data to publication-ready results</p>
    </div>
""", unsafe_allow_html=True)

# ===== Workflow Steps usando componentes nativos =====
steps = [
    {
        "num": "1",
        "icon": "📂",
        "title": "Data Ingestion",
        "desc": "Load multiple epidemiological datasets simultaneously. CSV, Excel, JSON, Parquet.",
        "tags": ["Multi-format", "Batch", "Auto-detect"],
        "page": "01_📂_Upload_and_Schema"
    },
    {
        "num": "2",
        "icon": "🧹",
        "title": "Data Preprocessing",
        "desc": "Advanced cleaning with outlier detection (IQR, Z-score) and intelligent imputation.",
        "tags": ["IQR", "Smart impute", "QC metrics"],
        "page": "02_🧹_Clean_Data"
    },
    {
        "num": "3",
        "icon": "📊",
        "title": "Epidemiological Visualization",
        "desc": "Population pyramids, epidemic curves, survival plots, and interactive dashboards.",
        "tags": ["Plotly", "Kaplan-Meier", "Epi curves"],
        "page": "03_📊_Data_Visualization"
    },
    {
        "num": "4",
        "icon": "🤖",
        "title": "Machine Learning Models",
        "desc": "Train 15+ algorithms including XGBoost with hyperparameter tuning and CV.",
        "tags": ["XGBoost", "GridSearch", "CV"],
        "page": "04_🤖_Modeling_and_Evaluation"
    },
    {
        "num": "5",
        "icon": "🏥",
        "title": "Biostatistical Analysis",
        "desc": "Cox proportional hazards, survival analysis, Poisson regression, OR/RR/HR.",
        "tags": ["Cox PH", "Survival", "Poisson"],
        "page": "04b_🏥_Epidemiological_Models"
    },
    {
        "num": "6",
        "icon": "📑",
        "title": "Report Generation",
        "desc": "Export publication-ready reports with statistics and visualizations in PDF/HTML.",
        "tags": ["PDF", "HTML", "Charts"],
        "page": "05_📑_Report"
    }
]

for step in steps:
    with st.container():
        cols = st.columns([0.5, 2, 1.5, 1])
        
        with cols[0]:
            st.markdown(f"""
                <div style='text-align: center; margin-top: 15px;'>
                    <div style='font-size: 3em;'>{step['icon']}</div>
                    <div style='width: 30px; height: 30px; background: linear-gradient(135deg, #22d3ee, #06b6d4);
                                border-radius: 50%; color: white; font-weight: 700; font-size: 0.9em;
                                display: flex; align-items: center; justify-content: center; margin: 10px auto;
                                box-shadow: 0 4px 12px rgba(34, 211, 238, 0.4);'>
                        {step['num']}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with cols[1]:
            st.markdown(f"### {step['title']}")
            st.markdown(f"<p style='color: rgba(255, 255, 255, 0.6); font-size: 0.95em;'>{step['desc']}</p>", 
                       unsafe_allow_html=True)
        
        with cols[2]:
            tags_html = " ".join([f"""<span style='background: rgba(34, 211, 238, 0.1); 
                                                border: 1px solid rgba(34, 211, 238, 0.3); 
                                                color: #22d3ee; padding: 4px 12px; border-radius: 6px; 
                                                font-size: 0.8em; margin-right: 5px;'>{tag}</span>""" 
                                 for tag in step['tags']])
            st.markdown(f"<div style='margin-top: 20px;'>{tags_html}</div>", unsafe_allow_html=True)
        
        with cols[3]:
            if st.button(f"Open →", key=step['page'], use_container_width=True):
                st.switch_page(f"pages/{step['page']}.py")
        
        st.markdown("<hr style='border: 1px solid rgba(255, 255, 255, 0.1); margin: 20px 0;'>", 
                   unsafe_allow_html=True)

# ===== CTA =====
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <div style='text-align: center; padding: 50px; background: linear-gradient(135deg, rgba(34, 211, 238, 0.1), rgba(6, 182, 212, 0.1));
                    border: 1px solid rgba(34, 211, 238, 0.2); border-radius: 20px;'>
            <h2 style='color: white; font-size: 2em; font-weight: 700; margin-bottom: 15px;'>
                Ready to Transform Your Research?
            </h2>
            <p style='color: rgba(255, 255, 255, 0.7); font-size: 1.1em; margin-bottom: 35px;'>
                Start analyzing your epidemiological data with cutting-edge AI tools
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Platform", use_container_width=True, type="primary"):
        st.switch_page("pages/01_📂_Upload_and_Schema.py")

# ===== Handle Navigation =====
query_params = st.query_params
if "page" in query_params:
    st.switch_page(f"pages/{query_params['page']}.py")
