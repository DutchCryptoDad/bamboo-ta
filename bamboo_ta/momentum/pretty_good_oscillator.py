# -*- coding: utf-8 -*-
# pretty_good_oscillator.py

import pandas as pd
import numpy as np


def pretty_good_oscillator(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
    """Pretty Good Oscillator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate SMA of close
    sma_close = df_copy["close"].rolling(window=length).mean()
    
    # Calculate ATR (Average True Range)
    tr = pd.DataFrame(index=df_copy.index)
    tr['hl'] = df_copy["high"] - df_copy["low"]
    tr['hc'] = (df_copy["high"] - df_copy["close"].shift(1)).abs()
    tr['lc'] = (df_copy["low"] - df_copy["close"].shift(1)).abs()
    atr = tr[['hl', 'hc', 'lc']].max(axis=1)
    
    # Calculate EMA of ATR
    ema_atr = atr.ewm(span=length, adjust=False).mean()
    
    # Calculate PGO
    df_copy["pgo"] = (df_copy["close"] - sma_close) / ema_atr
    
    return df_copy[["pgo"]]


pretty_good_oscillator.__doc__ = \
"""
Name:
    Pretty Good Oscillator

Description:
    The Pretty Good Oscillator (PGO) was created by Mark Johnson to measure the distance 
    of the current close price from its N-day Simple Moving Average (SMA), expressed in 
    terms of an average true range (ATR) over a similar period.
    
    Unlike traditional oscillators that are bounded within specified ranges, the PGO's 
    values can extend beyond traditional bounds, providing signals for potentially strong 
    trending moves. Readings above +3.0 indicate potentially strong bullish price moves, 
    while readings below -3.0 indicate potentially strong bearish price moves.
    
    Johnson designed this as a breakout system for longer-term trades, going long when 
    the indicator is greater than 3.0 and short when less than -3.0.

More info:
    https://library.tradingtechnologies.com/trade/chrt-ti-pretty-good-oscillator.html

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - length (int): The period for calculations. Default is 14.

Call with:
    df['pgo'] = bta.pretty_good_oscillator(df)['pgo']

Returns:
    pd.DataFrame: DataFrame with 'pgo' column.
"""


def test():
    """
    Test function for the pretty_good_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the pretty_good_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(pretty_good_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 