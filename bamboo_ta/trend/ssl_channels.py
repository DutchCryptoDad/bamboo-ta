# -*- coding: utf-8 -*-
# ssl_channels.py
import numpy as np
import pandas as pd


def ssl_channels(df: pd.DataFrame, length: int = 10, mode: str = "sma") -> pd.DataFrame:
    """SSL Channels"""
    df_copy = df.copy()

    if mode != "sma":
        raise ValueError(f"Mode '{mode}' not supported yet")

    # Calculate simple moving averages of high and low
    df_copy["sma_high"] = df_copy["high"].rolling(length).mean()
    df_copy["sma_low"] = df_copy["low"].rolling(length).mean()

    # Determine trend direction
    df_copy["hlv"] = np.where(
        df_copy["close"] > df_copy["sma_high"],
        1,
        np.where(df_copy["close"] < df_copy["sma_low"], -1, np.nan),
    )
    df_copy["hlv"] = df_copy["hlv"].ffill()

    # Calculate SSL channels
    df_copy["ssl_down"] = np.where(
        df_copy["hlv"] < 0, df_copy["sma_high"], df_copy["sma_low"]
    )
    df_copy["ssl_up"] = np.where(
        df_copy["hlv"] < 0, df_copy["sma_low"], df_copy["sma_high"]
    )

    return df_copy[["ssl_down", "ssl_up"]]


ssl_channels.__doc__ = """
Name:
    SSL Channels

Description:
    SSL Channels is an indicator based on the concept of using different moving averages
    to identify trends. This function calculates the SSL Down and SSL Up series.

More info:
    https://www.tradingview.com/script/xl7XbPTM-SSL-Channel-Chart/

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the SMA calculation. Default is 10.
    - mode (str): Type of moving average to use. Currently only 'sma' is supported.

Call with:
    ssl_result = bta.ssl_channels(df, length=10, mode='sma')
    df['ssl_down'] = ssl_result['ssl_down']
    df['ssl_up'] = ssl_result['ssl_up']

Returns:
    pd.DataFrame: DataFrame with 'ssl_down' and 'ssl_up' columns.
"""
