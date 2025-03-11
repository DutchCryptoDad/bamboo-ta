# -*- coding: utf-8 -*-
# average_true_range.py
import numpy as np
import pandas as pd


def average_true_range(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """Average True Range"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate True Range components
    df_copy["high_low"] = df_copy["high"] - df_copy["low"]
    df_copy["high_close"] = (df_copy["high"] - df_copy["close"].shift()).abs()
    df_copy["low_close"] = (df_copy["low"] - df_copy["close"].shift()).abs()

    # Calculate True Range
    df_copy["true_range"] = df_copy[["high_low", "high_close", "low_close"]].max(axis=1)

    # Calculate ATR as the rolling mean of True Range
    df_copy["atr"] = df_copy["true_range"].rolling(window=period, min_periods=1).mean()

    return df_copy[["atr"]]


average_true_range.__doc__ = """
Name:
    Average True Range (ATR)

Description:
    The Average True Range (ATR), smoothed by the Moving Average, is a measure of volatility. 
    It was introduced by Welles Wilder in his book 'New Concepts in Technical Trading Systems'.
    ATR is a volatility indicator that measures market volatility by decomposing the entire
    range of an asset price for a specific period.

More info:
    https://www.investopedia.com/terms/a/atr.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high', 'low', and 'close'.
    - period (int): Period for the ATR calculation. Default is 14.

Call with:
    df['atr'] = bta.average_true_range(df, 14)['atr']

Returns:
    pd.DataFrame: DataFrame with 'atr' column.
"""


def test():
    """
    Test function for the average_true_range indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the average_true_range indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(average_true_range)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
