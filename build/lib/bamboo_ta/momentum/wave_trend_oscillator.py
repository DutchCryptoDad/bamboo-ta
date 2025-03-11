# -*- coding: utf-8 -*-
# wave_trend_oscillator.py

import pandas as pd


def wave_trend_oscillator(
    df: pd.DataFrame, src: str = "close", n1: int = 8, n2: int = 12
) -> pd.DataFrame:
    """WaveTrend Oscillator"""

    df_copy = df.copy()

    # Get the source series
    src_series = df[src]

    # Define exponential moving average function
    def exponential_moving_average(series, period):
        """Calculate Exponential Moving Average for a given series"""
        return series.ewm(span=period, adjust=False).mean()

    # Define simple moving average function
    def simple_moving_average(series, period):
        """Calculate Simple Moving Average for a given series"""
        return series.rolling(window=period).mean()

    # Calculate EMA of source
    ema_src = exponential_moving_average(src_series, n1)

    # Calculate absolute difference between source and EMA
    diff_series = (src_series - ema_src).abs()

    # Calculate D (Exponential Moving Average of absolute difference)
    d = exponential_moving_average(diff_series, n1)

    # Calculate CI (Channel Index)
    ci = (src_series - ema_src) / (0.015 * d)

    # Calculate TCI (Exponential Moving Average of CI)
    tci = exponential_moving_average(ci, n2)

    # Calculate WaveTrend Oscillator (difference between TCI and SMA of TCI)
    wavetrend = tci - simple_moving_average(tci, 4)

    df_copy["wavetrend"] = wavetrend

    return df_copy[["wavetrend"]]


wave_trend_oscillator.__doc__ = """
Name:
    WaveTrend Oscillator

Description:
    The WaveTrend Oscillator is used to identify overbought and oversold conditions
    in the market.

    Inspired by:

Call with:
    df['wto'] = bta.wave_trend_oscillator(df, 'close')['wavetrend']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - n1 (int): Length for the first EMA. Default is 8.
    - n2 (int): Length for the second EMA. Default is 12.

Returns:
    pd.DataFrame: DataFrame with 'wavetrend' column.
"""


def test():
    """
    Test function for the wave_trend_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the wave_trend_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(wave_trend_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
