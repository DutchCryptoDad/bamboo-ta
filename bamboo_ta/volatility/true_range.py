# -*- coding: utf-8 -*-
# true_range.py
import numpy as np
import pandas as pd


def true_range(df: pd.DataFrame) -> pd.DataFrame:
    """True Range"""
    df_copy = df.copy()
    prev_close = df_copy["close"].shift()

    # Calculate the true range components
    true_range = pd.concat(
        [
            df_copy["high"] - df_copy["low"],
            (df_copy["high"] - prev_close).abs(),
            (df_copy["low"] - prev_close).abs(),
        ],
        axis=1,
    ).max(axis=1)

    df_copy["true_range"] = true_range

    return df_copy[["true_range"]]


true_range.__doc__ = """
Name:
    True Range (TR)

Description:
    The True Range indicator measures market volatility. True Range is defined as the greatest of the following:
    - The current high minus the current low
    - The absolute value of the current high minus the previous close
    - The absolute value of the current low minus the previous close
    
    This measure accounts for gaps in price movement and provides a more comprehensive 
    measure of price volatility than simply looking at the high-low range.

More info:
    https://www.investopedia.com/terms/a/atr.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.

Call with:
    df['true_range'] = bta.true_range(df)['true_range']

Returns:
    pd.DataFrame: DataFrame with 'true_range' column.
"""


def test():
    """
    Test function for the true_range indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the true_range indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(true_range)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
