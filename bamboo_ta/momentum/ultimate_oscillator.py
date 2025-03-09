# -*- coding: utf-8 -*-
# ultimate_oscillator.py

import pandas as pd
import numpy as np


def ultimate_oscillator(
    df: pd.DataFrame,
    high_col: str = "high",
    low_col: str = "low",
    close_col: str = "close",
    window1: int = 7,
    window2: int = 14,
    window3: int = 28,
    weight1: float = 4.0,
    weight2: float = 2.0,
    weight3: float = 1.0,
    fillna: bool = False,
) -> pd.DataFrame:
    """Ultimate Oscillator"""
    df_copy = df.copy()

    close_shift = df_copy[close_col].shift(1)
    true_range = np.maximum(df_copy[high_col], close_shift) - np.minimum(
        df_copy[low_col], close_shift
    )
    buying_pressure = df_copy[close_col] - np.minimum(df_copy[low_col], close_shift)

    min_periods_s = 0 if fillna else window1
    min_periods_m = 0 if fillna else window2
    min_periods_l = 0 if fillna else window3

    avg_s = (
        buying_pressure.rolling(window1, min_periods=min_periods_s).sum()
        / true_range.rolling(window1, min_periods=min_periods_s).sum()
    )
    avg_m = (
        buying_pressure.rolling(window2, min_periods=min_periods_m).sum()
        / true_range.rolling(window2, min_periods=min_periods_m).sum()
    )
    avg_l = (
        buying_pressure.rolling(window3, min_periods=min_periods_l).sum()
        / true_range.rolling(window3, min_periods=min_periods_l).sum()
    )

    uo = (
        100.0
        * ((weight1 * avg_s) + (weight2 * avg_m) + (weight3 * avg_l))
        / (weight1 + weight2 + weight3)
    )

    if fillna:
        uo = uo.fillna(50)

    df_copy["uo"] = uo

    return df_copy[["uo"]]


ultimate_oscillator.__doc__ = """
Name:
    Ultimate Oscillator

Description:
    The Ultimate Oscillator combines short-term, intermediate-term, and long-term
    price action into one oscillator.

Call with:
    df['uo'] = bta.ultimate_oscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']

Parameters:
    - df (pandas.DataFrame): DataFrame containing the data.
    - high_col (str): Name of the column containing high price data. Default is 'high'.
    - low_col (str): Name of the column containing low price data. Default is 'low'.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window1 (int): Short period. Default is 7.
    - window2 (int): Medium period. Default is 14.
    - window3 (int): Long period. Default is 28.
    - weight1 (float): Weight of short BP average for UO. Default is 4.0.
    - weight2 (float): Weight of medium BP average for UO. Default is 2.0.
    - weight3 (float): Weight of long BP average for UO. Default is 1.0.
    - fillna (bool): If True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with 'uo' column.
"""


def test():
    """
    Test function for the ultimate_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ultimate_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ultimate_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
