# -*- coding: utf-8 -*-
# smoothed_rate_of_change.py

import pandas as pd


def smoothed_rate_of_change(
    df: pd.DataFrame, roclen: int = 21, emalen: int = 13, smooth: int = 21
) -> pd.DataFrame:
    """Smoothed Rate of Change (SROC)"""
    df_copy = df.copy()

    # Calculate ROC
    roc = df_copy["close"].diff(roclen) / df_copy["close"].shift(roclen) * 100

    # Calculate EMA of the close price
    ema = df_copy["close"].ewm(span=emalen, adjust=False).mean()

    # Calculate SROC
    sroc = ema.diff(smooth) / ema.shift(smooth) * 100

    df_copy["sroc"] = sroc

    return df_copy[["sroc"]]


smoothed_rate_of_change.__doc__ = """
Name:
    Smoothed Rate of Change (SROC)

Description:
    The Smoothed Rate of Change (SROC) is a momentum oscillator that applies
    an exponential moving average (EMA) to the Rate of Change (ROC) to smooth
    out short-term fluctuations.

More info:
    https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/

Call with:
    df['sroc'] = bta.smoothed_rate_of_change(df, roclen=21, emalen=13, smooth=21)['sroc']

Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - roclen (int): Period for the ROC calculation. Default is 21.
    - emalen (int): Period for the EMA calculation. Default is 13.
    - smooth (int): Smoothing period for the ROC calculation. Default is 21.

Returns:
    pd.DataFrame: DataFrame with 'sroc' column.
"""
