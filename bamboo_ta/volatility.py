# -*- coding: utf-8 -*-
# volatility.py
import numpy as np
import pandas as pd


def AverageTrueRange(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Average True Range (ATR)

    The Average True Range (ATR), smoothed by the Moving Average, is a measure of volatility. It was introduced by Welles Wilder in his book 'New Concepts in Technical Trading Systems'.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high', 'low', and 'close'.
    - period (int): Period for the ATR calculation. Default is 14.

    Call with:
        df['atr'] = bta.AverageTrueRange(df, 14)['atr']

    Returns:
    - pd.DataFrame: DataFrame with 'atr' column.
    """
    df_copy = df.copy()
    df_copy['high_low'] = df_copy['high'] - df_copy['low']
    df_copy['high_close'] = (df_copy['high'] - df_copy['close'].shift()).abs()
    df_copy['low_close'] = (df_copy['low'] - df_copy['close'].shift()).abs()
    df_copy['true_range'] = df_copy[['high_low', 'high_close', 'low_close']].max(axis=1)
    df_copy['atr'] = df_copy['true_range'].rolling(window=period, min_periods=1).mean().round(2)

    return df_copy[['atr']]


def BollingerBands(df: pd.DataFrame, column: str = 'close', period: int = 20, std_dev: float = 2.0, ddof: int = 0) -> pd.DataFrame:
    """
    Bollinger Bands (BBANDS)

    Bollinger Bands are a type of statistical chart characterizing the prices and volatility over time of a financial instrument or commodity.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the BBANDS is to be applied. Default is 'close'.
    - period (int): Look-back period to compute the moving average. Default is 20.
    - std_dev (float): Number of standard deviations to compute the upper and lower bands. Default is 2.0.
    - ddof (int): Degrees of Freedom to use in standard deviation calculation. Default is 0.

    Call with:
        bb_result = bta.BollingerBands(df, 'close', 20, 2, 0)
        df['bb_upper'] = bb_result['bb_upper']
        df['bb_middle'] = bb_result['bb_middle']
        df['bb_lower'] = bb_result['bb_lower']

    Returns:
    - pd.DataFrame: DataFrame with 'bb_upper', 'bb_middle', 'bb_lower' columns.
    """
    df_copy = df.copy()

    # Calculate middle band (SMA)
    sma = df_copy[column].rolling(window=period).mean()

    # Calculate standard deviation of the specified column
    rolling_std = df_copy[column].rolling(window=period).std(ddof=ddof)

    # Calculate upper and lower bands
    df_copy['bb_upper'] = (sma + (rolling_std * std_dev)).round(2)
    df_copy['bb_middle'] = sma.round(2)
    df_copy['bb_lower'] = (sma - (rolling_std * std_dev)).round(2)

    return df_copy[['bb_upper', 'bb_middle', 'bb_lower']]


def TrueRange(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate True Range (TR)

    The True Range indicator measures market volatility. True Range is defined as the greatest of the following:
    - The current high minus the current low
    - The absolute value of the current high minus the previous close
    - The absolute value of the current low minus the previous close

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.

    Call with:
        df['true_range'] = bta.TrueRange(df)['true_range']

    Returns:
    - pd.DataFrame: DataFrame with 'true_range' column.
    """
    df_copy = df.copy()
    prev_close = df_copy['close'].shift()
    df_copy['true_range'] = pd.concat(
        [
            df_copy['high'] - df_copy['low'],
            (df_copy['high'] - prev_close).abs(),
            (df_copy['low'] - prev_close).abs()
        ], axis=1
    ).max(axis=1).round(2)

    return df_copy[['true_range']]

'''
TODO:
KeltnerChannel (+ width)
DonchianChannel (+ width)
Ulcer Index

    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ulcer_index

Bollingerbands width and more

'''