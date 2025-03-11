# -*- coding: utf-8 -*-
# top_percent_change.py
import pandas as pd


def top_percent_change(df: pd.DataFrame, length: int = 0) -> pd.Series:
    """
    Calculate the percentage change of the current close price from the range maximum open price.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data with required columns:
        - 'open': Opening price.
        - 'close': Closing price.
    - length (int, default=0): Lookback period for calculating the range maximum. If 0, calculates the percentage
      change between the current open and close prices.

    Call with:
        df['percent_change'] = bta.top_percent_change(df, length=3)

    Returns:
    - pd.Series: A Series representing the percentage change for each row in the DataFrame.
    """
    # Ensure the required columns are in the DataFrame
    if not {"open", "close"}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'open' and 'close' columns.")

    if length == 0:
        # Calculate percentage change for the current open and close prices
        percent_change = (df["open"] - df["close"]) / df["close"]
    else:
        # Calculate percentage change from the range maximum open price
        max_open = df["open"].rolling(window=length).max()
        percent_change = (max_open - df["close"]) / df["close"]

    return percent_change


top_percent_change.__doc__ = """
Name:
    Top Percent Change

Description:
    This indicator calculates the percentage change between a price and a reference price.
    When length=0, it measures the percent difference between the open and close of the current bar.
    When length>0, it measures the percent difference between the maximum open price over the
    lookback period and the current close price.
    
    The indicator is useful for identifying potential reversal points after significant price movements
    and can be used in momentum and mean-reversion strategies.

More info:
    https://www.investopedia.com/terms/p/percentage-change.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data with required columns:
        'open' and 'close'.
    - length (int, default=0): Lookback period for calculating the range maximum. If 0,
      calculates the percentage change between the current open and close prices.

Call with:
    df['percent_change'] = bta.top_percent_change(df, length=3)

Returns:
    pd.Series: A Series representing the percentage change for each row in the DataFrame.
"""


def test():
    """
    Test function for the top_percent_change indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the top_percent_change indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(top_percent_change)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
