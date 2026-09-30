# ⚡ PJM Energy Consumption Forecasting

### Machine Learning Based 30-Day Hourly Electricity Demand Forecasting

---

## 🔗 Project Links

🌐 **Live Streamlit Application**

https://pjm-energy-consumption-forecasting-ilvbysnospmklqinhj2psn.streamlit.app/

💻 **GitHub Repository**

https://github.com/adarsh-552/pjm-energy-consumption-forecasting

---

## 📌 Project Overview

This project focuses on forecasting **hourly electricity demand** using historical PJM energy consumption data.

The project follows an end-to-end machine learning workflow including:

- Data loading and preprocessing
- Exploratory Data Analysis
- Time-series feature engineering
- Model development
- Model evaluation
- 30-day hourly forecasting
- Interactive Streamlit dashboard
- Cloud deployment

The final forecasting application uses **XGBoost** to generate hourly electricity demand predictions for a 30-day forecasting horizon.

---

## 🎯 Project Objective

The main objective of this project is to forecast future hourly electricity demand using historical electricity consumption patterns.

### Objectives

- Analyze historical hourly electricity consumption
- Identify daily and weekly demand patterns
- Analyze seasonal demand behavior
- Perform exploratory data analysis
- Create time-series features
- Train machine learning forecasting models
- Evaluate forecasting performance
- Generate a 30-day hourly forecast
- Deploy the forecasting application using Streamlit

---

# 📊 Dataset

The project uses historical **PJM hourly electricity consumption data**.

### Dataset Characteristics

| Property | Description |
|---|---|
| Frequency | Hourly |
| Target Variable | `PJMW_MW` |
| Timestamp | `Datetime` |
| Forecast Horizon | 30 Days |
| Forecast Frequency | Hourly |
| Measurement | Megawatts (MW) |

The target variable represents electricity demand measured in **Megawatts (MW)**.

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
          ▼
    Model Evaluation
          │
          ▼
      Final Model
          │
          ▼
   30-Day Forecast
          │
          ▼
    Streamlit Dashboard
          │
          ▼
    Cloud Deployment
