# -*- coding: utf-8 -*-
# consecutive_higher_highs.py

import pandas as pd
import numpy as np


def consecutive_higher_highs(
    df: pd.DataFrame,
    length: int = 2,
    column: str = "high",
    as_count: bool = False
) -> pd.DataFrame:
    """Consecutive Higher Highs"""
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
        
        # For each row, calculate how many consecutive higher highs
        for i in range(len(series)):
            if i == 0:
                # First row has no previous value to compare
                continue
                
            # Check if current value is higher than previous
            if series.iloc[i] > series.iloc[i-1]:
                count.iloc[i] = count.iloc[i-1] + 1
        
        # Create the result
        result_column = f"consec_higher_{column}"
        df_copy[result_column] = count
    else:
        # Create a series that's True when current value > previous value
        higher = series > series.shift(1)
        
        # Initialize result series
        is_consecutive = pd.Series(False, index=series.index)
        
        # Set is_consecutive to True where we have at least 'length' consecutive higher values
        for i in range(length, len(higher)):
            is_consecutive.iloc[i] = True
            # Check the last 'length' values
            for j in range(length):
                if not higher.iloc[i-j]:
                    is_consecutive.iloc[i] = False
                    break
        
        # Create the result
        result_column = f"consec_higher_{column}_{length}"
        df_copy[result_column] = is_consecutive.astype(int)
    
    return df_copy[[result_column]]


consecutive_higher_highs.__doc__ = """
Name:
    Consecutive Higher Highs

Description:
    Identifies patterns of consecutive higher highs in a series.
    
    When as_count=True, this function returns a count of how many consecutive 
    higher values have occurred at each point in the series.
    
    When as_count=False, this function returns a binary indicator (1/0) that 
    signals when there have been at least 'length' consecutive higher values.
    
    This function is useful for detecting momentum continuation patterns,
    which can be useful for trend-following strategies, breakout confirmation,
    or as a filter for other trading signals.

More info:
    The concept of consecutive higher highs is commonly used in technical analysis
    to identify strong uptrends, especially in price series. It complements other
    trend identification methods and can be a useful confirmation signal.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The minimum number of consecutive higher values required. Default is 2.
    - column (str): The column name to use for calculations. Default is 'high'.
    - as_count (bool): If True, returns the count of consecutive higher values.
        If False, returns a binary indicator (1/0) when length is reached. Default is False.

Call with:
    # Get binary indicator for 3 consecutive higher highs
    result = bta.consecutive_higher_highs(df, length=3)
    df['three_higher_highs'] = result['consec_higher_high_3']
    
    # Get count of consecutive higher values
    result = bta.consecutive_higher_highs(df, as_count=True)
    df['higher_high_count'] = result['consec_higher_high']

Returns:
    pd.DataFrame: DataFrame with one column containing either:
        - The count of consecutive higher values (when as_count=True)
        - A binary indicator (1/0) for when length is reached (when as_count=False)
"""


def test():
    """
    Test function for the consecutive_higher_highs indicator.
    
    This function creates a simple test DataFrame with a price series
    and tests the consecutive_higher_highs functionality.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame
        data = {
            'high': [10, 11, 12, 11, 12, 13, 14, 15, 14, 15, 16]
        }
        df = pd.DataFrame(data)
        
        # Expected patterns:
        # - 3 consecutive higher highs at index 7 (values 13, 14, 15)
        # - 3 consecutive higher highs at index 10 (values 14, 15, 16)
        # 
        # For counting, we should see:
        # [0, 1, 2, 0, 1, 2, 3, 4, 0, 1, 2]
        
        # Test binary indicator with length=3
        result_binary = consecutive_higher_highs(df, length=3)
        expected_binary = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1]
        
        # Test count
        result_count = consecutive_higher_highs(df, as_count=True)
        expected_count = [0, 1, 2, 0, 1, 2, 3, 4, 0, 1, 2]
        
        # Display results
        print("Test DataFrame:")
        print(df)
        
        print("\nBinary indicator (length=3):")
        print(result_binary)
        print(f"Expected: {expected_binary}")
        print(f"Matches expected: {list(result_binary['consec_higher_high_3']) == expected_binary}")
        
        print("\nCount of consecutive higher highs:")
        print(result_count)
        print(f"Expected: {expected_count}")
        print(f"Matches expected: {list(result_count['consec_higher_high']) == expected_count}")
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 