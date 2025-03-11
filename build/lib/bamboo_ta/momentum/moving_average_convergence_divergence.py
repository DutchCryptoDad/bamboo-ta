# -*- coding: utf-8 -*-
# moving_average_convergence_divergence.py

import pandas as pd
import numpy as np

def macd(
    df: pd.DataFrame, 
    column: str = 'close', 
    short_window: int = 12, 
    long_window: int = 26, 
    signal_window: int = 9
) -> pd.DataFrame:
    """Moving Average Convergence Divergence (MACD)"""
    def ema_calculation(series, span):
        return series.ewm(span=span, adjust=False).mean()

    short_ema = ema_calculation(df[column], span=short_window)
    long_ema = ema_calculation(df[column], span=long_window)
    macd = short_ema - long_ema
    signal = ema_calculation(macd, span=signal_window)
    histogram = macd - signal

    df_copy = df.copy()
    df_copy['macd'] = macd
    df_copy['macd_signal'] = signal
    df_copy['macd_histogram'] = histogram
    
    return df_copy[['macd', 'macd_signal', 'macd_histogram']]

macd.__doc__ = \
"""
Name:
    Moving Average Convergence Divergence (MACD)

Description:
    MACD is a trend-following momentum indicator that shows the relationship 
    between two moving averages of a security's price.

More info:
    https://www.investopedia.com/terms/m/macd.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which MACD is to be calculated. Default is "close".
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - signal_window (int): The signal line period for EMA. Default is 9.

Call with:
    macd_result = bta.macd(df, 'close', 12, 26, 9)
    df['macd'] = macd_result['macd']
    df['macd_signal'] = macd_result['macd_signal']
    df['macd_histogram'] = macd_result['macd_histogram']

Returns:
    pd.DataFrame: DataFrame with 'macd', 'macd_signal', and 'macd_histogram' columns.
"""

def test():
    """
    Test function for the macd indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the macd indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(macd)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
