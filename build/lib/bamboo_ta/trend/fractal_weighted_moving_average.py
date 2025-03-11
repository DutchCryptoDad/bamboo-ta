# -*- coding: utf-8 -*-
# fractal_weighted_moving_average.py

import pandas as pd
import numpy as np


def fractal_weighted_moving_average(df: pd.DataFrame, length: int = 10, 
                                 column: str = "close") -> pd.DataFrame:
    """Fractal Weighted Moving Average (FWMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Generate Fibonacci sequence
    fibs = fibonacci_sequence(length, weighted=True)
    
    # Initialize result series
    fwma = pd.Series(np.nan, index=series.index)
    
    # Calculate FWMA
    for i in range(length - 1, len(series)):
        window = series.iloc[i - length + 1 : i + 1].values
        fwma.iloc[i] = np.sum(fibs * window)
    
    # Add result to DataFrame
    df_copy["fwma"] = fwma
    
    return df_copy[["fwma"]]


def fibonacci_sequence(n: int, weighted: bool = False) -> np.ndarray:
    """
    Generate a Fibonacci sequence of length n
    
    Args:
        n (int): Length of the sequence
        weighted (bool): If True, normalize the values to sum to 1
        
    Returns:
        np.ndarray: Fibonacci sequence
    """
    # Handle edge cases
    if n <= 0:
        return np.array([])
    if n == 1:
        return np.array([1])
    
    # Start with the first two Fibonacci numbers
    sequence = [1, 1]
    
    # Generate the rest of the sequence
    for i in range(2, n):
        sequence.append(sequence[i-1] + sequence[i-2])
    
    # Convert to numpy array
    result = np.array(sequence)
    
    # Normalize if weighted
    if weighted:
        return result / np.sum(result)
    
    return result


fractal_weighted_moving_average.__doc__ = \
"""
Name:
    Fractal Weighted Moving Average (FWMA)

Description:
    The Fractal Weighted Moving Average is a variation of the Weighted Moving Average
    where the weights are based on the Fibonacci sequence. The Fibonacci sequence is
    a series of numbers where each number is the sum of the two preceding ones, usually
    starting with 1 and 1. 
    
    By using the Fibonacci sequence as weights, more emphasis is placed on certain
    periods based on the natural mathematical progression found throughout nature.
    This creates a moving average that may better align with natural market cycles.

More info:
    https://www.investopedia.com/terms/f/fibonacci-retracement.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the FWMA calculation. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.fractal_weighted_moving_average(df)
    df['fwma'] = result['fwma']

Returns:
    pd.DataFrame: DataFrame with 'fwma' column.
"""


def test():
    """
    Test function for the fractal_weighted_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the fractal_weighted_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(fractal_weighted_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 