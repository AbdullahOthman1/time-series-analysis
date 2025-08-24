from .zscore import remove_outliers_zscore
from .interquartile_range import remove_outliers_iqr
from .regression_residuals import remove_outliers_linear_regression
from .local_outlier_factor import remove_outliers_lof

__all__ = [
    "remove_outliers_zscore",
    "remove_outliers_iqr",
    "remove_outliers_linear_regression",
    "remove_outliers_lof",
]
