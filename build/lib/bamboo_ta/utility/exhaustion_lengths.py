# -*- coding: utf-8 -*-
# exhaustion_lengths.py
import numpy as np
import pandas as pd
from typing import Tuple
from scipy.signal import argrelextrema


def exhaustion_lengths(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Calculate the average length of peaks and valleys to adjust the exhaustion bands dynamically.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing 'high' and 'low' columns.

    Call with:
        maj_len, min_len = exhaustion_lengths(df)
        df['maj_len'] = maj_len
        df['min_len'] = min_len

    Returns:
    - int, int: Average peak distance and average valley distance.
    """
    # Find relative maxima (peaks) and minima (valleys) in the 'high' and 'low' columns
    high_indices = argrelextrema(df["high"].to_numpy(), np.greater)[0]
    low_indices = argrelextrema(df["low"].to_numpy(), np.less)[0]

    # If there are fewer than two peaks or valleys, return zero
    if len(high_indices) < 2 or len(low_indices) < 2:
        return 0, 0

    # Calculate average and standard deviation of distances between peaks and valleys
    avg_peak_distance = np.mean(np.diff(high_indices))
    std_peak_distance = np.std(np.diff(high_indices))
    avg_valley_distance = np.mean(np.diff(low_indices))
    std_valley_distance = np.std(np.diff(low_indices))

    # Determine major and minor lengths using average + standard deviation
    maj_len = int(avg_peak_distance + std_peak_distance)
    min_len = int(avg_valley_distance + std_valley_distance)

    return maj_len, min_len


exhaustion_lengths.__doc__ = """
Name:
    Exhaustion Lengths

Description:
    This function calculates the average distances between price peaks and valleys
    to help determine appropriate lengths for exhaustion bands. It identifies relative
    maxima in the 'high' prices and relative minima in the 'low' prices, then calculates
    the average distance between consecutive peaks and valleys, plus their standard
    deviations.
    
    These values can be used to dynamically adjust exhaustion bands based on the
    natural cycles present in the price data.

More info:
    Price action often follows cyclical patterns where peaks and troughs occur at
    somewhat regular intervals. By measuring the average distance between these
    extremes, traders can better calibrate indicators to match the natural rhythm
    of the market being analyzed.
    
    The function uses scipy's argrelextrema to find local maxima and minima in the
    price series, then calculates statistics about their spacing.

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing 'high' and 'low' columns.

Call with:
    maj_len, min_len = bta.exhaustion_lengths(df)
    df['maj_len'] = maj_len
    df['min_len'] = min_len

Returns:
    Tuple[int, int]: A tuple containing:
    - maj_len: Average peak distance plus standard deviation (for major cycles)
    - min_len: Average valley distance plus standard deviation (for minor cycles)
    Returns (0, 0) if there are insufficient peaks or valleys to calculate.
"""


def test():
    """
    Test function for the exhaustion_lengths indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the exhaustion_lengths indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(exhaustion_lengths)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
