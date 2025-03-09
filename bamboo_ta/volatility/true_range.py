# -*- coding: utf-8 -*-
# true_range.py
import numpy as np
import pandas as pd


def true_range(df: pd.DataFrame) -> pd.DataFrame:
    """True Range"""
    df_copy = df.copy()
    prev_close = df_copy["close"].shift()

    # Calculate the true range components
    true_range = pd.concat(
        [
            df_copy["high"] - df_copy["low"],
            (df_copy["high"] - prev_close).abs(),
            (df_copy["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    df_copy["true_range"] = true_range

    return df_copy[["true_range"]]


true_range.__doc__ = """
Name:
    True Range (TR)

Description:
    The True Range indicator measures market volatility. True Range is defined as the greatest of the following:
    - The current high minus the current low
    - The absolute value of the current high minus the previous close
    - The absolute value of the current low minus the previous close
    
    This measure accounts for gaps in price movement and provides a more comprehensive 
    measure of price volatility than simply looking at the high-low range.

More info:
    https://www.investopedia.com/terms/a/atr.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.

Call with:
    df['true_range'] = bta.true_range(df)['true_range']

Returns:
    pd.DataFrame: DataFrame with 'true_range' column.
"""
