# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *
from .volatility import *
# from .utility import *


def Waddah_Attar_Explosion(df, sensitivity=150, fast_length=20, slow_length=40, channel_length=20, mult=2.0):
    """
    Waddah Attar Explosion Indicator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        WAE = bta.Waddah_Attar_Explosion(df)
        df['trend_up'] = WAE['trend_up']
        df['trend_down'] = WAE['trend_down']
        df['explosion_line'] = WAE['explosion_line']
        df['dead_zone_line'] = WAE['dead_zone_line']

    Returns:
    - pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    print("DataFrame columns:", df.columns)  # Debug print
    print("First few rows of the DataFrame:\n", df.head())  # Debug print

    # Calculate DEAD_ZONE
    dead_zone = RMA(TR(df), 100) * 3.7
    print("DEAD_ZONE calculated")  # Debug print

    # Calculate MACD
    macd_fast = EMA(df, 'close', fast_length)
    macd_slow = EMA(df, 'close', slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity
    print("MACD and t1 calculated")  # Debug print

    # Calculate Bollinger Bands
    bb = BollingerBands(df, column='close', period=channel_length, std_dev=mult)
    e1 = bb['BB_upper'] - bb['BB_lower']
    print("Bollinger Bands calculated")  # Debug print

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy['trend_up'] = trend_up.round(2)
    df_copy['trend_down'] = trend_down.round(2)
    df_copy['explosion_line'] = e1.round(2)
    df_copy['dead_zone_line'] = dead_zone.round(2)

    return df_copy[['trend_up', 'trend_down', 'explosion_line', 'dead_zone_line']]


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
