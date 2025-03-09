# -*- coding: utf-8 -*-
# stochastics_oscillator.py

import pandas as pd


def stochastics_oscillator(
    df: pd.DataFrame,
    high_col: str = "high",
    low_col: str = "low",
    close_col: str = "close",
    window: int = 14,
    smooth_window: int = 3,
    fillna: bool = False,
) -> pd.DataFrame:
    """Stochastic Oscillator"""
    df_copy = df.copy()

    high = df_copy[high_col]
    low = df_copy[low_col]
    close = df_copy[close_col]

    min_periods = 0 if fillna else window
    smin = low.rolling(window, min_periods=min_periods).min()
    smax = high.rolling(window, min_periods=min_periods).max()
    stoch_k = 100 * (close - smin) / (smax - smin)
    if fillna:
        stoch_k = stoch_k.fillna(50)

    min_periods = 0 if fillna else smooth_window
    stoch_d = stoch_k.rolling(smooth_window, min_periods=min_periods).mean()
    if fillna:
        stoch_d = stoch_d.fillna(50)

    stoch_hist = stoch_k - stoch_d
    if fillna:
        stoch_hist = stoch_hist.fillna(0)

    df_copy["stoch"] = stoch_k
    df_copy["stoch_signal"] = stoch_d
    df_copy["stoch_hist"] = stoch_hist

    return df_copy[["stoch", "stoch_signal", "stoch_hist"]]


stochastics_oscillator.__doc__ = """
Name:
    Stochastic Oscillator, Stochastic Signal, and Histogram Combined.

Description:
    The Stochastic Oscillator is a momentum indicator comparing a particular
    closing price of a security to a range of its prices over a certain period of time.

Call with:
    stoch = bta.stochastics_oscillator(df, 'high', 'low', 'close', 14, 3)
    df['stoch'] = stoch['stoch']
    df['stoch_signal'] = stoch['stoch_signal']
    df['stoch_hist'] = stoch['stoch_hist']

Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - high_col (str): Column name for 'High' prices. Default is 'high'.
    - low_col (str): Column name for 'Low' prices. Default is 'low'.
    - close_col (str): Column name for 'Close' prices. Default is 'close'.
    - window (int): Lookback period for stochastic calculation. Default is 14.
    - smooth_window (int): Lookback period for signal calculation. Default is 3.
    - fillna (bool): If True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with 'stoch', 'stoch_signal', and 'stoch_hist' columns.
"""


def test():
    """
    Test function for the stochastics_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the stochastics_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(stochastics_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
