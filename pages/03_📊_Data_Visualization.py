import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from chatbot import chatbot_sidebar

st.session_state["page_name"] = "Data Visualization"

st.title("📊 Interactive Data Visualization")

if "dataset" not in st.session_state:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state["dataset"]

# Dataset info
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Rows", f"{df.shape[0]:,}")
with col2:
    st.metric("Columns", df.shape[1])
with col3:
    num_cols = df.select_dtypes(include=["int64", "float64", "int32", "float32"]).columns.tolist()
    st.metric("Numeric", len(num_cols))
with col4:
    cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    st.metric("Categorical", len(cat_cols))

st.markdown("---")

# Tabs for different visualizations
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Distribution",
    "🔗 Relationships", 
    "📊 Comparisons",
    "🌡️ Heatmaps",
    "📉 Advanced",
    "🏥 Epidemiological"
])

with tab1:
    st.subheader("📈 Distribution Analysis")
    
    if num_cols:
        col = st.selectbox("Select numeric column:", num_cols, key="dist_col")
        
        viz_type = st.radio("Visualization type:", 
                           ["Histogram", "Box Plot", "Violin Plot", "Distribution Curve"],
                           horizontal=True)
        
        if viz_type == "Histogram":
            bins = st.slider("Number of bins:", 10, 100, 30)
            fig = px.histogram(df, x=col, nbins=bins, 
                              title=f"Distribution of {col}",
                              marginal="box")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Box Plot":
            fig = px.box(df, y=col, title=f"Box Plot of {col}",
                        points="outliers")
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Violin Plot":
            fig = px.violin(df, y=col, box=True, title=f"Violin Plot of {col}")
            st.plotly_chart(fig, use_container_width=True)
            
        elif viz_type == "Distribution Curve":
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=df[col], name="Histogram", 
                                       opacity=0.7, histnorm='probability density'))
            
            # Add KDE line
            from scipy import stats
            kde = stats.gaussian_kde(df[col].dropna())
            x_range = np.linspace(df[col].min(), df[col].max(), 100)
            fig.add_trace(go.Scatter(x=x_range, y=kde(x_range), 
                                    mode='lines', name='KDE', 
                                    line=dict(width=3)))
            
            fig.update_layout(title=f"Distribution of {col}", 
                            xaxis_title=col, yaxis_title="Density")
            st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        with st.expander("📊 Statistics"):
            stats_df = df[col].describe().to_frame()
            st.dataframe(stats_df, use_container_width=True)
    else:
        st.info("No numeric columns available")

with tab2:
    st.subheader("🔗 Relationship Analysis")
    
    if len(num_cols) >= 2:
        col1_rel, col2_rel = st.columns(2)
        
        with col1_rel:
            x_col = st.selectbox("X-axis:", num_cols, key="x_rel")
        with col2_rel:
            y_col = st.selectbox("Y-axis:", [c for c in num_cols if c != x_col], key="y_rel")
        
        # Optional color
        color_col = st.selectbox("Color by (optional):", [None] + cat_cols, key="color_rel")
        
        # Optional size
        size_col = st.selectbox("Size by (optional):", [None] + num_cols, key="size_rel")
        
        plot_type = st.radio("Plot type:", ["Scatter", "Line", "Scatter + Trend"], horizontal=True)
        
        if plot_type == "Scatter":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, size=size_col,
                           title=f"{y_col} vs {x_col}",
                           hover_data=df.columns[:5])
            st.plotly_chart(fig, use_container_width=True)
            
        elif plot_type == "Line":
            fig = px.line(df, x=x_col, y=y_col, color=color_col,
                         title=f"{y_col} vs {x_col}")
            st.plotly_chart(fig, use_container_width=True)
            
        elif plot_type == "Scatter + Trend":
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                           trendline="ols", 
                           title=f"{y_col} vs {x_col} (with trend)")
            st.plotly_chart(fig, use_container_width=True)
            
            # Show correlation
            corr = df[[x_col, y_col]].corr().iloc[0, 1]
            st.metric("Correlation", f"{corr:.3f}")
    else:
        st.info("Need at least 2 numeric columns for relationship analysis")

with tab3:
    st.subheader("📊 Comparison Analysis")
    
    if cat_cols and num_cols:
        col1_cmp, col2_cmp = st.columns(2)
        
        with col1_cmp:
            cat_col = st.selectbox("Category column:", cat_cols, key="cat_cmp")
        with col2_cmp:
            num_col = st.selectbox("Value column:", num_cols, key="num_cmp")
        
        plot_type = st.radio("Chart type:", 
                           ["Bar Chart", "Box Plot by Category", "Violin Plot by Category"],
                           horizontal=True)
        
        if plot_type == "Bar Chart":
            agg_func = st.selectbox("Aggregation:", ["mean", "sum", "median", "count"])
            
            if agg_func == "count":
                fig = px.histogram(df, x=cat_col, title=f"Count by {cat_col}")
            else:
                agg_df = df.groupby(cat_col)[num_col].agg(agg_func).reset_index()
                fig = px.bar(agg_df, x=cat_col, y=num_col,
                           title=f"{agg_func.title()} of {num_col} by {cat_col}")
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif plot_type == "Box Plot by Category":
            fig = px.box(df, x=cat_col, y=num_col, 
                        title=f"{num_col} distribution by {cat_col}",
                        points="outliers")
            st.plotly_chart(fig, use_container_width=True)
            
        elif plot_type == "Violin Plot by Category":
            fig = px.violin(df, x=cat_col, y=num_col, box=True,
                          title=f"{num_col} distribution by {cat_col}")
            st.plotly_chart(fig, use_container_width=True)
    
    elif cat_cols:
        st.markdown("#### Categorical Distribution")
        cat_col = st.selectbox("Select category:", cat_cols, key="cat_only")
        
        plot_type = st.radio("Chart type:", ["Bar Chart", "Pie Chart"], horizontal=True)
        
        value_counts = df[cat_col].value_counts()
        
        if plot_type == "Bar Chart":
            fig = px.bar(x=value_counts.index, y=value_counts.values,
                        labels={'x': cat_col, 'y': 'Count'},
                        title=f"Distribution of {cat_col}")
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig = px.pie(values=value_counts.values, names=value_counts.index,
                        title=f"Distribution of {cat_col}")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Need categorical and numeric columns for comparison")

with tab4:
    st.subheader("🌡️ Correlation Analysis")
    
    if len(num_cols) > 1:
        # Correlation matrix
        corr_matrix = df[num_cols].corr()
        
        viz_type = st.radio("Visualization:", ["Heatmap", "Clustermap"], horizontal=True)
        
        if viz_type == "Heatmap":
            fig = px.imshow(corr_matrix, 
                          text_auto='.2f',
                          aspect="auto",
                          color_continuous_scale='RdBu_r',
                          title="Correlation Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        else:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.clustermap(corr_matrix, annot=True, cmap="coolwarm", center=0,
                          fmt='.2f', linewidths=0.5)
            st.pyplot(plt.gcf())
        
        # Top correlations
        st.markdown("#### 🔝 Top Correlations")
        
        # Get upper triangle of correlation matrix
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool), k=1)
        corr_pairs = corr_matrix.where(mask).stack().reset_index()
        corr_pairs.columns = ['Variable 1', 'Variable 2', 'Correlation']
        corr_pairs['Abs Correlation'] = corr_pairs['Correlation'].abs()
        corr_pairs = corr_pairs.sort_values('Abs Correlation', ascending=False).head(10)
        
        st.dataframe(corr_pairs[['Variable 1', 'Variable 2', 'Correlation']], 
                    use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns for correlation analysis")

with tab5:
    st.subheader("📉 Advanced Visualizations")
    
    viz_choice = st.selectbox("Select visualization:", 
                             ["Pair Plot", "3D Scatter", "Parallel Coordinates", "Sunburst"])
    
    if viz_choice == "Pair Plot":
        if len(num_cols) >= 2:
            cols_to_plot = st.multiselect("Select columns (max 5):", num_cols, 
                                         default=num_cols[:min(3, len(num_cols))])
            
            if len(cols_to_plot) >= 2 and len(cols_to_plot) <= 5:
                color_by = st.selectbox("Color by:", [None] + cat_cols, key="pair_color")
                
                if st.button("Generate Pair Plot"):
                    with st.spinner("Creating pair plot..."):
                        fig = px.scatter_matrix(df, dimensions=cols_to_plot, color=color_by,
                                              title="Pair Plot")
                        fig.update_traces(diagonal_visible=False)
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Please select 2-5 columns")
        else:
            st.info("Need at least 2 numeric columns")
    
    elif viz_choice == "3D Scatter":
        if len(num_cols) >= 3:
            col1, col2, col3 = st.columns(3)
            with col1:
                x_col = st.selectbox("X-axis:", num_cols, key="3d_x")
            with col2:
                y_col = st.selectbox("Y-axis:", [c for c in num_cols if c != x_col], key="3d_y")
            with col3:
                z_col = st.selectbox("Z-axis:", [c for c in num_cols if c not in [x_col, y_col]], key="3d_z")
            
            color_by = st.selectbox("Color by:", [None] + cat_cols + num_cols, key="3d_color")
            
            fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col, color=color_by,
                              title="3D Scatter Plot")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 3 numeric columns for 3D scatter")
    
    elif viz_choice == "Parallel Coordinates":
        if len(num_cols) >= 2:
            cols_to_plot = st.multiselect("Select columns:", num_cols,
                                         default=num_cols[:min(4, len(num_cols))],
                                         key="parallel_cols")
            color_by = st.selectbox("Color by:", cat_cols + num_cols, key="parallel_color")
            
            if len(cols_to_plot) >= 2:
                fig = px.parallel_coordinates(df, dimensions=cols_to_plot,
                                            color=color_by,
                                            title="Parallel Coordinates Plot")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns")
    
    elif viz_choice == "Sunburst":
        if len(cat_cols) >= 2:
            path_cols = st.multiselect("Select hierarchy (in order):", cat_cols,
                                      default=cat_cols[:min(3, len(cat_cols))],
                                      key="sunburst_path")
            
            if len(path_cols) >= 2:
                fig = px.sunburst(df, path=path_cols, title="Sunburst Chart")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 categorical columns for sunburst")

with tab6:
    st.subheader("🏥 Epidemiological Visualizations")
    
    epi_viz = st.selectbox("Select epidemiological visualization:", [
        "Population Pyramid",
        "Age-Adjusted Rates",
        "Incidence/Prevalence Trends",
        "Survival Curve",
        "Geographical Heat Map",
        "2x2 Contingency Analysis"
    ])
    
    if epi_viz == "Population Pyramid":
        st.info("**Population Pyramid**: Visualize age and sex distribution of a population")
        
        age_col = st.selectbox("Age column:", df.columns, key="pyram_age")
        sex_col = st.selectbox("Sex/Gender column:", df.columns, key="pyram_sex")
        
        if st.button("Generate Pyramid"):
            try:
                # Group by age and sex
                pyramid_data = df.groupby([age_col, sex_col]).size().reset_index(name='count')
                
                # Create pyramid
                fig = go.Figure()
                
                for sex in pyramid_data[sex_col].unique():
                    sex_data = pyramid_data[pyramid_data[sex_col] == sex]
                    values = sex_data['count'].values
                    
                    # Make one side negative for pyramid effect
                    if sex == pyramid_data[sex_col].unique()[0]:
                        values = -values
                    
                    fig.add_trace(go.Bar(
                        y=sex_data[age_col],
                        x=values,
                        name=str(sex),
                        orientation='h'
                    ))
                
                fig.update_layout(
                    title="Population Pyramid",
                    barmode='overlay',
                    bargap=0.1,
                    xaxis=dict(title='Population'),
                    yaxis=dict(title='Age'),
                    height=600
                )
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif epi_viz == "Age-Adjusted Rates":
        st.info("**Age-Adjusted Rates**: Standardize rates across different age groups")
        
        age_col = st.selectbox("Age group column:", df.columns, key="age_adj_age")
        rate_col = st.selectbox("Rate/Count column:", num_cols, key="age_adj_rate")
        pop_col = st.selectbox("Population column:", num_cols, key="age_adj_pop")
        
        if st.button("Calculate Age-Adjusted Rate"):
            try:
                # Calculate crude rates per age group
                rates = df.groupby(age_col).apply(
                    lambda x: (x[rate_col].sum() / x[pop_col].sum()) * 100000
                ).reset_index(name='crude_rate')
                
                fig = px.bar(rates, x=age_col, y='crude_rate',
                           title="Age-Specific Rates (per 100,000)",
                           labels={'crude_rate': 'Rate per 100,000'})
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display table
                st.dataframe(rates.style.format({'crude_rate': '{:.2f}'}),
                           use_container_width=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif epi_viz == "Incidence/Prevalence Trends":
        st.info("**Disease Trends**: Visualize temporal patterns of disease occurrence")
        
        date_col = st.selectbox("Date column:", df.columns, key="trend_date")
        case_col = st.selectbox("Case count column (optional):", ["Count rows"] + num_cols, key="trend_cases")
        
        time_unit = st.radio("Aggregate by:", ["Day", "Week", "Month", "Year"], horizontal=True)
        
        if st.button("Generate Trend"):
            try:
                df_trend = df.copy()
                df_trend[date_col] = pd.to_datetime(df_trend[date_col])
                
                # Aggregate by time unit
                if time_unit == "Day":
                    df_trend['period'] = df_trend[date_col].dt.date
                elif time_unit == "Week":
                    df_trend['period'] = df_trend[date_col].dt.to_period('W').apply(lambda r: r.start_time)
                elif time_unit == "Month":
                    df_trend['period'] = df_trend[date_col].dt.to_period('M').apply(lambda r: r.start_time)
                else:  # Year
                    df_trend['period'] = df_trend[date_col].dt.year
                
                if case_col == "Count rows":
                    trend_data = df_trend.groupby('period').size().reset_index(name='cases')
                else:
                    trend_data = df_trend.groupby('period')[case_col].sum().reset_index(name='cases')
                
                fig = go.Figure()
                
                # Add line chart
                fig.add_trace(go.Scatter(
                    x=trend_data['period'],
                    y=trend_data['cases'],
                    mode='lines+markers',
                    name='Cases',
                    line=dict(width=2, color='red')
                ))
                
                # Add moving average
                if len(trend_data) > 7:
                    trend_data['ma7'] = trend_data['cases'].rolling(window=7, center=True).mean()
                    fig.add_trace(go.Scatter(
                        x=trend_data['period'],
                        y=trend_data['ma7'],
                        mode='lines',
                        name='7-period MA',
                        line=dict(width=3, dash='dash', color='blue')
                    ))
                
                fig.update_layout(
                    title=f"Disease Incidence Trend by {time_unit}",
                    xaxis_title="Time Period",
                    yaxis_title="Number of Cases",
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Summary stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Cases", f"{trend_data['cases'].sum():.0f}")
                with col2:
                    st.metric("Peak Cases", f"{trend_data['cases'].max():.0f}")
                with col3:
                    st.metric("Average per Period", f"{trend_data['cases'].mean():.1f}")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif epi_viz == "Survival Curve":
        st.info("**Kaplan-Meier Survival**: Visualize survival probability over time")
        
        time_col = st.selectbox("Time-to-event column:", num_cols, key="surv_time")
        event_col = st.selectbox("Event indicator (1=event, 0=censored):", df.columns, key="surv_event")
        group_col = st.selectbox("Group by (optional):", ["None"] + cat_cols, key="surv_group")
        
        if st.button("Generate Survival Curve"):
            try:
                from lifelines import KaplanMeierFitter
                
                kmf = KaplanMeierFitter()
                fig = go.Figure()
                
                if group_col != "None":
                    for group in df[group_col].unique():
                        mask = df[group_col] == group
                        kmf.fit(df.loc[mask, time_col], 
                               df.loc[mask, event_col],
                               label=str(group))
                        
                        fig.add_trace(go.Scatter(
                            x=kmf.survival_function_.index,
                            y=kmf.survival_function_[str(group)],
                            mode='lines',
                            name=f'{group}',
                            line=dict(width=2)
                        ))
                else:
                    kmf.fit(df[time_col], df[event_col])
                    
                    fig.add_trace(go.Scatter(
                        x=kmf.survival_function_.index,
                        y=kmf.survival_function_['KM_estimate'],
                        mode='lines',
                        name='Survival',
                        line=dict(width=2, color='blue')
                    ))
                
                fig.update_layout(
                    title="Kaplan-Meier Survival Curve",
                    xaxis_title="Time",
                    yaxis_title="Survival Probability",
                    yaxis_range=[0, 1]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.success(f"Median survival time: {kmf.median_survival_time_:.2f}")
                
            except ImportError:
                st.error("❌ Install 'lifelines' package: pip install lifelines")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif epi_viz == "Geographical Heat Map":
        st.info("**Geographic Distribution**: Map disease prevalence or incidence by region")
        
        region_col = st.selectbox("Region/Location column:", df.columns, key="geo_region")
        value_col = st.selectbox("Value to map:", num_cols, key="geo_value")
        
        agg_func = st.radio("Aggregation:", ["Sum", "Mean", "Count"], horizontal=True)
        
        if st.button("Generate Heat Map"):
            try:
                if agg_func == "Sum":
                    geo_data = df.groupby(region_col)[value_col].sum().reset_index()
                elif agg_func == "Mean":
                    geo_data = df.groupby(region_col)[value_col].mean().reset_index()
                else:  # Count
                    geo_data = df.groupby(region_col).size().reset_index(name=value_col)
                
                fig = px.bar(geo_data, x=region_col, y=value_col,
                           title=f"{agg_func} of {value_col} by {region_col}",
                           color=value_col,
                           color_continuous_scale='Reds')
                
                fig.update_layout(xaxis={'categoryorder':'total descending'})
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show high-risk areas
                top_5 = geo_data.nlargest(5, value_col)
                st.markdown("##### 🔴 Top 5 High-Risk Areas")
                st.dataframe(top_5, use_container_width=True)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif epi_viz == "2x2 Contingency Analysis":
        st.info("**2x2 Table**: Analyze association between exposure and outcome")
        
        exposure_col = st.selectbox("Exposure variable (binary):", df.columns, key="cont_exp")
        outcome_col = st.selectbox("Outcome variable (binary):", df.columns, key="cont_out")
        
        if st.button("Analyze Association"):
            try:
                from scipy import stats
                
                # Create contingency table
                cont_table = pd.crosstab(df[exposure_col], df[outcome_col])
                
                st.markdown("##### 📋 Contingency Table")
                st.dataframe(cont_table, use_container_width=True)
                
                if cont_table.shape == (2, 2):
                    a = cont_table.iloc[1, 1]  # Exposed + Diseased
                    b = cont_table.iloc[1, 0]  # Exposed + Not diseased
                    c = cont_table.iloc[0, 1]  # Unexposed + Diseased
                    d = cont_table.iloc[0, 0]  # Unexposed + Not diseased
                    
                    # Calculate measures
                    risk_exposed = a / (a + b)
                    risk_unexposed = c / (c + d)
                    risk_ratio = risk_exposed / risk_unexposed
                    odds_ratio = (a * d) / (b * c)
                    
                    # Chi-square test
                    chi2, p_value, dof, expected = stats.chi2_contingency(cont_table)
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Risk Ratio", f"{risk_ratio:.3f}")
                        st.caption("RR > 1: Increased risk")
                    
                    with col2:
                        st.metric("Odds Ratio", f"{odds_ratio:.3f}")
                        st.caption("OR > 1: Increased odds")
                    
                    with col3:
                        st.metric("Chi² p-value", f"{p_value:.4f}")
                        if p_value < 0.05:
                            st.caption("✓ Significant")
                        else:
                            st.caption("Not significant")
                    
                    # Visualization
                    fig = px.imshow(cont_table, text_auto=True, aspect="auto",
                                  labels=dict(x=outcome_col, y=exposure_col),
                                  title="Contingency Table Heatmap",
                                  color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
                    
                else:
                    st.warning("⚠️ Variables must be binary (2 categories each)")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Data preview
st.markdown("---")
with st.expander("📋 View Data"):
    st.dataframe(df, use_container_width=True)

chatbot_sidebar()
