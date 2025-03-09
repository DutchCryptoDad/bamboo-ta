# -*- coding: utf-8 -*-
# moving_average_convergence_divergence_leader.py

import pandas as pd
import numpy as np

def macd_leader(
    df: pd.DataFrame, 
    src: str = 'close', 
    fast_length: int = 12, 
    slow_length: int = 26, 
    signal_length: int = 9
) -> pd.DataFrame:
    """MACD Leader"""
    def ema_calculation(series, span):
        return series.ewm(span=span, adjust=False).mean()

    df_copy = df.copy()
    src_series = df[src]

    sema = ema_calculation(src_series, span=fast_length)
    lema = ema_calculation(src_series, span=slow_length)
    diff_sema = src_series - sema
    diff_lema = src_series - lema
    i1 = sema + ema_calculation(diff_sema, span=fast_length)
    i2 = lema + ema_calculation(diff_lema, span=slow_length)
    macd_leader = ((i1 - i2) / 10) * 10

    df_copy['macd_leader'] = macd_leader
    
    return df_copy[['macd_leader']]

macd_leader.__doc__ = \
"""
Name:
    MACD Leader

Description:
    The MACD Leader is a variation of the standard MACD that aims to provide an 
    earlier signal by using a different calculation method.

More info:
    https://www.investopedia.com/terms/m/macd.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - fast_length (int): Length for the fast EMA. Default is 12.
    - slow_length (int): Length for the slow EMA. Default is 26.
    - signal_length (int): Length for the signal EMA. Default is 9.

Call with:
    df['macd_leader'] = bta.macd_leader(df, 'close')['macd_leader']

Returns:
    pd.DataFrame: DataFrame with 'macd_leader' column.
"""