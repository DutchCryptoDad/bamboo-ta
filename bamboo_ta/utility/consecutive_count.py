# -*- coding: utf-8 -*-
# consecutive_count.py
import numpy as np


def consecutive_count(consecutive_diff: np.ndarray) -> float:
    """
    Calculate the average consecutive count of non-zero differences.

    Parameters:
    - consecutive_diff (np.ndarray): Array of consecutive differences.

    Returns:
    - float: Average consecutive count. If there are fewer than two non-zero differences, returns 0.
    """
    # Find indices of non-zero elements in the array
    non_zero_diff = np.where(consecutive_diff != 0)[0]

    # If fewer than two non-zero elements, return 0 as no valid calculation can be performed
    if len(non_zero_diff) < 2:
        return 0

    # Calculate and return the average distance between consecutive non-zero indices
    return np.mean(np.diff(non_zero_diff))


consecutive_count.__doc__ = """
Name:
    Consecutive Count

Description:
    This utility function calculates the average distance between non-zero elements in an array.
    It's particularly useful for analyzing patterns in time series data, such as determining 
    the average number of periods between significant events (like price movements exceeding
    a threshold, trend changes, or signal triggers).

More info:
    In algorithmic trading, this can be used to measure:
    - Frequency of crossover signals
    - Average distance between price spikes
    - Periodicity of market movements
    - Interval analysis for mean reversion or momentum

Parameters:
    - consecutive_diff (np.ndarray): A numpy array containing the differences or signal
      values where non-zero elements represent significant events.

Call with:
    # Example: Find average bars between RSI crossovers of 50
    crossover_array = np.where(df['rsi'] > 50, 1, 0).diff().fillna(0).values
    avg_distance = bta.consecutive_count(crossover_array)

Returns:
    float: The average number of indices between consecutive non-zero elements.
    Returns 0 if there are fewer than two non-zero elements.
"""


def test():
    """
    Test function for the consecutive_count indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the consecutive_count indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(consecutive_count)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
