# -*- coding: utf-8 -*-
# kdj.py

import pandas as pd
import numpy as np


def kdj(df: pd.DataFrame, length: int = 9, signal: int = 3) -> pd.DataFrame:
    """KDJ Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate highest high and lowest low over the specified period
    highest_high = df_copy["high"].rolling(window=length).max()
    lowest_low = df_copy["low"].rolling(window=length).min()
    
    # Calculate Fast K (same as in Stochastic)
    hl_range = highest_high - lowest_low
    hl_range = hl_range.replace(0, np.nan)  # Avoid division by zero
    fastk = 100 * (df_copy["close"] - lowest_low) / hl_range
    
    # Calculate K using RMA (Wilder's Smoothing Method)
    alpha_k = 1 / signal
    k = fastk.ewm(alpha=alpha_k, adjust=False).mean()
    
    # Calculate D using RMA on K
    d = k.ewm(alpha=alpha_k, adjust=False).mean()
    
    # Calculate J line
    j = 3 * k - 2 * d
    
    # Add results to the DataFrame
    df_copy["k"] = k
    df_copy["d"] = d
    df_copy["j"] = j
    
    return df_copy[["k", "d", "j"]]


kdj.__doc__ = \
"""
Name:
    KDJ

Description:
    The KDJ indicator, also known as the Random Index, is a technical indicator used 
    to analyze market momentum and trend reversals. It is a modification of the 
    Stochastic Oscillator with an additional J line that represents the divergence 
    of the D value from the K.
    
    The indicator consists of three lines:
    - K line: Similar to %K in the Stochastic Oscillator
    - D line: Similar to %D in the Stochastic Oscillator
    - J line: Represents the divergence of D from K (calculated as 3K - 2D)
    
    Unlike the Stochastic Oscillator, which is bounded between 0 and 100, the J line 
    can go beyond these boundaries, providing additional signals about market extremes.

More info:
    https://www.investopedia.com/terms/s/stochasticoscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - length (int): The period for calculating highest high and lowest low. Default is 9.
    - signal (int): The smoothing period. Default is 3.

Call with:
    result = bta.kdj(df)
    df['k'] = result['k']
    df['d'] = result['d']
    df['j'] = result['j']

Returns:
    pd.DataFrame: DataFrame with 'k', 'd', and 'j' columns.
"""


def test():
    """
    Test function for the kdj indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the kdj indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(kdj)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 