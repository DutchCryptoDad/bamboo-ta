# -*- coding: utf-8 -*-
# range_filter.py
import numpy as np
import pandas as pd


def range_filter(
    df: pd.DataFrame,
    column: str = "close",
    period: int = 100,
    multiplier: float = 3.0,
    fillna: bool = False,
) -> pd.DataFrame:
    """Range Filter Buy and Sell Indicator"""

    # Define internal EMA function
    def ema(series, span):
        """Exponential Moving Average (EMA)"""
        return series.ewm(span=span, adjust=False).mean()

    # Compute smoothed range
    price = df[column]
    abs_diff = np.abs(price - price.shift(1))
    avg_range = ema(abs_diff, period)
    smooth_range = ema(avg_range, period * 2 - 1) * multiplier

    # Initialize filter
    filt = price.copy()

    for i in range(1, len(df)):
        prev_filt = filt.iloc[i - 1] if i > 0 else price.iloc[i]
        if price.iloc[i] > prev_filt:
            filt.iloc[i] = max(prev_filt, price.iloc[i] - smooth_range.iloc[i])
        elif price.iloc[i] < prev_filt:
            filt.iloc[i] = min(prev_filt, price.iloc[i] + smooth_range.iloc[i])
        else:
            filt.iloc[i] = prev_filt

    # Determine trend direction
    upward = np.zeros(len(df))
    downward = np.zeros(len(df))

    for i in range(1, len(df)):
        if filt.iloc[i] > filt.iloc[i - 1]:
            upward[i] = upward[i - 1] + 1
        elif filt.iloc[i] < filt.iloc[i - 1]:
            downward[i] = downward[i - 1] + 1
        else:
            upward[i] = upward[i - 1]
            downward[i] = downward[i - 1]

    # Calculate bands
    high_band = filt + smooth_range
    low_band = filt - smooth_range

    # Generate buy/sell signals
    long_signal = ((price > filt) & (price > price.shift(1)) & (upward > 0)) | (
        (price > filt) & (price < price.shift(1)) & (upward > 0)
    )

    short_signal = ((price < filt) & (price < price.shift(1)) & (downward > 0)) | (
        (price < filt) & (price > price.shift(1)) & (downward > 0)
    )

    # Ensure signal continuity
    cond_ini = np.zeros(len(df))
    for i in range(1, len(df)):
        if long_signal.iloc[i]:
            cond_ini[i] = 1
        elif short_signal.iloc[i]:
            cond_ini[i] = -1
        else:
            cond_ini[i] = cond_ini[i - 1]

    long_signal = long_signal & (pd.Series(cond_ini).shift(1) == -1)
    short_signal = short_signal & (pd.Series(cond_ini).shift(1) == 1)

    if fillna:
        filt.fillna(method="bfill", inplace=True)
        high_band.fillna(method="bfill", inplace=True)
        low_band.fillna(method="bfill", inplace=True)
        long_signal.fillna(False, inplace=True)
        short_signal.fillna(False, inplace=True)

    df_copy = df.copy()
    df_copy["range_filter"] = filt
    df_copy["high_band"] = high_band
    df_copy["low_band"] = low_band
    df_copy["long_signal"] = long_signal.astype(int)  # Convert boolean to int (0 or 1)
    df_copy["short_signal"] = short_signal.astype(int)

    return df_copy[
        ["range_filter", "high_band", "low_band", "long_signal", "short_signal"]
    ]


range_filter.__doc__ = """
Name:
    Range Filter Buy and Sell Indicator

Description:
    This indicator smooths price action using a range filter based on a volatility-adjusted
    moving average. It identifies uptrends and downtrends while filtering out noise.

More info:
    https://www.tradingview.com/script/J3TL15C9-Range-Filter-Strategy/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which the range filter is calculated. Default is "close".
    - period (int): Sampling period for smoothing range calculation. Default is 100.
    - multiplier (float): Multiplier for the smoothed range. Default is 3.0.
    - fillna (bool): If True, fills nan values. Default is False.

Call with:
    range_filter_result = bta.range_filter(df, "close", 100, 3.0)
    df["range_filter"] = range_filter_result["range_filter"]
    df["high_band"] = range_filter_result["high_band"]
    df["low_band"] = range_filter_result["low_band"]
    df["long_signal"] = range_filter_result["long_signal"]
    df["short_signal"] = range_filter_result["short_signal"]

Returns:
    pd.DataFrame: DataFrame with 'range_filter', 'high_band', 'low_band', 'long_signal', 'short_signal'.
"""


def test():
    """
    Test function for the range_filter indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the range_filter indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(range_filter)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
