# -*- coding: utf-8 -*-
# heiken_ashi.py
import numpy as np
import pandas as pd


def heiken_ashi(df, pre_smoothing_period=None, post_smoothing_period=None):
    """Heiken Ashi"""

    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # If pre-smoothing is required
    if pre_smoothing_period:
        df_copy["open"] = EMA(df_copy, "open", pre_smoothing_period)
        df_copy["close"] = EMA(df_copy, "close", pre_smoothing_period)
        df_copy["high"] = EMA(df_copy, "high", pre_smoothing_period)
        df_copy["low"] = EMA(df_copy, "low", pre_smoothing_period)

    # Regular Heiken Ashi calculations
    df_copy["ha_close"] = (
        df_copy["open"] + df_copy["high"] + df_copy["low"] + df_copy["close"]
    ) / 4
    df_copy.reset_index(inplace=True)

    ha_open = [(df_copy["open"][0] + df_copy["close"][0]) / 2]
    [
        ha_open.append((ha_open[i] + df_copy["ha_close"].values[i]) / 2)
        for i in range(0, len(df_copy) - 1)
    ]

    df_copy["ha_open"] = ha_open
    df_copy.set_index("index", inplace=True)

    df_copy["ha_high"] = df_copy[["ha_open", "ha_close", "high"]].max(axis=1)
    df_copy["ha_low"] = df_copy[["ha_open", "ha_close", "low"]].min(axis=1)

    # If post-smoothing is required
    if post_smoothing_period:
        df_copy["ha_open"] = EMA(df_copy, "ha_open", post_smoothing_period)
        df_copy["ha_high"] = EMA(df_copy, "ha_high", post_smoothing_period)
        df_copy["ha_low"] = EMA(df_copy, "ha_low", post_smoothing_period)
        df_copy["ha_close"] = EMA(df_copy, "ha_close", post_smoothing_period)

    return df_copy[["ha_open", "ha_high", "ha_low", "ha_close"]]


heiken_ashi.__doc__ = """
Name:
    Heiken Ashi

Description:
    Heiken Ashi (HA) with Optional Pre and Post Smoothing

    Heiken Ashi is a type of price chart that shares some characteristics with
    candlestick charts but differs due to the values used to plot them. This
    modified version allows for optional smoothing of the original data before
    the Heiken Ashi calculation and/or smoothing of the Heiken Ashi values
    themselves, aiming to provide a more refined and smoother representation
    of price action, making it easier to identify the trend.

More info:
    https://www.investopedia.com/terms/h/heikenashi.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns:
        'open', 'high', 'low', and 'close'.
    - pre_smoothing_period (int, optional): Period for EMA pre-smoothing of the
        original data. If provided, original price bars are smoothed before Heiken
        Ashi calculations.
    - post_smoothing_period (int, optional): Period for EMA post-smoothing of
        Heiken Ashi values. If provided, Heiken Ashi values are smoothed post calculations.

Call with:
    ha_df = bta.heiken_ashi(df)
    df['ha_open'] = ha_df['ha_open']
    df['ha_high'] = ha_df['ha_high']
    df['ha_low'] = ha_df['ha_low']
    df['ha_close'] = ha_df['ha_close']

Returns:
    pd.DataFrame: DataFrame with 'ha_open', 'ha_high', 'ha_low', and 'ha_close' columns.
"""


def test():
    """
    Test function for the heiken_ashi indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the heiken_ashi indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(heiken_ashi)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
