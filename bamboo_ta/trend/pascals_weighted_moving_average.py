# -*- coding: utf-8 -*-
# pascals_weighted_moving_average.py

import pandas as pd
import numpy as np


def pascals_weighted_moving_average(df: pd.DataFrame, length: int = 10, 
                                 column: str = "close") -> pd.DataFrame:
    """Pascal's Weighted Moving Average (PWMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Validate parameters
    length = int(length) if length > 0 else 10
    
    # Generate Pascal's Triangle weights
    weights = pascals_triangle(length)
    
    # Initialize result series
    pwma = pd.Series(np.nan, index=series.index)
    
    # Calculate PWMA
    for i in range(length - 1, len(series)):
        window = series.iloc[i - length + 1 : i + 1].values
        pwma.iloc[i] = np.sum(weights * window)
    
    # Add result to DataFrame
    df_copy["pwma"] = pwma
    
    return df_copy[["pwma"]]


def pascals_triangle(n: int) -> np.ndarray:
    """
    Generate the nth row of Pascal's Triangle with normalized weights
    
    Args:
        n (int): Length of the row
        
    Returns:
        np.ndarray: Normalized weights from Pascal's Triangle
    """
    # Handle edge cases
    if n <= 0:
        return np.array([])
    if n == 1:
        return np.array([1.0])
    
    # Initialize the first row of Pascal's Triangle
    triangle = [1]
    
    # Generate the nth row
    for i in range(n - 1):
        # Calculate the next row
        next_row = [1]
        for j in range(len(triangle) - 1):
            next_row.append(triangle[j] + triangle[j + 1])
        next_row.append(1)
        triangle = next_row
    
    # Convert to numpy array
    triangle = np.array(triangle, dtype=float)
    
    # Normalize weights to sum to 1
    return triangle / np.sum(triangle)


pascals_weighted_moving_average.__doc__ = \
"""
Name:
    Pascal's Weighted Moving Average (PWMA)

Description:
    Pascal's Weighted Moving Average is a type of weighted moving average where the
    weights are based on Pascal's Triangle. This creates a symmetric bell-curved weight
    distribution that gives more importance to the middle values in the calculation window.
    
    Pascal's Triangle is a triangular array of numbers where each number is the sum of the
    two numbers directly above it. When used as weights for a moving average, it creates
    a naturally balanced weight distribution that can effectively filter price noise while
    maintaining responsiveness to significant price movements.

More info:
    https://en.wikipedia.org/wiki/Pascal%27s_triangle
    https://www.investopedia.com/terms/w/weighted_average.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the PWMA calculation. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.pascals_weighted_moving_average(df)
    df['pwma'] = result['pwma']

Returns:
    pd.DataFrame: DataFrame with 'pwma' column.
"""


def test():
    """
    Test function for the pascals_weighted_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the pascals_weighted_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(pascals_weighted_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 