# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *


def SMA(df, column="close", period=21):
    """
    Simple Moving Average (SMA)

    Call with:
        df['sma'] = bta.SMA(df, "close", 50)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which SMA is to be calculated. Default is "close".
    - period (int): The period over which SMA is to be calculated. Default is 30.

    Returns:
    - pandas.Series: A series of SMA values.

    Description:
    The Simple Moving Average is the unweighted mean of the previous 'period' data points.
    """
    return df[column].rolling(window=period).mean()


def EMA(df, column="close", period=21):
    """
    Exponential Moving Average (EMA)

    Call with:
        df['ema'] = bta.EMA(df, "close", 50)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EMA is to be calculated. Default is "close".
    - period (int): The period over which EMA is to be calculated. Default is 30.

    Returns:
    - pandas.Series: A series of EMA values.

    Description:
    The Exponential Moving Average gives more weight to recent prices and thus reacts more quickly to price changes than the Simple Moving Average.
    """
    return df[column].ewm(span=period, adjust=False).mean()


def LSMA(df, column="close", period=21):
    """
    Least Squares Moving Average (LSMA)

    Call with:
        df['lsma'] = bta.LSMA(df, "close", 50)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which LSMA is to be calculated. Default is "close".
    - period (int): The period over which LSMA is to be calculated. Default is 21.

    Returns:
    - pandas.Series: A series of LSMA values.

    Description:
    LSMA uses linear regression to compute the trend of the data over a specified period. It fits a straight line to the data points using the method of least squares to depict the direction of movement.
    """
    lsma_values = []

    for i in range(period - 1, len(df)):
        # Extract the most recent N df points
        subset = df.iloc[i + 1 - period:i + 1]

        # Perform linear regression to fit a line
        x = np.arange(len(subset))
        y = subset[column].values
        slope, intercept = np.polyfit(x, y, 1)

        # Calculate the LSMA value using the linear equation
        lsma = intercept + slope * (period - 1)
        lsma_values.append(lsma)

    lsma_series = pd.Series(lsma_values, index=df.index[period - 1:])

    return lsma_series


def SuperTrend(df, column="close", length=7, multiplier=3.0, offset=0):
    """
    Supertrend Indicator

    Call with:
        supertrend_result = bta.SuperTrend(df, "close", 7, 3.0, 0)
        df['supertrend'] = supertrend_result['ST_trend']
        df['supertrend_d'] = supertrend_result['ST_direction']
        df['supertrend_l'] = supertrend_result['ST_long']
        df['supertrend_s'] = supertrend_result['ST_short']


    Args:
    - df (pd.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the Supertrend is to be applied. Default is "close".
    - length (int): The period over which the indicator is to be calculated.
    - multiplier (float): Multiplier for ATR value.
    - offset (int): How many periods to offset the result. Default: 0.

    Returns:
    - Dict[str, pd.Series]: A dictionary with 'ST_trend', 'ST_direction', 'ST_long', and 'ST_short' as keys.
    """

    # Calculate ATR
    atr = multiplier * (df['high'] - df['low']).ewm(span=length).mean()

    # Calculate Supertrend
    hl2 = (df['high'] + df['low']) / 2
    upperband = hl2 + atr
    lowerband = hl2 - atr

    direction = [0]  # Initialize direction to 0
    trend = [np.nan]  # Initial trend value
    long_signal = [np.nan]  # Initial long signal
    short_signal = [np.nan]  # Initial short signal

    for i in range(1, len(df)):
        if df[column][i] > upperband[i - 1]:
            direction.append(1)  # Bullish direction
        elif df[column][i] < lowerband[i - 1]:
            direction.append(-1)  # Bearish direction
        else:
            direction.append(direction[-1])
            if direction[-1] > 0 and lowerband[i] < lowerband[i - 1]:
                lowerband[i] = lowerband[i - 1]
            if direction[-1] < 0 and upperband[i] > upperband[i - 1]:
                upperband[i] = upperband[i - 1]

        if direction[-1] > 0:
            trend.append(lowerband[i])
            long_signal.append(lowerband[i])
            short_signal.append(np.nan)
        else:
            trend.append(upperband[i])
            long_signal.append(np.nan)
            short_signal.append(upperband[i])

    # Apply offset if needed
    if offset != 0:
        trend = pd.Series(trend).shift(offset).tolist()
        direction = pd.Series(direction).shift(offset).tolist()
        long_signal = pd.Series(long_signal).shift(offset).tolist()
        short_signal = pd.Series(short_signal).shift(offset).tolist()

    # Return the values as a dictionary
    return {
        f"ST_trend": pd.Series(trend, index=df.index),
        f"ST_direction": pd.Series(direction, index=df.index),
        f"ST_long": pd.Series(long_signal, index=df.index),
        f"ST_short": pd.Series(short_signal, index=df.index)
    }
