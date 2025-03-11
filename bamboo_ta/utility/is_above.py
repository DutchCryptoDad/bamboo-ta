# -*- coding: utf-8 -*-
# is_above.py

import pandas as pd
import numpy as np


def is_above(
    df: pd.DataFrame,
    column_a: str,
    column_b: str,
    as_int: bool = True
) -> pd.DataFrame:
    """Is Above Indicator"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    if column_a not in df.columns:
        raise KeyError(f"DataFrame must contain '{column_a}' column")
    if column_b not in df.columns:
        raise KeyError(f"DataFrame must contain '{column_b}' column")
    
    # Extract the series
    series_a = df_copy[column_a]
    series_b = df_copy[column_b]
    
    # Convert values very close to zero to exactly zero
    series_a = series_a.apply(lambda x: 0 if abs(x) < np.finfo(float).eps else x)
    series_b = series_b.apply(lambda x: 0 if abs(x) < np.finfo(float).eps else x)
    
    # Calculate if series_a is above series_b
    result = series_a >= series_b
    
    # Convert to integer if requested
    if as_int:
        result = result.astype(int)
    
    # Create result column name
    result_column = f"{column_a}_above_{column_b}"
    
    # Add result to DataFrame
    df_copy[result_column] = result
    
    return df_copy[[result_column]]


is_above.__doc__ = """
Name:
    Is Above Indicator

Description:
    Determines whether values in one series are greater than or equal to
    values in another series. This creates a binary indicator (or boolean) that
    can be used for generating signals or conditions in trading strategies.

More info:
    This indicator is useful for identifying when one indicator or price series
    crosses above another, which is often used as a bullish signal in technical analysis.
    Common applications include when a fast moving average crosses above a slow moving 
    average, or when price crosses above a key indicator level.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the columns specified.
    - column_a (str): The column to check if it's above column_b.
    - column_b (str): The column to compare against.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Check if the fast EMA is above the slow EMA
    df['ema_fast_above_slow'] = bta.is_above(df, 'ema_9', 'ema_21')['ema_9_above_ema_21']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 where column_a is above
    column_b, and 0 otherwise (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column_a}_above_{column_b}'.
"""


def test():
    """
    Test function for the is_above indicator.
    
    This function creates a simple test DataFrame with two series
    and tests the is_above functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame
        data = {
            'series_a': [10, 20, 30, 25, 15],
            'series_b': [15, 15, 25, 25, 10]
        }
        
        # Expected results for is_above
        expected_integer = [0, 1, 1, 0, 1]
        expected_boolean = [False, True, True, False, True]
        
        # Create a DataFrame with test data
        df = pd.DataFrame(data)
        
        # Test with as_int=True (default)
        result_int = is_above(df, 'series_a', 'series_b')
        
        # Test with as_int=False
        result_bool = is_above(df, 'series_a', 'series_b', as_int=False)
        
        # Print results
        print("Test DataFrame:")
        print(df)
        
        print("\nIs Above (as integers):")
        print(result_int)
        print(f"Expected: {expected_integer}")
        print(f"Matches expected: {list(result_int['series_a_above_series_b']) == expected_integer}")
        
        print("\nIs Above (as booleans):")
        print(result_bool)
        print(f"Expected: {expected_boolean}")
        print(f"Matches expected: {list(result_bool['series_a_above_series_b']) == expected_boolean}")
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 