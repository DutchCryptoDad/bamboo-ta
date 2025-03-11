# -*- coding: utf-8 -*-
# is_above_value.py

import pandas as pd
import numpy as np


def is_above_value(
    df: pd.DataFrame,
    column: str,
    value: float,
    as_int: bool = True
) -> pd.DataFrame:
    """Is Above Value Indicator"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate value parameter
    if not isinstance(value, (int, float, complex)):
        raise ValueError("value must be a number (integer, float, or complex)")
    
    # Extract the series
    series = df_copy[column]
    
    # Convert values very close to zero to exactly zero
    series = series.apply(lambda x: 0 if abs(x) < np.finfo(float).eps else x)
    
    # Calculate if series is above value
    result = series >= value
    
    # Convert to integer if requested
    if as_int:
        result = result.astype(int)
    
    # Create result column name (replace decimal point with underscore for column name)
    value_str = str(value).replace(".", "_")
    result_column = f"{column}_above_{value_str}"
    
    # Add result to DataFrame
    df_copy[result_column] = result
    
    return df_copy[[result_column]]


is_above_value.__doc__ = """
Name:
    Is Above Value Indicator

Description:
    Determines whether values in a series are greater than or equal to
    a specified constant value. This creates a binary indicator (or boolean) that
    can be used for generating signals or conditions in trading strategies.

More info:
    This indicator is useful for identifying when a price or indicator exceeds a certain
    threshold or level, which can be used for breakout detection, overbought/oversold
    conditions, or other trading signals. It's simpler than comparing two series when
    one of the values is constant.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - column (str): The column to check if it's above the specified value.
    - value (float): The constant value to compare against.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Check if price is above a resistance level
    df['price_above_200'] = bta.is_above_value(df, 'close', 200)['close_above_200']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 where the specified column
    is above the value, and 0 otherwise (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column}_above_{value}'.
"""


def test():
    """
    Test function for the is_above_value indicator.
    
    This function creates a simple test DataFrame with price data
    and tests the is_above_value functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame
        data = {
            'price': [95, 100, 105, 110, 100, 95]
        }
        
        # Value to test against
        test_value = 100
        
        # Expected results for is_above_value
        expected_integer = [0, 1, 1, 1, 1, 0]  # Note: 100 >= 100 is True
        expected_boolean = [False, True, True, True, True, False]
        
        # Create a DataFrame with test data
        df = pd.DataFrame(data)
        
        # Test with as_int=True (default)
        result_int = is_above_value(df, 'price', test_value)
        
        # Test with as_int=False
        result_bool = is_above_value(df, 'price', test_value, as_int=False)
        
        # Print results
        print("Test DataFrame:")
        print(df)
        
        print(f"\nIs Above Value {test_value} (as integers):")
        print(result_int)
        print(f"Expected: {expected_integer}")
        print(f"Matches expected: {list(result_int[f'price_above_{test_value}']) == expected_integer}")
        
        print(f"\nIs Above Value {test_value} (as booleans):")
        print(result_bool)
        print(f"Expected: {expected_boolean}")
        print(f"Matches expected: {list(result_bool[f'price_above_{test_value}']) == expected_boolean}")
        
        # Test with decimal value
        decimal_value = 102.5
        result_decimal = is_above_value(df, 'price', decimal_value)
        print(f"\nIs Above Value {decimal_value} (decimal value):")
        print(result_decimal)
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 