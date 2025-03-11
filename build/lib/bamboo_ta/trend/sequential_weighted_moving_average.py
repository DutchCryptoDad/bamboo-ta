# -*- coding: utf-8 -*-
# sequential_weighted_moving_average.py

import pandas as pd
import numpy as np


def sequential_weighted_moving_average(df: pd.DataFrame, length: int = 10, 
                                    asc: bool = True, column: str = "close") -> pd.DataFrame:
    """Sequential Weighted Moving Average (SWMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Validate parameters
    length = int(length) if length > 0 else 10
    
    # Generate symmetric triangle weights
    weights = symmetric_triangle(length, weighted=True)
    
    # Initialize result series
    swma = pd.Series(np.nan, index=series.index)
    
    # Calculate SWMA
    for i in range(length - 1, len(series)):
        window = series.iloc[i - length + 1 : i + 1].values
        swma.iloc[i] = np.sum(weights * window)
    
    # Add result to DataFrame
    df_copy["swma"] = swma
    
    return df_copy[["swma"]]


def symmetric_triangle(length: int, weighted: bool = False) -> np.ndarray:
    """
    Generate symmetric triangle weights
    
    Args:
        length (int): The size of the triangle
        weighted (bool): Whether to normalize the weights to sum to 1
        
    Returns:
        np.ndarray: The triangle weights
    """
    # Handle edge cases
    if length <= 0:
        return np.array([])
    if length == 1:
        return np.array([1.0])
    
    # Generate the symmetric triangle
    if length % 2 == 0:  # Even length
        first_half = np.arange(1, length//2 + 1)
        second_half = np.arange(length//2, 0, -1)
        triangle = np.concatenate([first_half, second_half])
    else:  # Odd length
        first_half = np.arange(1, length//2 + 1)
        second_half = np.arange(length//2 + 1, 0, -1)
        triangle = np.concatenate([first_half, second_half])
    
    # Normalize weights if requested
    if weighted:
        return triangle / np.sum(triangle)
    
    return triangle


sequential_weighted_moving_average.__doc__ = \
"""
Name:
    Sequential Weighted Moving Average (SWMA)

Description:
    A weighted moving average where weights are based on a symmetric triangle pattern.
    For example: n=3 -> [1/4, 2/4, 1/4], n=4 -> [1/6, 2/6, 2/6, 1/6], etc.
    This creates a symmetric weight distribution that gives more importance to the
    middle values in the calculation window.
    
    This moving average has variable length in contrast to TradingView's fixed
    length of 4. It effectively smooths price data while reducing lag and maintaining
    responsiveness to significant price movements.

More info:
    https://www.tradingview.com/study-script-reference/#fun_swma

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the SWMA calculation. Default is 10.
    - asc (bool): Whether recent values should weigh more. Default is True.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.sequential_weighted_moving_average(df)
    df['swma'] = result['swma']

Returns:
    pd.DataFrame: DataFrame with 'swma' column.
"""


def test():
    """
    Test function for the sequential_weighted_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the sequential_weighted_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(sequential_weighted_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 