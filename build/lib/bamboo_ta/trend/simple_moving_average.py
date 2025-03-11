# -*- coding: utf-8 -*-
# simple_moving_average.py
import pandas as pd


def simple_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """Simple Moving Average (SMA)"""
    df_copy = df.copy()
    df_copy["sma"] = df_copy[column].rolling(window=period).mean()

    return df_copy[["sma"]]


simple_moving_average.__doc__ = """
Name:
    Simple Moving Average (SMA)

Description:
    The Simple Moving Average is the unweighted mean of the previous 'period' data points.

More info:
    https://www.investopedia.com/terms/s/sma.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which SMA is to be calculated. Default is 'close'.
    - period (int): The period over which SMA is to be calculated. Default is 21.

Call with:
    df['sma'] = bta.simple_moving_average(df, 'close', 50)['sma']

Returns:
    pd.DataFrame: DataFrame with 'sma' column.
"""


def test():
    """
    Test function for the simple_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the simple_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(simple_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
