# Time Series Task

This repository contains code and resources for time series analysis and forecasting.

## Directory Structure

```
time-series-task/
├── data/               # Datasets for analysis
├── notebooks/          # Jupyter notebooks with experiments and EDA
├── output              # Folder for saving the results from the module.
├── timeseries_module/  # Custom time series analysis module
├── pyproject.toml      # Project dependencies and configuration
├── README.md           # Project documentation
├── usage.ipynb         # File for using the timeseries_module.
```

## Getting Started

1. **Clone the repository:**
    ```bash
    git clone https://github.com/AbdullahOthman1/time-series-task.git
    cd time-series-task
    ```

2. **Install dependencies:**
    - Install Python packages using the `pyproject.toml` file:
      ```bash
      pip install .
      ```

3. **Explore notebooks:**
    - Open files in the `notebooks/` directory for exploratory data analysis.

## Project Overview

- **Data:** Time series datasets for forecasting tasks.
- **Code:** Scripts and modules for preprocessing, modeling, and evaluation.
- **Notebooks:** Step-by-step analysis and results.
- **Timeseries_Module** A module that can handle missing values, removing outliers and applying rolling window.