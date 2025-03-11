# -*- coding: utf-8 -*-
# average_directional_index.py

import pandas as pd
import numpy as np


def average_directional_index(
    df: pd.DataFrame, 
    length: int = 14, 
    signal_length: int = 14, 
    scalar: float = 100,
    drift: int = 1
) -> pd.DataFrame:
    """Average Directional Movement (ADX)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 14
    signal_length = int(signal_length) if signal_length > 0 else length
    scalar = float(scalar) if scalar > 0 else 100
    drift = int(drift) if drift > 0 else 1
    
    # Calculate ATR
    high, low, close = df_copy["high"], df_copy["low"], df_copy["close"]
    
    # True Range
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Average True Range
    atr = true_range.rolling(window=length).mean()
    
    # Calculate directional movement
    up_move = high - high.shift(drift)
    down_move = low.shift(drift) - low
    
    # Positive and negative directional movement
    pos_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
    neg_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
    
    # Calculate smoothed directional movement (using RMA method)
    pos_dm_ema = pd.Series(pos_dm).ewm(alpha=1/length, adjust=False).mean()
    neg_dm_ema = pd.Series(neg_dm).ewm(alpha=1/length, adjust=False).mean()
    
    # Calculate directional indicators
    k = scalar / atr
    dmp = k * pos_dm_ema
    dmn = k * neg_dm_ema
    
    # Calculate directional index
    dx = scalar * abs(dmp - dmn) / (dmp + dmn).replace(0, np.nan)
    
    # Calculate average directional index
    adx = dx.ewm(alpha=1/signal_length, adjust=False).mean()
    
    # Store results
    df_copy["adx"] = adx
    df_copy["dmp"] = dmp
    df_copy["dmn"] = dmn
    
    return df_copy[["adx", "dmp", "dmn"]]


average_directional_index.__doc__ = \
"""
Name:
    Average Directional Movement Index (ADX)

Description:
    The Average Directional Index (ADX) is a technical analysis indicator used to 
    quantify trend strength. It was developed by J. Welles Wilder and is part of 
    the Directional Movement System.
    
    The ADX is non-directional; it registers trend strength whether price is trending 
    up or down. The indicator typically ranges from 0 to 100, with readings above 25 
    indicating a strong trend and readings below 20 indicating a weak or non-trending 
    market.
    
    The ADX is calculated using the Positive Directional Indicator (+DI) and Negative 
    Directional Indicator (-DI), which measure upward and downward price movement 
    respectively. These indicators are included in the output of this function as 
    'dmp' and 'dmn'.
    
    Typical interpretation:
    - ADX > 25: Strong trend (direction determined by +DI and -DI)
    - ADX < 20: Weak or absent trend
    - When +DI crosses above -DI: Potential bullish signal
    - When -DI crosses above +DI: Potential bearish signal

More info:
    https://www.investopedia.com/terms/a/adx.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): Period for calculating directional movement. Default is 14.
    - signal_length (int): Smoothing period for ADX calculation. Default is equal to length.
    - scalar (float): Scaling factor for the indicators. Default is 100.
    - drift (int): The difference period for directional movement. Default is 1.

Call with:
    result = bta.average_directional_index(df)
    df['adx'] = result['adx']
    df['plus_di'] = result['dmp']
    df['minus_di'] = result['dmn']

Returns:
    pd.DataFrame: DataFrame with 'adx', 'dmp' (plus DI), and 'dmn' (minus DI) columns.
"""


def test():
    """
    Test function for the average_directional_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the average_directional_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(average_directional_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 