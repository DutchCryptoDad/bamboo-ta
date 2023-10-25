# -*- coding: utf-8 -*-
from pandas import DataFrame
import math
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


def WMA(df, column="close", period=9):
    """
    TradingView-Style Weighted Moving Average (WMA)

    Call with:
        df['wma'] = bta.WMA(df, "close", 9)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which WMA is to be calculated. Default is "close".
    - period (int): The period over which WMA is to be calculated. Default is 9.

    Returns:
    - pandas.Series: A series of WMA values.

    Description:
    The Weighted Moving Average assigns weights linearly. The most recent data gets the highest weight.
    """
    weights = range(1, period + 1)
    numerator = df[column].rolling(window=period).apply(
        lambda x: sum(weights * x), raw=True)
    denominator = sum(weights)
    return numerator / denominator


def HMA(df, column="close", period=9):
    """
    Hull Moving Average (HMA)

    Call with:
        df['hma'] = bta.HMA(df, "close", 9)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which HMA is to be calculated. Default is "close".
    - period (int): The period over which HMA is to be calculated. Default is 9.

    Returns:
    - pandas.Series: A series of HMA values.

    Description:
    Hull Moving Average (HMA) is an improved moving average, responsive and with minimal lag. It involves the combination of WMA (Weighted Moving Average) with different periods.
    """

    # We're assuming that WMA is defined in the same file and thus is accessible here.
    half_length = math.floor(period / 2)
    sqrt_length = math.floor(math.sqrt(period))

    wma_half = WMA(df, column=column, period=half_length)
    wma_full = WMA(df, column=column, period=period)

    h = 2 * wma_half - wma_full
    h_df = DataFrame(h, columns=[column])
    hma = WMA(h_df, column=column, period=sqrt_length)

    return hma


def ZLEMA(df, column="close", period=21):
    """
    Zero Lag Exponential Moving Average (ZLEMA)

    Call with:
        df['zlema'] = bta.ZLEMA(df, "close", 21)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZLEMA is to be calculated. Default is "close".
    - period (int): The period over which ZLEMA is to be calculated. Default is 21.

    Returns:
    - pandas.Series: A series of ZLEMA values.

    Description:
    Zero Lag Exponential Moving Average (ZLEMA) is an EMA that adjusts for lag, making it more responsive to recent price changes. It uses lagged data differences to adjust the EMA calculation, thereby supposedly removing the inherent lag of EMA.
    """
    lag = int((period - 1) / 2)

    # Calculating the adjusted data series
    ema_data = df[column] + (df[column] - df[column].shift(lag))

    # Computing the EMA of the adjusted data series
    zlema = ema_data.ewm(span=period, adjust=False).mean()

    return zlema
