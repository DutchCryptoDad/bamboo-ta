# -*- coding: utf-8 -*-
# volatility.py
import numpy as np
import pandas as pd


def Average_True_Range(df, period=14):
# def ATR(df, period=14):
    """
    Average True Range (ATR)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high', 'low', and 'close'.
    - period (int): Period for the ATR calculation. Default is 14.

    Call with:
        atr = Average_True_Range(df)
        df['atr'] = atr

    Returns:
    - pd.Series: Series of ATR values.
    """
    df_copy = df.copy()
    df_copy['high_low'] = df_copy['high'] - df_copy['low']
    df_copy['high_close'] = (df_copy['high'] - df_copy['close'].shift()).abs()
    df_copy['low_close'] = (df_copy['low'] - df_copy['close'].shift()).abs()
    df_copy['true_range'] = df_copy[['high_low', 'high_close', 'low_close']].max(axis=1)
    df_copy['atr'] = df_copy['true_range'].rolling(window=period, min_periods=1).mean()

    return df_copy['atr']


def Bollinger_Bands(df, column="close", period=20, std_dev=2, ddof=0):
    """
    Bollinger Bands (BBANDS)

    Call with:
        bb_result = bta.Bollinger_Bands(df, "close", 21, 2, 0)
        df['bb_upper'] = bb_result['BB_upper']
        df['bb_middle'] = bb_result['BB_middle']
        df['bb_lower'] = bb_result['BB_lower']

    Args:
    df (pd.DataFrame): DataFrame containing the data
    column (str): The column name on which the BBANDS is to be applied
    period (int): Look-back period to compute the moving average
    std_dev (int): Number of standard deviations to compute the upper and lower bands
    ddof (int): Degrees of Freedom to use in standard deviation calculation. Default: 0

    Returns:
    pd.DataFrame: DataFrame with 'Upper_Band', 'Middle_Band', 'Lower_Band' columns added.
    """

    # Local import to avoid circular dependency
    from .trend import SMA

    # Middle Band = SMA
    sma = SMA(df, column=column, period=period)

    # Calculate standard deviation of the specified column
    rolling_std = df[column].rolling(window=period).std(ddof=ddof)

    # Upper Band = Middle Band + (std_dev * rolling standard deviation)
    upper_band = sma + (rolling_std * std_dev)

    # Lower Band = Middle Band - (std_dev * rolling standard deviation)
    lower_band = sma - (rolling_std * std_dev)

    # Returning as DataFrame
    return pd.DataFrame({
        'BB_upper': upper_band,
        'BB_middle': sma,
        'BB_lower': lower_band
    })


# def TR(df):
#     """
#     True Range (TR) calculation.
    
#     Parameters:
#     - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high', 'low', and 'close'.
    
#     Returns:
#     - pandas.Series: A series of True Range values.
#     """
#     high_low = df['high'] - df['low']
#     high_close = np.abs(df['high'] - df['close'].shift())
#     low_close = np.abs(df['low'] - df['close'].shift())

#     tr = high_low.combine(high_close, max).combine(low_close, max)
#     return tr


def True_Range(df):
    """
    Calculate True Range (TR)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.

    Call with:
        tr = True_Range(df)
        df['true_range'] = tr

    Returns:
    - pd.Series: Series of True Range values.
    """
    df_copy = df.copy()
    prev_close = df_copy['close'].shift()
    df_copy['true_range'] = pd.concat([df_copy['high'] - df_copy['low'], abs(df_copy['high'] - prev_close), abs(df_copy['low'] - prev_close)], axis=1).max(axis=1)

    return df_copy['true_range']


'''
TODO:
KeltnerChannel (+ width)
DonchianChannel (+ width)
Ulcer Index

    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ulcer_index

Bollingerbands width and more

'''