# -*- coding: utf-8 -*-
# brar.py

import pandas as pd
import numpy as np


def brar(df: pd.DataFrame, length: int = 26, scalar: float = 100, drift: int = 1) -> pd.DataFrame:
    """BR and AR Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate high-open and open-low ranges
    high_open_range = df_copy["high"] - df_copy["open"]
    open_low_range = df_copy["open"] - df_copy["low"]
    
    # Make sure no division by zero (replace zeros with NaN)
    open_low_range = open_low_range.replace(0, np.nan)
    
    # Calculate high-close[yesterday] and close[yesterday]-low
    previous_close = df_copy["close"].shift(drift)
    hcy = df_copy["high"] - previous_close
    cyl = previous_close - df_copy["low"]
    
    # Zero out negative values
    hcy = hcy.where(hcy > 0, 0)
    cyl = cyl.where(cyl > 0, 0)
    
    # Make sure no division by zero for BR calculation
    cyl_sum = cyl.rolling(window=length).sum()
    cyl_sum = cyl_sum.replace(0, np.nan)
    
    # Calculate AR and BR
    ar = scalar * high_open_range.rolling(window=length).sum() / open_low_range.rolling(window=length).sum()
    br = scalar * hcy.rolling(window=length).sum() / cyl_sum
    
    # Prepare the result
    df_copy["ar"] = ar
    df_copy["br"] = br
    
    return df_copy[["ar", "br"]]


brar.__doc__ = \
"""
Name:
    BR and AR

Description:
    BR (Bias Ratio) and AR (Arbiter Ratio) are momentum indicators commonly used
    in Asian markets. They measure buying and selling pressure by comparing price
    movements to open, high, low, and close values.
    
    AR compares the strength of the bulls (high - open) versus the bears (open - low).
    BR compares today's high with yesterday's close (bulls) versus yesterday's close
    with today's low (bears).
    
    Values above 100 indicate bullish strength, while values below 100 indicate
    bearish strength. Extreme readings may indicate overbought or oversold conditions.

More info:
    This indicator is particularly popular in Chinese and other Asian markets.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low',
      and 'close' columns.
    - length (int): Lookback period for calculations. Default is 26.
    - scalar (float): Multiplier for the ratio. Default is 100.
    - drift (int): The difference period for previous close. Default is 1.

Call with:
    result = bta.brar(df)
    df['ar'] = result['ar']
    df['br'] = result['br']

Returns:
    pd.DataFrame: DataFrame with 'ar' and 'br' columns.
"""


def test():
    """
    Test function for the brar indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the brar indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(brar)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 