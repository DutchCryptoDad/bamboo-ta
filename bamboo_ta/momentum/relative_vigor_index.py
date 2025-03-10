# -*- coding: utf-8 -*-
# relative_vigor_index.py

import pandas as pd
import numpy as np


def relative_vigor_index(df: pd.DataFrame, length: int = 14, swma_length: int = 4) -> pd.DataFrame:
    """Relative Vigor Index"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate close-open range and high-low range
    close_open_range = df_copy["close"] - df_copy["open"]
    high_low_range = df_copy["high"] - df_copy["low"]
    
    # Handle potential division by zero in high-low range
    high_low_range = high_low_range.replace(0, np.nan)
    
    # Apply SWMA (Symmetrically Weighted Moving Average)
    co_swma = symmetrically_weighted_ma(close_open_range, swma_length)
    hl_swma = symmetrically_weighted_ma(high_low_range, swma_length)
    
    # Calculate the sum over the specified period
    co_sum = co_swma.rolling(window=length).sum()
    hl_sum = hl_swma.rolling(window=length).sum()
    
    # Calculate RVI
    rvi = co_sum / hl_sum
    
    # Calculate the signal line (SWMA of RVI)
    signal = symmetrically_weighted_ma(rvi, swma_length)
    
    # Add results to the DataFrame
    df_copy["rvi"] = rvi
    df_copy["rvi_signal"] = signal
    
    return df_copy[["rvi", "rvi_signal"]]


def symmetrically_weighted_ma(series, length):
    """
    Calculate Symmetrically Weighted Moving Average
    
    This is a weighted moving average where the weights are symmetric and sum to 1.
    For example, with length=4, the weights are [1/6, 2/6, 2/6, 1/6].
    """
    weights = None
    if length == 4:  # Most common case
        weights = np.array([1/6, 2/6, 2/6, 1/6])
    else:
        # Generate symmetric weights for any length
        half = length // 2
        if length % 2 == 0:  # Even length
            weights = np.concatenate([
                np.arange(1, half + 1),
                np.arange(half, 0, -1)
            ])
        else:  # Odd length
            mid = (length + 1) // 2
            weights = np.concatenate([
                np.arange(1, mid),
                np.array([mid]),
                np.arange(mid - 1, 0, -1)
            ])
        weights = weights / weights.sum()  # Normalize to sum to 1
    
    # Apply the weighted moving average
    result = series.rolling(window=length).apply(
        lambda x: np.sum(x * weights[:len(x)]) if len(x) == length else np.nan,
        raw=True
    )
    
    return result


relative_vigor_index.__doc__ = \
"""
Name:
    Relative Vigor Index

Description:
    The Relative Vigor Index (RVI) is a momentum oscillator that measures the 
    strength of a trend by comparing the closing price to the trading range. 
    It is based on the observation that during uptrends, prices tend to close 
    higher than they open, while during downtrends, prices tend to close lower 
    than they open.
    
    The indicator consists of two lines: the RVI line and its signal line.
    A buy signal may be generated when the RVI line crosses above the signal line,
    while a sell signal may occur when the RVI line crosses below the signal line.

More info:
    https://www.investopedia.com/terms/r/relative_vigor_index.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 
      'low', and 'close' columns.
    - length (int): The period for summing the SWMA values. Default is 14.
    - swma_length (int): The period for the Symmetrically Weighted Moving Average. 
      Default is 4.

Call with:
    result = bta.relative_vigor_index(df)
    df['rvi'] = result['rvi']
    df['rvi_signal'] = result['rvi_signal']

Returns:
    pd.DataFrame: DataFrame with 'rvi' and 'rvi_signal' columns.
"""


def test():
    """
    Test function for the relative_vigor_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the relative_vigor_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(relative_vigor_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 