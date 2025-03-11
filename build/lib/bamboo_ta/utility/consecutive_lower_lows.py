# -*- coding: utf-8 -*-
# consecutive_lower_lows.py

import pandas as pd
import numpy as np


def consecutive_lower_lows(
    df: pd.DataFrame,
    length: int = 2,
    column: str = "low",
    as_count: bool = False
) -> pd.DataFrame:
    """Consecutive Lower Lows"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Get the column series
    series = df_copy[column]
    
    if as_count:
        # Initialize the count series with zeros
        count = pd.Series(0, index=series.index)
        
        # For each row, calculate how many consecutive lower lows
        for i in range(len(series)):
            if i == 0:
                # First row has no previous value to compare
                continue
                
            # Check if current value is lower than previous
            if series.iloc[i] < series.iloc[i-1]:
                count.iloc[i] = count.iloc[i-1] + 1
        
        # Create the result
        result_column = f"consec_lower_{column}"
        df_copy[result_column] = count
    else:
        # Create a series that's True when current value < previous value
        lower = series < series.shift(1)
        
        # Initialize result series
        is_consecutive = pd.Series(False, index=series.index)
        
        # Set is_consecutive to True where we have at least 'length' consecutive lower values
        for i in range(length, len(lower)):
            is_consecutive.iloc[i] = True
            # Check the last 'length' values
            for j in range(length):
                if not lower.iloc[i-j]:
                    is_consecutive.iloc[i] = False
                    break
        
        # Create the result
        result_column = f"consec_lower_{column}_{length}"
        df_copy[result_column] = is_consecutive.astype(int)
    
    return df_copy[[result_column]]


consecutive_lower_lows.__doc__ = """
Name:
    Consecutive Lower Lows

Description:
    Identifies patterns of consecutive lower lows in a series.
    
    When as_count=True, this function returns a count of how many consecutive 
    lower values have occurred at each point in the series.
    
    When as_count=False, this function returns a binary indicator (1/0) that 
    signals when there have been at least 'length' consecutive lower values.
    
    This function is useful for detecting downtrend momentum patterns,
    which can be useful for trend-following strategies, breakdown confirmation,
    or as a filter for other trading signals.

More info:
    The concept of consecutive lower lows is commonly used in technical analysis
    to identify strong downtrends, especially in price series. It complements other
    trend identification methods and can be a useful confirmation signal.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The minimum number of consecutive lower values required. Default is 2.
    - column (str): The column name to use for calculations. Default is 'low'.
    - as_count (bool): If True, returns the count of consecutive lower values.
        If False, returns a binary indicator (1/0) when length is reached. Default is False.

Call with:
    # Get binary indicator for 3 consecutive lower lows
    result = bta.consecutive_lower_lows(df, length=3)
    df['three_lower_lows'] = result['consec_lower_low_3']
    
    # Get count of consecutive lower values
    result = bta.consecutive_lower_lows(df, as_count=True)
    df['lower_low_count'] = result['consec_lower_low']

Returns:
    pd.DataFrame: DataFrame with one column containing either:
        - The count of consecutive lower values (when as_count=True)
        - A binary indicator (1/0) for when length is reached (when as_count=False)
"""


def test():
    """
    Test function for the consecutive_lower_lows indicator.
    
    This function creates a simple test DataFrame with a price series
    and tests the consecutive_lower_lows functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame
        data = {
            'low': [10, 9, 8, 9, 8, 7, 6, 5, 6, 5, 4]
        }
        df = pd.DataFrame(data)
        
        # Expected patterns:
        # - 3 consecutive lower lows at index 7 (values 7, 6, 5)
        # - 3 consecutive lower lows at index 10 (values 6, 5, 4)
        # 
        # For counting, we should see:
        # [0, 1, 2, 0, 1, 2, 3, 4, 0, 1, 2]
        
        # Test binary indicator with length=3
        result_binary = consecutive_lower_lows(df, length=3)
        expected_binary = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        
        # Test count
        result_count = consecutive_lower_lows(df, as_count=True)
        expected_count = [0, 1, 2, 0, 1, 2, 3, 4, 0, 1, 2]
        
        # Display results
        print("Test DataFrame:")
        print(df)
        
        print("\nBinary indicator (length=3):")
        print(result_binary)
        print(f"Expected: {expected_binary}")
        print(f"Matches expected: {list(result_binary['consec_lower_low_3']) == expected_binary}")
        
        print("\nCount of consecutive lower lows:")
        print(result_count)
        print(f"Expected: {expected_count}")
        print(f"Matches expected: {list(result_count['consec_lower_low']) == expected_count}")
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 