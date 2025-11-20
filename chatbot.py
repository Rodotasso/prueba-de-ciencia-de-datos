import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def chatbot_sidebar():
    st.sidebar.markdown("## 🏥 Chat with AI Epidemiologist!")

    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.sidebar.error("⚠️ GROQ_API_KEY not found!")
        st.sidebar.info("📝 Add your API key to .env file. See .env.example for template.")
        st.sidebar.markdown("[Get free API key →](https://console.groq.com/keys)")
        return

    if "dataset" not in st.session_state or "datasets" not in st.session_state:
        st.sidebar.warning("⚠️ Please upload a dataset first.")
        return

    # Dataset selector if multiple datasets exist
    if len(st.session_state.get("datasets", {})) > 1:
        st.sidebar.markdown("### 📂 Select Dataset")
        dataset_names = list(st.session_state["datasets"].keys())
        selected_dataset = st.sidebar.selectbox(
            "Choose dataset for chat:",
            dataset_names,
            key="chatbot_dataset_selector"
        )
        df = st.session_state["datasets"][selected_dataset]
        st.sidebar.caption(f"Chatting about: **{selected_dataset}**")
    else:
        df = st.session_state["dataset"]

    try:
        # Initialize LLM with error handling
        model_name = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        llm = ChatGroq(
            model=model_name,
            api_key=api_key,
            temperature=0
        )

        user_input = st.sidebar.text_area("💬 Ask me about your dataset:", height=100)
        
        if st.sidebar.button("🚀 Send", use_container_width=True):
            if user_input.strip():
                with st.sidebar.spinner("🤔 Thinking..."):
                    try:
                        # Get basic stats
                        stats = {
                            "rows": len(df),
                            "columns": len(df.columns),
                            "missing": df.isnull().sum().sum(),
                            "numeric_cols": df.select_dtypes(include=['number']).columns.tolist(),
                            "categorical_cols": df.select_dtypes(exclude=['number']).columns.tolist()
                        }
                        
                        prompt = f"""
You are an expert epidemiologist and biostatistician with a PhD in Public Health. Your expertise includes:
- Advanced epidemiological methods (cohort studies, case-control studies, RCTs)
- Survival analysis (Kaplan-Meier, Cox proportional hazards)
- Disease surveillance and outbreak investigation
- Statistical inference in public health contexts
- Risk assessment (OR, RR, HR, PAR)
- Population health metrics (incidence, prevalence, mortality rates)

Analyze this epidemiological/health dataset:

**Dataset Stats:**
- Observations: {stats['rows']}
- Variables: {stats['columns']}
- Missing values: {stats['missing']}
- Quantitative variables: {', '.join(stats['numeric_cols'][:10])}
- Categorical variables: {', '.join(stats['categorical_cols'][:10])}

**Data Preview (first 5 rows):**
{df.head(5).to_string()}

**Variable types:**
{df.dtypes.to_string()}

**Research Question:** {user_input}

Provide a rigorous epidemiological analysis. Include:
1. Appropriate statistical methods for this question
2. Key epidemiological considerations (confounders, bias, causality)
3. Specific metrics or analyses recommended (e.g., incidence rates, survival curves, risk ratios)
4. Interpretation in public health context

Use doctoral-level technical language and cite relevant epidemiological principles.
"""

                        response = llm.invoke(prompt)
                        st.sidebar.success("✅ Response:")
                        st.sidebar.write(response.content.strip())

                    except Exception as e:
                        st.sidebar.error(f"❌ Error generating response: {str(e)}")
                        if "rate limit" in str(e).lower():
                            st.sidebar.info("⏱️ Rate limit reached. Please wait a moment and try again.")
            else:
                st.sidebar.warning("Please enter a question first.")

    except Exception as e:
        st.sidebar.error(f"❌ Failed to initialize chatbot: {str(e)}")
        st.sidebar.info("💡 Make sure your GROQ_API_KEY is valid.")
