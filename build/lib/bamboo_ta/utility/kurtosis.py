# -*- coding: utf-8 -*-
# kurtosis.py

import pandas as pd
import numpy as np


def kurtosis(
    df: pd.DataFrame,
    length: int = 30,
    min_periods: int = None,
    column: str = "close"
) -> pd.DataFrame:
    """Kurtosis Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 30
    min_periods = int(min_periods) if min_periods and min_periods > 0 else length
    
    # Get the price series
    price = df_copy[column]
    
    # Calculate the rolling kurtosis
    kurt = price.rolling(window=length, min_periods=min_periods).kurt()
    
    # Store result in DataFrame
    df_copy["kurtosis"] = kurt
    
    return df_copy[["kurtosis"]]


kurtosis.__doc__ = \
"""
Name:
    Kurtosis

Description:
    Kurtosis is a statistical measure that describes the shape of a distribution's tails
    in relation to its overall shape. It quantifies whether the tails of a distribution
    contain extreme values compared to a normal distribution.
    
    In the context of financial markets:
    - High kurtosis (>3, leptokurtic): Indicates frequent extreme returns, fat tails
    - Normal kurtosis (=3, mesokurtic): Matches a normal distribution
    - Low kurtosis (<3, platykurtic): Indicates fewer extreme returns, thin tails
    
    Traders use kurtosis to:
    - Assess the risk of extreme price movements
    - Evaluate the appropriateness of normal distribution assumptions
    - Develop risk management strategies for handling outlier events

More info:
    https://www.investopedia.com/terms/k/kurtosis.asp
    https://en.wikipedia.org/wiki/Kurtosis

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the kurtosis calculation. Default is 30.
    - min_periods (int): Minimum number of observations required to calculate kurtosis.
      Default is the same as length.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.kurtosis(df, length=30)
    df['kurtosis'] = result['kurtosis']

Returns:
    pd.DataFrame: DataFrame with 'kurtosis' column containing the indicator values.
"""


def test():
    """
    Test function for the kurtosis indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the kurtosis indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(kurtosis)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 