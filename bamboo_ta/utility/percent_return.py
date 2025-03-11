# -*- coding: utf-8 -*-
# percent_return.py

import pandas as pd
import numpy as np


def percent_return(
    df: pd.DataFrame,
    length: int = 1,
    cumulative: bool = False,
    column: str = "close"
) -> pd.DataFrame:
    """Percent Return Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 1
    cumulative = bool(cumulative)
    
    # Get the price series
    price = df_copy[column]
    
    # Calculate the percent return
    if cumulative:
        # Cumulative percent return relative to the first value
        pct_ret = (price / price.iloc[0]) - 1
    else:
        # Period-over-period percent return
        pct_ret = price.pct_change(periods=length)  # Equivalent to (price / price.shift(length)) - 1
    
    # Name based on parameters
    name = "cum_percent_return" if cumulative else "percent_return"
    
    # Store result in DataFrame
    df_copy[name] = pct_ret
    
    return df_copy[[name]]


percent_return.__doc__ = \
"""
Name:
    Percent Return

Description:
    Calculates the percentage return of a price series, which measures the change in value
    of an asset or investment as a percentage of the initial investment.
    
    Two modes are available:
    1. Period-over-period percent return (default): (price_t / price_{t-length}) - 1
    2. Cumulative percent return: (price_t / price_0) - 1, measuring total return since the beginning
    
    Percentage returns are commonly used in finance for:
    - Performance measurement and comparison
    - Risk assessment
    - Investment decision making
    - Portfolio analysis

More info:
    https://www.investopedia.com/terms/r/return.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The period for calculating returns. Default is 1.
    - cumulative (bool): If True, returns the cumulative percentage returns since the beginning.
      If False, returns period-over-period percentage returns. Default is False.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Period-over-period percent returns
    result = bta.percent_return(df, length=1)
    df['percent_return'] = result['percent_return']
    
    # Cumulative percent returns
    result = bta.percent_return(df, cumulative=True)
    df['cum_percent_return'] = result['cum_percent_return']

Returns:
    pd.DataFrame: DataFrame with 'percent_return' or 'cum_percent_return' column (depending on parameters).
"""


def test():
    """
    Test function for the percent_return indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the percent_return indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(percent_return)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 