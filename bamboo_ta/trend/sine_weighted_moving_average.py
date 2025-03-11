# -*- coding: utf-8 -*-
# sine_weighted_moving_average.py

import pandas as pd
import numpy as np


def sine_weighted_moving_average(df: pd.DataFrame, length: int = 14, 
                              column: str = "close") -> pd.DataFrame:
    """Sine Weighted Moving Average (SINWMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Validate parameters
    length = int(length) if length > 0 else 14
    
    # Generate sine weights
    sines = np.array([np.sin((i + 1) * np.pi / (length + 1)) for i in range(0, length)])
    weights = sines / np.sum(sines)
    
    # Initialize result series
    sinwma = pd.Series(np.nan, index=series.index)
    
    # Calculate SINWMA
    for i in range(length - 1, len(series)):
        window = series.iloc[i - length + 1 : i + 1].values
        sinwma.iloc[i] = np.sum(weights * window)
    
    # Add result to DataFrame
    df_copy["sinwma"] = sinwma
    
    return df_copy[["sinwma"]]


sine_weighted_moving_average.__doc__ = \
"""
Name:
    Sine Weighted Moving Average (SINWMA)

Description:
    A weighted moving average where the weights are based on a sine function.
    This gives more weight to the middle values in the calculation window,
    creating a more responsive indicator that reduces lag compared to a simple
    moving average while still smoothing price action effectively.
    
    The weights follow a sine wave pattern, with the highest weights in the middle
    of the window and lower weights at the beginning and end. This creates a
    bell-shaped weighting scheme that can help filter out noise while maintaining
    sensitivity to significant price changes.

More info:
    https://www.tradingview.com/script/6MWFvnPO-Sine-Weighted-Moving-Average/
    Created by Everget on TradingView

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the SINWMA calculation. Default is 14.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.sine_weighted_moving_average(df)
    df['sinwma'] = result['sinwma']

Returns:
    pd.DataFrame: DataFrame with 'sinwma' column.
"""


def test():
    """
    Test function for the sine_weighted_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the sine_weighted_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(sine_weighted_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 