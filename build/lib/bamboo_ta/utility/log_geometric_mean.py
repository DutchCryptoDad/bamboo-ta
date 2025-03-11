# -*- coding: utf-8 -*-
# log_geometric_mean.py

import pandas as pd
import numpy as np


def log_geometric_mean(
    df: pd.DataFrame,
    length: int = 30,
    min_periods: int = None,
    column: str = "close"
) -> pd.DataFrame:
    """Log Geometric Mean Indicator"""
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
    
    # Calculate log geometric mean using rolling windows
    def calc_log_gmean(series):
        if len(series) < min_periods:
            return np.nan
            
        n = len(series)
        if n < 2:
            return 0
        
        # Add 1 to handle zeros (will subtract later)
        adjusted_series = series.fillna(0) + 1
            
        # Ensure all values are positive
        if np.all(adjusted_series > 0):
            # Calculate log geometric mean
            return np.exp(np.log(adjusted_series).sum() / n) - 1
        
        return np.nan
    
    # Apply the calculation to rolling windows
    df_copy[f"log_gmean_{length}"] = df_copy[column].rolling(window=length, min_periods=min_periods).apply(
        calc_log_gmean, raw=False
    )
    
    return df_copy[[f"log_gmean_{length}"]]


log_geometric_mean.__doc__ = """
Name:
    Logarithmic Geometric Mean

Description:
    Calculates the rolling logarithmic geometric mean of a price series over a specified window length.
    The log geometric mean is defined as exp(mean(log(x))) - 1 and is particularly useful for analyzing
    returns over multiple periods. It provides a more accurate measure of average growth rate than
    the arithmetic mean, especially when dealing with percentage changes.

More info:
    https://en.wikipedia.org/wiki/Geometric_mean#Relationship_with_logarithms

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate log geometric mean on. Default is 'close'.

Call with:
    df['log_gmean_30'] = bta.log_geometric_mean(df)['log_gmean_30']

Returns:
    pd.DataFrame: DataFrame with log geometric mean values in a column named 'log_gmean_{length}'.
"""


def test():
    """
    Test function for the log_geometric_mean indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the log_geometric_mean indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(log_geometric_mean)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 