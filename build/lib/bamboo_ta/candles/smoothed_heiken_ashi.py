# -*- coding: utf-8 -*-
# smoothed_heiken_ashi.py
import pandas as pd
import numpy as np


def smoothed_heiken_ashi(
    df: pd.DataFrame, len_: int = 10, len2: int = 10, fillna: bool = False
) -> pd.DataFrame:
    """Smoothed Heiken Ashi"""

    # Create a copy of the input DataFrame
    df_copy = df.copy()

    # First level smoothing using EMA on original OHLC prices
    ema_open = df_copy["open"].ewm(span=len_, adjust=False).mean()
    ema_close = df_copy["close"].ewm(span=len_, adjust=False).mean()
    ema_high = df_copy["high"].ewm(span=len_, adjust=False).mean()
    ema_low = df_copy["low"].ewm(span=len_, adjust=False).mean()

    # Compute first-level Heiken Ashi values
    ha_close = (ema_open + ema_high + ema_low + ema_close) / 4

    # Initialize ha_open with same index as df_copy
    ha_open = pd.Series(index=df_copy.index, dtype="float64")
    # For the first bar, set ha_open as the average of ema_open and ema_close
    ha_open.iloc[0] = (ema_open.iloc[0] + ema_close.iloc[0]) / 2

    # For subsequent bars, compute ha_open recursively
    for i in range(1, len(df_copy)):
        ha_open.iloc[i] = (ha_open.iloc[i - 1] + ha_close.iloc[i - 1]) / 2

    # Compute ha_high and ha_low
    ha_high = pd.concat([ema_high, ha_open, ha_close], axis=1).max(axis=1)
    ha_low = pd.concat([ema_low, ha_open, ha_close], axis=1).min(axis=1)

    # Second level smoothing on Heiken Ashi values using EMA
    sha_open = ha_open.ewm(span=len2, adjust=False).mean()
    sha_close = ha_close.ewm(span=len2, adjust=False).mean()
    sha_high = ha_high.ewm(span=len2, adjust=False).mean()
    sha_low = ha_low.ewm(span=len2, adjust=False).mean()

    # Determine candle color: red if sha_open > sha_close else green
    sha_color = pd.Series(
        np.where(sha_open > sha_close, "red", "green"), index=df_copy.index
    )

    # Optionally fill NaN values
    if fillna:
        sha_open = sha_open.fillna(0)
        sha_close = sha_close.fillna(0)
        sha_high = sha_high.fillna(0)
        sha_low = sha_low.fillna(0)
        sha_color = sha_color.fillna("")

    # Prepare final DataFrame with Smoothed Heiken Ashi values
    result = pd.DataFrame(
        {
            "sha_open": sha_open,
            "sha_high": sha_high,
            "sha_low": sha_low,
            "sha_close": sha_close,
            "sha_color": sha_color,
        }
    )

    return result


smoothed_heiken_ashi.__doc__ = """
Name:
    Smoothed Heiken Ashi Candles

Description:
    This function computes the Smoothed Heiken Ashi Candles using two levels of exponential 
    moving average (EMA) smoothing. The first smoothing is applied to the original OHLC 
    prices, and then the Heiken Ashi values are computed.
    A second smoothing is applied to the Heiken Ashi values to produce the final smoothed 
    candle values.

More info:
    https://www.investopedia.com/terms/h/heikenashi.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the columns 'open', 'high', 'low', and 'close'.
    - len_ (int): The period for the first level EMA smoothing of the original prices. Default is 10.
    - len2 (int): The period for the second level EMA smoothing of the Heiken Ashi values. Default is 10.
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    sha_result = bta.smoothed_heiken_ashi(df, len_=10, len2=10)
    df['sha_open'] = sha_result['sha_open']
    df['sha_high'] = sha_result['sha_high']
    df['sha_low'] = sha_result['sha_low']
    df['sha_close'] = sha_result['sha_close']
    df['sha_color'] = sha_result['sha_color']

Returns:
    pd.DataFrame: DataFrame with columns 'sha_open', 'sha_high', 'sha_low', 'sha_close', and 'sha_color'.
"""


def test():
    """
    Test function for the smoothed_heiken_ashi indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the smoothed_heiken_ashi indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(smoothed_heiken_ashi)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
