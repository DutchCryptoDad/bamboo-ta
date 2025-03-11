# -*- coding: utf-8 -*-
# waddah_attar_explosion_atr.py

import numpy as np
import pandas as pd


def waddah_attar_explosion_atr(
    df: pd.DataFrame,
    sensitivity: int = 150,
    fast_length: int = 20,
    slow_length: int = 40,
    channel_length: int = 20,
    mult: float = 2.0,
) -> pd.DataFrame:
    """Waddah Attar Explosion ATR"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate EMA
    def calculate_ema(series, period):
        return series.ewm(span=period, adjust=False).mean()

    # Calculate RMA
    def calculate_rma(series, period):
        return series.ewm(alpha=1 / period, adjust=False).mean()

    # Calculate DEAD_ZONE
    true_range = pd.DataFrame(
        {
            "high_low": df["high"] - df["low"],
            "high_close": (df["high"] - df["close"].shift()).abs(),
            "low_close": (df["low"] - df["close"].shift()).abs(),
        }
    )
    true_range["true_range"] = true_range[["high_low", "high_close", "low_close"]].max(
        axis=1
    )
    dead_zone = calculate_rma(true_range["true_range"], 100) * 3.7

    # Calculate MACD
    macd_fast = calculate_ema(df["close"], fast_length)
    macd_slow = calculate_ema(df["close"], slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity

    # Calculate Bollinger Bands
    # Calculate Bollinger Bands manually
    bb_middle = df["close"].rolling(window=channel_length).mean()
    bb_std = df["close"].rolling(window=channel_length).std()
    bb_upper = bb_middle + (bb_std * mult)
    bb_lower = bb_middle - (bb_std * mult)
    bb = pd.DataFrame({"bb_upper": bb_upper, "bb_lower": bb_lower})
    e1 = bb["bb_upper"] - bb["bb_lower"]

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy["trend_up"] = trend_up
    df_copy["trend_down"] = trend_down
    df_copy["explosion_line"] = e1
    df_copy["dead_zone_line"] = dead_zone.values

    return df_copy[["trend_up", "trend_down", "explosion_line", "dead_zone_line"]]


waddah_attar_explosion_atr.__doc__ = """
Name:
    Waddah Attar Explosion ATR

Description:
    The Waddah Attar Explosion indicator is used to identify potential breakout
    opportunities by combining the MACD and Bollinger Bands. The dead zone line
    is based on ATR in this indicator.

    Inspired by: https://www.tradingview.com/script/d9IjcYyS-Waddah-Attar-Explosion-V2-SHK/

Call with:
    wae = bta.waddah_attar_explosion_atr(df)
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
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

Returns:
    pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.
"""


def test():
    """
    Test function for the waddah_attar_explosion_atr indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the waddah_attar_explosion_atr indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(waddah_attar_explosion_atr)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
