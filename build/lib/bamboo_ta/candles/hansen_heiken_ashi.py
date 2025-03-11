# -*- coding: utf-8 -*-
# hansen_heiken_ashi.py
import numpy as np
import pandas as pd


def hansen_heiken_ashi(df: pd.DataFrame, period: int = 6) -> pd.DataFrame:
    """Hansen Heiken Ashi"""

    # Create a copy of the DataFrame to prevent altering the original
    df_copy = df.copy()

    # Calculate the Hansen Heikin Ashi components
    df_copy["hhclose"] = (
        df_copy["open"] + df_copy["high"] + df_copy["low"] + df_copy["close"]
    ) / 4
    df_copy["hhopen"] = (
        df_copy["open"].shift(2) + df_copy["close"].shift(2)
    ) / 2  # Modified formula
    df_copy["hhhigh"] = df_copy[["open", "close", "high"]].max(axis=1)
    df_copy["hhlow"] = df_copy[["open", "close", "low"]].min(axis=1)

    # Apply smoothing with SMA
    df_copy["emac"] = df_copy["hhclose"].rolling(window=period).mean()
    df_copy["emao"] = df_copy["hhopen"].rolling(window=period).mean()

    # Return the calculated components
    return df_copy[["emac", "emao"]]


hansen_heiken_ashi.__doc__ = """
Name:
    Hansen Heiken Ashi (HHA)

Description:
    The Hansen Heiken Ashi is a modified version of the Heiken Ashi candlestick calculation
    with additional smoothing using a Simple Moving Average (SMA). It aims to reduce noise
    in the data for better trend visualization.

More info:
    https://www.investopedia.com/terms/h/heikenashi.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC (open, high, low, close) data.
    - period (int): Period for the Simple Moving Average (SMA) to smooth data. Default is 6.

Call with:
    hha_result = bta.hansen_heiken_ashi(df, period=6)
    df['hha_emac'] = hha_result['emac']
    df['hha_emao'] = hha_result['emao']

Returns:
    pd.DataFrame: DataFrame containing the smoothed 'emac' and 'emao' columns.
"""


def test():
    """
    Test function for the hansen_heiken_ashi indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the hansen_heiken_ashi indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(hansen_heiken_ashi)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
