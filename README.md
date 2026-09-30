# ⚡ PJM Energy Consumption Forecasting

### Machine Learning Based 30-Day Hourly Electricity Demand Forecasting

---

## 🔗 Project Links

🌐 **Live Streamlit Application:**  
https://pjm-energy-consumption-forecasting-ilvbysnospmklqinhj2psn.streamlit.app/


📓 **Jupyter Notebook:**  
`PJM_Energy_Forecasting.ipynb`

💻 **GitHub Repository:**  
https://github.com/adarsh-552/pjm-energy-consumption-forecasting

---

## 📌 Project Overview

This project focuses on forecasting **hourly electricity demand** using historical PJM energy consumption data.

The project follows an end-to-end machine learning workflow including data preprocessing, exploratory data analysis, time-series feature engineering, model development, model evaluation, final forecasting and Streamlit deployment.

Multiple forecasting approaches were evaluated, including statistical forecasting methods and gradient boosting models such as **XGBoost and LightGBM**.

Based on the evaluation performed on the chronological test dataset, **XGBoost was selected as the final forecasting model** and used to generate a **30-day / 720-hour electricity demand forecast**.

---

## 🎯 Project Objective

The main objective of this project is to predict future hourly electricity demand using historical consumption patterns.

The project aims to:

- Analyze historical hourly electricity consumption
- Identify daily, weekly and seasonal demand patterns
- Analyze holiday and non-holiday demand
- Perform exploratory data analysis
- Engineer meaningful time-series features
- Compare multiple forecasting approaches
- Evaluate models using MAE, RMSE and MAPE
- Select a suitable forecasting model
- Generate a 30-day hourly forecast
- Deploy the final forecasting application using Streamlit

---

# 📊 Dataset

The project uses historical **PJM hourly electricity consumption data**.

### Dataset Characteristics

- **Frequency:** Hourly
- **Target Variable:** `PJMW_MW`
- **Timestamp Column:** `Datetime`
- **Forecast Horizon:** 30 Days
- **Forecast Frequency:** Hourly

The target variable represents electricity consumption measured in **MW (Megawatts)**.

---

# 🔄 Project Workflow

```text
Historical PJM Energy Data
          │
          ▼
   Data Loading & Cleaning
          │
          ▼
 Exploratory Data Analysis
          │
          ▼
  Feature Engineering
          │
          ├── Temporal Features
          ├── Cyclical Features
          ├── Lag Features
          └── Rolling Features
          │
          ▼
    Model Development
          │
          ├── Seasonal Naive
          ├── Exponential Smoothing
          ├── Holt's Linear Trend
          ├── Holt-Winters
          ├── XGBoost
          └── LightGBM
          │
          ▼
     Model Evaluation
          │
          ▼
        XGBoost
          │
          ▼
   30-Day / 720-Hour Forecast
          │
          ▼
    Streamlit Dashboard
          │
          ▼
    Cloud Deployment
    