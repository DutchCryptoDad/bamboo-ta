# -*- coding: utf-8 -*-
# geometric_mean.py

import pandas as pd
import numpy as np


def geometric_mean(
    df: pd.DataFrame,
    length: int = 30,
    min_periods: int = None,
    column: str = "close"
) -> pd.DataFrame:
    """Geometric Mean Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    if length <= 0:
        raise ValueError("Length must be greater than 0")
    
    # Set min_periods to length if not specified
    if min_periods is None:
        min_periods = length
    
    # Calculate geometric mean using rolling windows
    def calc_gmean(series):
        if len(series) < min_periods:
            return np.nan
            
        # Check for zeros or negative values
        has_zeros = 0 in series.values
        
        # Add 1 to handle zeros (will subtract later)
        if has_zeros:
            adjusted_series = series.fillna(0) + 1
        else:
            adjusted_series = series
            
        # Ensure all values are positive
        if np.all(adjusted_series > 0):
            # Calculate geometric mean
            mean = adjusted_series.prod() ** (1 / len(series))
            
            # Subtract 1 if we added it before
            return mean if not has_zeros else mean - 1
        
        return np.nan
    
    # Apply the calculation to rolling windows
    df_copy[f"gmean_{length}"] = df_copy[column].rolling(window=length, min_periods=min_periods).apply(
        calc_gmean, raw=False
    )
    
    return df_copy[[f"gmean_{length}"]]


geometric_mean.__doc__ = """
Name:
    Geometric Mean

Description:
    Calculates the rolling geometric mean of a price series over a specified window length.
    The geometric mean is defined as the nth root of the product of n numbers.
    It is less affected by extreme values than the arithmetic mean, making it useful
    for analyzing percentage changes or ratios like returns.

More info:
    https://en.wikipedia.org/wiki/Geometric_mean

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate geometric mean on. Default is 'close'.

Call with:
    df['gmean_30'] = bta.geometric_mean(df)['gmean_30']

Returns:
    pd.DataFrame: DataFrame with geometric mean values in a column named 'gmean_{length}'.
"""


def test():
    """
    Test function for the geometric_mean indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the geometric_mean indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(geometric_mean)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 