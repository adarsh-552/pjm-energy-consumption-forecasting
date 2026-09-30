# ⚡ PJM Energy Consumption Forecasting

### Machine Learning Based 30-Day Hourly Electricity Demand Forecasting

## 🔗 Live Dashboard

**Streamlit App:**  
PASTE_YOUR_STREAMLIT_LINK_HERE

---

## 📌 Project Overview

This project develops a machine learning based forecasting system to predict hourly electricity demand using historical PJM energy consumption data.

The project combines exploratory data analysis, time-series feature engineering and gradient boosting models to identify temporal consumption patterns and generate a 30-day hourly electricity demand forecast.

The final XGBoost model is deployed through an interactive Streamlit dashboard.

---

## 🎯 Project Objective

The main objectives of this project are:

- Analyze historical hourly electricity consumption
- Identify temporal and seasonal demand patterns
- Engineer meaningful time-series features
- Evaluate multiple forecasting approaches
- Select a suitable machine learning model
- Generate a 30-day hourly electricity demand forecast
- Deploy the final forecasting application

---

## 🏗️ Project Workflow

```text
Historical PJM Energy Data
          ↓
     Data Cleaning
          ↓
Exploratory Data Analysis
          ↓
  Feature Engineering
          ↓
 Model Development
          ↓
 Model Evaluation
          ↓
     XGBoost
          ↓
  30-Day Forecast
          ↓
 Streamlit Dashboard
          ↓
 Cloud Deployment

 ---

## 🔧 Feature Engineering

### Temporal Features

- Hour
- Day
- Month
- Year
- Day of Week
- Holiday Indicator

### Cyclical Features

- Hour Sin / Cos
- Month Sin / Cos
- Day-of-Week Sin / Cos

### Lag Features

- Lag 1 hour
- Lag 24 hours
- Lag 168 hours

### Rolling Features

- 24-hour Rolling Mean
- 168-hour Rolling Mean
- 24-hour Rolling Standard Deviation

All rolling features were calculated using previous observations to avoid data leakage.

---

## 🤖 Models Evaluated

The project evaluated several forecasting approaches.

### Statistical Models

- Seasonal Naive
- Simple Exponential Smoothing
- Holt's Linear Trend
- Holt-Winters

### Machine Learning Models

- XGBoost
- LightGBM

The final deployed model is **XGBoost**.

---

## 🏆 XGBoost Model Performance

| Metric | Result |
|---|---:|
| MAE | **57.12 MW** |
| RMSE | **77.09 MW** |
| MAPE | **0.99%** |

The model was evaluated using a chronological last-year test split.

---

## 🔮 30-Day Forecast

The final XGBoost model generated a recursive hourly forecast for the next 30 days.

| Forecast Information | Value |
|---|---:|
| Forecast Horizon | **30 Days** |
| Total Predictions | **720 Hours** |
| Average Demand | **5,733.2 MW** |
| Minimum Demand | **3,975.65 MW** |
| Maximum Demand | **7,425.06 MW** |

### Forecast Period

**03 August 2018 01:00 → 02 September 2018 00:00**

---

## 📊 Streamlit Dashboard

The deployed dashboard provides:

- Forecast summary
- Average, minimum and peak demand
- Interactive 30-day forecast visualization
- Demand pattern analysis
- Peak demand analysis
- XGBoost model performance
- 720-hour forecast data
- CSV / Excel download
---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Machine Learning | XGBoost, LightGBM |
| Development | Jupyter Notebook |
| Dashboard | Streamlit |
| Data Format | Excel |
| Deployment | Streamlit Community Cloud |

---

## 📁 Project Structure

```text
pjm-energy-consumption-forecasting/
│
├── PJM_Energy_Forecasting.ipynb
├── streamlit_app.py
├── requirements.txt
├── PJM_30_Day_Forecast_XGBoost.xlsx
├── PJM_30_Day_Forecast.xlsx
├── PJMW_MW_Hourly.xlsx
└── README.md