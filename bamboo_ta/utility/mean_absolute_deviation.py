# -*- coding: utf-8 -*-
# mean_absolute_deviation.py

import pandas as pd
import numpy as np


def mean_absolute_deviation(
    df: pd.DataFrame,
    length: int = 30,
    min_periods: int = None,
    column: str = "close"
) -> pd.DataFrame:
    """Mean Absolute Deviation Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 30
    min_periods = int(min_periods) if min_periods and min_periods > 0 else length
    
    # Get the price series
    price = df_copy[column]
    
    # Define the MAD calculation function
    def mad_func(series):
        """Calculate Mean Absolute Deviation: mean(|x - mean(x)|)"""
        return np.abs(series - series.mean()).mean()
    
    # Calculate the rolling mean absolute deviation
    mad = price.rolling(window=length, min_periods=min_periods).apply(
        mad_func, raw=True
    )
    
    # Store result in DataFrame
    df_copy["mad"] = mad
    
    return df_copy[["mad"]]


mean_absolute_deviation.__doc__ = \
"""
Name:
    Mean Absolute Deviation

Description:
    Mean Absolute Deviation (MAD) is a measure of variability that quantifies the average
    distance between each data point and the mean. Unlike standard deviation, which squares
    the differences, MAD uses the absolute differences, making it less sensitive to outliers.
    
    In financial markets, MAD can be used to:
    - Measure price volatility in a less outlier-sensitive way than standard deviation
    - Identify periods of market stability or instability
    - Develop trading systems that adapt to changing market conditions
    - Set more robust stop-loss levels that are less affected by extreme price movements
    
    The calculation is the mean of the absolute deviations from the mean: mean(|x - mean(x)|)

More info:
    https://en.wikipedia.org/wiki/Average_absolute_deviation
    https://www.investopedia.com/terms/a/absolute-deviation.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the MAD calculation. Default is 30.
    - min_periods (int): Minimum number of observations required to calculate MAD.
      Default is the same as length.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.mean_absolute_deviation(df, length=30)
    df['mad'] = result['mad']

Returns:
    pd.DataFrame: DataFrame with 'mad' column containing the indicator values.
"""


def test():
    """
    Test function for the mean_absolute_deviation indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the mean_absolute_deviation indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(mean_absolute_deviation)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 