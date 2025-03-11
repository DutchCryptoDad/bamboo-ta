# -*- coding: utf-8 -*-
# cross_value.py

import pandas as pd
import numpy as np


def cross_value(
    df: pd.DataFrame,
    column: str,
    value: float,
    direction: str = "above",
    as_int: bool = True
) -> pd.DataFrame:
    """Cross Value Indicator"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate direction parameter
    if direction not in ["above", "below"]:
        raise ValueError("direction must be 'above' or 'below'")
    
    # Validate value parameter
    if not isinstance(value, (int, float)):
        raise ValueError("value must be a number (int or float)")
    
    # Extract the series
    series = df_copy[column]
    
    # Convert values very close to zero to exactly zero
    series = series.apply(lambda x: 0 if abs(x) < np.finfo(float).eps else x)
    
    # Calculate current and previous state
    if direction == "above":
        # Current: Series is above value, Previous: Series was below value
        current = series > value
        previous = series.shift(1) < value
        
        # Crossed above: current is above AND previous was below
        cross_result = current & previous
    else:  # direction == "below"
        # Current: Series is below value, Previous: Series was above value
        current = series < value
        previous = series.shift(1) > value
        
        # Crossed below: current is below AND previous was above
        cross_result = current & previous
    
    # Convert to integer if requested
    if as_int:
        cross_result = cross_result.astype(int)
    
    # Create result column name
    cross_type = "xav" if direction == "above" else "xbv"
    result_column = f"{column}_{cross_type}_{value}"
    
    # Add result to DataFrame
    df_copy[result_column] = cross_result
    
    return df_copy[[result_column]]


cross_value.__doc__ = """
Name:
    Cross Value Indicator

Description:
    Determines when a series crosses above or below a specified constant value.
    This creates a binary indicator (or boolean) that can be used for
    generating signals or conditions in trading strategies.

More info:
    Value crossovers are fundamental signals in technical analysis.
    They occur when a series (like price or an oscillator) crosses either above or below
    a specific threshold or level. For example, RSI crossing above 70 or below 30,
    or price crossing above/below a key price level.
    
    This function detects the exact point of crossing, which marks a change in direction
    or momentum relative to the specified value. It returns 1 (or True) only at the 
    candle where the crossing occurs.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - column (str): The column to check for crossing above/below the value.
    - value (float): The constant value to compare against.
    - direction (str): The direction of the cross, either 'above' or 'below'. Default is 'above'.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Detect when RSI crosses above 70 (overbought)
    df['rsi_overbought'] = bta.cross_value(df, 'rsi', 70, 'above')['rsi_xav_70']
    
    # Detect when RSI crosses below 30 (oversold)
    df['rsi_oversold'] = bta.cross_value(df, 'rsi', 30, 'below')['rsi_xbv_30']
    
    # Detect when price crosses above a key level
    df['price_above_support'] = bta.cross_value(df, 'close', 100, 'above')['close_xav_100']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 at points where the specified
    column crosses above/below the value (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column}_xav_{value}' for crossing above, or
    '{column}_xbv_{value}' for crossing below.
"""


def test():
    """
    Test function for the cross_value indicator.
    
    This function creates a simple test DataFrame with a price series
    and tests the cross_value functionality against a constant level.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame with a series that crosses a constant value
        data = {
            'price': [95, 98, 100, 102, 105, 103, 100, 98, 95]
        }
        
        # Test value
        level = 100
        
        # Expected results
        # price crosses above 100 at index 2 (price: 100, then goes up)
        # price crosses below 100 at index 6 (price: 100, then goes down)
        expected_cross_above = [0, 0, 1, 0, 0, 0, 0, 0, 0]
        expected_cross_below = [0, 0, 0, 0, 0, 0, 1, 0, 0]
        
        # Create a DataFrame with test data
        df = pd.DataFrame(data)
        
        # Test crossing above
        result_above = cross_value(df, 'price', level, 'above')
        
        # Test crossing below
        result_below = cross_value(df, 'price', level, 'below')
        
        # Print results
        print("Test DataFrame:")
        print(df)
        print(f"Testing crosses with level: {level}")
        
        print("\nPrice Crosses Above Level:")
        print(result_above)
        print(f"Expected: {expected_cross_above}")
        print(f"Matches expected: {list(result_above[f'price_xav_{level}']) == expected_cross_above}")
        
        print("\nPrice Crosses Below Level:")
        print(result_below)
        print(f"Expected: {expected_cross_below}")
        print(f"Matches expected: {list(result_below[f'price_xbv_{level}']) == expected_cross_below}")
        
        # Test with boolean output
        result_above_bool = cross_value(df, 'price', level, 'above', as_int=False)
        print("\nPrice Crosses Above Level (Boolean):")
        print(result_above_bool)
        
        # Test with a different value
        diff_level = 103
        result_diff = cross_value(df, 'price', diff_level, 'above')
        expected_diff = [0, 0, 0, 0, 1, 0, 0, 0, 0]  # Crosses above 103 at index 4
        
        print(f"\nPrice Crosses Above {diff_level}:")
        print(result_diff)
        print(f"Expected: {expected_diff}")
        print(f"Matches expected: {list(result_diff[f'price_xav_{diff_level}']) == expected_diff}")
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 