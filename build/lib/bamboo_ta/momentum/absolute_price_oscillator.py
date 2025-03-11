# -*- coding: utf-8 -*-
# absolute_price_oscillator.py

import pandas as pd


def absolute_price_oscillator(df: pd.DataFrame, fast_length: int = 12, slow_length: int = 26, mamode: str = "sma") -> pd.DataFrame:
    """Absolute Price Oscillator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Make sure fast_length < slow_length
    if fast_length > slow_length:
        fast_length, slow_length = slow_length, fast_length
    
    # Calculate the moving averages based on the mode
    if mamode.lower() == "sma":
        fast_ma = df_copy["close"].rolling(window=fast_length).mean()
        slow_ma = df_copy["close"].rolling(window=slow_length).mean()
    elif mamode.lower() == "ema":
        fast_ma = df_copy["close"].ewm(span=fast_length, adjust=False).mean()
        slow_ma = df_copy["close"].ewm(span=slow_length, adjust=False).mean()
    else:
        raise ValueError("mamode must be either 'sma' or 'ema'")
    
    # Calculate APO
    df_copy["apo"] = fast_ma - slow_ma
    
    return df_copy[["apo"]]


absolute_price_oscillator.__doc__ = \
"""
Name:
    Absolute Price Oscillator

Description:
    The Absolute Price Oscillator (APO) is a momentum indicator that measures 
    the difference between two moving averages, typically an exponential 
    moving average (EMA). It's similar to the MACD (Moving Average Convergence 
    Divergence) but doesn't include a signal line. The APO helps identify the 
    momentum and trend direction of a security.

More info:
    https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/absolute-price-oscillator-apo/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - fast_length (int): Period for the faster moving average. Default is 12.
    - slow_length (int): Period for the slower moving average. Default is 26.
    - mamode (str): Moving average type, either 'sma' or 'ema'. Default is 'sma'.

Call with:
    df['apo'] = bta.absolute_price_oscillator(df)['apo']

For Signal line:
    df['apo_signal'] = df['apo'].rolling(window=9).mean()  # Using SMA for signal

Returns:
    pd.DataFrame: DataFrame with 'apo' column.
"""


def test():
    """
    Test function for the absolute_price_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the absolute_price_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(absolute_price_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 