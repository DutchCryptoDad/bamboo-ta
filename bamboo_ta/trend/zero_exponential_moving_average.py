# -*- coding: utf-8 -*-
# zero_exponential_moving_average.py
import pandas as pd


def zero_exponential_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """Zero Exponential Moving Average (ZEMA)"""
    df_copy = df.copy()

    # Calculate EMA components
    ema1 = df_copy[column].ewm(span=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, adjust=False).mean()

    # ZEMA calculation
    df_copy["zema"] = 2 * ema1 - ema2

    return df_copy[["zema"]]


zero_exponential_moving_average.__doc__ = """
Name:
    Zero Exponential Moving Average (ZEMA)

Description:
    The Zero Exponential Moving Average (ZEMA) is an improved version of the Exponential
    Moving Average (EMA) that reduces lag by incorporating a zero-lag component.

More info:
    The ZEMA applies the formula: 2 * EMA(period) - EMA(EMA(period)) to reduce lag.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZEMA is to be calculated. Default is 21.

Call with:
    df['zema'] = bta.zero_exponential_moving_average(df, 'close', 21)['zema']

Returns:
    pd.DataFrame: DataFrame with 'zema' column.
"""
