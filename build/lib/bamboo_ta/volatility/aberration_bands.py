# -*- coding: utf-8 -*-
# aberration_bands.py

import pandas as pd
import numpy as np


def aberration_bands(
    df: pd.DataFrame, length: int = 5, atr_length: int = 15
) -> pd.DataFrame:
    """Aberration Bands (ABER)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 5
    atr_length = int(atr_length) if atr_length > 0 else 15
    
    # Calculate typical price (HLC3)
    df_copy["tp"] = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3
    
    # Calculate ATR
    high_low = df_copy["high"] - df_copy["low"]
    high_close_prev = abs(df_copy["high"] - df_copy["close"].shift(1))
    low_close_prev = abs(df_copy["low"] - df_copy["close"].shift(1))
    
    # True Range
    tr = pd.DataFrame({
        "hl": high_low,
        "hc": high_close_prev,
        "lc": low_close_prev
    }).max(axis=1)
    
    # ATR
    atr = tr.rolling(window=atr_length).mean()
    
    # Calculate Aberration Bands
    zg = df_copy["tp"].rolling(window=length).mean()  # Middle band (SMA of typical price)
    sg = zg + atr  # Upper band (middle + ATR)
    xg = zg - atr  # Lower band (middle - ATR)
    
    # Store results
    df_copy["aber_middle"] = zg
    df_copy["aber_upper"] = sg
    df_copy["aber_lower"] = xg
    df_copy["aber_atr"] = atr
    
    return df_copy[["aber_middle", "aber_upper", "aber_lower", "aber_atr"]]


aberration_bands.__doc__ = \
"""
Name:
    Aberration Bands (ABER)

Description:
    Aberration Bands are a volatility-based indicator similar to Keltner Channels.
    The indicator consists of three bands:
    - Middle band: Simple Moving Average of the typical price (HLC3)
    - Upper band: Middle band + Average True Range
    - Lower band: Middle band - Average True Range
    
    These bands can be used to identify overbought and oversold conditions,
    as well as potential breakout opportunities when price moves outside the bands.

More info:
    There are few definitive resources on this indicator, as it is less commonly used
    than other volatility-based bands like Bollinger Bands or Keltner Channels.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for the SMA calculation. Default is 5.
    - atr_length (int): The period for the ATR calculation. Default is 15.

Call with:
    result = bta.aberration_bands(df)
    df['aber_middle'] = result['aber_middle']
    df['aber_upper'] = result['aber_upper']
    df['aber_lower'] = result['aber_lower']
    df['aber_atr'] = result['aber_atr']

Returns:
    pd.DataFrame: DataFrame with 'aber_middle', 'aber_upper', 'aber_lower', and 'aber_atr' columns.
"""


def test():
    """
    Test function for the aberration_bands indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the aberration_bands indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(aberration_bands)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 