# -*- coding: utf-8 -*-
# cross.py

import pandas as pd
import numpy as np


def cross(
    df: pd.DataFrame,
    column_a: str,
    column_b: str,
    direction: str = "above",
    as_int: bool = True
) -> pd.DataFrame:
    """Cross Indicator"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    if column_a not in df.columns:
        raise KeyError(f"DataFrame must contain '{column_a}' column")
    if column_b not in df.columns:
        raise KeyError(f"DataFrame must contain '{column_b}' column")
    
    # Validate direction parameter
    if direction not in ["above", "below"]:
        raise ValueError("direction must be 'above' or 'below'")
    
    # Extract the series
    series_a = df_copy[column_a]
    series_b = df_copy[column_b]
    
    # Convert values very close to zero to exactly zero
    series_a = series_a.apply(lambda x: 0 if abs(x) < np.finfo(float).eps else x)
    series_b = series_b.apply(lambda x: 0 if abs(x) < np.finfo(float).eps else x)
    
    # Calculate current and previous state
    current = series_a > series_b  # Current: A is above B
    previous = series_a.shift(1) < series_b.shift(1)  # Previous: A was below B
    
    # Determine crossover based on direction
    if direction == "above":
        # Crossed above: current is above AND previous was below
        cross_result = current & previous
    else:  # direction == "below"
        # Crossed below: current is below AND previous was above
        cross_result = (~current) & (~previous)
    
    # Convert to integer if requested
    if as_int:
        cross_result = cross_result.astype(int)
    
    # Create result column name
    cross_type = "xa" if direction == "above" else "xb"
    result_column = f"{column_a}_{cross_type}_{column_b}"
    
    # Add result to DataFrame
    df_copy[result_column] = cross_result
    
    return df_copy[[result_column]]


cross.__doc__ = """
Name:
    Cross Indicator

Description:
    Determines when one series crosses above or below another series.
    This creates a binary indicator (or boolean) that can be used for
    generating signals or conditions in trading strategies.

More info:
    Crossovers are one of the most fundamental signals in technical analysis.
    They occur when one series (like a faster moving average) crosses either above or below
    another series (like a slower moving average). Crossing above is typically
    considered a bullish signal, while crossing below is typically a bearish signal.
    
    This function detects the exact point of crossing, which marks a change in direction
    or momentum. It returns 1 (or True) only at the candle where the crossing occurs.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the columns specified.
    - column_a (str): The column to check if it's crossing above/below column_b.
    - column_b (str): The column to compare against.
    - direction (str): The direction of the cross, either 'above' or 'below'. Default is 'above'.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Detect when fast EMA crosses above slow EMA
    df['ema_cross_up'] = bta.cross(df, 'ema_9', 'ema_21', 'above')['ema_9_xa_ema_21']
    
    # Detect when fast EMA crosses below slow EMA
    df['ema_cross_down'] = bta.cross(df, 'ema_9', 'ema_21', 'below')['ema_9_xb_ema_21']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 at points where column_a
    crosses above/below column_b (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column_a}_xa_{column_b}' for crossing above, or
    '{column_a}_xb_{column_b}' for crossing below.
"""


def test():
    """
    Test function for the cross indicator.
    
    This function creates a simple test DataFrame with two series
    and tests the cross functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame with series that cross each other
        data = {
            'fast': [5, 10, 15, 20, 25, 20, 15, 10, 5],
            'slow': [15, 15, 15, 15, 15, 15, 15, 15, 15]
        }
        
        # Expected results
        # fast crosses above slow at index 2 (fast: 15, slow: 15)
        # fast crosses below slow at index 6 (fast: 15, slow: 15)
        expected_cross_above = [0, 0, 1, 0, 0, 0, 0, 0, 0]
        expected_cross_below = [0, 0, 0, 0, 0, 0, 1, 0, 0]
        
        # Create a DataFrame with test data
        df = pd.DataFrame(data)
        
        # Test crossing above
        result_above = cross(df, 'fast', 'slow', 'above')
        
        # Test crossing below
        result_below = cross(df, 'fast', 'slow', 'below')
        
        # Print results
        print("Test DataFrame:")
        print(df)
        
        print("\nFast Crosses Above Slow:")
        print(result_above)
        print(f"Expected: {expected_cross_above}")
        print(f"Matches expected: {list(result_above['fast_xa_slow']) == expected_cross_above}")
        
        print("\nFast Crosses Below Slow:")
        print(result_below)
        print(f"Expected: {expected_cross_below}")
        print(f"Matches expected: {list(result_below['fast_xb_slow']) == expected_cross_below}")
        
        # Add test for exact crossing at specific values
        # Create test data where series cross right at a specific value
        data_exact = {
            'price': [95, 100, 105, 110, 105, 100, 95],
            'level': [100, 100, 100, 100, 100, 100, 100]  # Constant level
        }
        df_exact = pd.DataFrame(data_exact)
        
        # Expected results
        # price crosses above level at index 1 (both are 100, then price goes up)
        # price crosses below level at index 5 (both are 100, then price goes down)
        expected_exact_above = [0, 1, 0, 0, 0, 0, 0]
        expected_exact_below = [0, 0, 0, 0, 0, 1, 0]
        
        result_exact_above = cross(df_exact, 'price', 'level', 'above')
        result_exact_below = cross(df_exact, 'price', 'level', 'below')
        
        print("\nExact Value Cross Test (Price vs 100 level):")
        print(df_exact)
        
        print("\nPrice Crosses Above 100:")
        print(result_exact_above)
        print(f"Expected: {expected_exact_above}")
        print(f"Matches expected: {list(result_exact_above['price_xa_level']) == expected_exact_above}")
        
        print("\nPrice Crosses Below 100:")
        print(result_exact_below)
        print(f"Expected: {expected_exact_below}")
        print(f"Matches expected: {list(result_exact_below['price_xb_level']) == expected_exact_below}")
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 