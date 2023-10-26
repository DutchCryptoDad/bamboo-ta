# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import EMA


def HeikinAshi(df, pre_smoothing_period=None, post_smoothing_period=None):
    """
    Heikin Ashi (HA) with Optional Pre and Post Smoothing

    Call with:
    - Regular Heiken Ashi:
        ha_df = HeikinAshi(df)

    - With pre-smoothing of the original data:
        ha_df = HeikinAshi(df, pre_smoothing_period=14)

    - With both pre and post smoothing:
        ha_df = HeikinAshi(df, pre_smoothing_period=14, post_smoothing_period=14)

    After calling, the following columns can be extracted:
        df['HA_Close'] = ha_df['HA_Close']
        df['HA_Open'] = ha_df['HA_Open']
        df['HA_High'] = ha_df['HA_High']
        df['HA_Low'] = ha_df['HA_Low']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - pre_smoothing_period (int, optional): Period for EMA pre-smoothing of the original data. If provided, original price bars are smoothed before Heikin Ashi calculations.
    - post_smoothing_period (int, optional): Period for EMA post-smoothing of Heikin Ashi values. If provided, Heikin Ashi values are smoothed post calculations.

    Returns:
    - pd.DataFrame: DataFrame with 'HA_Close', 'HA_Open', 'HA_High', 'HA_Low' columns.

    Description:
    Heikin Ashi is a type of price chart that shares some characteristics with candlestick charts but differs due to the values used to plot them. This modified version allows for optional smoothing of the original data before the Heikin Ashi calculation and/or smoothing of the Heikin Ashi values themselves, aiming to provide a more refined and smoother representation of price action, making it easier to identify the trend.
    """
    df_copy = df.copy()

    # If pre-smoothing is required
    if pre_smoothing_period:
        df_copy['open'] = EMA(df_copy, 'open', pre_smoothing_period)
        df_copy['close'] = EMA(df_copy, 'close', pre_smoothing_period)
        df_copy['high'] = EMA(df_copy, 'high', pre_smoothing_period)
        df_copy['low'] = EMA(df_copy, 'low', pre_smoothing_period)

    # Regular Heikin Ashi calculations
    df_copy['HA_Close'] = (df_copy['open'] + df_copy['high'] +
                           df_copy['low'] + df_copy['close']) / 4
    df_copy.reset_index(inplace=True)
    ha_open = [(df_copy['open'][0] + df_copy['close'][0]) / 2]
    [ha_open.append((ha_open[i] + df_copy['HA_Close'].values[i]) / 2)
     for i in range(0, len(df_copy) - 1)]
    df_copy['HA_Open'] = ha_open
    df_copy.set_index('index', inplace=True)
    df_copy['HA_High'] = df_copy[['HA_Open', 'HA_Close', 'high']].max(axis=1)
    df_copy['HA_Low'] = df_copy[['HA_Open', 'HA_Close', 'low']].min(axis=1)

    # If post-smoothing is required
    if post_smoothing_period:
        df_copy['HA_Open'] = EMA(df_copy, 'HA_Open', post_smoothing_period)
        df_copy['HA_High'] = EMA(df_copy, 'HA_High', post_smoothing_period)
        df_copy['HA_Low'] = EMA(df_copy, 'HA_Low', post_smoothing_period)
        df_copy['HA_Close'] = EMA(df_copy, 'HA_Close', post_smoothing_period)

    return df_copy[['HA_Open', 'HA_High', 'HA_Low', 'HA_Close']]
