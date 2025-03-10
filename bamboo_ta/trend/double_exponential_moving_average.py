# -*- coding: utf-8 -*-
# double_exponential_moving_average.py

import pandas as pd


def double_exponential_moving_average(df: pd.DataFrame, length: int = 10, 
                                    column: str = "close") -> pd.DataFrame:
    """Double Exponential Moving Average (DEMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Calculate first EMA
    ema1 = df_copy[column].ewm(span=length, adjust=False).mean()
    
    # Calculate second EMA (EMA of first EMA)
    ema2 = ema1.ewm(span=length, adjust=False).mean()
    
    # Calculate DEMA
    dema = 2 * ema1 - ema2
    
    # Add result to DataFrame
    df_copy["dema"] = dema
    
    return df_copy[["dema"]]


double_exponential_moving_average.__doc__ = \
"""
Name:
    Double Exponential Moving Average (DEMA)

Description:
    The Double Exponential Moving Average attempts to create a smoother average with less
    lag than the standard Exponential Moving Average (EMA). It was developed by Patrick Mulloy
    and first published in the February 1994 issue of "Technical Analysis of Stocks & Commodities" magazine.
    
    The DEMA uses multiple EMA calculations to reduce the lag of traditional moving averages.
    By giving more weight to recent prices and reducing the lag associated with traditional
    moving averages, the DEMA can be more responsive to price changes.

More info:
    https://www.tradingview.com/support/solutions/43000502589-double-exponential-moving-average-dema/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the DEMA calculation. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.double_exponential_moving_average(df)
    df['dema'] = result['dema']

Returns:
    pd.DataFrame: DataFrame with 'dema' column.
"""


def test():
    """
    Test function for the double_exponential_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the double_exponential_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(double_exponential_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 