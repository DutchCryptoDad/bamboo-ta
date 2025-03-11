# -*- coding: utf-8 -*-
# skew.py

import pandas as pd
import numpy as np


def skew(
    df: pd.DataFrame,
    length: int = 30,
    min_periods: int = None,
    column: str = "close"
) -> pd.DataFrame:
    """Skew Indicator"""
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
    
    # Calculate skew
    df_copy[f"skew_{length}"] = df_copy[column].rolling(window=length, min_periods=min_periods).skew()
    
    return df_copy[[f"skew_{length}"]]


skew.__doc__ = """
Name:
    Rolling Skew

Description:
    Calculates the rolling skew of a price series over a specified window length.
    Skew measures the asymmetry of the distribution of returns around its mean.
    Positive skew indicates a distribution with a long right tail, while negative 
    skew indicates a distribution with a long left tail.

More info:
    https://en.wikipedia.org/wiki/Skewness

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate skew on. Default is 'close'.

Call with:
    df['skew_30'] = bta.skew(df)['skew_30']

Returns:
    pd.DataFrame: DataFrame with skew values in a column named 'skew_{length}'.
"""


def test():
    """
    Test function for the skew indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the skew indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(skew)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 