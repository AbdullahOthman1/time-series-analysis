from pathlib import Path
import pandas as pd

def export_csv(obj, path: str | Path):
    path = Path(path)
    if isinstance(obj, pd.Series):
        obj = obj.to_frame()
    obj.to_csv(path, index=False)
