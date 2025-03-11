# -*- coding: utf-8 -*-
# holt_winters_moving_average.py

import pandas as pd
import numpy as np


def holt_winters_moving_average(df: pd.DataFrame, alpha: float = 0.2, beta: float = 0.1, 
                              gamma: float = 0.1, column: str = "close") -> pd.DataFrame:
    """Holt-Winters Moving Average (HWMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Validate parameters
    alpha = float(alpha) if 0 < alpha < 1 else 0.2
    beta = float(beta) if 0 < beta < 1 else 0.1
    gamma = float(gamma) if 0 < gamma < 1 else 0.1
    
    # Initialize variables
    last_a = last_v = 0
    last_f = series.iloc[0]
    
    # Initialize result series
    hwma = pd.Series(np.nan, index=series.index)
    
    # Calculate HWMA
    for i in range(len(series)):
        # Calculate forecast component
        f = (1.0 - alpha) * (last_f + last_v + 0.5 * last_a) + alpha * series.iloc[i]
        
        # Calculate trend component
        v = (1.0 - beta) * (last_v + last_a) + beta * (f - last_f)
        
        # Calculate seasonality component
        a = (1.0 - gamma) * last_a + gamma * (v - last_v)
        
        # Calculate HWMA
        hwma.iloc[i] = (f + v + 0.5 * a)
        
        # Update values for next iteration
        last_a, last_f, last_v = a, f, v
    
    # Add result to DataFrame
    df_copy["hwma"] = hwma
    
    return df_copy[["hwma"]]


holt_winters_moving_average.__doc__ = \
"""
Name:
    Holt-Winters Moving Average (HWMA)

Description:
    The Holt-Winters Moving Average is a triple exponential smoothing method that accounts
    for trend and seasonality in time series data. It uses three parameters (alpha, beta, gamma)
    to control the smoothing of the level, trend, and seasonality components.
    
    This implementation is based on the Holt-Winters method but simplified for use as a
    moving average indicator in technical analysis. It's particularly useful for data that
    exhibits both trend and cyclical patterns.

More info:
    https://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - alpha (float): Smoothing parameter for the level component (0 < alpha < 1). Default is 0.2.
    - beta (float): Smoothing parameter for the trend component (0 < beta < 1). Default is 0.1.
    - gamma (float): Smoothing parameter for the seasonality component (0 < gamma < 1). Default is 0.1.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.holt_winters_moving_average(df)
    df['hwma'] = result['hwma']

Returns:
    pd.DataFrame: DataFrame with 'hwma' column.
"""


def test():
    """
    Test function for the holt_winters_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the holt_winters_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(holt_winters_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 