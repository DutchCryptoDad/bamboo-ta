# -*- coding: utf-8 -*-
# volatility.py
import numpy as np
import pandas as pd


def average_true_range(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """
    Average True Range (ATR)

    The Average True Range (ATR), smoothed by the Moving Average, is a measure of volatility. It was introduced by Welles Wilder in his book 'New Concepts in Technical Trading Systems'.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high', 'low', and 'close'.
    - period (int): Period for the ATR calculation. Default is 14.

    Call with:
        df['atr'] = bta.average_true_range(df, 14)['atr']

    Returns:
    - pd.DataFrame: DataFrame with 'atr' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate True Range components
    df_copy['high_low'] = df_copy['high'] - df_copy['low']
    df_copy['high_close'] = (df_copy['high'] - df_copy['close'].shift()).abs()
    df_copy['low_close'] = (df_copy['low'] - df_copy['close'].shift()).abs()

    # Calculate True Range
    df_copy['true_range'] = df_copy[['high_low', 'high_close', 'low_close']].max(axis=1)

    # Calculate ATR as the rolling mean of True Range
    df_copy['atr'] = df_copy['true_range'].rolling(window=period, min_periods=1).mean()

    return df_copy[['atr']]


def bollinger_bands(df: pd.DataFrame, column: str = 'close', period: int = 20, std_dev: float = 2.0, ddof: int = 0) -> pd.DataFrame:
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
        bb_result = bta.bollinger_bands(df, 'close', 20, 2, 0)
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
    df_copy['bb_upper'] = sma + (rolling_std * std_dev)
    df_copy['bb_middle'] = sma
    df_copy['bb_lower'] = sma - (rolling_std * std_dev)

    return df_copy[['bb_upper', 'bb_middle', 'bb_lower']]


def bbw_expansion(df: pd.DataFrame, upper_band: str = 'bb_upper', lower_band: str = 'bb_lower', 
                  middle_band: str = 'bb_middle', mult: float = 1.05, rolling_window: int = 20) -> pd.DataFrame:
    """
    Bollinger Band Width (BBW) Expansion Detector

    Detects if the Bollinger Band Width (BBW) of the last observation exceeds a 
    rolling maximum by a specified multiplier. This can signal a potential increase 
    in market volatility.
    This indicator requires the bta.bollinger_bands function to be used in the dataframe too.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing Bollinger Band columns.
    - upper_band (str): Column name for the upper Bollinger Band. Default is 'bb_upper'.
    - lower_band (str): Column name for the lower Bollinger Band. Default is 'bb_lower'.
    - middle_band (str): Column name for the middle Bollinger Band. Default is 'bb_middle'.
    - mult (float): Multiplier to compare the last BBW value against the rolling maximum. Default is 1.1.
    - rolling_window (int): Rolling window size for calculating the maximum BBW. Default is 20.

    Call with:
        df['bbw_expansion'] = bta.bbw_expansion(df, upper_band='bb_upper', lower_band='bb_lower', 
                                                middle_band='bb_middle', mult=1.1, rolling_window=20)['bbw_expansion']

    Returns:
    - pd.DataFrame: DataFrame with additional columns:
        - 'bb_width': Bollinger Band Width values.
        - 'bbw_expansion': Indicator for expansion (1 if condition met, 0 otherwise).
    """
    # Create a copy of the DataFrame to prevent modifying the original
    df_copy = df.copy()

    # Calculate the Bollinger Band Width (BBW)
    df_copy['bb_width'] = (df_copy[upper_band] - df_copy[lower_band]) / df_copy[middle_band]

    # Calculate the rolling maximum of BBW
    df_copy['rolling_max'] = df_copy['bb_width'].rolling(window=rolling_window).max()

    # Detect expansion where the BBW exceeds the rolling max by the multiplier
    df_copy['bbw_expansion'] = (df_copy['bb_width'] > (df_copy['rolling_max'] * mult)).astype(int)

    # Return the DataFrame with the calculated columns
    return df_copy[['bb_width', 'bbw_expansion']]


def true_range(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate True Range (TR)

    The True Range indicator measures market volatility. True Range is defined as the greatest of the following:
    - The current high minus the current low
    - The absolute value of the current high minus the previous close
    - The absolute value of the current low minus the previous close

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.

    Call with:
        df['true_range'] = bta.true_range(df)['true_range']

    Returns:
    - pd.DataFrame: DataFrame with 'true_range' column.
    """
    df_copy = df.copy()
    prev_close = df_copy['close'].shift()
    
    # Calculate the true range components
    true_range = pd.concat(
        [
            df_copy['high'] - df_copy['low'],
            (df_copy['high'] - prev_close).abs(),
            (df_copy['low'] - prev_close).abs()
        ], axis=1
    ).max(axis=1)

    df_copy['true_range'] = true_range

    return df_copy[['true_range']]

'''
TODO:
KeltnerChannel (+ width)
DonchianChannel (+ width)
Ulcer Index

    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ulcer_index

Bollingerbands width and more

'''