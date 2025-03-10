# -*- coding: utf-8 -*-
# coppock_curve.py

import pandas as pd
import numpy as np


def coppock_curve(df: pd.DataFrame, length: int = 10, fast: int = 11, slow: int = 14) -> pd.DataFrame:
    """Coppock Curve"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate Rate of Change for fast and slow periods
    fast_roc = df_copy["close"].pct_change(fast) * 100
    slow_roc = df_copy["close"].pct_change(slow) * 100
    
    # Sum the ROC values
    total_roc = fast_roc + slow_roc
    
    # Apply weighted moving average to the sum
    def weighted_ma(window):
        if len(window) < length:
            return np.nan
        weights = np.arange(1, len(window) + 1)
        return np.sum(window * weights) / np.sum(weights)
    
    df_copy["coppock"] = total_roc.rolling(window=length).apply(
        weighted_ma, raw=True
    )
    
    return df_copy[["coppock"]]


coppock_curve.__doc__ = \
"""
Name:
    Coppock Curve

Description:
    The Coppock Curve is a long-term price momentum indicator developed by Edwin 
    Sedgwick Coppock. It was originally designed for monthly analysis of equity 
    indices, intended to identify major bottoms in the stock market. The indicator 
    uses rate of change and a weighted moving average to identify long-term trend changes.
    
    It's typically used as a buy signal when it crosses above zero from below. The indicator 
    is particularly effective in identifying major market bottoms following significant 
    declines.

More info:
    https://en.wikipedia.org/wiki/Coppock_curve
    https://www.investopedia.com/terms/c/coppockcurve.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the weighted moving average. Default is 10.
    - fast (int): The faster ROC period. Default is 11.
    - slow (int): The slower ROC period. Default is 14.

Call with:
    df['coppock'] = bta.coppock_curve(df)['coppock']

Returns:
    pd.DataFrame: DataFrame with 'coppock' column.
"""


def test():
    """
    Test function for the coppock_curve indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the coppock_curve indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(coppock_curve)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 