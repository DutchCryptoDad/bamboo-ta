# -*- coding: utf-8 -*-
# rate_of_change.py
import numpy as np
import pandas as pd


def rate_of_change(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """Rate of Change (ROC)"""
    df_copy = df.copy()

    df_copy["roc"] = df_copy[column].diff(period) / df_copy[column].shift(period) * 100

    return df_copy[["roc"]]


rate_of_change.__doc__ = """
Name:
    Rate of Change (ROC)

Description:
    The Rate of Change (ROC) is a momentum oscillator that measures the percentage
    change in price between the current price and the price n periods ago.

More info:
    https://www.investopedia.com/terms/r/rateofchange.asp

Call with:
    df['roc'] = bta.rate_of_change(df, column='close', period=21)['roc']

Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the ROC is to be applied. Default is 'close'.
    - period (int): Period for the ROC calculation. Default is 21.

Returns:
    pd.DataFrame: DataFrame with 'roc' column.
"""


def test():
    """
    Test function for the rate_of_change indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the rate_of_change indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(rate_of_change)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
