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
```
---

# ⚙️ Feature Engineering

Time-series features were created to help the machine learning model capture electricity demand patterns.

## Temporal Features

- `Hour`
- `Day`
- `Month`
- `Year`
- `DayOfWeekNum`
- `IsHoliday`

## Cyclical Features

Cyclical encoding was used to represent periodic time relationships.

- `Hour_sin`
- `Hour_cos`
- `Month_sin`
- `Month_cos`
- `DayOfWeek_sin`
- `DayOfWeek_cos`

## Lag Features

Previous electricity consumption values were used to capture historical demand behavior.

## Rolling Features

Rolling statistics were used to capture recent demand trends.

---

# 🤖 Model Development

The project evaluates forecasting approaches using statistical and machine-learning methods.

### Statistical Forecasting

- Seasonal Naive
- Exponential Smoothing
- Holt's Linear Trend
- Holt-Winters

### Machine Learning

- XGBoost
- LightGBM

The final deployed forecasting model is **XGBoost**.

---

# 📏 Model Evaluation

Model performance was evaluated using:

- **MAE** — Mean Absolute Error
- **RMSE** — Root Mean Squared Error
- **MAPE** — Mean Absolute Percentage Error

A chronological test split was used to preserve the time-series nature of the dataset.

---

# 🔮 30-Day Forecast

The final forecasting system generates hourly electricity demand predictions for a **30-day forecasting horizon**.

### Forecast Details

| Information | Value |
|---|---:|
| Forecast Horizon | 30 Days |
| Forecast Frequency | Hourly |
| Total Predictions | 720 Hours |
| Final Model | XGBoost |

---

# 🔁 Forecasting Approach

The forecasting system uses a recursive prediction approach.

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
Predict Next Hour
      │
      ▼
Repeat Until 720 Hours
```
---

## ⭐ Project Highlights

- End-to-end electricity demand forecasting workflow
- Time-series based feature engineering
- Machine learning model evaluation
- 30-day / 720-hour hourly forecasting
- Interactive Streamlit dashboard
- Downloadable forecast results
- Cloud deployment using Streamlit Community Cloud

---

## 🔗 Quick Access

🌐 **Live Dashboard:**  
https://pjm-energy-consumption-forecasting-ilvbysnospmklqinhj2psn.streamlit.app/

💻 **GitHub Repository:**  
https://github.com/adarsh-552/pjm-energy-consumption-forecasting

---

---

# 👨‍💻 Author

## Adarsh Nallannagiri

**B.Tech – Computer Science Engineering**

📧 **Email:** aadharsh172@gmail.com

💻 **GitHub:** [adarsh-552](https://github.com/adarsh-552)

🔗 **LinkedIn:** [Adarsh Nallannagiri](https://www.linkedin.com/in/adarsh-nallannagiri/)

### Areas of Interest

- Data Science
- Machine Learning
- Python
- Data Analytics
- Full-Stack Development

---

⭐ **Thank you for exploring this project!**

