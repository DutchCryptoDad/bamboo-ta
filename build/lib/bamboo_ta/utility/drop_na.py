# -*- coding: utf-8 -*-
# drop_na.py
import math
import numpy as np
import pandas as pd


def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows with 'NaN' values and handle very large numbers and zeros in numeric columns.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.

    Call with:
        df['df_cleaned'] = bta.drop_na(df)

    Returns:
    - pd.DataFrame: DataFrame without NaN values, extremely large values, and zeroes in numeric columns.
    """
    df_copy = df.copy()

    # Select numeric columns
    number_cols = df_copy.select_dtypes(include=np.number).columns.tolist()

    # Replace extremely large values (greater than exp(709)) with NaN
    df_copy[number_cols] = df_copy[number_cols].where(
        df_copy[number_cols] < math.exp(709)
    )

    # Replace zero values with NaN
    df_copy[number_cols] = df_copy[number_cols].replace(0.0, np.nan)

    # Drop rows with any NaN values
    df_cleaned = df_copy.dropna()

    return df_cleaned


drop_na.__doc__ = """
Name:
    Drop NA

Description:
    This utility function cleans a DataFrame by removing rows with NaN values and
    handling problematic values in numeric columns. It addresses three common issues
    in financial data:
    
    1. NaN (Not a Number) values which can cause calculation errors
    2. Extremely large values that might cause overflow issues in calculations
    3. Zero values which can cause division by zero errors in certain calculations
    
    The function is particularly useful as a pre-processing step before applying
    technical indicators or conducting analysis.

More info:
    Data cleaning is a critical step in any data analysis workflow. In financial
    time series data, missing values, zeros, and extremely large values can lead
    to errors or misleading results in technical indicators.
    
    This function uses a threshold of e^709 (approximately 8.22e+307) to identify
    extremely large values, which is close to the largest finite floating-point
    number in Python.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing financial data to be cleaned.

Call with:
    # Clean a dataframe before analysis
    clean_df = bta.drop_na(df)
    
    # Alternative: preserve original and use cleaned for calculations
    calc_df = bta.drop_na(df.copy())
    results = my_calculation_function(calc_df)

Returns:
    pd.DataFrame: A cleaned DataFrame with:
    - All rows containing NaN values removed
    - Extremely large values (>e^709) replaced with NaN and then removed
    - Zero values replaced with NaN and then removed
"""


def test():
    """
    Test function for the drop_na indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the drop_na indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(drop_na)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
