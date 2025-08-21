# timeseries_toolkit/pipeline.py
from __future__ import annotations
from pathlib import Path
import pandas as pd
from .strategies.base import MissingValueStrategy, OutlierStrategy
from .utils import export_csv

class TimeSeriesAnalyzer:
    def __init__(
        self,
        missing_strategy: MissingValueStrategy | None = None,
        outlier_strategy: OutlierStrategy | None = None,
        output_dir: str | Path = "output",
    ):
        self.missing_strategy = missing_strategy
        self.outlier_strategy = outlier_strategy
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self, df: pd.DataFrame, export: bool = True) -> dict:
        results: dict[str, object] = {"original": df.copy()}

        # 1) Missing values
        working = df.copy()
        if self.missing_strategy is not None:
            working = self.missing_strategy.fit(working).transform(working)
            results["missing_handled"] = working.copy()
        else:
            results["missing_handled"] = working.copy()

        # 2) Outliers (DROP-ONLY)
        outlier_removed_pct = None
        if self.outlier_strategy is not None:
            before_n = len(working)
            cleaned = self.outlier_strategy.fit(working).transform(working)
            after_n = len(cleaned)
            results["outliers_handled"] = cleaned.copy()

            # Optional: provide indices removed and a boolean mask for convenience
            removed_idx = working.index.difference(cleaned.index)
            results["outliers_removed_index"] = removed_idx
            mask_keep = working.index.isin(cleaned.index)
            results["outliers_keep_mask"] = pd.Series(mask_keep, index=working.index, name="keep")

            outlier_removed_pct = 0.0 if before_n == 0 else (before_n - after_n) / before_n
            working = cleaned  # continue with cleaned data for any later stages
        else:
            results["outliers_handled"] = working.copy()

        # 3) Summary
        miss_pct = results["missing_handled"].isna().mean().rename("missing_pct")  # per column
        summary = miss_pct.to_frame()
        if outlier_removed_pct is not None:
            summary.loc["__rows_removed_as_outliers__", "missing_pct"] = pd.NA
            summary.loc["__rows_removed_as_outliers__", "outlier_removed_pct"] = outlier_removed_pct
        results["summary"] = summary

        # 4) Exports
        if export:
            export_csv(results["missing_handled"], self.output_dir / "missing_handled.csv")
            export_csv(results["outliers_handled"], self.output_dir / "outliers_handled.csv")

        return results
