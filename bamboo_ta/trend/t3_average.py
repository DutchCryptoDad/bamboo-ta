# -*- coding: utf-8 -*-
# t3_average.py
import pandas as pd


def t3_average(df: pd.DataFrame, length: int = 5) -> pd.DataFrame:
    """T3 Average"""
    df_copy = df.copy()

    # Calculating multiple EMA stages
    df_copy["xe1"] = df_copy["close"].ewm(span=length, adjust=False).mean()
    df_copy["xe2"] = df_copy["xe1"].ewm(span=length, adjust=False).mean()
    df_copy["xe3"] = df_copy["xe2"].ewm(span=length, adjust=False).mean()
    df_copy["xe4"] = df_copy["xe3"].ewm(span=length, adjust=False).mean()
    df_copy["xe5"] = df_copy["xe4"].ewm(span=length, adjust=False).mean()
    df_copy["xe6"] = df_copy["xe5"].ewm(span=length, adjust=False).mean()

    # Constants for T3 calculation
    b = 0.7
    c1 = -b * b * b
    c2 = 3 * b * b + 3 * b * b * b
    c3 = -6 * b * b - 3 * b - 3 * b * b * b
    c4 = 1 + 3 * b + b * b * b + 3 * b * b

    # T3 average calculation
    df_copy["t3_average"] = (
        c1 * df_copy["xe6"]
        + c2 * df_copy["xe5"]
        + c3 * df_copy["xe4"]
        + c4 * df_copy["xe3"]
    )

    return df_copy[["t3_average"]]


t3_average.__doc__ = """
Name:
    T3 Average

Description:
    The T3 average is a smoothed moving average designed to reduce lag while maintaining
    responsiveness to price changes. This implementation uses multiple exponential moving
    averages (EMA) to achieve its smoothing effect.

More info:
    Tim Tillson's T3 indicator: 
    https://www.investopedia.com/terms/t/t3-oscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the EMA calculation. Default is 5.

Call with:
    df['t3_average'] = bta.t3_average(df, length=5)['t3_average']

Returns:
    pd.DataFrame: DataFrame with 't3_average' column.
"""
