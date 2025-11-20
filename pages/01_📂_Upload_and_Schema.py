import streamlit as st
import pandas as pd
import json
from io import StringIO

from chatbot import chatbot_sidebar

st.title("📂 Upload & Schema")

# Initialize session state for datasets
if "datasets" not in st.session_state:
    st.session_state["datasets"] = {}

st.markdown("""
### 🎯 Supported Formats
Upload one or multiple files:
- **CSV** (.csv)
- **Excel** (.xlsx, .xls)
- **JSON** (.json)
- **Parquet** (.parquet)
""")

# Multi-file uploader
uploaded_files = st.file_uploader(
    "📤 Upload your data files (drag multiple files or click to browse)",
    type=["csv", "xlsx", "xls", "json", "parquet"],
    accept_multiple_files=True
)

def load_file(file):
    """Load file based on extension with error handling"""
    try:
        file_extension = file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            # Try different encodings
            try:
                df = pd.read_csv(file)
            except UnicodeDecodeError:
                file.seek(0)
                df = pd.read_csv(file, encoding='latin-1')
            return df, None
            
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(file, engine='openpyxl' if file_extension == 'xlsx' else 'xlrd')
            return df, None
            
        elif file_extension == 'json':
            file.seek(0)
            content = file.read()
            data = json.loads(content)
            
            # Handle different JSON structures
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                # Try to convert dict to DataFrame
                try:
                    df = pd.DataFrame(data)
                except:
                    df = pd.DataFrame([data])
            else:
                return None, "Unsupported JSON structure"
            return df, None
            
        elif file_extension == 'parquet':
            df = pd.read_parquet(file)
            return df, None
            
        else:
            return None, f"Unsupported file type: {file_extension}"
            
    except Exception as e:
        return None, f"Error loading file: {str(e)}"

if uploaded_files:
    st.markdown("---")
    st.subheader("📊 Loaded Datasets")
    
    success_count = 0
    error_count = 0
    
    for uploaded_file in uploaded_files:
        with st.expander(f"📄 {uploaded_file.name}", expanded=True):
            df, error = load_file(uploaded_file)
            
            if error:
                st.error(f"❌ {error}")
                error_count += 1
            else:
                # Store dataset
                st.session_state["datasets"][uploaded_file.name] = df
                st.session_state["dataset"] = df  # Set as current dataset
                st.session_state["uploaded_filename"] = uploaded_file.name
                
                success_count += 1
                
                # Display info
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Rows", f"{len(df):,}")
                with col2:
                    st.metric("Columns", len(df.columns))
                with col3:
                    st.metric("Missing Values", f"{df.isnull().sum().sum():,}")
                with col4:
                    file_size = uploaded_file.size / 1024  # KB
                    st.metric("Size", f"{file_size:.1f} KB")
                
                # Data preview
                st.markdown("**Preview (first 10 rows):**")
                st.dataframe(df.head(10), use_container_width=True)
                
                # Schema info
                st.markdown("**Schema:**")
                schema_df = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.astype(str),
                    'Non-Null': df.count().values,
                    'Null': df.isnull().sum().values,
                    'Unique': [df[col].nunique() for col in df.columns]
                })
                st.dataframe(schema_df, use_container_width=True)
    
    # Summary
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.success(f"✅ Successfully loaded: {success_count} file(s)")
    with col2:
        if error_count > 0:
            st.error(f"❌ Failed to load: {error_count} file(s)")

    # Dataset selector if multiple files
    if len(st.session_state["datasets"]) > 1:
        st.markdown("---")
        st.subheader("🎯 Select Active Dataset")
        st.info("💡 Select which dataset to use for cleaning, visualization, and modeling:")
        
        dataset_names = list(st.session_state["datasets"].keys())
        selected_dataset = st.selectbox(
            "Active dataset:",
            dataset_names,
            index=dataset_names.index(st.session_state["uploaded_filename"]) if st.session_state["uploaded_filename"] in dataset_names else 0
        )
        
        if st.button("✅ Set as Active Dataset"):
            st.session_state["dataset"] = st.session_state["datasets"][selected_dataset]
            st.session_state["uploaded_filename"] = selected_dataset
            st.success(f"✅ Active dataset set to: **{selected_dataset}**")
            st.rerun()

else:
    st.info("👆 Upload one or more data files to get started!")
    
    # Example
    st.markdown("---")
    st.markdown("### 📘 Tips")
    st.markdown("""
    - **Multiple files**: Upload multiple datasets to compare or analyze separately
    - **Large files**: Files up to 200MB are supported
    - **Encoding**: CSV files with special characters are automatically handled
    - **JSON**: Supports both array and object structures
    """)

# Chatbot sidebar
chatbot_sidebar()
