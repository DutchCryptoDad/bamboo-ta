# -*- coding: utf-8 -*-
# simple_moving_average.py
import pandas as pd


def simple_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """Simple Moving Average (SMA)"""
    df_copy = df.copy()
    df_copy["sma"] = df_copy[column].rolling(window=period).mean()

    return df_copy[["sma"]]


simple_moving_average.__doc__ = """
Name:
    Simple Moving Average (SMA)

Description:
    The Simple Moving Average is the unweighted mean of the previous 'period' data points.

More info:
    https://www.investopedia.com/terms/s/sma.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which SMA is to be calculated. Default is 'close'.
    - period (int): The period over which SMA is to be calculated. Default is 21.

Call with:
    df['sma'] = bta.simple_moving_average(df, 'close', 50)['sma']

Returns:
    pd.DataFrame: DataFrame with 'sma' column.
"""
