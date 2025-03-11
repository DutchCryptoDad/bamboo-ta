# -*- coding: utf-8 -*-
# true_strength_index.py

import pandas as pd


def true_strength_index(
    df: pd.DataFrame,
    close_col: str = "close",
    window_slow: int = 25,
    window_fast: int = 13,
    fillna: bool = False,
) -> pd.DataFrame:
    """True Strength Index (TSI)"""
    df_copy = df.copy()

    diff_close = df_copy[close_col] - df_copy[close_col].shift(1)
    min_periods_r = 0 if fillna else window_slow
    min_periods_s = 0 if fillna else window_fast

    smoothed = (
        diff_close.ewm(span=window_slow, min_periods=min_periods_r, adjust=False)
        .mean()
        .ewm(span=window_fast, min_periods=min_periods_s, adjust=False)
        .mean()
    )
    smoothed_abs = (
        abs(diff_close)
        .ewm(span=window_slow, min_periods=min_periods_r, adjust=False)
        .mean()
        .ewm(span=window_fast, min_periods=min_periods_s, adjust=False)
        .mean()
    )

    tsi = smoothed / smoothed_abs * 100
    if fillna:
        tsi = tsi.fillna(0)

    df_copy["tsi"] = tsi

    return df_copy[["tsi"]]


true_strength_index.__doc__ = """
Name:
    True Strength Index (TSI)

Description:
    The True Strength Index (TSI) shows both trend direction and overbought/oversold conditions.

Call with:
    df['tsi'] = bta.true_strength_index(df, 'close', 25, 13)['tsi']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the close column.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window_slow (int): High period. Default is 25.
    - window_fast (int): Low period. Default is 13.
    - fillna (bool): If True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with 'tsi' column.
"""


def test():
    """
    Test function for the true_strength_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the true_strength_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(true_strength_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
