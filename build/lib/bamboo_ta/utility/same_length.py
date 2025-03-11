# -*- coding: utf-8 -*-
# same_length.py
import numpy as np


def same_length(bigger: np.ndarray, shorter: np.ndarray) -> np.ndarray:
    """
    Ensures the shorter array has the same length as the bigger array by padding with NaN values.

    Parameters:
    - bigger (np.ndarray): The array with the larger size.
    - shorter (np.ndarray): The array with the smaller size.

    Call with:
        padded_array = same_length(bigger_array, shorter_array)

    Returns:
    - np.ndarray: The shorter array padded with NaN values to match the size of the bigger array.
    """
    if not isinstance(bigger, np.ndarray) or not isinstance(shorter, np.ndarray):
        raise ValueError("Both inputs must be NumPy arrays.")

    if bigger.shape[0] < shorter.shape[0]:
        raise ValueError(
            "The first array must be bigger or equal in length to the second array."
        )

    # Calculate how many NaN values to add to the shorter array
    pad_size = bigger.shape[0] - shorter.shape[0]

    # Return the concatenated array of NaNs followed by the shorter array
    return np.concatenate((np.full(pad_size, np.nan), shorter))


same_length.__doc__ = """
Name:
    Same Length

Description:
    This utility function ensures that two arrays have the same length by padding
    the shorter array with NaN values at the beginning. This is particularly useful
    when working with technical indicators that have different lookback periods,
    resulting in arrays of different lengths that need to be aligned for calculations
    or visualization.

More info:
    When calculating technical indicators, the initial periods often result in NaN values
    due to insufficient data for the calculation. Different indicators may have different
    lookback periods, resulting in varying numbers of initial NaN values. This function
    helps align these indicators by padding the shorter array appropriately.

Parameters:
    - bigger (np.ndarray): The array with the larger size.
    - shorter (np.ndarray): The array with the smaller size.

Call with:
    # Example: Aligning EMA with different periods
    ema_short = calculate_ema(df['close'], period=5)  # Has fewer NaN values
    ema_long = calculate_ema(df['close'], period=20)  # Has more NaN values
    aligned_ema_short = bta.same_length(ema_long, ema_short)

Returns:
    np.ndarray: The shorter array padded with NaN values at the beginning to match
    the size of the bigger array.
"""


def test():
    """
    Test function for the same_length indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the same_length indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(same_length)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
