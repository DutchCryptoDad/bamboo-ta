# -*- coding: utf-8 -*-
# quantile.py

import pandas as pd
import numpy as np


def quantile(
    df: pd.DataFrame,
    length: int = 30,
    q: float = 0.5,
    min_periods: int = None,
    column: str = "close"
) -> pd.DataFrame:
    """Quantile Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 30
    q = float(q) if 0 < q < 1 else 0.5
    min_periods = int(min_periods) if min_periods and min_periods > 0 else length
    
    # Get the price series
    price = df_copy[column]
    
    # Calculate the rolling quantile
    quantile_values = price.rolling(window=length, min_periods=min_periods).quantile(q)
    
    # Generate a name for the result column that includes the quantile value
    quantile_formatted = str(q).replace('.', '_')
    result_column = f"quantile_{quantile_formatted}"
    
    # Store result in DataFrame
    df_copy[result_column] = quantile_values
    
    return df_copy[[result_column]]


quantile.__doc__ = \
"""
Name:
    Quantile

Description:
    The Quantile indicator calculates the specified quantile of a price series over a rolling
    window. Quantiles divide a dataset into equal parts, with the quantile value representing
    the threshold that divides the data in the specified proportion.
    
    Common quantiles include:
    - 0.5 (median): The middle value, dividing the dataset into two equal halves
    - 0.25 (first quartile): Divides the bottom 25% from the top 75%
    - 0.75 (third quartile): Divides the bottom 75% from the top 25%
    
    In financial markets, rolling quantiles can be used to:
    - Identify price levels that are historically significant
    - Develop trading systems based on statistical thresholds
    - Create adaptive indicators that adjust to changing market conditions
    - Filter outliers by focusing on specific segments of the price distribution

More info:
    https://en.wikipedia.org/wiki/Quantile
    https://www.investopedia.com/terms/q/quantile.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the quantile calculation. Default is 30.
    - q (float): The quantile to calculate, must be between 0 and 1. Default is 0.5 (median).
    - min_periods (int): Minimum number of observations required to calculate the quantile.
      Default is the same as length.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Calculate the median (50th percentile)
    result = bta.quantile(df, length=30, q=0.5)
    df['quantile_0_5'] = result['quantile_0_5']
    
    # Calculate the first quartile (25th percentile)
    result = bta.quantile(df, length=30, q=0.25)
    df['quantile_0_25'] = result['quantile_0_25']

Returns:
    pd.DataFrame: DataFrame with a quantile column (name depends on the q parameter).
"""


def test():
    """
    Test function for the quantile indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the quantile indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(quantile)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 