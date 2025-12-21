# train_model.py
"""
Train Random Forest model on Seattle weather dataset
with proper feature scaling.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import joblib
from math import sqrt

# 1) Load dataset
df = pd.read_csv("seattle-weather.csv")

print("✅ Data loaded successfully!")
print("Shape:", df.shape)

# 2) Select features & target
target = "temp_max"
features = ["precipitation", "temp_min", "wind"]

df = df.dropna(subset=[target] + features)

X = df[features]
y = df[target]

# 3) Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4) SCALE FEATURES  🔥 (IMPORTANT)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5) Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 6) Evaluate
y_pred = model.predict(X_test_scaled)
rmse = sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f}")
print(f"R² score: {r2:.2f}")

# 7) Save model + scaler
joblib.dump(model, "climate_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model saved as climate_model.pkl")
print("✅ Scaler saved as scaler.pkl")

# 8) Save predictions
pred_df = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
pred_df.to_csv("predictions.csv", index=False)
print("📂 Predictions saved")
