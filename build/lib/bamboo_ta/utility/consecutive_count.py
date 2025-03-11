# -*- coding: utf-8 -*-
# consecutive_count.py
import numpy as np
import pandas as pd


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

Important Notes:
    - This function returns a single float value, not a DataFrame.
    
    - When used with bamboo_ta's test_indicator function, it will fail with
      "Error: consecutive_count did not return a DataFrame" because test_indicator
      expects a DataFrame return type.
    
    - To use with test_indicator, you need to create a wrapper function:
      ```python
      def consecutive_count_wrapper(df):
          # Create a sample array with some non-zero elements
          sample_array = df['close'].diff().fillna(0).values
          
          # Call the actual function
          result = consecutive_count(sample_array)
          
          # Return as DataFrame for test_indicator compatibility
          return pd.DataFrame({'consecutive_count': [result]})
      ```
    
    - This function is not designed to be applied directly to a DataFrame column
      but to a prepared numpy array. It is typically used as part of a larger
      calculation rather than as a standalone indicator.
"""


def test():
    """
    Test function for the consecutive_count indicator.
    """
    try:
        from bamboo_ta.bamboo_ta import test_indicator

        # Create a wrapper function that returns a DataFrame
        def consecutive_count_wrapper(df):
            # Create a sample array from the DataFrame
            sample_array = df["close"].diff().fillna(0).values

            # Call the actual function
            result = consecutive_count(sample_array)

            # Return as DataFrame for test_indicator compatibility
            return pd.DataFrame({"consecutive_count": [result]})

        # Test using the wrapper
        test_indicator(consecutive_count_wrapper)

    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
