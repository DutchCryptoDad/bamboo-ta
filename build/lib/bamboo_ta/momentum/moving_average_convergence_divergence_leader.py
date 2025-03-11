# -*- coding: utf-8 -*-
# moving_average_convergence_divergence_leader.py

import pandas as pd
import numpy as np

def macd_leader(
    df: pd.DataFrame, 
    src: str = 'close', 
    fast_length: int = 12, 
    slow_length: int = 26, 
    signal_length: int = 9
) -> pd.DataFrame:
    """MACD Leader"""
    def ema_calculation(series, span):
        return series.ewm(span=span, adjust=False).mean()

    df_copy = df.copy()
    src_series = df[src]

    sema = ema_calculation(src_series, span=fast_length)
    lema = ema_calculation(src_series, span=slow_length)
    diff_sema = src_series - sema
    diff_lema = src_series - lema
    i1 = sema + ema_calculation(diff_sema, span=fast_length)
    i2 = lema + ema_calculation(diff_lema, span=slow_length)
    macd_leader = ((i1 - i2) / 10) * 10

    df_copy['macd_leader'] = macd_leader
    
    return df_copy[['macd_leader']]

macd_leader.__doc__ = \
"""
Name:
    MACD Leader

Description:
    The MACD Leader is a variation of the standard MACD that aims to provide an 
    earlier signal by using a different calculation method.

More info:
    https://www.investopedia.com/terms/m/macd.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - fast_length (int): Length for the fast EMA. Default is 12.
    - slow_length (int): Length for the slow EMA. Default is 26.
    - signal_length (int): Length for the signal EMA. Default is 9.

Call with:
    df['macd_leader'] = bta.macd_leader(df, 'close')['macd_leader']

Returns:
    pd.DataFrame: DataFrame with 'macd_leader' column.
"""

def test():
    """
    Test function for the macd_leader indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the macd_leader indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(macd_leader)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
