import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

from chatbot import chatbot_sidebar

st.session_state["page_name"] = "Clean"

st.title("🧹 Advanced Data Cleaning")

# Check if dataset exists in session_state
if "dataset" not in st.session_state:
    st.warning("⚠️ Please upload a dataset first in the Upload & Schema page.")
    st.stop()

# Load dataset
df = st.session_state["dataset"].copy()

# Show current dataset info
st.subheader("📊 Current Dataset")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Rows", f"{len(df):,}")
with col2:
    st.metric("Columns", len(df.columns))
with col3:
    st.metric("Missing Values", f"{df.isnull().sum().sum():,}")

st.dataframe(df.head(10), use_container_width=True)

st.markdown("---")

# -------------------------
# Cleaning Options
# -------------------------
st.subheader("🔧 Cleaning Operations")

tab1, tab2, tab3, tab4 = st.tabs(["🗑️ Remove Data", "🔄 Handle Missing", "📐 Outliers", "⚙️ Transform"])

with tab1:
    st.markdown("### Remove Unwanted Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.checkbox("Remove Duplicates"):
            before = len(df)
            df = df.drop_duplicates()
            after = len(df)
            st.success(f"✅ Removed {before - after} duplicate rows")
    
    with col2:
        if st.checkbox("Remove Completely Empty Rows"):
            before = len(df)
            df = df.dropna(how='all')
            after = len(df)
            st.success(f"✅ Removed {before - after} empty rows")
    
    # Remove columns
    st.markdown("#### Drop Columns")
    cols_to_drop = st.multiselect(
        "Select columns to remove:",
        df.columns.tolist(),
        key="drop_cols"
    )
    if cols_to_drop and st.button("🗑️ Drop Selected Columns"):
        df = df.drop(columns=cols_to_drop)
        st.success(f"✅ Dropped {len(cols_to_drop)} column(s)")

with tab2:
    st.markdown("### Handle Missing Values")
    
    # Show missing values summary
    missing_summary = pd.DataFrame({
        'Column': df.columns,
        'Missing': df.isnull().sum().values,
        'Percentage': (df.isnull().sum().values / len(df) * 100).round(2)
    })
    missing_summary = missing_summary[missing_summary['Missing'] > 0]
    
    if len(missing_summary) > 0:
        st.dataframe(missing_summary, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.checkbox("Drop All Missing Values"):
                before = len(df)
                df = df.dropna()
                after = len(df)
                st.success(f"✅ Removed {before - after} rows with missing values")
        
        with col2:
            threshold = st.slider("Drop rows with missing threshold %", 0, 100, 50)
            if st.button(f"Drop rows with >{threshold}% missing"):
                threshold_count = len(df.columns) * (threshold / 100)
                before = len(df)
                df = df.dropna(thresh=len(df.columns) - threshold_count)
                after = len(df)
                st.success(f"✅ Removed {before - after} rows")
        
        st.markdown("#### Smart Imputation")
        
        impute_col = st.selectbox("Select column to impute:", missing_summary['Column'].tolist())
        
        if impute_col:
            col_type = df[impute_col].dtype
            
            if pd.api.types.is_numeric_dtype(df[impute_col]):
                impute_method = st.radio(
                    "Imputation method:",
                    ["Mean", "Median", "Mode", "Forward Fill", "Backward Fill", "Interpolate"],
                    key="numeric_impute"
                )
                
                if st.button(f"Apply {impute_method} Imputation"):
                    if impute_method == "Mean":
                        df[impute_col].fillna(df[impute_col].mean(), inplace=True)
                    elif impute_method == "Median":
                        df[impute_col].fillna(df[impute_col].median(), inplace=True)
                    elif impute_method == "Mode":
                        df[impute_col].fillna(df[impute_col].mode()[0], inplace=True)
                    elif impute_method == "Forward Fill":
                        df[impute_col].fillna(method='ffill', inplace=True)
                    elif impute_method == "Backward Fill":
                        df[impute_col].fillna(method='bfill', inplace=True)
                    elif impute_method == "Interpolate":
                        df[impute_col] = df[impute_col].interpolate()
                    
                    st.success(f"✅ Applied {impute_method} imputation to {impute_col}")
                    st.rerun()
            else:
                impute_method = st.radio(
                    "Imputation method:",
                    ["Mode", "Forward Fill", "Backward Fill", "Custom Value"],
                    key="cat_impute"
                )
                
                if impute_method == "Custom Value":
                    custom_value = st.text_input("Enter custom value:")
                    if st.button("Apply Custom Value"):
                        df[impute_col].fillna(custom_value, inplace=True)
                        st.success(f"✅ Filled {impute_col} with '{custom_value}'")
                        st.rerun()
                else:
                    if st.button(f"Apply {impute_method}"):
                        if impute_method == "Mode":
                            df[impute_col].fillna(df[impute_col].mode()[0], inplace=True)
                        elif impute_method == "Forward Fill":
                            df[impute_col].fillna(method='ffill', inplace=True)
                        elif impute_method == "Backward Fill":
                            df[impute_col].fillna(method='bfill', inplace=True)
                        
                        st.success(f"✅ Applied {impute_method} to {impute_col}")
                        st.rerun()
    else:
        st.success("✅ No missing values found!")

with tab3:
    st.markdown("### Detect and Handle Outliers")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        outlier_col = st.selectbox("Select numeric column:", numeric_cols, key="outlier_col")
        
        method = st.radio("Detection method:", ["IQR Method", "Z-Score Method"], key="outlier_method")
        
        if method == "IQR Method":
            Q1 = df[outlier_col].quantile(0.25)
            Q3 = df[outlier_col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[outlier_col] < lower_bound) | (df[outlier_col] > upper_bound)]
            
            st.info(f"📊 Range: [{lower_bound:.2f}, {upper_bound:.2f}]")
            st.warning(f"⚠️ Found {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")
            
        else:  # Z-Score
            z_threshold = st.slider("Z-score threshold:", 2.0, 4.0, 3.0, 0.5)
            z_scores = np.abs(stats.zscore(df[outlier_col].dropna()))
            outliers = df[np.abs(stats.zscore(df[outlier_col].fillna(df[outlier_col].mean()))) > z_threshold]
            
            st.warning(f"⚠️ Found {len(outliers)} outliers ({len(outliers)/len(df)*100:.1f}%)")
        
        if len(outliers) > 0:
            action = st.radio("Action:", ["Remove Outliers", "Cap Outliers (Winsorize)", "Do Nothing"])
            
            if action == "Remove Outliers" and st.button("🗑️ Remove Outliers"):
                before = len(df)
                if method == "IQR Method":
                    df = df[(df[outlier_col] >= lower_bound) & (df[outlier_col] <= upper_bound)]
                else:
                    df = df[np.abs(stats.zscore(df[outlier_col].fillna(df[outlier_col].mean()))) <= z_threshold]
                after = len(df)
                st.success(f"✅ Removed {before - after} outlier rows")
                st.rerun()
                
            elif action == "Cap Outliers (Winsorize)" and st.button("📌 Cap Outliers"):
                if method == "IQR Method":
                    df[outlier_col] = df[outlier_col].clip(lower=lower_bound, upper=upper_bound)
                else:
                    mean = df[outlier_col].mean()
                    std = df[outlier_col].std()
                    df[outlier_col] = df[outlier_col].clip(lower=mean - z_threshold*std, upper=mean + z_threshold*std)
                st.success(f"✅ Capped outliers in {outlier_col}")
                st.rerun()
    else:
        st.info("No numeric columns found for outlier detection")

with tab4:
    st.markdown("### Transform Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.checkbox("Standardize Column Names"):
            df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
            st.success("✅ Standardized column names")
    
    with col2:
        if st.checkbox("Remove Leading/Trailing Spaces"):
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.strip() if df[col].dtype == 'object' else df[col]
            st.success("✅ Trimmed string columns")
    
    st.markdown("#### Convert Data Types")
    type_col = st.selectbox("Select column:", df.columns.tolist(), key="type_col")
    new_type = st.selectbox("Convert to:", ["int", "float", "string", "datetime", "category"])
    
    if st.button("🔄 Convert Type"):
        try:
            if new_type == "int":
                df[type_col] = pd.to_numeric(df[type_col], errors='coerce').astype('Int64')
            elif new_type == "float":
                df[type_col] = pd.to_numeric(df[type_col], errors='coerce')
            elif new_type == "string":
                df[type_col] = df[type_col].astype(str)
            elif new_type == "datetime":
                df[type_col] = pd.to_datetime(df[type_col], errors='coerce')
            elif new_type == "category":
                df[type_col] = df[type_col].astype('category')
            
            st.success(f"✅ Converted {type_col} to {new_type}")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Conversion failed: {str(e)}")

# -------------------------
# Save Cleaned Data
# -------------------------
st.markdown("---")
st.subheader("💾 Save Changes")

col1, col2 = st.columns(2)

with col1:
    if st.button("✅ Save Cleaned Dataset", use_container_width=True):
        st.session_state["dataset"] = df
        st.session_state["datasets"][st.session_state["uploaded_filename"]] = df
        st.success("✅ Cleaned dataset saved! This version will be used in the next steps.")
        st.balloons()

with col2:
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="cleaned_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

# Preview
st.subheader("👀 Current Preview")
st.dataframe(df.head(20), use_container_width=True)

# Statistics
with st.expander("📈 Quick Statistics"):
    st.dataframe(df.describe(), use_container_width=True)

chatbot_sidebar()
