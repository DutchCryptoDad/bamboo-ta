# -*- coding: utf-8 -*-
# chande_kroll_stop.py

import pandas as pd
import numpy as np


def chande_kroll_stop(
    df: pd.DataFrame,
    atr_length: int = 10,
    atr_scalar: float = 1.0,
    stop_length: int = 9,
    trading_view_mode: bool = True
) -> pd.DataFrame:
    """Chande Kroll Stop (CKSP)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    atr_length = int(atr_length) if atr_length > 0 else 10
    atr_scalar = float(atr_scalar) if atr_scalar > 0 else 1.0 if trading_view_mode else 3.0
    stop_length = int(stop_length) if stop_length > 0 else 9 if trading_view_mode else 20
    
    # Calculate True Range
    tr1 = df_copy["high"] - df_copy["low"]
    tr2 = abs(df_copy["high"] - df_copy["close"].shift(1))
    tr3 = abs(df_copy["low"] - df_copy["close"].shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate ATR based on the mode
    if trading_view_mode:
        # Using RMA (Wilder's Moving Average) method
        atr = true_range.ewm(alpha=1/atr_length, adjust=False).mean()
    else:
        # Using SMA method
        atr = true_range.rolling(window=atr_length).mean()
    
    # Calculate initial stop values
    long_stop_initial = df_copy["high"].rolling(window=atr_length).max() - atr_scalar * atr
    short_stop_initial = df_copy["low"].rolling(window=atr_length).min() + atr_scalar * atr
    
    # Calculate final stop values
    df_copy["long_stop"] = long_stop_initial.rolling(window=stop_length).max()
    df_copy["short_stop"] = short_stop_initial.rolling(window=stop_length).min()
    
    return df_copy[["long_stop", "short_stop"]]


chande_kroll_stop.__doc__ = \
"""
Name:
    Chande Kroll Stop (CKSP)

Description:
    The Chande Kroll Stop was developed by Tushar Chande and Stanley Kroll in their book
    "The New Technical Trader". It is a trend-following indicator that creates dynamic 
    stop-loss levels based on market volatility measured by the Average True Range (ATR).
    
    The indicator generates two lines:
    - Long Stop: Used as a trailing stop for long positions
    - Short Stop: Used as a trailing stop for short positions
    
    The calculation can be done in two modes:
    - TradingView mode: Uses RMA for ATR and defaults to (10, 1, 9) for parameters
    - Book mode: Uses SMA for ATR and defaults to (10, 3, 20) for parameters
    
    Traditional usage involves:
    - Selling when price closes below the Long Stop
    - Buying when price closes above the Short Stop
    - Using the stops as trailing stop-loss levels to protect profits

More info:
    https://www.multicharts.com/discussion/viewtopic.php?t=48914
    "The New Technical Trader", Wiley 1st ed. ISBN 9780471597803, page 95

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - atr_length (int): Period for ATR and first stop calculation. Default is 10.
    - atr_scalar (float): ATR multiplier for stop calculation. Default is 1.0 in TradingView mode, 3.0 in book mode.
    - stop_length (int): Length for the final stop calculation. Default is 9 in TradingView mode, 20 in book mode.
    - trading_view_mode (bool): If True, uses TradingView implementation (RMA for ATR), otherwise uses book implementation (SMA for ATR). Default is True.

Call with:
    result = bta.chande_kroll_stop(df)
    df['long_stop'] = result['long_stop']
    df['short_stop'] = result['short_stop']

Returns:
    pd.DataFrame: DataFrame with 'long_stop' and 'short_stop' columns.
"""


def test():
    """
    Test function for the chande_kroll_stop indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the chande_kroll_stop indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(chande_kroll_stop)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 