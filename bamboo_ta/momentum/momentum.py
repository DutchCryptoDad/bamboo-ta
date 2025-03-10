# -*- coding: utf-8 -*-
# momentum.py

import pandas as pd
import numpy as np


def momentum(df: pd.DataFrame, length: int = 10) -> pd.DataFrame:
    """Momentum Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate Momentum
    df_copy["mom"] = df_copy["close"].diff(length)
    
    return df_copy[["mom"]]


momentum.__doc__ = \
"""
Name:
    Momentum

Description:
    The Momentum indicator measures the amount that a security's price has changed over 
    a given time period. It simply shows the difference between the current price and 
    the price "n" periods ago.
    
    It is one of the simplest momentum indicators to use and understand. The momentum 
    indicator can be used as a trend-following oscillator similar to the Moving Average 
    Convergence Divergence (MACD). When used this way, buy signals are generated when 
    the indicator crosses above zero, and sell signals when it crosses below zero.

More info:
    https://www.investopedia.com/terms/m/momentum.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for momentum calculation. Default is 10.

Call with:
    df['mom'] = bta.momentum(df)['mom']

Returns:
    pd.DataFrame: DataFrame with 'mom' column.
"""


def test():
    """
    Test function for the momentum indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the momentum indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(momentum)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 