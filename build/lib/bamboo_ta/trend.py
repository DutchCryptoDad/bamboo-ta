# -*- coding: utf-8 -*-
from pandas import DataFrame
import math
import numpy as np
import pandas as pd
# from .bamboo_ta import *
from .volatility import BollingerBands
# from .trend import SMA, EMA, LSMA, HMA, WMA


def AlligatorBands(df, column="close", jaw_period=13, teeth_period=8, lips_period=5, jaw_shift=8, teeth_shift=5, lips_shift=3):
    """
    Bill Williams Alligator Indicator

    Call with:
        alligator_result = bta.AlligatorBands(df, "high", 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
        df['jaw'] = alligator_result['jaw']
        df['teeth'] = alligator_result['teeth']
        df['lips'] = alligator_result['lips']

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    column (str): The column name on which the Alligator is to be applied. Default is "close".
    jaw_period (int): Period for the Alligator's Jaw (blue line). Default is 13.
    teeth_period (int): Period for the Alligator's Teeth (red line). Default is 8.
    lips_period (int): Period for the Alligator's Lips (green line). Default is 5.
    jaw_shift (int): Number of periods to shift the Jaw line into the future. Default is 8.
    teeth_shift (int): Number of periods to shift the Teeth line into the future. Default is 5.
    lips_shift (int): Number of periods to shift the Lips line into the future. Default is 3.

    Returns:
    pd.DataFrame: DataFrame with 'jaw', 'teeth', and 'lips' columns added, optionally shifted into the future.
    """

    df['jaw'] = df[column].rolling(window=jaw_period).mean().shift(jaw_shift)
    df['teeth'] = df[column].rolling(
        window=teeth_period).mean().shift(teeth_shift)
    df['lips'] = df[column].rolling(
        window=lips_period).mean().shift(lips_shift)

    return df[['jaw', 'teeth', 'lips']]


def BollingerTrend(df, column="close", short_length=20, long_length=50, std_dev=2.0):
    """
    Bollinger Trend Indicator

    Call with:
        df['BBTrend'] = bta.BollingerTrend(df, "close", 20, 50, 2.0)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is "close".
    - short_length (int): The period for the short Bollinger Bands. Default is 20.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - stddev (float): The standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Returns:
    - pandas.Series: A series of BBTrend values.
    """
    # Calculate short Bollinger Bands
    short_bb = BollingerBands(df, column=column, period=short_length, std_dev=std_dev)
    short_middle = short_bb['BB_middle']
    short_upper = short_bb['BB_upper']
    short_lower = short_bb['BB_lower']

    # Calculate long Bollinger Bands
    long_bb = BollingerBands(df, column=column, period=long_length, std_dev=std_dev)
    long_middle = long_bb['BB_middle']
    long_upper = long_bb['BB_upper']
    long_lower = long_bb['BB_lower']

    # Calculate BBTrend
    bbtrend = (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper)) / short_middle * 100
    bbtrend = bbtrend.round(2)
    
    return bbtrend


def BollingerTrendFastWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14):
    """
    Bollinger Trend Indicator with selectable Moving Average

    This function calculates the Bollinger Trend (BBTrend) and applies a selected moving average to the BBTrend.

    Usage:
        BollingerTrendFast = bta.BollingerTrendFastWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14)
        
        df['BollingerTrendFast'] = BollingerTrendFast['BBTrend']
        df['BollingerTrendFastMA'] = BollingerTrendFast['BBTrendMA']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is "close".
    - short_length (int): The period for the short Bollinger Bands. Default is 10.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - short_stddev (float): The standard deviation multiplier for the short Bollinger Bands. Default is 1.0.
    - long_stddev (float): The standard deviation multiplier for the long Bollinger Bands. Default is 2.0.
    - ma_type (str): The type of moving average to use ("SMA", "EMA", "LSMA", "HMA", "WMA"). Default is "SMA".
    - ma_length (int): The period for the moving average. Default is 14.

    Returns:
    - pandas.DataFrame: DataFrame with 'BBTrend' and 'MA' columns.
    
    Example:
        result = BollingerTrendWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14)
        df['BBTrend'] = result['BBTrend']
        df['MA'] = result['MA']
    """

    # Calculate short Bollinger Bands
    short_bb = BollingerBands(df, column=column, period=short_length, std_dev=short_stddev)
    short_middle = short_bb['BB_middle']
    short_upper = short_bb['BB_upper']
    short_lower = short_bb['BB_lower']

    # Calculate long Bollinger Bands
    long_bb = BollingerBands(df, column=column, period=long_length, std_dev=long_stddev)
    long_middle = long_bb['BB_middle']
    long_upper = long_bb['BB_upper']
    long_lower = long_bb['BB_lower']

    # Calculate BBTrend
    bbtrend = (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper)) / short_middle * 100
    bbtrend = bbtrend.round(2)

    # Select and calculate the moving average
    if ma_type == "SMA":
        ma = SMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    elif ma_type == "EMA":
        ma = EMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    elif ma_type == "LSMA":
        ma = LSMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    elif ma_type == "HMA":
        ma = HMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    elif ma_type == "WMA":
        ma = WMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    else:
        raise ValueError("Unsupported moving average type")

    # Returning as DataFrame
    result = df.copy()
    result['BBTrend'] = bbtrend.round(2)
    result['BBTrendMA'] = ma.round(2)

    return result[['BBTrend', 'BBTrendMA']]


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

    ema = df[column].ewm(span=period, adjust=False).mean()
    
    return ema


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

    lsma = pd.Series(lsma_values, index=df.index[period - 1:])

    return lsma


def RMA(series, period):
    """
    Relative Moving Average (RMA) calculation.
    
    Parameters:
    - series (pandas.Series): Input series on which RMA is to be calculated.
    - period (int): The period over which RMA is to be calculated.
    
    Returns:
    - pandas.Series: A series of RMA values.
    """
    return series.ewm(alpha=1/period, adjust=False).mean()


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

    sma = df[column].rolling(window=period).mean()
    
    return sma


def stdev(series, period):
    """
    Calculate the standard deviation over a specified period.

    Parameters:
    - series (pd.Series): The data series to calculate the standard deviation for.
    - period (int): The period over which to calculate the standard deviation.

    Returns:
    - pd.Series: The standard deviation of the series.
    """
    return series.rolling(window=period).std()


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

    wma = numerator / denominator
    
    return wma


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


