# AQI Prediction using Machine Learning

## Problem Overview
This project predicts Air Quality Index (AQI) using environmental pollutant data such as PM2.5, PM10, NO2, and SO2.

## Data Source
The dataset was collected from publicly available air quality datasets and processed by computing AQI using CPCB guidelines.

## Models Used
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor (Final Model)

Random Forest was selected due to its superior performance in terms of RMSE and R².

## Steps to Run Streamlit App
1. Install dependencies  
   `pip install streamlit scikit-learn pandas`
2. Run the app  
   `streamlit run app.py`
