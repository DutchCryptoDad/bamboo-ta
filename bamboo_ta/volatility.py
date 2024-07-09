# -*- coding: utf-8 -*-
# volatility.py
import numpy as np
import pandas as pd

def BollingerBands(df, column="close", period=20, std_dev=2, ddof=0):
    """
    Bollinger Bands (BBANDS)

    Call with:
        bb_result = bta.BollingerBands(df, "close", 21, 2, 0)
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


def TR(df):
    """
    True Range (TR) calculation.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high', 'low', and 'close'.
    
    Returns:
    - pandas.Series: A series of True Range values.
    """
    high_low = df['high'] - df['low']
    high_close = np.abs(df['high'] - df['close'].shift())
    low_close = np.abs(df['low'] - df['close'].shift())

    tr = high_low.combine(high_close, max).combine(low_close, max)
    return tr