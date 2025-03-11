# -*- coding: utf-8 -*-
# is_below.py

import pandas as pd
import numpy as np


def is_below(
    df: pd.DataFrame,
    column_a: str,
    column_b: str,
    as_int: bool = True
) -> pd.DataFrame:
    """Is Below Indicator"""
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
    
    # Calculate if series_a is below series_b
    result = series_a <= series_b
    
    # Convert to integer if requested
    if as_int:
        result = result.astype(int)
    
    # Create result column name
    result_column = f"{column_a}_below_{column_b}"
    
    # Add result to DataFrame
    df_copy[result_column] = result
    
    return df_copy[[result_column]]


is_below.__doc__ = """
Name:
    Is Below Indicator

Description:
    Determines whether values in one series are less than or equal to
    values in another series. This creates a binary indicator (or boolean) that
    can be used for generating signals or conditions in trading strategies.

More info:
    This indicator is useful for identifying when one indicator or price series
    falls below another, which is often used as a bearish signal in technical analysis.
    Common applications include when a fast moving average crosses below a slow moving 
    average, or when price falls below a key support level or indicator.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the columns specified.
    - column_a (str): The column to check if it's below column_b.
    - column_b (str): The column to compare against.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Check if the fast EMA is below the slow EMA
    df['ema_fast_below_slow'] = bta.is_below(df, 'ema_9', 'ema_21')['ema_9_below_ema_21']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 where column_a is below
    column_b, and 0 otherwise (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column_a}_below_{column_b}'.
"""


def test():
    """
    Test function for the is_below indicator.
    
    This function creates a simple test DataFrame with two series
    and tests the is_below functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame
        data = {
            'series_a': [10, 20, 30, 25, 15],
            'series_b': [15, 15, 25, 25, 10]
        }
        
        # Expected results for is_below
        expected_integer = [1, 0, 0, 0, 0]
        expected_boolean = [True, False, False, False, False]
        
        # Create a DataFrame with test data
        df = pd.DataFrame(data)
        
        # Test with as_int=True (default)
        result_int = is_below(df, 'series_a', 'series_b')
        
        # Test with as_int=False
        result_bool = is_below(df, 'series_a', 'series_b', as_int=False)
        
        # Print results
        print("Test DataFrame:")
        print(df)
        
        print("\nIs Below (as integers):")
        print(result_int)
        print(f"Expected: {expected_integer}")
        print(f"Matches expected: {list(result_int['series_a_below_series_b']) == expected_integer}")
        
        print("\nIs Below (as booleans):")
        print(result_bool)
        print(f"Expected: {expected_boolean}")
        print(f"Matches expected: {list(result_bool['series_a_below_series_b']) == expected_boolean}")
        
        # Add test for the equal case (should be counted as "below" since we use <=)
        data_equal = {
            'price': [10, 20, 30, 40, 50],
            'level': [10, 20, 30, 40, 50]  # Exactly equal
        }
        df_equal = pd.DataFrame(data_equal)
        result_equal = is_below(df_equal, 'price', 'level')
        print("\nTesting with equal values (should all be 1/True):")
        print(result_equal)
        print(f"All values are 1: {all(result_equal['price_below_level'] == 1)}")
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 