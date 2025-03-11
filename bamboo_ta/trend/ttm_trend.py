# -*- coding: utf-8 -*-
# ttm_trend.py

import pandas as pd
import numpy as np


def ttm_trend(
    df: pd.DataFrame,
    length: int = 6
) -> pd.DataFrame:
    """TTM Trend Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 6
    
    # Calculate the average price of the previous 'length' bars
    # First calculate HL2 for the current bar
    trend_avg = (df_copy["high"] + df_copy["low"]) / 2
    
    # Add HL2 for the previous bars
    for i in range(1, length):
        trend_avg = trend_avg + (df_copy["high"].shift(i) + df_copy["low"].shift(i)) / 2
    
    # Divide by the length to get the average
    trend_avg = trend_avg / length
    
    # Determine the trend: 1 if close > trend_avg, -1 otherwise
    ttm_trend_val = (df_copy["close"] > trend_avg).astype(int)
    ttm_trend_val = ttm_trend_val.replace(0, -1)
    
    # Store results in DataFrame
    df_copy["ttm_trend"] = ttm_trend_val
    
    return df_copy[["ttm_trend"]]


ttm_trend.__doc__ = \
"""
Name:
    TTM Trend

Description:
    The TTM Trend indicator is from John Carter's book "Mastering the Trade" and is designed
    to identify the current trend direction. It compares the current closing price to the
    average price of the previous 'length' bars.
    
    The indicator returns:
    - 1 (bullish/uptrend) when the close is above the average price
    - -1 (bearish/downtrend) when the close is below the average price
    
    In traditional implementations, this indicator is used to color price bars green (bullish)
    or red (bearish). A common trading strategy is to consider a change in trend after two
    consecutive bars of the opposite color.
    
    This indicator can help traders stay in a trade until the trend changes, providing a
    simple yet effective way to identify potential entry and exit points.

More info:
    https://www.prorealcode.com/prorealtime-indicators/ttm-trend-price/
    John Carter's book "Mastering the Trade"

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The number of bars to include in the average price calculation. Default is 6.

Call with:
    result = bta.ttm_trend(df, length=6)
    df['ttm_trend'] = result['ttm_trend']  # 1 for bullish, -1 for bearish

Returns:
    pd.DataFrame: DataFrame with 'ttm_trend' column containing the indicator values (1 or -1).
"""


def test():
    """
    Test function for the ttm_trend indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ttm_trend indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ttm_trend)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 