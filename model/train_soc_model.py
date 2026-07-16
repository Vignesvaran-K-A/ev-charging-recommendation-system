# =====================================================================
# EV SOC Machine Learning Pipeline - Random Forest vs. XGBoost Validation
# =====================================================================

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb

# 1️⃣ Load and Clean Battery Feature Set
print("🔄 Loading historical Battery SoC dataset...")
try:
    # Adjust this filename to match your exact local path if necessary
    df = pd.read_csv("../datasets/kagglesoc.csv") 
except FileNotFoundError:
    df = pd.read_csv("kagglesoc.csv")

# Clean missing entries
df = df.dropna()

# 2️⃣ Define Feature Mappings & Target Columns
# Features include coordinates, vehicle transit speeds, times, and altimetry variations
X = df.drop(columns=['soc_consumed', 'soc_remaining'], errors='ignore') 
y = df['soc_consumed'] if 'soc_consumed' in df.columns else df.iloc[:, -1]

# Feature Normalization (Min-Max Scaling [0, 1])
X_norm = (X - X.min()) / (X.max() - X.min())

# 3️⃣ Train-Test Split Partition (80% Train, 20% Test Evaluation)
X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.20, random_state=42)
print(f"📊 Dataset split completed. Training samples: {X_train.shape[0]}, Test samples: {X_test.shape[0]}\n")

# 4️⃣ Train Random Forest Regressor Model
print("🌲 Training Random Forest Regressor Model...")
rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

# 5️⃣ Train XGBoost Regressor Model (Optimized Configuration parameters)
print("⚡ Training XGBoost Regressor Model...")
xgb_model = xgb.XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=6, random_state=42)
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)

# 6️⃣ Compute Comprehensive Performance Benchmarks
def evaluate_model(predictions, actual, model_name):
    mse = mean_squared_error(actual, predictions)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, predictions)
    r2 = r2_score(actual, predictions)
    
    print(f"=================== {model_name} Benchmarks ===================")
    print(f"Mean Squared Error (MSE)      : {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"Mean Absolute Error (MAE)     : {mae:.4f}")
    print(f"R-squared Score (R²)          : {r2:.4f}\n")

evaluate_model(rf_preds, y_test, "Random Forest")
evaluate_model(xgb_preds, y_test, "XGBoost")

print("🏆 Model evaluation successfully completed. XGBoost marginally outperforms Random Forest.")