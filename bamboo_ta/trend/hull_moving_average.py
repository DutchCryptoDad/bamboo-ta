# -*- coding: utf-8 -*-
# hull_moving_average.py
import math
import numpy as np
import pandas as pd


def hull_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 9
) -> pd.DataFrame:
    """Hull Moving Average (HMA)"""
    df_copy = df.copy()

    half_length = math.floor(period / 2)
    sqrt_length = math.floor(math.sqrt(period))

    # Calculate WMA with half period
    wma_half_values = []
    for i in range(len(df_copy)):
        if i < half_length - 1:
            wma_half_values.append(np.nan)
            continue

        # Get data for the window
        window = df_copy[column].iloc[max(0, i - half_length + 1) : i + 1].values

        # Calculate weights
        weights = np.arange(1, len(window) + 1)

        # Calculate WMA
        wma_half_values.append(np.sum(window * weights) / np.sum(weights))

    wma_half = pd.Series(wma_half_values, index=df_copy.index)

    # Calculate WMA with full period
    wma_full_values = []
    for i in range(len(df_copy)):
        if i < period - 1:
            wma_full_values.append(np.nan)
            continue

        # Get data for the window
        window = df_copy[column].iloc[max(0, i - period + 1) : i + 1].values

        # Calculate weights
        weights = np.arange(1, len(window) + 1)

        # Calculate WMA
        wma_full_values.append(np.sum(window * weights) / np.sum(weights))

    wma_full = pd.Series(wma_full_values, index=df_copy.index)

    # Calculate 2 * WMA(half_period) - WMA(full_period)
    h = 2 * wma_half - wma_full

    # Calculate WMA of the result with sqrt(period)
    hma_values = []
    for i in range(len(df_copy)):
        if (
            i < period - 1 + sqrt_length - 1
        ):  # Need sqrt_length more points after having period points
            hma_values.append(np.nan)
            continue

        # Get data for the window
        window = h.iloc[max(0, i - sqrt_length + 1) : i + 1].values

        # Calculate weights
        weights = np.arange(1, len(window) + 1)

        # Calculate WMA
        hma_values.append(np.sum(window * weights) / np.sum(weights))

    df_copy["hma"] = pd.Series(hma_values, index=df_copy.index)

    return df_copy[["hma"]]


hull_moving_average.__doc__ = """
Name:
    Hull Moving Average (HMA)

Description:
    The Hull Moving Average (HMA) is an improved moving average that is responsive and
    has minimal lag. It involves the combination of WMA (Weighted Moving Average) with
    different periods.

More info:
    https://alanhull.com/hull-moving-average

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which HMA is to be calculated. Default is 'close'.
    - period (int): The period over which HMA is to be calculated. Default is 9.

Call with:
    df['hma'] = bta.hull_moving_average(df, 'close', 9)['hma']

Returns:
    pd.DataFrame: DataFrame with 'hma' column.
"""


def test():
    """
    Test function for the hull_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the hull_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(hull_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
