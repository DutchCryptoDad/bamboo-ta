# -*- coding: utf-8 -*-
# aroon.py

import pandas as pd
import numpy as np


def aroon(df: pd.DataFrame, length: int = 14, scalar: float = 100) -> pd.DataFrame:
    """Aroon & Aroon Oscillator (AROON)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 14
    scalar = float(scalar) if scalar > 0 else 100
    
    # Helper functions to find the position of recent highs and lows
    def recent_maximum_index(x):
        return len(x) - 1 - np.argmax(x)
    
    def recent_minimum_index(x):
        return len(x) - 1 - np.argmin(x)
    
    # Calculate days since highest high and lowest low
    high_periods = df_copy["high"].rolling(window=length, min_periods=length).apply(
        recent_maximum_index, raw=True
    )
    
    low_periods = df_copy["low"].rolling(window=length, min_periods=length).apply(
        recent_minimum_index, raw=True
    )
    
    # Calculate Aroon Up and Aroon Down
    df_copy["aroon_up"] = scalar * (1 - (high_periods / length))
    df_copy["aroon_down"] = scalar * (1 - (low_periods / length))
    
    # Calculate Aroon Oscillator
    df_copy["aroon_osc"] = df_copy["aroon_up"] - df_copy["aroon_down"]
    
    return df_copy[["aroon_up", "aroon_down", "aroon_osc"]]


aroon.__doc__ = \
"""
Name:
    Aroon & Aroon Oscillator (AROON)

Description:
    The Aroon indicator is a technical indicator used to identify trend changes in the 
    price of an asset, as well as the strength of that trend. It consists of two lines: 
    Aroon Up and Aroon Down.
    
    Aroon Up measures the time since the highest price within the look-back period, 
    while Aroon Down measures the time since the lowest price within that period. 
    The values are normalized to a range between 0 and 100.
    
    The Aroon Oscillator is calculated as the difference between Aroon Up and Aroon Down, 
    resulting in a single line that oscillates between -100 and 100.
    
    Typical interpretations:
    - Aroon Up > 70 and Aroon Down < 30: Strong uptrend
    - Aroon Down > 70 and Aroon Up < 30: Strong downtrend
    - Both Aroon Up and Aroon Down < 50: Indicates consolidation
    - Aroon Oscillator > 50: Uptrend
    - Aroon Oscillator < -50: Downtrend
    - Crossover of Aroon Up and Aroon Down: Potential trend reversal

More info:
    https://www.investopedia.com/terms/a/aroon.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): Look-back period for the calculation. Default is 14.
    - scalar (float): Scaling factor for the indicators. Default is 100.

Call with:
    result = bta.aroon(df)
    df['aroon_up'] = result['aroon_up']
    df['aroon_down'] = result['aroon_down']
    df['aroon_osc'] = result['aroon_osc']

Returns:
    pd.DataFrame: DataFrame with 'aroon_up', 'aroon_down', and 'aroon_osc' columns.
"""


def test():
    """
    Test function for the aroon indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the aroon indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(aroon)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 