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
        ha_df = bta.HeikinAshi(df)

    - With pre-smoothing of the original data:
        ha_df = bta.HeikinAshi(df, pre_smoothing_period=14)

    - With both pre and post smoothing:
        ha_df = bta.HeikinAshi(df, pre_smoothing_period=14, post_smoothing_period=14)

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


def LinRegCandles(df, linreg_length=11, sma_signal=True, signal_length=11):
    """
    Linear Regression Candles with Optional Signal Line

    Call with:
    - Regular Linear Regression Candles with SMA signal line:
        lr_df = bta.LinRegCandles(df)

    - With EMA signal line:
        lr_df = bta.LinRegCandles(df, sma_signal=False)

    - With SMA signal line:
        lr_df = bta.LinRegCandles(df, sma_signal=True)

    After calling, the following columns can be extracted:
        df['LRC_Open'] = lr_df['bopen']
        df['LRC_High'] = lr_df['bhigh']
        df['LRC_Low'] = lr_df['blow']
        df['LRC_Close'] = lr_df['bclose']
        df['LRC_Signal'] = lr_df['signal']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - linreg_length (int, optional): Period for linear regression calculation. Default is 11.
    - sma_signal (bool, optional): If True, uses SMA for the signal line. If False, uses EMA. Default is True.
    - signal_length (int, optional): Period for the moving average signal line. Default is 11.

    Returns:
    - pd.DataFrame: DataFrame with 'bopen', 'bhigh', 'blow', 'bclose' as the Linear Regression Candles, and 'signal' as the signal line.

    Description:
    The Linear Regression Candles transform the traditional OHLC bars using a linear regression algorithm, providing a smoothed representation of price action. The function also provides an optional signal line, which can be either an SMA or an EMA of the Linear Regression Candle close. This signal line can help to identify trends and potential trading signals.
    """
    df_copy = df.copy()

    # Calculate linear regression coefficients for open, high, low, and close
    df_copy['bopen'] = df_copy['open'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[
            1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['bhigh'] = df_copy['high'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[
            1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['blow'] = df_copy['low'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[
            1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['bclose'] = df_copy['close'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[
            1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    # Calculate the signal line using SMA or EMA
    if sma_signal:
        df_copy['signal'] = df_copy['bclose'].rolling(
            window=signal_length).mean()
    else:
        df_copy['signal'] = df_copy['bclose'].ewm(
            span=signal_length, adjust=False).mean()

    return df_copy
