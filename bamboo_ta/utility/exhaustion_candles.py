# -*- coding: utf-8 -*-
# exhaustion_candles.py
import numpy as np
import pandas as pd
from typing import Tuple


def exhaustion_candles(
    df: pd.DataFrame, window: int = 1, multiplier: int = 1
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate the average consecutive length of ups and downs to adjust the exhaustion bands dynamically.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the 'close' price series.
    - window (int): Lookback window for calculation.
    - multiplier (int): Scalar multiplier for both major and minor quality.

    Call with:
        maj_qual, min_qual = exhaustion_candles(df, window, multiplier)
        df['maj_qual'] = maj_qual
        df['min_qual'] = min_qual

    Returns:
    - Tuple[np.ndarray, np.ndarray]: Arrays of major and minor quality values.
    """

    # Function to calculate average consecutive count
    def consecutive_count(consecutive_diff: np.ndarray) -> float:
        # Find indices of non-zero elements in the array
        non_zero_diff = np.where(consecutive_diff != 0)[0]

        # If fewer than two non-zero elements, return 0 as no valid calculation can be performed
        if len(non_zero_diff) < 2:
            return 0

        # Calculate and return the average distance between consecutive non-zero indices
        return np.mean(np.diff(non_zero_diff))

    consecutive_diff = np.sign(df["close"].diff())
    maj_qual = np.zeros(len(df))
    min_qual = np.zeros(len(df))

    # Ensure multiplier is applied consistently
    multiplier = np.full(len(df), multiplier)

    for i in range(len(df)):
        idx_range = (
            consecutive_diff[i - window + 1 : i + 1]
            if i >= window
            else consecutive_diff[: i + 1]
        )
        avg_consecutive = consecutive_count(idx_range)

        # Ensure avg_consecutive is a scalar, not an array
        if isinstance(avg_consecutive, np.ndarray):
            avg_consecutive = avg_consecutive.item()

        maj_qual[i] = (
            int(avg_consecutive * (3 * multiplier[i]))
            if not np.isnan(avg_consecutive)
            else 0
        )
        min_qual[i] = (
            int(avg_consecutive * (3 * multiplier[i]))
            if not np.isnan(avg_consecutive)
            else 0
        )

    return maj_qual, min_qual


exhaustion_candles.__doc__ = """
Name:
    Exhaustion Candles

Description:
    This function calculates values for dynamically adjusting exhaustion bands based on
    the average consecutive length of price movements in the same direction. It helps
    identify potential price exhaustion points where trends might reverse.
    
    The function analyzes the pattern of consecutive up and down price movements within
    a specified window and calculates quality values that can be used to set dynamic
    band widths for detecting exhaustion points.

More info:
    Exhaustion is a market condition where a trend has extended for so long that it
    becomes unsustainable and is likely to reverse. This function helps identify
    such points by calculating values based on the consistency and length of price
    movements in a particular direction.

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the 'close' price series.
    - window (int, default=1): Lookback window for calculation.
    - multiplier (int, default=1): Scalar multiplier for both major and minor quality values.

Call with:
    maj_qual, min_qual = bta.exhaustion_candles(df, window=5, multiplier=2)
    df['maj_qual'] = maj_qual
    df['min_qual'] = min_qual

Returns:
    Tuple[np.ndarray, np.ndarray]: Two arrays containing major and minor quality values
    that can be used to set dynamic band widths for detecting exhaustion points.
"""


def test():
    """
    Test function for the exhaustion_candles indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the exhaustion_candles indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(exhaustion_candles)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
