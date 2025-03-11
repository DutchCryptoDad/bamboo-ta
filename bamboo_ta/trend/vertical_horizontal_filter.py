# -*- coding: utf-8 -*-
# vertical_horizontal_filter.py

import pandas as pd
import numpy as np


def vertical_horizontal_filter(
    df: pd.DataFrame,
    length: int = 28,
    drift: int = 1,
    column: str = "close"
) -> pd.DataFrame:
    """Vertical Horizontal Filter (VHF)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 28
    drift = int(drift) if drift > 0 else 1
    
    # Calculate the highest and lowest prices in the period
    highest_close = df_copy[column].rolling(window=length).max()
    lowest_close = df_copy[column].rolling(window=length).min()
    
    # Calculate the numerator (absolute difference between highest and lowest)
    numerator = np.abs(highest_close - lowest_close)
    
    # Calculate the denominator (sum of absolute price changes over the period)
    price_changes = np.abs(df_copy[column].diff(drift))
    denominator = price_changes.rolling(window=length).sum()
    
    # Calculate the VHF
    vhf = numerator / denominator
    
    # Store result in DataFrame
    df_copy["vhf"] = vhf
    
    return df_copy[["vhf"]]


vertical_horizontal_filter.__doc__ = \
"""
Name:
    Vertical Horizontal Filter (VHF)

Description:
    The Vertical Horizontal Filter (VHF) was created by Adam White to identify
    trending and ranging markets. It measures the ratio of the largest price
    movement (vertical movement) to the sum of price changes (horizontal movement)
    over a specified period.
    
    Higher VHF values indicate a strong trend (either up or down), while
    lower values suggest a ranging or sideways market. Traders often use this
    indicator to select appropriate trading strategies based on market conditions:
    trend-following strategies for high VHF values, and range-trading strategies
    for low VHF values.
    
    VHF is particularly useful as a precursor to applying other technical indicators,
    as it helps determine whether trend-following or oscillator-based indicators
    would be more appropriate for the current market conditions.

More info:
    https://www.incrediblecharts.com/indicators/vertical_horizontal_filter.php

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for calculating VHF. Default is 28.
    - drift (int): The period difference to calculate price changes. Default is 1.
    - column (str): Name of the column to use for calculations. Default is 'close'.

Call with:
    result = bta.vertical_horizontal_filter(df, length=28)
    df['vhf'] = result['vhf']

Returns:
    pd.DataFrame: DataFrame with 'vhf' column containing the indicator values.
"""


def test():
    """
    Test function for the vertical_horizontal_filter indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the vertical_horizontal_filter indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(vertical_horizontal_filter)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 