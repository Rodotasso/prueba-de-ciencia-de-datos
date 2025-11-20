import streamlit as st
import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test
import statsmodels.api as sm
from statsmodels.genmod.families import Poisson, Binomial
from sklearn.model_selection import train_test_split
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

from chatbot import chatbot_sidebar

st.session_state["page_name"] = "Epidemiological Models"

st.title("🏥 Advanced Epidemiological & Biostatistical Models")

# -------------------------
# Load dataset
# -------------------------
if "dataset" not in st.session_state:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state["dataset"].copy()

# -------------------------
# Model Selection
# -------------------------
st.sidebar.markdown("## 📋 Model Type")

model_type = st.sidebar.selectbox(
    "Select Analysis Type:",
    [
        "Survival Analysis (Kaplan-Meier)",
        "Cox Proportional Hazards",
        "Poisson Regression (Incidence Rates)",
        "Logistic Regression (Odds Ratios)",
        "Risk Ratios & Relative Risk",
        "Standardized Mortality Ratio (SMR)",
        "Epidemic Curve Analysis"
    ]
)

st.markdown("---")

# ========================
# SURVIVAL ANALYSIS
# ========================
if model_type == "Survival Analysis (Kaplan-Meier)":
    st.subheader("⏱️ Kaplan-Meier Survival Analysis")
    
    st.info("""
    **Kaplan-Meier Estimator**: Non-parametric statistic to estimate survival probability over time.
    Commonly used in clinical trials and cohort studies.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        duration_col = st.selectbox("⏰ Time-to-Event Column:", df.columns)
    with col2:
        event_col = st.selectbox("🎯 Event Indicator (1=event, 0=censored):", df.columns)
    with col3:
        group_col = st.selectbox("👥 Grouping Variable (optional):", ["None"] + df.columns.tolist())
    
    if st.button("🚀 Run Kaplan-Meier Analysis", type="primary"):
        try:
            kmf = KaplanMeierFitter()
            
            if group_col != "None":
                # Stratified analysis
                fig = go.Figure()
                groups = df[group_col].unique()
                
                logrank_results = []
                
                for group in groups:
                    mask = df[group_col] == group
                    kmf.fit(df.loc[mask, duration_col], 
                           df.loc[mask, event_col],
                           label=str(group))
                    
                    # Add survival curve
                    fig.add_trace(go.Scatter(
                        x=kmf.survival_function_.index,
                        y=kmf.survival_function_[str(group)],
                        mode='lines',
                        name=f'{group_col}={group}',
                        line=dict(width=2)
                    ))
                
                # Log-rank test
                if len(groups) == 2:
                    group1 = df[df[group_col] == groups[0]]
                    group2 = df[df[group_col] == groups[1]]
                    
                    results = logrank_test(
                        group1[duration_col], group2[duration_col],
                        group1[event_col], group2[event_col]
                    )
                    
                    st.success(f"**Log-Rank Test**")
                    st.metric("p-value", f"{results.p_value:.4f}")
                    st.metric("Test Statistic", f"{results.test_statistic:.4f}")
                    
                    if results.p_value < 0.05:
                        st.warning("⚠️ Significant difference in survival between groups (p < 0.05)")
                    else:
                        st.info("✓ No significant difference in survival between groups")
                
                fig.update_layout(
                    title=f"Kaplan-Meier Survival Curves by {group_col}",
                    xaxis_title=f"Time ({duration_col})",
                    yaxis_title="Survival Probability",
                    hovermode='x unified'
                )
                
            else:
                # Single curve
                kmf.fit(df[duration_col], df[event_col])
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=kmf.survival_function_.index,
                    y=kmf.survival_function_['KM_estimate'],
                    mode='lines',
                    name='Survival Function',
                    line=dict(width=2, color='blue')
                ))
                
                # Confidence intervals
                fig.add_trace(go.Scatter(
                    x=kmf.confidence_interval_.index,
                    y=kmf.confidence_interval_['KM_estimate_upper_0.95'],
                    mode='lines',
                    name='95% CI Upper',
                    line=dict(width=0),
                    showlegend=False
                ))
                
                fig.add_trace(go.Scatter(
                    x=kmf.confidence_interval_.index,
                    y=kmf.confidence_interval_['KM_estimate_lower_0.95'],
                    mode='lines',
                    name='95% CI',
                    fill='tonexty',
                    line=dict(width=0)
                ))
                
                fig.update_layout(
                    title="Kaplan-Meier Survival Curve",
                    xaxis_title=f"Time ({duration_col})",
                    yaxis_title="Survival Probability"
                )
                
                # Summary statistics
                st.markdown("#### 📊 Summary Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Median Survival Time", f"{kmf.median_survival_time_:.2f}")
                with col2:
                    total_events = df[event_col].sum()
                    st.metric("Total Events", f"{int(total_events)}")
                with col3:
                    censored = len(df) - total_events
                    st.metric("Censored", f"{int(censored)}")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Save to session state
            st.session_state['survival_results'] = {
                'kmf': kmf,
                'duration_col': duration_col,
                'event_col': event_col
            }
            
        except Exception as e:
            st.error(f"❌ Error in analysis: {str(e)}")

# ========================
# COX PROPORTIONAL HAZARDS
# ========================
elif model_type == "Cox Proportional Hazards":
    st.subheader("📈 Cox Proportional Hazards Model")
    
    st.info("""
    **Cox PH Model**: Semi-parametric model for survival analysis. 
    Estimates hazard ratios (HR) and adjusts for covariates. HR > 1 indicates increased hazard.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        duration_col = st.selectbox("⏰ Time-to-Event Column:", df.columns)
    with col2:
        event_col = st.selectbox("🎯 Event Indicator:", df.columns)
    
    covariates = st.multiselect(
        "📊 Select Covariates (independent variables):",
        [col for col in df.columns if col not in [duration_col, event_col]]
    )
    
    if st.button("🚀 Run Cox PH Model", type="primary"):
        if not covariates:
            st.warning("⚠️ Please select at least one covariate.")
        else:
            try:
                # Prepare data
                cox_df = df[[duration_col, event_col] + covariates].copy()
                
                # Handle categorical variables
                categorical_cols = cox_df[covariates].select_dtypes(include=['object', 'category']).columns
                if len(categorical_cols) > 0:
                    cox_df = pd.get_dummies(cox_df, columns=categorical_cols, drop_first=True)
                
                # Remove missing values
                cox_df = cox_df.dropna()
                
                # Fit Cox model
                cph = CoxPHFitter()
                cph.fit(cox_df, duration_col=duration_col, event_col=event_col)
                
                # Display summary
                st.markdown("#### 📋 Cox PH Model Results")
                
                results_df = cph.summary
                results_df['HR'] = np.exp(results_df['coef'])
                results_df['HR_95%_Lower'] = np.exp(results_df['coef lower 95%'])
                results_df['HR_95%_Upper'] = np.exp(results_df['coef upper 95%'])
                
                display_df = results_df[['coef', 'HR', 'HR_95%_Lower', 'HR_95%_Upper', 'p']].copy()
                display_df.columns = ['Coefficient', 'Hazard Ratio', 'HR 95% CI Lower', 'HR 95% CI Upper', 'p-value']
                
                st.dataframe(display_df.style.format({
                    'Coefficient': '{:.4f}',
                    'Hazard Ratio': '{:.4f}',
                    'HR 95% CI Lower': '{:.4f}',
                    'HR 95% CI Upper': '{:.4f}',
                    'p-value': '{:.4f}'
                }), use_container_width=True)
                
                # Interpretation
                st.markdown("#### 🔍 Interpretation")
                for var in display_df.index:
                    hr = display_df.loc[var, 'Hazard Ratio']
                    p_val = display_df.loc[var, 'p-value']
                    
                    if p_val < 0.05:
                        if hr > 1:
                            pct_increase = (hr - 1) * 100
                            st.warning(f"**{var}**: HR = {hr:.2f} (p={p_val:.4f}) - {pct_increase:.1f}% **increased** hazard")
                        else:
                            pct_decrease = (1 - hr) * 100
                            st.success(f"**{var}**: HR = {hr:.2f} (p={p_val:.4f}) - {pct_decrease:.1f}% **decreased** hazard (protective)")
                    else:
                        st.info(f"**{var}**: HR = {hr:.2f} (p={p_val:.4f}) - Not statistically significant")
                
                # Forest plot
                st.markdown("#### 🌲 Forest Plot (Hazard Ratios)")
                
                fig = go.Figure()
                
                y_pos = list(range(len(display_df)))
                
                # Add confidence intervals
                for i, var in enumerate(display_df.index):
                    fig.add_trace(go.Scatter(
                        x=[display_df.loc[var, 'HR 95% CI Lower'], display_df.loc[var, 'HR 95% CI Upper']],
                        y=[i, i],
                        mode='lines',
                        line=dict(color='gray', width=2),
                        showlegend=False
                    ))
                
                # Add point estimates
                fig.add_trace(go.Scatter(
                    x=display_df['Hazard Ratio'],
                    y=y_pos,
                    mode='markers',
                    marker=dict(size=10, color='blue'),
                    name='Hazard Ratio',
                    text=[f"HR: {hr:.2f}" for hr in display_df['Hazard Ratio']],
                    hovertemplate='%{text}<br>%{x:.2f}<extra></extra>'
                ))
                
                # Add reference line at HR=1
                fig.add_vline(x=1, line_dash="dash", line_color="red", annotation_text="HR=1 (No effect)")
                
                fig.update_layout(
                    title="Hazard Ratios with 95% Confidence Intervals",
                    xaxis_title="Hazard Ratio (log scale)",
                    yaxis=dict(
                        tickmode='array',
                        tickvals=y_pos,
                        ticktext=display_df.index
                    ),
                    xaxis_type="log",
                    height=max(400, len(display_df) * 50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Model diagnostics
                st.markdown("#### 🔬 Model Diagnostics")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Concordance Index", f"{cph.concordance_index_:.4f}")
                    st.caption("Values > 0.5 indicate predictive ability (0.7-0.8 is good)")
                
                with col2:
                    st.metric("Log-Likelihood", f"{cph.log_likelihood_:.2f}")
                
                # Save to session state
                st.session_state['cox_model'] = cph
                
            except Exception as e:
                st.error(f"❌ Error in Cox model: {str(e)}")

# ========================
# POISSON REGRESSION
# ========================
elif model_type == "Poisson Regression (Incidence Rates)":
    st.subheader("📊 Poisson Regression for Incidence Rates")
    
    st.info("""
    **Poisson Regression**: Used for modeling count data and incidence rates.
    Commonly applied to disease counts, hospitalization rates, and mortality data.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        count_col = st.selectbox("🎯 Count/Cases Column:", df.columns)
    with col2:
        exposure_col = st.selectbox("👥 Exposure/Person-Time Column (optional):", ["None"] + df.columns.tolist())
    
    predictors = st.multiselect(
        "📊 Select Predictor Variables:",
        [col for col in df.columns if col not in [count_col, exposure_col]]
    )
    
    if st.button("🚀 Run Poisson Regression", type="primary"):
        if not predictors:
            st.warning("⚠️ Please select at least one predictor.")
        else:
            try:
                # Prepare data
                model_df = df[[count_col] + predictors].copy()
                
                # Handle categorical variables
                categorical_cols = model_df[predictors].select_dtypes(include=['object', 'category']).columns
                if len(categorical_cols) > 0:
                    model_df = pd.get_dummies(model_df, columns=categorical_cols, drop_first=True)
                
                model_df = model_df.dropna()
                
                y = model_df[count_col]
                X = model_df.drop(columns=[count_col])
                X = sm.add_constant(X)
                
                # Add exposure if provided
                if exposure_col != "None":
                    exposure = df.loc[model_df.index, exposure_col]
                    poisson_model = sm.GLM(y, X, family=Poisson(), exposure=exposure)
                else:
                    poisson_model = sm.GLM(y, X, family=Poisson())
                
                results = poisson_model.fit()
                
                # Display results
                st.markdown("#### 📋 Poisson Regression Results")
                
                # Extract coefficients
                coef_df = pd.DataFrame({
                    'Coefficient': results.params,
                    'Std Error': results.bse,
                    'z-value': results.tvalues,
                    'p-value': results.pvalues,
                    'IRR': np.exp(results.params),  # Incidence Rate Ratio
                    'IRR_95%_Lower': np.exp(results.conf_int()[0]),
                    'IRR_95%_Upper': np.exp(results.conf_int()[1])
                })
                
                st.dataframe(coef_df.style.format({
                    'Coefficient': '{:.4f}',
                    'Std Error': '{:.4f}',
                    'z-value': '{:.4f}',
                    'p-value': '{:.4f}',
                    'IRR': '{:.4f}',
                    'IRR_95%_Lower': '{:.4f}',
                    'IRR_95%_Upper': '{:.4f}'
                }), use_container_width=True)
                
                # Interpretation
                st.markdown("#### 🔍 Interpretation (Incidence Rate Ratios)")
                for var in coef_df.index[1:]:  # Skip intercept
                    irr = coef_df.loc[var, 'IRR']
                    p_val = coef_df.loc[var, 'p-value']
                    
                    if p_val < 0.05:
                        if irr > 1:
                            pct_increase = (irr - 1) * 100
                            st.warning(f"**{var}**: IRR = {irr:.2f} (p={p_val:.4f}) - {pct_increase:.1f}% **higher** incidence rate")
                        else:
                            pct_decrease = (1 - irr) * 100
                            st.success(f"**{var}**: IRR = {irr:.2f} (p={p_val:.4f}) - {pct_decrease:.1f}% **lower** incidence rate")
                    else:
                        st.info(f"**{var}**: IRR = {irr:.2f} (p={p_val:.4f}) - Not statistically significant")
                
                # Model fit statistics
                st.markdown("#### 🔬 Model Fit Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("AIC", f"{results.aic:.2f}")
                with col2:
                    st.metric("BIC", f"{results.bic:.2f}")
                with col3:
                    st.metric("Deviance", f"{results.deviance:.2f}")
                
                # Save to session state
                st.session_state['poisson_model'] = results
                
            except Exception as e:
                st.error(f"❌ Error in Poisson regression: {str(e)}")

# ========================
# ODDS RATIOS (LOGISTIC)
# ========================
elif model_type == "Logistic Regression (Odds Ratios)":
    st.subheader("🎲 Logistic Regression for Odds Ratios")
    
    st.info("""
    **Logistic Regression for Case-Control Studies**: Estimates odds ratios (OR).
    OR > 1 indicates increased odds of outcome, OR < 1 indicates decreased odds (protective).
    """)
    
    outcome_col = st.selectbox("🎯 Binary Outcome (disease/case):", df.columns)
    
    predictors = st.multiselect(
        "📊 Select Exposure/Risk Factors:",
        [col for col in df.columns if col != outcome_col]
    )
    
    if st.button("🚀 Calculate Odds Ratios", type="primary"):
        if not predictors:
            st.warning("⚠️ Please select at least one predictor.")
        else:
            try:
                # Prepare data
                model_df = df[[outcome_col] + predictors].copy()
                
                # Handle categorical variables
                categorical_cols = model_df[predictors].select_dtypes(include=['object', 'category']).columns
                if len(categorical_cols) > 0:
                    model_df = pd.get_dummies(model_df, columns=categorical_cols, drop_first=True)
                
                model_df = model_df.dropna()
                
                y = model_df[outcome_col]
                X = model_df.drop(columns=[outcome_col])
                X = sm.add_constant(X)
                
                # Fit logistic regression
                logit_model = sm.GLM(y, X, family=Binomial())
                results = logit_model.fit()
                
                # Display results
                st.markdown("#### 📋 Odds Ratios")
                
                or_df = pd.DataFrame({
                    'Coefficient': results.params,
                    'Odds Ratio': np.exp(results.params),
                    'OR_95%_Lower': np.exp(results.conf_int()[0]),
                    'OR_95%_Upper': np.exp(results.conf_int()[1]),
                    'p-value': results.pvalues
                })
                
                st.dataframe(or_df.style.format({
                    'Coefficient': '{:.4f}',
                    'Odds Ratio': '{:.4f}',
                    'OR_95%_Lower': '{:.4f}',
                    'OR_95%_Upper': '{:.4f}',
                    'p-value': '{:.4f}'
                }), use_container_width=True)
                
                # Clinical interpretation
                st.markdown("#### 🔍 Clinical Interpretation")
                for var in or_df.index[1:]:  # Skip intercept
                    odds_ratio = or_df.loc[var, 'Odds Ratio']
                    p_val = or_df.loc[var, 'p-value']
                    ci_lower = or_df.loc[var, 'OR_95%_Lower']
                    ci_upper = or_df.loc[var, 'OR_95%_Upper']
                    
                    if p_val < 0.05:
                        if odds_ratio > 1:
                            st.warning(f"**{var}**: OR = {odds_ratio:.2f} (95% CI: {ci_lower:.2f}-{ci_upper:.2f}) - **Risk factor** for {outcome_col}")
                        else:
                            st.success(f"**{var}**: OR = {odds_ratio:.2f} (95% CI: {ci_lower:.2f}-{ci_upper:.2f}) - **Protective** against {outcome_col}")
                    else:
                        st.info(f"**{var}**: OR = {odds_ratio:.2f} (95% CI: {ci_lower:.2f}-{ci_upper:.2f}) - Not significant (p={p_val:.4f})")
                
                # Forest plot
                st.markdown("#### 🌲 Forest Plot (Odds Ratios)")
                
                fig = go.Figure()
                
                plot_df = or_df[1:]  # Exclude intercept
                y_pos = list(range(len(plot_df)))
                
                # Confidence intervals
                for i, var in enumerate(plot_df.index):
                    fig.add_trace(go.Scatter(
                        x=[plot_df.loc[var, 'OR_95%_Lower'], plot_df.loc[var, 'OR_95%_Upper']],
                        y=[i, i],
                        mode='lines',
                        line=dict(color='gray', width=2),
                        showlegend=False
                    ))
                
                # Point estimates
                fig.add_trace(go.Scatter(
                    x=plot_df['Odds Ratio'],
                    y=y_pos,
                    mode='markers',
                    marker=dict(size=10, color='darkblue'),
                    name='Odds Ratio'
                ))
                
                # Reference line at OR=1
                fig.add_vline(x=1, line_dash="dash", line_color="red", annotation_text="OR=1 (No effect)")
                
                fig.update_layout(
                    title="Odds Ratios with 95% Confidence Intervals",
                    xaxis_title="Odds Ratio (log scale)",
                    xaxis_type="log",
                    yaxis=dict(
                        tickmode='array',
                        tickvals=y_pos,
                        ticktext=plot_df.index
                    ),
                    height=max(400, len(plot_df) * 50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Model performance
                st.markdown("#### 📊 Model Performance")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("AIC", f"{results.aic:.2f}")
                with col2:
                    st.metric("Log-Likelihood", f"{results.llf:.2f}")
                
            except Exception as e:
                st.error(f"❌ Error in analysis: {str(e)}")

# ========================
# RISK RATIOS
# ========================
elif model_type == "Risk Ratios & Relative Risk":
    st.subheader("⚖️ Risk Ratios & Relative Risk Analysis")
    
    st.info("""
    **Risk Ratio (RR) / Relative Risk**: The ratio of the probability of an event occurring in the exposed group versus unexposed.
    RR > 1 indicates increased risk, RR < 1 indicates decreased risk.
    Used in cohort studies and RCTs.
    """)
    
    outcome_col = st.selectbox("🎯 Binary Outcome (disease/event):", df.columns)
    exposure_col = st.selectbox("📊 Binary Exposure:", [col for col in df.columns if col != outcome_col])
    
    if st.button("🚀 Calculate Risk Ratios", type="primary"):
        try:
            # Create 2x2 contingency table
            contingency_table = pd.crosstab(df[exposure_col], df[outcome_col])
            
            st.markdown("#### 📋 2x2 Contingency Table")
            st.dataframe(contingency_table, use_container_width=True)
            
            # Extract values
            if contingency_table.shape == (2, 2):
                a = contingency_table.iloc[1, 1]  # Exposed + Diseased
                b = contingency_table.iloc[1, 0]  # Exposed + Not diseased
                c = contingency_table.iloc[0, 1]  # Unexposed + Diseased
                d = contingency_table.iloc[0, 0]  # Unexposed + Not diseased
                
                # Calculate risk in each group
                risk_exposed = a / (a + b)
                risk_unexposed = c / (c + d)
                
                # Risk Ratio
                risk_ratio = risk_exposed / risk_unexposed
                
                # Odds Ratio (for comparison)
                odds_ratio = (a * d) / (b * c)
                
                # Confidence intervals (using log method)
                se_log_rr = np.sqrt((1/a) - (1/(a+b)) + (1/c) - (1/(c+d)))
                rr_ci_lower = np.exp(np.log(risk_ratio) - 1.96 * se_log_rr)
                rr_ci_upper = np.exp(np.log(risk_ratio) + 1.96 * se_log_rr)
                
                # Attributable risk
                attributable_risk = risk_exposed - risk_unexposed
                attributable_risk_pct = (attributable_risk / risk_exposed) * 100
                
                # Population attributable risk
                overall_disease = (a + c) / (a + b + c + d)
                par = overall_disease - risk_unexposed
                par_pct = (par / overall_disease) * 100
                
                # Display results
                st.markdown("#### 📊 Risk Measures")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Risk in Exposed", f"{risk_exposed:.4f}")
                    st.caption(f"{risk_exposed*100:.2f}%")
                
                with col2:
                    st.metric("Risk in Unexposed", f"{risk_unexposed:.4f}")
                    st.caption(f"{risk_unexposed*100:.2f}%")
                
                with col3:
                    st.metric("Attributable Risk", f"{attributable_risk:.4f}")
                    st.caption(f"AR% = {attributable_risk_pct:.1f}%")
                
                st.markdown("---")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("##### 🎯 Risk Ratio (RR)")
                    st.metric("RR", f"{risk_ratio:.4f}")
                    st.caption(f"95% CI: [{rr_ci_lower:.4f}, {rr_ci_upper:.4f}]")
                    
                    if risk_ratio > 1:
                        increase_pct = (risk_ratio - 1) * 100
                        st.warning(f"Exposed group has **{increase_pct:.1f}% higher risk**")
                    elif risk_ratio < 1:
                        decrease_pct = (1 - risk_ratio) * 100
                        st.success(f"Exposed group has **{decrease_pct:.1f}% lower risk** (protective)")
                    else:
                        st.info("No difference in risk between groups")
                
                with col2:
                    st.markdown("##### 🎲 Odds Ratio (OR)")
                    st.metric("OR", f"{odds_ratio:.4f}")
                    st.caption("For comparison (case-control)")
                
                # Population Attributable Risk
                st.markdown("#### 🌍 Population Attributable Risk (PAR)")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("PAR", f"{par:.4f}")
                with col2:
                    st.metric("PAR %", f"{par_pct:.2f}%")
                
                st.info(f"**Interpretation**: {par_pct:.1f}% of {outcome_col} cases in the population can be attributed to {exposure_col}")
                
                # Chi-square test
                chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
                
                st.markdown("#### 🔬 Statistical Significance")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Chi-square", f"{chi2:.4f}")
                with col2:
                    st.metric("p-value", f"{p_value:.4f}")
                
                if p_value < 0.05:
                    st.success("✓ Association is statistically significant (p < 0.05)")
                else:
                    st.info("No statistically significant association (p ≥ 0.05)")
                
            else:
                st.error("⚠️ Both exposure and outcome must be binary (2 categories each)")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ========================
# SMR (Standardized Mortality Ratio)
# ========================
elif model_type == "Standardized Mortality Ratio (SMR)":
    st.subheader("📈 Standardized Mortality Ratio (SMR)")
    
    st.info("""
    **SMR**: Compares observed deaths in a study population to expected deaths based on a reference population.
    SMR > 1 indicates higher mortality than expected, SMR < 1 indicates lower mortality.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        observed_col = st.selectbox("🎯 Observed Deaths:", df.columns)
    with col2:
        expected_col = st.selectbox("📊 Expected Deaths:", [col for col in df.columns if col != observed_col])
    
    strata_col = st.selectbox("👥 Stratification Variable (optional):", ["None"] + [col for col in df.columns if col not in [observed_col, expected_col]])
    
    if st.button("🚀 Calculate SMR", type="primary"):
        try:
            if strata_col != "None":
                # Stratified analysis
                smr_results = []
                
                for stratum in df[strata_col].unique():
                    subset = df[df[strata_col] == stratum]
                    observed = subset[observed_col].sum()
                    expected = subset[expected_col].sum()
                    smr = observed / expected if expected > 0 else np.nan
                    
                    # Confidence interval (Poisson approximation)
                    ci_lower = (observed / expected) * np.exp(-1.96 / np.sqrt(observed)) if observed > 0 else 0
                    ci_upper = (observed / expected) * np.exp(1.96 / np.sqrt(observed)) if observed > 0 else 0
                    
                    smr_results.append({
                        'Stratum': stratum,
                        'Observed': observed,
                        'Expected': expected,
                        'SMR': smr,
                        'CI_Lower': ci_lower,
                        'CI_Upper': ci_upper
                    })
                
                smr_df = pd.DataFrame(smr_results)
                
                st.markdown("#### 📊 Stratified SMR Results")
                st.dataframe(smr_df.style.format({
                    'Observed': '{:.0f}',
                    'Expected': '{:.2f}',
                    'SMR': '{:.4f}',
                    'CI_Lower': '{:.4f}',
                    'CI_Upper': '{:.4f}'
                }), use_container_width=True)
                
                # Visualization
                fig = go.Figure()
                
                y_pos = list(range(len(smr_df)))
                
                # CI lines
                for i, row in smr_df.iterrows():
                    fig.add_trace(go.Scatter(
                        x=[row['CI_Lower'], row['CI_Upper']],
                        y=[i, i],
                        mode='lines',
                        line=dict(color='gray', width=2),
                        showlegend=False
                    ))
                
                # SMR points
                fig.add_trace(go.Scatter(
                    x=smr_df['SMR'],
                    y=y_pos,
                    mode='markers',
                    marker=dict(size=12, color='red'),
                    name='SMR'
                ))
                
                # Reference line at SMR=1
                fig.add_vline(x=1, line_dash="dash", line_color="green", annotation_text="SMR=1 (Expected)")
                
                fig.update_layout(
                    title="Standardized Mortality Ratios with 95% CI",
                    xaxis_title="SMR",
                    yaxis=dict(
                        tickmode='array',
                        tickvals=y_pos,
                        ticktext=smr_df['Stratum']
                    ),
                    height=max(400, len(smr_df) * 50)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                # Overall SMR
                observed_total = df[observed_col].sum()
                expected_total = df[expected_col].sum()
                smr = observed_total / expected_total
                
                # Confidence interval
                ci_lower = smr * np.exp(-1.96 / np.sqrt(observed_total))
                ci_upper = smr * np.exp(1.96 / np.sqrt(observed_total))
                
                st.markdown("#### 📊 Overall SMR")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Observed Deaths", f"{observed_total:.0f}")
                with col2:
                    st.metric("Expected Deaths", f"{expected_total:.2f}")
                with col3:
                    st.metric("SMR", f"{smr:.4f}")
                
                st.caption(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
                
                if smr > 1:
                    excess = ((smr - 1) * 100)
                    st.warning(f"⚠️ Mortality is **{excess:.1f}% higher** than expected")
                elif smr < 1:
                    reduction = ((1 - smr) * 100)
                    st.success(f"✓ Mortality is **{reduction:.1f}% lower** than expected")
                else:
                    st.info("Mortality matches expected rate")
                
                # Statistical test
                if ci_lower > 1:
                    st.error("🔴 Significantly **higher** mortality (CI excludes 1)")
                elif ci_upper < 1:
                    st.success("🟢 Significantly **lower** mortality (CI excludes 1)")
                else:
                    st.info("🟡 Not significantly different from expected (CI includes 1)")
                    
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# ========================
# EPIDEMIC CURVE
# ========================
elif model_type == "Epidemic Curve Analysis":
    st.subheader("📈 Epidemic Curve (Epi Curve) Analysis")
    
    st.info("""
    **Epidemic Curve**: Visual representation of disease cases over time.
    Used in outbreak investigations to identify patterns, mode of transmission, and intervention impact.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        date_col = st.selectbox("📅 Date Column:", df.columns)
    with col2:
        case_col = st.selectbox("📊 Case Count (optional):", ["None"] + df.columns.tolist())
    
    group_by_col = st.selectbox("👥 Group By (optional):", ["None"] + [col for col in df.columns if col not in [date_col, case_col]])
    
    time_unit = st.radio("⏰ Time Unit:", ["Day", "Week", "Month"], horizontal=True)
    
    if st.button("🚀 Generate Epidemic Curve", type="primary"):
        try:
            # Convert to datetime
            df_epi = df.copy()
            df_epi[date_col] = pd.to_datetime(df_epi[date_col])
            
            # Group by time unit
            if time_unit == "Day":
                df_epi['time_period'] = df_epi[date_col].dt.date
            elif time_unit == "Week":
                df_epi['time_period'] = df_epi[date_col].dt.to_period('W').apply(lambda r: r.start_time)
            else:  # Month
                df_epi['time_period'] = df_epi[date_col].dt.to_period('M').apply(lambda r: r.start_time)
            
            # Aggregate cases
            if case_col != "None":
                if group_by_col != "None":
                    epi_data = df_epi.groupby(['time_period', group_by_col])[case_col].sum().reset_index()
                    
                    fig = px.bar(epi_data, x='time_period', y=case_col, color=group_by_col,
                                title=f"Epidemic Curve by {time_unit} (Grouped by {group_by_col})",
                                labels={'time_period': f'{time_unit}', case_col: 'Number of Cases'})
                else:
                    epi_data = df_epi.groupby('time_period')[case_col].sum().reset_index()
                    
                    fig = px.bar(epi_data, x='time_period', y=case_col,
                                title=f"Epidemic Curve by {time_unit}",
                                labels={'time_period': f'{time_unit}', case_col: 'Number of Cases'})
            else:
                # Count rows as cases
                if group_by_col != "None":
                    epi_data = df_epi.groupby(['time_period', group_by_col]).size().reset_index(name='cases')
                    
                    fig = px.bar(epi_data, x='time_period', y='cases', color=group_by_col,
                                title=f"Epidemic Curve by {time_unit} (Grouped by {group_by_col})",
                                labels={'time_period': f'{time_unit}', 'cases': 'Number of Cases'})
                else:
                    epi_data = df_epi.groupby('time_period').size().reset_index(name='cases')
                    
                    fig = px.bar(epi_data, x='time_period', y='cases',
                                title=f"Epidemic Curve by {time_unit}",
                                labels={'time_period': f'{time_unit}', 'cases': 'Number of Cases'})
            
            fig.update_layout(
                xaxis_title=f"Date ({time_unit})",
                yaxis_title="Number of Cases",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Summary statistics
            st.markdown("#### 📊 Outbreak Summary")
            
            total_cases = epi_data['cases'].sum() if 'cases' in epi_data.columns else epi_data[case_col].sum()
            peak_date = epi_data.loc[epi_data[['cases', case_col][0 if 'cases' in epi_data.columns else 1]].idxmax(), 'time_period']
            peak_cases = epi_data[['cases', case_col][0 if 'cases' in epi_data.columns else 1]].max()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Cases", f"{total_cases:.0f}")
            with col2:
                st.metric("Peak Date", str(peak_date)[:10])
            with col3:
                st.metric("Peak Cases", f"{peak_cases:.0f}")
            
            # Epidemiological interpretation
            st.markdown("#### 🔍 Pattern Interpretation")
            
            # Calculate growth rate
            if len(epi_data) > 1:
                case_series = epi_data['cases'] if 'cases' in epi_data.columns else epi_data[case_col]
                
                # Simple classification
                first_half = case_series[:len(case_series)//2].mean()
                second_half = case_series[len(case_series)//2:].mean()
                
                if second_half > first_half * 1.2:
                    st.warning("📈 **Increasing trend**: Cases are rising. Outbreak may be accelerating.")
                elif second_half < first_half * 0.8:
                    st.success("📉 **Decreasing trend**: Cases are declining. Outbreak may be under control.")
                else:
                    st.info("↔️ **Stable/Plateau**: Cases are relatively stable.")
                
                # Check for single vs continuous source
                peak_idx = case_series.idxmax()
                total_duration = len(case_series)
                
                if peak_idx < total_duration * 0.3:
                    st.info("🎯 **Pattern suggests**: Possible **point-source** outbreak (early peak)")
                elif peak_idx > total_duration * 0.7:
                    st.info("📡 **Pattern suggests**: Possible **propagated** outbreak (late peak)")
                else:
                    st.info("🌊 **Pattern suggests**: Could be **continuous common source** outbreak")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

chatbot_sidebar()
