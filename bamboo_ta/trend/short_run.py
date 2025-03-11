# -*- coding: utf-8 -*-
# short_run.py

import pandas as pd
import numpy as np


def short_run(
    df: pd.DataFrame,
    fast_column: str,
    slow_column: str,
    length: int = 2,
    as_int: bool = True
) -> pd.DataFrame:
    """Short Run Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = [fast_column, slow_column]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 2
    
    # Get fast and slow series
    fast = df_copy[fast_column]
    slow = df_copy[slow_column]
    
    # Calculate directional conditions
    fast_decreasing = fast.diff(length) < 0
    slow_increasing = slow.diff(length) > 0
    slow_decreasing = slow.diff(length) < 0
    
    # Calculate Short Run conditions
    potential_top = fast_decreasing & slow_increasing  # Fast decreasing, slow increasing - potential top
    both_decreasing = fast_decreasing & slow_decreasing  # Both fast and slow decreasing
    
    # Combine conditions
    short_run_series = potential_top | both_decreasing
    
    # Convert to integer if specified
    if as_int:
        short_run_series = short_run_series.astype(int)
    
    # Add result to DataFrame
    df_copy["short_run"] = short_run_series
    
    return df_copy[["short_run"]]


short_run.__doc__ = \
"""
Name:
    Short Run Indicator

Description:
    The Short Run indicator identifies potential short/bearish conditions by analyzing 
    the relationship between a fast and slow series. It returns True (or 1) when 
    either of the following conditions is met:
    
    1. Potential Top: The fast series is decreasing while the slow series is 
       increasing, which may indicate a potential top formation or reversal.
    
    2. Both Decreasing: Both the fast and slow series are decreasing, which 
       indicates a potential ongoing bearish trend.
    
    This indicator can be used with any two series, but it's commonly applied to:
    - Fast and slow moving averages
    - Price and a moving average
    - A momentum indicator and its signal line
    
    The Short Run indicator is particularly useful for identifying potential entry 
    points for short positions or for confirming an existing bearish trend.

More info:
    None

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified columns.
    - fast_column (str): The column name for the fast series.
    - slow_column (str): The column name for the slow series.
    - length (int): The lookback period for determining whether series are increasing/decreasing. Default is 2.
    - as_int (bool): If True, returns the result as integers (1 for True, 0 for False). Default is True.

Call with:
    # Using two moving averages
    result = bta.short_run(df, 'sma_20', 'sma_50')
    df['short_run'] = result['short_run']
    
    # Using price and a moving average
    result = bta.short_run(df, 'close', 'sma_50')
    df['short_run'] = result['short_run']

Returns:
    pd.DataFrame: DataFrame with 'short_run' column indicating potential short conditions.
"""


def test():
    """
    Test function for the short_run indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the short_run indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(short_run)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 