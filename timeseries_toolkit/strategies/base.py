# timeseries_toolkit/strategies/base.py
from __future__ import annotations
from typing import Protocol, runtime_checkable
import pandas as pd

@runtime_checkable
class MissingValueStrategy(Protocol):
    def fit(self, df: pd.DataFrame) -> "MissingValueStrategy": ...
    def transform(self, df: pd.DataFrame) -> pd.DataFrame: ...

@runtime_checkable
class OutlierStrategy(Protocol):
    """
    Drop-only outlier strategies.
    Implementations must return a cleaned DataFrame from transform()
    (e.g., rows with outliers removed or capped as desired).
    """
    def fit(self, df: pd.DataFrame) -> "OutlierStrategy": ...
    def transform(self, df: pd.DataFrame) -> pd.DataFrame: ...
