# Climate Prediction using Machine Learning

This project predicts temperature using a machine learning model.
help us to understand machine learning concepts
and deployment using Streamlit.

## Project Objective

The objective of this project is to:
- Train a machine learning model using historical weather data
- Predict temperature based on weather conditions
- Deploy the model using a Streamlit web application

## Machine Learning Details

- Algorithm used: Random Forest Regression
- Input features:
  - Precipitation
  - Minimum Temperature
  - Wind Speed
- Target output:
  - Maximum Temperature
- Feature scaling: StandardScaler

## Project Structure

- app.py : Main Streamlit app for ML prediction
- train_model.py : Script used to train the model
- weather_dashboard.py : Real-time weather dashboard (additional feature)
- climate_model.pkl : Trained machine learning model
- scaler.pkl : Feature scaler
- README.md : Project documentation

## How to Run the Project

1. Install required libraries:
   pip install -r requirements.txt

2. Train the model:
   python train_model.py

3. Run the prediction app:
   streamlit run app.py

## Weather Dashboard

The weather dashboard shows real-time weather information.
This module is for visualization only and does not perform
machine learning predictions.

## Author

Shashank Singh  
B.Tech (CSE / AI-ML)  

