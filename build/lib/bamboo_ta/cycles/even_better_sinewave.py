# -*- coding: utf-8 -*-
# even_better_sinewave.py
import numpy as np
import pandas as pd


def even_better_sinewave(df, length=40, bars=10):
    """Even Better SineWave (EBSW)"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")

    # Validate arguments
    length = int(length) if length and length > 38 else 40
    bars = int(bars) if bars and bars > 0 else 10

    # Initialize variables
    alpha1 = HP = 0  # alpha and HighPass
    a1 = b1 = c1 = c2 = c3 = 0
    Filt = Pwr = Wave = 0

    lastClose = lastHP = 0
    FilterHist = [0, 0]  # Filter history

    # Calculate Result
    close_values = df["close"].values
    m = len(close_values)
    result = [np.nan for _ in range(0, length - 1)] + [0]
    
    for i in range(length, m):
        # HighPass filter cyclic components whose periods are shorter than Duration input
        alpha1 = (1 - np.sin(360 / length * np.pi / 180)) / np.cos(360 / length * np.pi / 180)
        HP = 0.5 * (1 + alpha1) * (close_values[i] - lastClose) + alpha1 * lastHP

        # Smooth with a Super Smoother Filter from equation 3-3
        a1 = np.exp(-np.sqrt(2) * np.pi / bars)
        b1 = 2 * a1 * np.cos(np.sqrt(2) * 180 / bars * np.pi / 180)
        c2 = b1
        c3 = -1 * a1 * a1
        c1 = 1 - c2 - c3
        Filt = c1 * (HP + lastHP) / 2 + c2 * FilterHist[1] + c3 * FilterHist[0]

        # 3 Bar average of Wave amplitude and power
        Wave = (Filt + FilterHist[1] + FilterHist[0]) / 3
        Pwr = (Filt * Filt + FilterHist[1] * FilterHist[1] + FilterHist[0] * FilterHist[0]) / 3

        # Normalize the Average Wave to Square Root of the Average Power
        # Avoid division by zero
        if Pwr > 0:
            Wave = Wave / np.sqrt(Pwr)
        else:
            Wave = 0

        # Update storage, result
        FilterHist.append(Filt)  # Append new Filt value
        FilterHist.pop(0)  # Remove first element of list (left) -> updating/trim
        lastHP = HP
        lastClose = close_values[i]
        result.append(Wave)

    # Create Series with the result
    df_copy["ebsw"] = result

    return df_copy[["ebsw"]]


even_better_sinewave.__doc__ = """
Name:
    Even Better SineWave (EBSW)

Description:
    The Even Better SineWave (EBSW) indicator measures market cycles and uses a low pass filter 
    to remove noise. Its output is a bounded signal between -1 and 1, and the maximum length 
    of a detected trend is limited by its length input. This indicator can be used to identify 
    cyclical patterns in price movements and potential turning points in the market.

More info:
    https://www.prorealcode.com/prorealtime-indicators/even-better-sinewave/
    J.F.Ehlers 'Cycle Analytics for Traders', 2014

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Maximum cycle/trend period. Values between 40-48 work as expected 
      with minimum value of 39. Default is 40.
    - bars (int): Period of low pass filtering. Default is 10.

Call with:
    result = bta.even_better_sinewave(df)
    df['ebsw'] = result['ebsw']

Returns:
    pd.DataFrame: DataFrame with 'ebsw' column containing the Even Better SineWave values.
"""


def test():
    """
    Test function for the even_better_sinewave indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the even_better_sinewave indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(even_better_sinewave)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 