# -*- coding: utf-8 -*-
# log_return.py

import pandas as pd
import numpy as np


def log_return(
    df: pd.DataFrame,
    length: int = 1,
    cumulative: bool = False,
    column: str = "close"
) -> pd.DataFrame:
    """Log Return Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 1
    cumulative = bool(cumulative)
    
    # Get the price series
    price = df_copy[column]
    
    # Calculate the log return
    if cumulative:
        # Cumulative log return relative to the first value
        log_ret = np.log(price / price.iloc[0])
    else:
        # Period-over-period log return
        log_ret = np.log(price / price.shift(length))
    
    # Name based on parameters
    name = "cum_log_return" if cumulative else "log_return"
    
    # Store result in DataFrame
    df_copy[name] = log_ret
    
    return df_copy[[name]]


log_return.__doc__ = \
"""
Name:
    Log Return

Description:
    Calculates the logarithmic return of a price series. Logarithmic returns are useful
    in financial analysis because they are additive over time and better approximate
    normally distributed returns, which is important for statistical analysis.
    
    Two modes are available:
    1. Period-over-period log return (default): log(price_t / price_{t-length})
    2. Cumulative log return: log(price_t / price_0), measuring return since the beginning
    
    Log returns are especially useful for:
    - Comparing performance across different assets
    - Statistical analysis that assumes normality
    - Time series modeling and forecasting

More info:
    https://www.quantstart.com/articles/Returns-Arithmetic-and-Logarithmic/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The period for calculating returns. Default is 1.
    - cumulative (bool): If True, returns the cumulative log returns since the beginning.
      If False, returns period-over-period log returns. Default is False.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Period-over-period log returns
    result = bta.log_return(df, length=1)
    df['log_return'] = result['log_return']
    
    # Cumulative log returns
    result = bta.log_return(df, cumulative=True)
    df['cum_log_return'] = result['cum_log_return']

Returns:
    pd.DataFrame: DataFrame with 'log_return' or 'cum_log_return' column (depending on parameters).
"""


def test():
    """
    Test function for the log_return indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the log_return indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(log_return)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 