# -*- coding: utf-8 -*-
# waddah_attar_explosion.py

import numpy as np
import pandas as pd


def waddah_attar_explosion(
    df: pd.DataFrame,
    sensitivity: int = 150,
    fast_length: int = 20,
    slow_length: int = 40,
    channel_length: int = 20,
    dead_zone: int = 20,
    mult: float = 2.0,
) -> pd.DataFrame:
    """
    Waddah Attar Explosion
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate EMA
    def calculate_ema(series, period):
        return series.ewm(span=period, adjust=False).mean()

    # Calculate MACD
    macd_fast = calculate_ema(df["close"], fast_length)
    macd_slow = calculate_ema(df["close"], slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity

    # Calculate the middle band (SMA)
    middle_band = df["close"].rolling(window=channel_length).mean()

    # Calculate the standard deviation
    std_dev = df["close"].rolling(window=channel_length).std(ddof=0)

    # Calculate upper and lower bands
    upper_band = middle_band + (std_dev * mult)
    lower_band = middle_band - (std_dev * mult)

    # Calculate the band width (explosion line)
    e1 = upper_band - lower_band

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy["trend_up"] = trend_up
    df_copy["trend_down"] = trend_down
    df_copy["explosion_line"] = e1
    df_copy["dead_zone_line"] = dead_zone

    return df_copy[["trend_up", "trend_down", "explosion_line", "dead_zone_line"]]


waddah_attar_explosion.__doc__ = """
Name:
    Waddah Attar Explosion Indicator

Description:
    The Waddah Attar Explosion indicator is used to identify potential breakout
    opportunities by combining the MACD and Bollinger Bands.

    Inspired by: https://www.tradingview.com/script/iu3kKWDI-Waddah-Attar-Explosion-LazyBear/

Call with:
    wae = bta.waddah_attar_explosion(df)
    df['trend_up'] = wae['trend_up']
    df['trend_down'] = wae['trend_down']
    df['explosion_line'] = wae['explosion_line']
    df['dead_zone_line'] = wae['dead_zone_line']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - dead_zone (int): Dead zone factor for the indicator. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

Returns:
    pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.
"""


def test():
    """
    Test function for the waddah_attar_explosion indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the waddah_attar_explosion indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(waddah_attar_explosion)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
