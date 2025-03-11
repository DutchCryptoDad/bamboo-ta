# -*- coding: utf-8 -*-
# long_run.py

import pandas as pd
import numpy as np


def long_run(
    df: pd.DataFrame,
    fast_column: str,
    slow_column: str,
    length: int = 2,
    as_int: bool = True
) -> pd.DataFrame:
    """Long Run Indicator"""
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
    
    # Calculate increasing conditions
    fast_increasing = fast.diff(length) > 0
    slow_increasing = slow.diff(length) > 0
    slow_decreasing = slow.diff(length) < 0
    
    # Calculate Long Run conditions
    potential_bottom = fast_increasing & slow_decreasing  # Fast increasing, slow decreasing - potential bottom
    both_increasing = fast_increasing & slow_increasing   # Both fast and slow increasing
    
    # Combine conditions
    long_run_series = potential_bottom | both_increasing
    
    # Convert to integer if specified
    if as_int:
        long_run_series = long_run_series.astype(int)
    
    # Add result to DataFrame
    df_copy["long_run"] = long_run_series
    
    return df_copy[["long_run"]]


long_run.__doc__ = \
"""
Name:
    Long Run Indicator

Description:
    The Long Run indicator identifies potential long/bullish conditions by analyzing 
    the relationship between a fast and slow series. It returns True (or 1) when 
    either of the following conditions is met:
    
    1. Potential Bottom: The fast series is increasing while the slow series is 
       decreasing, which may indicate a potential bottom formation or reversal.
    
    2. Both Increasing: Both the fast and slow series are increasing, which 
       indicates a potential ongoing bullish trend.
    
    This indicator can be used with any two series, but it's commonly applied to:
    - Fast and slow moving averages
    - Price and a moving average
    - A momentum indicator and its signal line
    
    The Long Run indicator is particularly useful for identifying potential entry 
    points for long positions or for confirming an existing bullish trend.

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
    result = bta.long_run(df, 'sma_20', 'sma_50')
    df['long_run'] = result['long_run']
    
    # Using price and a moving average
    result = bta.long_run(df, 'close', 'sma_50')
    df['long_run'] = result['long_run']

Returns:
    pd.DataFrame: DataFrame with 'long_run' column indicating potential long conditions.
"""


def test():
    """
    Test function for the long_run indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the long_run indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(long_run)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 