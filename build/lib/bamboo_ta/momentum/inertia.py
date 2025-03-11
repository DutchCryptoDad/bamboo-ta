# -*- coding: utf-8 -*-
# inertia.py

import pandas as pd
import numpy as np


def inertia(df: pd.DataFrame, length: int = 20, rvi_length: int = 14, swma_length: int = 4) -> pd.DataFrame:
    """Inertia Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate RVI first
    # We use the same code as in relative_vigor_index.py but only need the RVI value, not the signal
    
    # Calculate close-open range and high-low range
    close_open_range = df_copy["close"] - df_copy["open"]
    high_low_range = df_copy["high"] - df_copy["low"]
    
    # Handle potential division by zero in high-low range
    high_low_range = high_low_range.replace(0, np.nan)
    
    # Apply SWMA (Symmetrically Weighted Moving Average)
    co_swma = symmetrically_weighted_ma(close_open_range, swma_length)
    hl_swma = symmetrically_weighted_ma(high_low_range, swma_length)
    
    # Calculate the sum over the specified period
    co_sum = co_swma.rolling(window=rvi_length).sum()
    hl_sum = hl_swma.rolling(window=rvi_length).sum()
    
    # Calculate RVI
    rvi = co_sum / hl_sum
    
    # Calculate Inertia using Linear Regression
    inertia_val = linear_regression(rvi, length)
    
    # Add results to the DataFrame
    df_copy["inertia"] = inertia_val
    
    return df_copy[["inertia"]]


def symmetrically_weighted_ma(series, length):
    """
    Calculate Symmetrically Weighted Moving Average
    
    This is a weighted moving average where the weights are symmetric and sum to 1.
    For example, with length=4, the weights are [1/6, 2/6, 2/6, 1/6].
    """
    weights = None
    if length == 4:  # Most common case
        weights = np.array([1/6, 2/6, 2/6, 1/6])
    else:
        # Generate symmetric weights for any length
        half = length // 2
        if length % 2 == 0:  # Even length
            weights = np.concatenate([
                np.arange(1, half + 1),
                np.arange(half, 0, -1)
            ])
        else:  # Odd length
            mid = (length + 1) // 2
            weights = np.concatenate([
                np.arange(1, mid),
                np.array([mid]),
                np.arange(mid - 1, 0, -1)
            ])
        weights = weights / weights.sum()  # Normalize to sum to 1
    
    # Apply the weighted moving average
    result = series.rolling(window=length).apply(
        lambda x: np.sum(x * weights[:len(x)]) if len(x) == length else np.nan,
        raw=True
    )
    
    return result


def linear_regression(series, length):
    """
    Calculate the linear regression line endpoint (forecast) for each window of data.
    This is equivalent to the LSQRMA (Least Squares Moving Average).
    """
    result = pd.Series(index=series.index)
    
    # Apply linear regression to each window
    for i in range(length - 1, len(series)):
        if i - (length - 1) < 0:  # Handle edge case
            result.iloc[i] = np.nan
            continue
            
        y = series.iloc[i-(length-1):i+1].values
        x = np.arange(length)
        
        # Calculate regression coefficients
        try:
            slope, intercept = np.polyfit(x, y, 1)
            
            # Calculate the regression line's endpoint (which is the LSQRMA value)
            regression_val = intercept + slope * (length - 1)
            result.iloc[i] = regression_val
        except:
            result.iloc[i] = np.nan
    
    return result


inertia.__doc__ = \
"""
Name:
    Inertia

Description:
    Inertia was developed by Donald Dorsey and was introduced in his article in 
    September 1995. It combines the Relative Vigor Index (RVI) with a Least Squares 
    Moving Average (LSQRMA) to create a momentum oscillator that attempts to identify 
    the "inertia" of price movement.
    
    The indicator is essentially the Relative Vigor Index smoothed by the Least 
    Squares Moving Average. Traditionally, values above 50 indicate positive inertia
    (bullish), while values below 50 indicate negative inertia (bearish).

More info:
    https://www.investopedia.com/terms/r/relative_vigor_index.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 
      'low', and 'close' columns.
    - length (int): The period for the linear regression calculation. Default is 20.
    - rvi_length (int): The period for the RVI calculation. Default is 14.
    - swma_length (int): The period for the SWMA used in RVI calculation. Default is 4.

Call with:
    df['inertia'] = bta.inertia(df)['inertia']

Returns:
    pd.DataFrame: DataFrame with 'inertia' column.
"""


def test():
    """
    Test function for the inertia indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the inertia indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(inertia)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 