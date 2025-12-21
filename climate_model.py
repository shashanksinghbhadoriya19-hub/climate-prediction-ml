# -------------------------------
# climate_model.py (for seattle-weather.csv)
# -------------------------------

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

# Step 1: Load the dataset
data = pd.read_csv('seattle-weather.csv')
print("✅ Dataset loaded successfully!")
print(data.head())

# Step 2: Handle missing data (if any)
data = data.dropna()

# Step 3: Define features (inputs) and target (output)
# We'll predict the maximum temperature (temp_max)
X = data[['precipitation', 'temp_min', 'wind']]
y = data['temp_max']

# Step 4: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Step 5: Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)
print("✅ Model training completed!")

# Step 6: Save the trained model
pickle.dump(model, open('climate_model.pkl', 'wb'))
print("✅ Model saved as 'climate_model.pkl'")
