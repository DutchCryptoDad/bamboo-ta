# -*- coding: utf-8 -*-
# vortex_indicator.py

import pandas as pd
import numpy as np


def vortex_indicator(
    df: pd.DataFrame,
    length: int = 14,
    drift: int = 1
) -> pd.DataFrame:
    """Vortex Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 14
    drift = int(drift) if drift > 0 else 1
    
    # Calculate True Range
    high = df_copy["high"]
    low = df_copy["low"]
    close = df_copy["close"]
    
    # True Range calculation
    prev_close = close.shift(1)
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    tr = pd.DataFrame({
        "tr1": tr1,
        "tr2": tr2,
        "tr3": tr3
    }).max(axis=1)
    
    # Sum of True Range over the period
    tr_sum = tr.rolling(window=length).sum()
    
    # Calculate Positive and Negative Vortex Movements
    # Positive VM: |Current High - Previous Low|
    vm_plus = (high - low.shift(drift)).abs()
    
    # Negative VM: |Current Low - Previous High|
    vm_minus = (low - high.shift(drift)).abs()
    
    # Sum of VM over the period
    vm_plus_sum = vm_plus.rolling(window=length).sum()
    vm_minus_sum = vm_minus.rolling(window=length).sum()
    
    # Calculate Vortex Indicator values
    # Positive VI
    vi_plus = vm_plus_sum / tr_sum
    
    # Negative VI
    vi_minus = vm_minus_sum / tr_sum
    
    # Store results in DataFrame
    df_copy["vi_plus"] = vi_plus
    df_copy["vi_minus"] = vi_minus
    
    return df_copy[["vi_plus", "vi_minus"]]


vortex_indicator.__doc__ = \
"""
Name:
    Vortex Indicator

Description:
    The Vortex Indicator is a technical analysis indicator composed of two oscillating 
    lines - VI+ (positive) and VI- (negative). These lines capture positive and negative 
    trend movement and are designed to identify the start of a new trend or the continuation 
    of an existing trend.
    
    The indicator works by comparing the current price to the previous price, in relation 
    to the true range. When VI+ crosses above VI-, it may indicate the start of a new 
    uptrend. Conversely, when VI- crosses above VI+, it may signal the beginning of a 
    new downtrend.
    
    The Vortex Indicator is particularly useful for trend identification and confirmation,
    and is often used in conjunction with other technical indicators.

More info:
    https://school.stockcharts.com/doku.php?id=technical_indicators:vortex_indicator

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for calculating the indicator. Default is 14.
    - drift (int): The difference period for VM calculations. Default is 1.

Call with:
    result = bta.vortex_indicator(df, length=14)
    df['vi_plus'] = result['vi_plus']  # Positive Vortex Indicator line
    df['vi_minus'] = result['vi_minus']  # Negative Vortex Indicator line

Returns:
    pd.DataFrame: DataFrame with 'vi_plus' and 'vi_minus' columns containing the indicator values.
"""


def test():
    """
    Test function for the vortex_indicator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the vortex_indicator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(vortex_indicator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 