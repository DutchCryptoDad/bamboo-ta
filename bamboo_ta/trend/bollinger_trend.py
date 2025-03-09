# -*- coding: utf-8 -*-
# bollinger_trend.py
import numpy as np
import pandas as pd


def bollinger_trend(
    df: pd.DataFrame,
    column: str = "close",
    short_length: int = 20,
    long_length: int = 50,
    std_dev: float = 2.0,
) -> pd.DataFrame:
    """Bollinger Trend Indicator"""
    df_copy = df.copy()

    # Calculate short Bollinger Bands
    short_middle = df_copy[column].rolling(window=short_length).mean()
    short_std = df_copy[column].rolling(window=short_length).std()
    short_upper = short_middle + short_std * std_dev
    short_lower = short_middle - short_std * std_dev

    # Calculate long Bollinger Bands
    long_middle = df_copy[column].rolling(window=long_length).mean()
    long_std = df_copy[column].rolling(window=long_length).std()
    long_upper = long_middle + long_std * std_dev
    long_lower = long_middle - long_std * std_dev

    # Calculate BBTrend
    bbtrend = (
        (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper))
        / short_middle
        * 100
    )

    # Fill NaN values that may arise from the calculation
    bbtrend = bbtrend.fillna(0)

    df_copy["bbtrend"] = bbtrend

    return df_copy[["bbtrend"]]


bollinger_trend.__doc__ = """
Name:
    Bollinger Trend Indicator

Description:
    The Bollinger Trend Indicator calculates the trend based on the difference
    between short and long Bollinger Bands.

More info:
    https://www.tradingview.com/script/UtMK7hNw-Bollinger-Trend/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is 'close'.
    - short_length (int): The period for the short Bollinger Bands. Default is 20.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - std_dev (float): The standard deviation multiplier for the Bollinger Bands. Default is 2.0.

Call with:
    df['bbtrend'] = bta.bollinger_trend(df, 'close', 20, 50, 2.0)['bbtrend']

Returns:
    pd.DataFrame: DataFrame with 'bbtrend' column.
"""
