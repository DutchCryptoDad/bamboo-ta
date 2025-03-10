# -*- coding: utf-8 -*-
# fisher_transform.py

import pandas as pd
import numpy as np


def fisher_transform(df: pd.DataFrame, length: int = 9, signal: int = 1) -> pd.DataFrame:
    """Fisher Transform"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate HL2 (mid prices)
    hl2 = (df_copy["high"] + df_copy["low"]) / 2
    
    # Calculate the highest and lowest values over the specified period
    highest_hl2 = hl2.rolling(window=length).max()
    lowest_hl2 = hl2.rolling(window=length).min()
    
    # Calculate the range and ensure it's not too small
    hl_range = highest_hl2 - lowest_hl2
    hl_range = hl_range.replace(0, 0.001)
    hl_range = np.where(hl_range < 0.001, 0.001, hl_range)
    
    # Calculate the normalized price position in the range
    position = ((hl2 - lowest_hl2) / hl_range) - 0.5
    
    # Apply the Fisher Transform
    fisher_result = pd.Series(index=df_copy.index)
    v_prev = 0
    fisher_prev = 0
    
    # First values will be NaN until we have enough data
    fisher_result.iloc[:length-1] = np.nan
    fisher_result.iloc[length-1] = 0
    
    # Calculate Fisher Transform iteratively
    for i in range(length, len(df_copy)):
        v = 0.66 * position.iloc[i] + 0.67 * v_prev
        v = min(max(v, -0.999), 0.999)  # Bound v between -0.999 and 0.999
        fisher_result.iloc[i] = 0.5 * (np.log((1 + v) / (1 - v)) + fisher_prev)
        
        # Update previous values for next iteration
        v_prev = v
        fisher_prev = fisher_result.iloc[i]
    
    # Calculate the signal line
    signal_line = fisher_result.shift(signal)
    
    # Add results to the DataFrame
    df_copy["fisher"] = fisher_result
    df_copy["fisher_signal"] = signal_line
    
    return df_copy[["fisher", "fisher_signal"]]


fisher_transform.__doc__ = \
"""
Name:
    Fisher Transform

Description:
    The Fisher Transform is a technical indicator created by John F. Ehlers that 
    converts prices into a Gaussian normal distribution. The indicator aims to 
    identify significant price reversals by normalizing prices over a specified 
    period and applying a mathematical formula to amplify and clarify price turning points.
    
    The indicator consists of two lines: the Fisher Transform line and its signal line. 
    A reversal signal is suggested when these two lines cross. The indicator helps 
    traders identify potential overbought and oversold conditions and price reversal points.

More info:
    https://www.investopedia.com/terms/f/fisher-transform.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): The period for price normalization. Default is 9.
    - signal (int): The period for the signal line. Default is 1.

Call with:
    result = bta.fisher_transform(df)
    df['fisher'] = result['fisher']
    df['fisher_signal'] = result['fisher_signal']

Returns:
    pd.DataFrame: DataFrame with 'fisher' and 'fisher_signal' columns.
"""


def test():
    """
    Test function for the fisher_transform indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the fisher_transform indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(fisher_transform)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 