# -*- coding: utf-8 -*-
# relative_strength_index.py

import pandas as pd
import numpy as np


def relative_strength_index(
    df: pd.DataFrame, column: str = "close", period: int = 14, scalar: float = 100
) -> pd.DataFrame:
    """Relative Strength Index (RSI)"""

    df_copy = df.copy()

    # Calculate price changes
    delta = df_copy[column].diff()

    # Separate gains and losses
    positive = delta.copy()
    negative = delta.copy()

    positive[positive < 0] = 0  # Make negatives 0 for the positive series
    negative[negative > 0] = 0  # Make positives 0 for the negative series

    # Calculate Wilder's RMA (Rolling Moving Average)
    # Using EWM with alpha=1/period which is equivalent to Wilder's RMA
    alpha = 1.0 / period
    positive_avg = positive.ewm(alpha=alpha, min_periods=period).mean()
    negative_avg = negative.abs().ewm(alpha=alpha, min_periods=period).mean()

    # Calculate RSI using pandas-ta's approach
    rsi = scalar * positive_avg / (positive_avg + negative_avg)

    df_copy["rsi"] = rsi

    return df_copy[["rsi"]]


relative_strength_index.__doc__ = """
Name:
    Relative Strength Index (RSI)

Description:
    RSI measures the magnitude of recent price changes to evaluate overbought or oversold
    conditions in the price of a stock or other asset. This implementation follows 
    the pandas-ta library approach, which uses EWM (Exponential Weighted Moving Average)
    with alpha=1/period to implement Wilder's RMA (Rolling Moving Average).

More info:
    https://www.investopedia.com/terms/r/rsi.asp
    https://github.com/twopirllc/pandas-ta/blob/main/pandas_ta/momentum/rsi.py

Call with:
    df['rsi'] = bta.relative_strength_index(df, column='close', period=14)['rsi']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which RSI is to be calculated. Default is "close".
    - period (int): The period over which RSI is to be calculated. Default is 14.
    - scalar (float): How much to magnify the result. Default is 100.

Returns:
    pd.DataFrame: DataFrame with 'rsi' column.
"""


def test():
    """
    Test function for the relative_strength_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the relative_strength_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(relative_strength_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
