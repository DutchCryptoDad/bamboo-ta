# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *


def RSI(df, column="close", period=14):
    """
    Relative Strength Index (RSI)

    Call with:
        df['rsi'] = bta.RSI(df, "close", 14)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which RSI is to be calculated. Default is "close".
    - period (int): The period over which RSI is to be calculated. Default is 14.

    Returns:
    - pandas.Series: A series of RSI values.

    Description:
    RSI measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset.
    """
    delta = df[column].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    for i in range(period, len(df)):
        avg_gain[i] = (avg_gain[i-1] * (period - 1) + gain[i]) / period
        avg_loss[i] = (avg_loss[i-1] * (period - 1) + loss[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def MACD(df, column="close", short_window=12, long_window=26, signal_window=9):
    """
    Moving Average Convergence Divergence (MACD)

    Call with:
        macd_result = bta.MACD(df, "close", 12, 26, 9)
        df['macd'] = macd_result['MACD']
        df['macd_signal'] = macd_result['MACD_signal']
        df['macd_histogram'] = macd_result['MACD_histogram']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - signal_window (int): The signal line period for EMA. Default is 9.

    Returns:
    - pd.DataFrame: DataFrame with 'MACD', 'Signal', and 'Histogram' columns.

    Description:
    MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.
    """
    short_ema = EMA(df, column=column, period=short_window)
    long_ema = EMA(df, column=column, period=long_window)
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    histogram = macd - signal

    # Returning as DataFrame
    return pd.DataFrame({
        'MACD': macd,
        'MACD_signal': signal,
        'MACD_histogram': histogram
    })


def EWO(df, column="close", sma1_period=5, sma2_period=35):
    """
    Elliott Wave Oscillator (EWO)

    Call with:
        df['ewo'] = bta.EWO(df, "close", 5, 35)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EWO is to be calculated. Default is "close".
    - sma1_period (int): The period for the shorter SMA used in EWO calculation. Default is 5.
    - sma2_period (int): The period for the longer SMA used in EWO calculation. Default is 35.

    Returns:
    - pandas.Series: A series of EWO values.

    Description:
    The Elliott Wave Oscillator (EWO) is a specific tool to help you identify the trend and the overall market pattern to assist in finding future trading opportunities. It is derived by calculating the difference between a short and long period simple moving average, then normalizing the result with the close price.
    """
    sma1 = df[column].rolling(window=sma1_period).mean()
    sma2 = df[column].rolling(window=sma2_period).mean()
    ewo = (sma1 - sma2) / df[column] * 100

    return ewo
