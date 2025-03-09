# -*- coding: utf-8 -*-
# exponential_moving_average.py
import pandas as pd


def exponential_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """Exponential Moving Average (EMA)"""
    df_copy = df.copy()

    # Calculate Exponential Moving Average
    df_copy["ema"] = df_copy[column].ewm(span=period, adjust=False).mean()

    # Set first `period - 1` values to NaN using `.loc[]` to avoid chained assignment warning
    df_copy.loc[: period - 1, "ema"] = pd.NA

    return df_copy[["ema"]]


exponential_moving_average.__doc__ = """
Name:
    Exponential Moving Average (EMA)

Description:
    The Exponential Moving Average gives more weight to recent prices and thus reacts
    more quickly to price changes than the Simple Moving Average.

More info:
    https://www.investopedia.com/terms/e/ema.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EMA is to be calculated. Default is 'close'.
    - period (int): The period over which EMA is to be calculated. Default is 21.

Call with:
    df['ema'] = bta.exponential_moving_average(df, "close", 21)['ema']

Returns:
    pd.DataFrame: DataFrame with 'ema' column, where first `period-1` values are NaN.
"""
