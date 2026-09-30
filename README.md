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
    ---

# ⚙️ Feature Engineering

Several time-series features were created to help the machine learning models understand temporal electricity demand patterns.

## 1. Temporal Features

- `Hour`
- `Day`
- `Month`
- `Year`
- `DayOfWeekNum`
- `IsHoliday`

## 2. Cyclical Features

Cyclical encoding was used for periodic time-based variables.

- `Hour_sin`
- `Hour_cos`
- `Month_sin`
- `Month_cos`
- `DayOfWeek_sin`
- `DayOfWeek_cos`

This helps the model understand relationships such as:

```text
23:00 → 00:00
December → January
Sunday → Monday
---

# 🔮 30-Day Forecast

The final XGBoost model was used to generate a recursive hourly forecast for the next 30 days.

### Forecast Summary

| Forecast Information | Value |
|---|---:|
| Model | **XGBoost** |
| Forecast Horizon | **30 Days** |
| Total Predictions | **720 Hours** |
| Average Demand | **5,733.2 MW** |
| Minimum Demand | **3,975.65 MW** |
| Maximum Demand | **7,425.06 MW** |

### Forecast Period

**03 August 2018 01:00 → 02 September 2018 00:00**

---

# 🔁 Forecasting Approach

The future forecast was generated using a recursive prediction approach.

```text
Historical Data
      │
      ▼
Generate Features
      │
      ▼
XGBoost Prediction
      │
      ▼
Add Prediction to History
      │
      ▼
Generate Next-Hour Features
      │
      ▼
XGBoost Prediction
      │
      ▼
Repeat for 720 Hours 
---

# 📌 Key Findings

- Historical PJM electricity demand shows strong temporal patterns.
- Daily and weekly consumption patterns are important for short-term forecasting.
- Lag features capture previous consumption behavior effectively.
- Rolling statistics provide information about recent demand trends.
- Cyclical encoding helps represent periodic time relationships.
- XGBoost achieved **57.12 MW MAE**, **77.09 MW RMSE**, and approximately **0.99% MAPE** on the chronological test set.
- LightGBM achieved **58.06 MW MAE**, **77.28 MW RMSE**, and approximately **1.00% MAPE**.
- The final XGBoost model was used to generate a **720-hour / 30-day forecast**.
- The forecasting system was deployed as an interactive Streamlit application.

---

# 🎓 Project Outcome

This project demonstrates an end-to-end electricity demand forecasting workflow:

```text
Data Collection
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
XGBoost Forecasting
      ↓
30-Day Forecast
      ↓
Streamlit Deployment