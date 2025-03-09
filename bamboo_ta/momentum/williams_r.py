# -*- coding: utf-8 -*-
# williams_r.py

import pandas as pd
import numpy as np


def williams_r(
    df: pd.DataFrame,
    high_col: str = "high",
    low_col: str = "low",
    close_col: str = "close",
    lbp: int = 14,
    fillna: bool = False,
) -> pd.DataFrame:
    """Williams %R"""
    df_copy = df.copy()

    min_periods = 0 if fillna else lbp
    highest_high = df_copy[high_col].rolling(lbp, min_periods=min_periods).max()
    lowest_low = df_copy[low_col].rolling(lbp, min_periods=min_periods).min()

    wr = -100 * (highest_high - df_copy[close_col]) / (highest_high - lowest_low)

    if fillna:
        wr = wr.fillna(-50)

    df_copy["williams_r"] = wr

    return df_copy[["williams_r"]]


williams_r.__doc__ = """
Name:
    Williams %R

Description:
    The Williams %R is a momentum indicator that measures overbought and oversold levels.

More info:
    https://www.tradingview.com/support/solutions/43000501985/
    https://www.tradingview.com/script/REGZq58T-Williams-R/

Call with:
    df['williams_r'] = bta.williams_r(df, 'high', 'low', 'close', 14)['williams_r']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the high, low, and close columns.
    - high_col (str): Name of the column containing high price data. Default is 'high'.
    - low_col (str): Name of the column containing low price data. Default is 'low'.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - lbp (int): Lookback period. Default is 14.
    - fillna (bool): If True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with 'williams_r' column.
"""


def test():
    """
    Test function for the williams_r indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the williams_r indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(williams_r)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
