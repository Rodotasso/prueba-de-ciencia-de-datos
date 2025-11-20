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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Distribution",
    "🔗 Relationships", 
    "📊 Comparisons",
    "🌡️ Heatmaps",
    "📉 Advanced"
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

# Data preview
st.markdown("---")
with st.expander("📋 View Data"):
    st.dataframe(df, use_container_width=True)

chatbot_sidebar()
