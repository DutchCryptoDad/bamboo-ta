# -*- coding: utf-8 -*-
# wave_trend.py

import pandas as pd


def wave_trend(
    df: pd.DataFrame, chlen: int = 10, avg: int = 21, smalen: int = 4
) -> pd.DataFrame:
    """WaveTrend"""
    df_copy = df.copy()

    # Calculate HLC3 (typical price)
    df_copy["hlc3"] = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3

    # Define exponential moving average function
    def exponential_moving_average(df, column, period):
        """Calculate Exponential Moving Average for a given column"""
        return df[column].ewm(span=period, adjust=False).mean()

    # Calculate ESA (Exponential Moving Average of HLC3)
    df_copy["esa"] = exponential_moving_average(df_copy, "hlc3", chlen)

    # Calculate absolute difference between HLC3 and ESA
    df_copy["abs_diff"] = (df_copy["hlc3"] - df_copy["esa"]).abs()

    # Calculate D (Exponential Moving Average of absolute difference)
    df_copy["d"] = exponential_moving_average(df_copy, "abs_diff", chlen)

    # Calculate CI (Channel Index)
    df_copy["ci"] = (df_copy["hlc3"] - df_copy["esa"]) / (0.015 * df_copy["d"])

    # Calculate TCI (Exponential Moving Average of CI)
    df_copy["tci"] = exponential_moving_average(df_copy, "ci", avg)

    # Set WT1 equal to TCI
    df_copy["wt1"] = df_copy["tci"]

    # Calculate WT2 as Simple Moving Average of WT1
    df_copy["wt2"] = df_copy["wt1"].rolling(window=smalen).mean()

    return df_copy[["wt1", "wt2"]]


wave_trend.__doc__ = """
Name:
    WaveTrend

Description:
    The WaveTrend is used to identify overbought and oversold conditions in the market.

Inspired by:
    https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/

Call with:
    wt = bta.wave_trend(df, chlen=10, avg=21, smalen=4)
    df['wt1'] = wt['wt1']
    df['wt2'] = wt['wt2']

Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - chlen (int): Channel length for the EMA calculation. Default is 10.
    - avg (int): Average period for the EMA calculation. Default is 21.
    - smalen (int): Period for the SMA calculation. Default is 4.

Returns:
    pd.DataFrame: DataFrame with 'wt1' and 'wt2' columns.
"""


def test():
    """
    Test function for the wave_trend indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the wave_trend indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(wave_trend)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
