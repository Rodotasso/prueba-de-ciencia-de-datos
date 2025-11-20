import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, GradientBoostingRegressor
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, 
                            mean_squared_error, r2_score, mean_absolute_error, 
                            classification_report, confusion_matrix)
import plotly.graph_objects as go
import plotly.express as px

try:
    from xgboost import XGBClassifier, XGBRegressor
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

from chatbot import chatbot_sidebar

st.session_state["page_name"] = "Modeling and Evaluation"

st.title("🤖 Advanced ML Modeling & Evaluation")

# -------------------------
# Load dataset
# -------------------------
if "dataset" not in st.session_state:
    st.warning("⚠️ Please upload a dataset first.")
    st.stop()

df = st.session_state["dataset"].copy()

# -------------------------
# Configuration
# -------------------------
st.sidebar.markdown("## ⚙️ Model Configuration")

# Target selection
target_col = st.sidebar.selectbox("🎯 Select Target Column:", df.columns)

# Feature selection
all_features = [col for col in df.columns if col != target_col]
selected_features = st.sidebar.multiselect(
    "📊 Select Features:",
    all_features,
    default=all_features
)

# Test size
test_size = st.sidebar.slider("Test Size (%):", 10, 40, 20) / 100

# Random state
random_state = st.sidebar.number_input("Random State:", 0, 100, 42)

if not selected_features:
    st.warning("⚠️ Please select at least one feature.")
    st.stop()

# -------------------------
# Data Preparation
# -------------------------
st.subheader("📋 Data Preparation")

with st.expander("🔍 View Configuration", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Target:** {target_col}")
        st.info(f"**Features:** {len(selected_features)}")
    with col2:
        st.info(f"**Total Samples:** {len(df)}")
        st.info(f"**Train/Test Split:** {int((1-test_size)*100)}/{int(test_size*100)}")

try:
    X = df[selected_features].copy()
    y = df[target_col].copy()
    
    # Handle missing values
    if X.isnull().sum().sum() > 0:
        st.warning(f"⚠️ Found {X.isnull().sum().sum()} missing values. Filling with mean/mode...")
        for col in X.columns:
            if X[col].dtype in ['float64', 'int64']:
                X[col].fillna(X[col].mean(), inplace=True)
            else:
                X[col].fillna(X[col].mode()[0] if len(X[col].mode()) > 0 else 'Unknown', inplace=True)
    
    # Encode categorical features
    categorical_cols = X.select_dtypes(include=['object', 'category']).columns
    if len(categorical_cols) > 0:
        st.info(f"🔄 Encoding {len(categorical_cols)} categorical features...")
        X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)
    
    # Determine problem type
    unique_targets = y.nunique()
    
    if y.dtype == 'object' or y.dtype.name == 'category' or unique_targets <= 10:
        problem_type = "classification"
        st.success(f"✅ **Problem Type:** Classification ({unique_targets} classes)")
    else:
        problem_type = "regression"
        st.success(f"✅ **Problem Type:** Regression")
    
    # Encode target if classification
    if problem_type == "classification":
        le = LabelEncoder()
        y_encoded = le.fit_transform(y)
        st.session_state['label_encoder'] = le
    else:
        y_encoded = y
    
    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=test_size, random_state=random_state
    )
    
    st.success(f"✅ Train set: {len(X_train)} samples | Test set: {len(X_test)} samples")

except Exception as e:
    st.error(f"❌ Error in data preparation: {str(e)}")
    st.stop()

# -------------------------
# Model Selection
# -------------------------
st.markdown("---")
st.subheader("🎯 Model Selection")

if problem_type == "classification":
    available_models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=random_state),
        "Decision Tree": DecisionTreeClassifier(random_state=random_state),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "Support Vector Machine": SVC(random_state=random_state),
        "Gradient Boosting": GradientBoostingClassifier(random_state=random_state),
    }
    
    if XGBOOST_AVAILABLE:
        available_models["XGBoost"] = XGBClassifier(random_state=random_state, eval_metric='logloss')
    
else:  # Regression
    available_models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(),
        "Lasso Regression": Lasso(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=random_state),
        "Decision Tree": DecisionTreeRegressor(random_state=random_state),
        "K-Nearest Neighbors": KNeighborsRegressor(),
        "Support Vector Machine": SVR(),
        "Gradient Boosting": GradientBoostingRegressor(random_state=random_state),
    }
    
    if XGBOOST_AVAILABLE:
        available_models["XGBoost"] = XGBRegressor(random_state=random_state)

selected_models = st.multiselect(
    "Select models to train:",
    list(available_models.keys()),
    default=list(available_models.keys())[:3]
)

# Advanced options
with st.expander("⚙️ Advanced Options"):
    col1, col2 = st.columns(2)
    
    with col1:
        use_scaling = st.checkbox("Standardize Features", value=True)
        use_cv = st.checkbox("Use Cross-Validation", value=True)
    
    with col2:
        cv_folds = st.slider("CV Folds:", 3, 10, 5) if use_cv else 5
        optimize_hyperparams = st.checkbox("Optimize Hyperparameters (slower)", value=False)

# -------------------------
# Train Models
# -------------------------
if st.button("🚀 Train Models", type="primary", use_container_width=True):
    if not selected_models:
        st.warning("⚠️ Please select at least one model.")
    else:
        results = []
        
        # Scale features if needed
        if use_scaling:
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
        else:
            X_train_scaled = X_train
            X_test_scaled = X_test
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for idx, model_name in enumerate(selected_models):
            status_text.text(f"Training {model_name}... ({idx+1}/{len(selected_models)})")
            
            try:
                model = available_models[model_name]
                
                # Hyperparameter optimization
                if optimize_hyperparams and model_name in ["Random Forest", "Gradient Boosting"]:
                    with st.spinner(f"Optimizing {model_name}..."):
                        if problem_type == "classification":
                            param_grid = {
                                'n_estimators': [50, 100, 200],
                                'max_depth': [5, 10, None]
                            }
                        else:
                            param_grid = {
                                'n_estimators': [50, 100, 200],
                                'max_depth': [5, 10, None]
                            }
                        
                        grid_search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1)
                        grid_search.fit(X_train_scaled, y_train)
                        model = grid_search.best_estimator_
                        st.info(f"Best params for {model_name}: {grid_search.best_params_}")
                else:
                    model.fit(X_train_scaled, y_train)
                
                # Predictions
                y_pred = model.predict(X_test_scaled)
                
                # Metrics
                if problem_type == "classification":
                    accuracy = accuracy_score(y_test, y_pred)
                    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
                    
                    # Cross-validation
                    if use_cv:
                        cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv_folds)
                        cv_mean = cv_scores.mean()
                    else:
                        cv_mean = None
                    
                    results.append({
                        'Model': model_name,
                        'Accuracy': accuracy,
                        'Precision': precision,
                        'Recall': recall,
                        'F1-Score': f1,
                        'CV Score': cv_mean,
                        'Predictions': y_pred,
                        'Model Object': model
                    })
                    
                else:  # Regression
                    mse = mean_squared_error(y_test, y_pred)
                    rmse = np.sqrt(mse)
                    mae = mean_absolute_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                    
                    # Cross-validation
                    if use_cv:
                        cv_scores = cross_val_score(model, X_train_scaled, y_train, 
                                                   cv=cv_folds, scoring='r2')
                        cv_mean = cv_scores.mean()
                    else:
                        cv_mean = None
                    
                    results.append({
                        'Model': model_name,
                        'RMSE': rmse,
                        'MAE': mae,
                        'R² Score': r2,
                        'CV Score': cv_mean,
                        'Predictions': y_pred,
                        'Model Object': model
                    })
            
            except Exception as e:
                st.error(f"❌ {model_name} failed: {str(e)}")
            
            progress_bar.progress((idx + 1) / len(selected_models))
        
        status_text.empty()
        progress_bar.empty()
        
        # -------------------------
        # Display Results
        # -------------------------
        if results:
            st.markdown("---")
            st.subheader("📊 Model Results")
            
            # Results table
            results_df = pd.DataFrame(results)
            
            if problem_type == "classification":
                display_cols = ['Model', 'Accuracy', 'Precision', 'Recall', 'F1-Score']
                if use_cv:
                    display_cols.append('CV Score')
                
                results_display = results_df[display_cols].copy()
                results_display = results_display.style.format({
                    col: "{:.4f}" for col in display_cols if col != 'Model'
                }).background_gradient(subset=[col for col in display_cols if col != 'Model'], 
                                      cmap='RdYlGn', vmin=0, vmax=1)
                
                st.dataframe(results_display, use_container_width=True)
                
                # Best model
                best_idx = results_df['Accuracy'].idxmax()
                best_model = results_df.loc[best_idx]
                
                st.success(f"🏆 **Best Model:** {best_model['Model']} with Accuracy = {best_model['Accuracy']:.4f}")
                
                # Confusion Matrix for best model
                st.markdown("#### 🎯 Confusion Matrix (Best Model)")
                cm = confusion_matrix(y_test, best_model['Predictions'])
                
                fig = px.imshow(cm, text_auto=True, aspect="auto",
                              labels=dict(x="Predicted", y="Actual"),
                              title=f"Confusion Matrix - {best_model['Model']}")
                st.plotly_chart(fig, use_container_width=True)
                
            else:  # Regression
                display_cols = ['Model', 'RMSE', 'MAE', 'R² Score']
                if use_cv:
                    display_cols.append('CV Score')
                
                results_display = results_df[display_cols].copy()
                st.dataframe(results_display, use_container_width=True)
                
                # Best model (highest R²)
                best_idx = results_df['R² Score'].idxmax()
                best_model = results_df.loc[best_idx]
                
                st.success(f"🏆 **Best Model:** {best_model['Model']} with R² = {best_model['R² Score']:.4f}")
                
                # Actual vs Predicted plot
                st.markdown("#### 📈 Actual vs Predicted (Best Model)")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=y_test, y=best_model['Predictions'],
                                        mode='markers', name='Predictions'))
                fig.add_trace(go.Scatter(x=[y_test.min(), y_test.max()],
                                        y=[y_test.min(), y_test.max()],
                                        mode='lines', name='Perfect Fit',
                                        line=dict(dash='dash', color='red')))
                fig.update_layout(xaxis_title="Actual", yaxis_title="Predicted",
                                title=f"Actual vs Predicted - {best_model['Model']}")
                st.plotly_chart(fig, use_container_width=True)
            
            # Model comparison chart
            st.markdown("#### 📊 Model Comparison")
            
            if problem_type == "classification":
                fig = go.Figure()
                metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
                for metric in metrics:
                    fig.add_trace(go.Bar(name=metric, x=results_df['Model'], 
                                        y=results_df[metric]))
                fig.update_layout(barmode='group', 
                                title="Classification Metrics Comparison",
                                yaxis_title="Score")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = go.Figure()
                fig.add_trace(go.Bar(name='R² Score', x=results_df['Model'], 
                                    y=results_df['R² Score']))
                fig.update_layout(title="R² Score Comparison",
                                yaxis_title="R² Score")
                st.plotly_chart(fig, use_container_width=True)
            
            # Save to session state
            st.session_state['model_results'] = results
            st.session_state['best_model'] = best_model['Model Object']
            st.session_state['best_model_name'] = best_model['Model']
            st.session_state['best_score'] = best_model['Accuracy'] if problem_type == "classification" else best_model['R² Score']
            st.session_state['problem_type'] = problem_type
            st.session_state['feature_names'] = X.columns.tolist()
            
            st.balloons()

chatbot_sidebar()
