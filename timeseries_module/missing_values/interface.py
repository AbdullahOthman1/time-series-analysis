import pandas as pd

def apply_missing_values(func, df: pd.DataFrame, value_column: str, **kwargs) -> pd.DataFrame:
    """
    Apply a missing-values function to a DataFrame column.

    func: function
        A function like fill_forward, fill_backward, etc.
    df: pd.DataFrame
        The input DataFrame.
    value_column: str
        The column to apply the method on.
    kwargs:
        Extra parameters for the function.
    """
    return func(df, value_column, **kwargs)