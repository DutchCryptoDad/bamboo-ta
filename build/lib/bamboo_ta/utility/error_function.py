# -*- coding: utf-8 -*-
# error_function.py

import pandas as pd
import numpy as np


def error_function(
    df: pd.DataFrame,
    length: int = 30,
    min_periods: int = None,
    column: str = "close"
) -> pd.DataFrame:
    """Error Function (erf) Indicator"""
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
    
    # Define the erf calculation function
    def calc_erf(x):
        """Error Function erf(x) implementation
        The algorithm comes from Handbook of Mathematical Functions, formula 7.1.26.
        """
        # Save the sign of x
        sign = 1 if x >= 0 else -1
        x = abs(x)

        # Constants from the approximation formula
        a1 =  0.254829592
        a2 = -0.284496736
        a3 =  1.421413741
        a4 = -1.453152027
        a5 =  1.061405429
        p  =  0.3275911

        # A&S formula 7.1.26
        t = 1.0 / (1.0 + p * x)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * np.exp(-x * x)
        return sign * y  # erf(-x) = -erf(x)
    
    # Apply the erf function to the rolling standardized values
    def apply_erf(series):
        if len(series) < min_periods:
            return np.nan
            
        # Standardize the last value in the window
        if np.std(series) > 0:
            standardized = (series.iloc[-1] - np.mean(series)) / np.std(series)
            return calc_erf(standardized)
        
        return np.nan
    
    # Apply the calculation to rolling windows
    df_copy[f"erf_{length}"] = df_copy[column].rolling(window=length, min_periods=min_periods).apply(
        apply_erf, raw=False
    )
    
    return df_copy[[f"erf_{length}"]]


error_function.__doc__ = """
Name:
    Error Function (erf)

Description:
    Applies the error function (erf) to rolling standardized values of a price series.
    
    The error function, also called the Gauss error function, is a special function
    of sigmoid shape that occurs in probability, statistics, and partial differential
    equations. It is defined as:
    
    erf(x) = (2/√π) ∫(0 to x) e^(-t²) dt
    
    In this implementation, we:
    1. Take a rolling window of the specified length
    2. Standardize the latest value in the window
    3. Apply the error function to this standardized value
    
    This provides a measure of how many standard deviations the current price
    is from the mean, transformed through the erf function to range between -1 and 1.

More info:
    https://en.wikipedia.org/wiki/Error_function

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate on. Default is 'close'.

Call with:
    df['erf_30'] = bta.error_function(df)['erf_30']

Returns:
    pd.DataFrame: DataFrame with error function values in a column named 'erf_{length}'.
"""


def test():
    """
    Test function for the error_function indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the error_function indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(error_function)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 