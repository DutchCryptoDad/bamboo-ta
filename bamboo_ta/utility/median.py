# -*- coding: utf-8 -*-
# median.py

import pandas as pd
import numpy as np


def median(
    df: pd.DataFrame,
    length: int = 30,
    min_periods: int = None,
    column: str = "close"
) -> pd.DataFrame:
    """Median Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 30
    min_periods = int(min_periods) if min_periods and min_periods > 0 else length
    
    # Get the price series
    price = df_copy[column]
    
    # Calculate the rolling median
    median_values = price.rolling(window=length, min_periods=min_periods).median()
    
    # Store result in DataFrame
    df_copy["median"] = median_values
    
    return df_copy[["median"]]


median.__doc__ = \
"""
Name:
    Median

Description:
    The Median indicator calculates the rolling median of a price series over a specified
    period. Unlike a simple moving average which can be skewed by outliers, the median
    represents the middle value in a series and is more robust to extreme values.
    
    In financial markets, the rolling median can be used to:
    - Identify the central tendency of price movements with less sensitivity to outliers
    - Filter out market noise in highly volatile conditions
    - Develop trading systems that are less affected by price spikes or flash crashes
    - Complement traditional moving averages for a more complete view of market conditions
    
    The median is often considered a more robust measure of central tendency compared to the mean
    when the price distribution contains outliers or exhibits skewness.

More info:
    https://www.incrediblecharts.com/indicators/median_price.php
    https://en.wikipedia.org/wiki/Median

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the median calculation. Default is 30.
    - min_periods (int): Minimum number of observations required to calculate median.
      Default is the same as length.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.median(df, length=30)
    df['median'] = result['median']

Returns:
    pd.DataFrame: DataFrame with 'median' column containing the indicator values.
"""


def test():
    """
    Test function for the median indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the median indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(median)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 