# 📊 Time Series Task

This repository contains code and resources for **time series analysis and forecasting**.  
It provides modular tools for handling missing values, detecting outliers, and applying rolling window statistics.  
The project also integrates with databases and includes exploratory notebooks.

---

## 📂 Directory Structure

```
time-series-task/
├── data/                         # Datasets (temperature, solar, synthetic, outliers, etc.)
│   ├── temperature_2014_18.csv
│   ├── solar_data_khulna_from_jan_2014_to_nov_2022.csv
│   ├── outliers_data.csv
│   ├── data1.csv ... data8.csv
│   ├── 4threads.csv, 6threads.csv, seasonal_daily_2025.csv, trend_daily_2025.csv
│
├── database/                     # Database integration
│   ├── init_db.py                # Initialize schema (schema.sql)
│   ├── insertion.py              # Insert data into DB
│   ├── outlier_io.py             # Outlier results I/O
│   ├── rolling_io.py             # Rolling statistics I/O
│   └── schema.sql
│
├── notebooks/                    # Jupyter notebooks
│   ├── data_exploration.ipynb
│   └── rolling_window_exploration.ipynb
│
├── output/                       # Generated results
│   ├── 4threads/                 # Cleaned + rolling CSVs
│   ├── temperature_2014_18_mean/
│   ├── temperature_2014_18_mean_750/
│   └── temperature_2014_18_std/
│
├── timeseries_module/            # Main module
│   ├── main.py                   # Run pipeline
│   ├── pipeline.py               # Data processing pipeline
│   ├── missing_values/           # Missing value handling
│   │   ├── fill_forward.py
│   │   ├── fill_backward.py
│   │   ├── linear_interpolation.py
│   │   └── window_mean.py
│   ├── outliers/                 # Outlier detection
│   │   ├── interquartile_range.py
│   │   ├── zscore.py
│   │   ├── local_outlier_factor.py
│   │   └── regression_residuals.py
│   └── rolling/                  # Rolling window statistics
│       ├── mean.py, std.py, var.py, sum.py
│       ├── min_.py, max_.py, median.py, quantile.py
│
├── usage.ipynb                   # Example usage of timeseries_module
├── stress_test.py                # Reading the CPU/RAM usage percent.
├── rolling_pipeline.py           # Read and Update the data to store to the DB. 
├── outlier_pipeline.py           # Read and Update the data to store to the DB. 
├── pyproject.toml                # Project dependencies/config
└── README.md                     # Project documentation
```

---

## ⚙️ Features

### 🧹 Missing Value Handling
- Forward fill, Backward fill
- Linear interpolation
- Window mean

### 🚨 Outlier Detection
- Interquartile Range (IQR)
- Z-Score
- Local Outlier Factor (LOF)
- Regression residuals

### 📈 Rolling Window Statistics
- Mean, Std, Var, Sum
- Min, Max, Median, Quantile

### 🗄️ Database Integration
- Initialize schema (`schema.sql`)
- Insert data (`insertion.py`)
- Manage outlier/rolling outputs

### 📑 Notebooks
- **`data_exploration.ipynb`** → Explore datasets
- **`rolling_window_exploration.ipynb`** → Rolling statistics experiments
- **`usage.ipynb`** → How to use `timeseries_module`

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/AbdullahOthman1/time-series-task.git
cd time-series-task
```

### 2️⃣ Install Dependencies
```bash
pip install .
```

### 3️⃣ Explore Notebooks
Open Jupyter and run any notebook in `notebooks/`:
```bash
jupyter notebook
```

---

## 🏃 Usage

### Run the Main Pipeline
```bash
python timeseries_module/main.py
```

### Use Specific Functions
```python
from timeseries_module.missing_values.methods import fill_forward
from timeseries_module.outliers.methods import zscore
from timeseries_module.rolling.methods import mean
```

### Database Setup
```bash
python database/init_db.py
```

---

## 📊 Example Workflow

1. Load dataset from `data/`
2. Handle missing values (forward fill / interpolation / window mean)
3. Detect outliers (IQR / Z-score / LOF / regression residuals)
4. Apply rolling statistics (mean, std, quantile, etc.)
5. Save processed results into `output/`
6. Optionally push results into database (`database/`)

---

## 📦 Datasets

- `temperature_2014_18.csv` → Historical temperature dataset  
- `solar_data_khulna_from_jan_2014_to_nov_2022.csv` → Solar energy data  
- `outliers_data.csv` → Data with anomalies  
- Synthetic series: `data1.csv … data8.csv`  
- Thread performance: `4threads.csv`, `6threads.csv`  
- Seasonal/trend datasets: `seasonal_daily_2025.csv`, `trend_daily_2025.csv`  

---

## Authors

- **Abdullah Othman**  
- Original repo: [AbdullahOthman1/time-series-task](https://github.com/AbdullahOthman1/time-series-task)

