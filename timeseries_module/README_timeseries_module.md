# timeseries_module

> Comprehensive utilities for cleaning, transforming, and analyzing time‑series data: missing‑value handling, outlier detection, rolling features, and a simple pipeline and CLI entry point.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Modules](#modules)
- [CLI / Entry Point](#cli--entry-point)
- [Examples](#examples)
- [Developing](#developing)
- [License](#license)

## Overview
This package organizes common time‑series preprocessing tasks into small, focused modules. 
It aims to be framework‑agnostic and easy to compose into data science workflows or production pipelines.

**Key capabilities**
- Fill/flag missing values with configurable strategies.
- Detect and fix outliers (statistical rules or model‑based).
- Generate rolling‑window statistics and features.
- Chain steps together with a simple pipeline (`pipeline.py`).

## Installation
```bash
pip install -e .  # if a pyproject/setup is added
```
Or simply copy the `timeseries_module/` folder into your project and import the pieces you need.

## Quick Start
```python
from timeseries_module.pipeline import TimeSeriesPipeline  # if available
from timeseries_module.missing_values import strategies  # example submodule
from timeseries_module.rolling import features           # example submodule

```

## Module Structure
```
timeseries_module/
├── __init__.py
├── main.py
├── pipeline.py
│
├── missing_values/
│   ├── __init__.py
│   ├── interface.py
│   ├── methods/
│   │   ├── __init__.py
│   │   ├── fill_backward.py
│   │   ├── fill_forward.py
│   │   ├── linear_interpolation.py
│   │   ├── window_mean.py
│   │
├── outliers/
│   ├── __init__.py
│   ├── interface.py
│   ├── methods/
│   │   ├── __init__.py
│   │   ├── interquartile_range.py
│   │   ├── local_outlier_factor.py
│   │   ├── regression_residuals.py
│   │   ├── zscore.py
│   │
├── rolling/
│   ├── __init__.py
│   ├── interface.py
│   ├── methods/
│   │   ├── __init__.py
│   │   ├── max_.py
│   │   ├── mean.py
│   │   ├── median.py
│   │   ├── min_.py
│   │   ├── quantile.py
│   │   ├── std.py
│   │   ├── sum.py
│   │   ├── var.py

```

## Modules
### `timeseries_module/main.py`
Entry-point script demonstrating module usage.

**Functions**
### `main(input_df, output_path, outlier_sensitivity_degree, value_column, missing_value_function, outlier_fn, time_column, rolling_fn, rolling_kwargs, export)`

Main entry point for the **time series module**.

**Workflow on the specified `value_column`:**
1. *(Optional)* Fill missing values using the chosen function (e.g., `fill_forward`).
2. *(Optional)* Remove outliers according to a sensitivity profile: `"LOW" | "MEDIUM" | "HIGH"`.
3. *(Optional)* Apply a rolling function (e.g., moving average, rolling statistics).
4. Export the processed data to the given `output_path` if `export=True`.

### `timeseries_module/missing_values/interface.py`
Module utilities.

**Functions**
- `apply_missing_values(func, df, value_column)`
  - Apply a missing-values function to a DataFrame column. func: function A function like fill_forward, fill_backward, etc. df: pd.DataFrame The input DataFrame. value_column: str The column to apply the method on. kwargs: Extra parameters for the function.

### `timeseries_module/missing_values/methods/fill_backward.py`
Module utilities.

**Functions**
- `fill_backward(df, value_column, limit)`
  - Fill missing values backward (next valid observation is carried backward).

### `timeseries_module/missing_values/methods/fill_forward.py`
Module utilities.

**Functions**
- `fill_forward(df, value_column, limit)`
  - Fill missing values forward (previous valid observation is carried forward).

### `timeseries_module/missing_values/methods/linear_interpolation.py`
Module utilities.

**Functions**
- `linear_interpolation(df, value_column, limit_direction, limit)`
  - Fill missing values using linear interpolation.

### `timeseries_module/missing_values/methods/window_mean.py`
Module utilities.

**Functions**
- `window_mean(df, value_column, window, min_periods, center)`
  - Fill missing values using rolling window mean.

### `timeseries_module/missing_values/methods/__init__.py`
Module utilities.

### `timeseries_module/missing_values/__init__.py`
Module utilities.

### `timeseries_module/outliers/interface.py`
Module utilities.

**Functions**
- `apply_outliers(func, df, value_column)`
  - Apply an outlier-removal function to a DataFrame column. func: function A function like: - remove_outliers_zscore - remove_outliers_iqr - remove_outliers_linear_regression - remove_outliers_lof df: pd.DataFrame The input DataFrame. value_column: str The column to apply the method on. kwargs: Extra…
- `handle_outliers(df, outlier_fn, value_column, sensitivity_degree, time_column)`
  - Wrapper that applies an outlier function using a hard-coded sensitivity level. df: pd.DataFrame The input data. outlier_fn: function A function like: - remove_outliers_zscore - remove_outliers_iqr - remove_outliers_linear_regression - remove_outliers_lof sensitivity_degree: str One of: 'low',…

### `timeseries_module/outliers/methods/interquartile_range.py`
Module utilities.

**Functions**
- `remove_outliers_iqr(df, value_column, threshold)`
  - Remove rows outside [Q1 - threshold*IQR, Q3 + threshold*IQR] for `value_column`. Keeps NaN rows.

### `timeseries_module/outliers/methods/local_outlier_factor.py`
Detection and treatment of outliers in time series.

**Functions**
- `remove_outliers_lof(df, value_column, time_column, n_neighbors, contamination, include_time)`
  - Use Local Outlier Factor (LOF) to remove outliers in `value_column`. Optionally include time as a feature.

### `timeseries_module/outliers/methods/regression_residuals.py`
Module utilities.

**Functions**
- `remove_outliers_linear_regression(df, value_column, time_column, threshold)`
  - Fit a linear regression of value vs. time, then remove rows whose residual z-score exceeds `threshold`. Rows with NaN in `value_column` are kept.

### `timeseries_module/outliers/methods/zscore.py`
Module utilities.

**Functions**
- `remove_outliers_zscore(df, value_column, threshold)`
  - Remove rows where the z-score of `value_column` exceeds `threshold`. Keeps NaN rows.

### `timeseries_module/outliers/methods/__init__.py`
Module utilities.

### `timeseries_module/outliers/__init__.py`
Module utilities.

### `timeseries_module/pipeline.py`
Composable preprocessing / modeling pipeline for time series.

**Functions**
- `run_pipeline(input_df, output_path, outlier_sensitivity_degree, value_column, missing_value_function, outlier_fn, time_column, rolling_fn, rolling_kwargs, export)`

  Runs a minimal **cleaning pipeline** on a time-series DataFrame, with an optional rolling step.

  **Pipeline steps on `value_column`:**
  1. *(Optional)* Fill missing values using the provided function (e.g., forward fill, mean imputation).
  2. *(Optional)* Remove outliers based on a sensitivity profile: `"low" | "medium" | "high"`.
  3. *(Optional)* Apply a rolling function (e.g., rolling mean, moving statistics).
  4. Export the processed DataFrame to `output_path` if `export=True`.


### `timeseries_module/rolling/interface.py`
Module utilities.

**Functions**
- `apply_rolling(func, df, value_column)`
  - Apply a rolling function to a DataFrame column.
- `compute_rolling(df, rolling_fn, value_column)`
  - Wrapper that applies a rolling function with simple defaults. df: pd.DataFrame The input data. rolling_fn: function One of your rolling methods: - rolling_mean / rolling_median / rolling_sum / rolling_min / rolling_max - rolling_std / rolling_var - rolling_quantile value_column: str Column to…

### `timeseries_module/rolling/methods/max_.py`
Module utilities.

**Functions**
- `rolling_max(df, value_column, window, min_periods, center, output_column)`

### `timeseries_module/rolling/methods/mean.py`
Module utilities.

**Functions**
- `rolling_mean(df, value_column, window, min_periods, center, output_column)`

### `timeseries_module/rolling/methods/median.py`
Module utilities.

**Functions**
- `rolling_median(df, value_column, window, min_periods, center, output_column)`

### `timeseries_module/rolling/methods/min_.py`
Module utilities.

**Functions**
- `rolling_min(df, value_column, window, min_periods, center, output_column)`

### `timeseries_module/rolling/methods/quantile.py`
Module utilities.

**Functions**
- `rolling_quantile(df, value_column, window, q, min_periods, center, method, output_column)`
  - Rolling quantile using the NEW pandas API (>= 2.2), which uses `method=...` instead of the deprecated/removed `interpolation=`. Parameters ---------- q : float The quantile in [0, 1]. method : str | None Quantile algorithm name per pandas >= 2.2 (e.g., "linear", etc.). If None, pandas' default is…

### `timeseries_module/rolling/methods/std.py`
Module utilities.

**Functions**
- `rolling_std(df, value_column, window, min_periods, center, ddof, output_column)`

### `timeseries_module/rolling/methods/sum.py`
Module utilities.

**Functions**
- `rolling_sum(df, value_column, window, min_periods, center, output_column)`

### `timeseries_module/rolling/methods/var.py`
Module utilities.

**Functions**
- `rolling_var(df, value_column, window, min_periods, center, ddof, output_column)`

### `timeseries_module/rolling/methods/__init__.py`
Module utilities.

### `timeseries_module/rolling/__init__.py`
Module utilities.

### `timeseries_module/__init__.py`
Module utilities.
