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
