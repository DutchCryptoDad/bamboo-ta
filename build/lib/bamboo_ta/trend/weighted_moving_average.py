# -*- coding: utf-8 -*-
# weighted_moving_average.py
import pandas as pd


def weighted_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 10
) -> pd.DataFrame:
    """Weighted Moving Average (WMA)"""
    df_copy = df.copy()
    weights = pd.Series(range(1, period + 1))
    df_copy["wma"] = (
        df_copy[column]
        .rolling(period)
        .apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    )

    return df_copy[["wma"]]


weighted_moving_average.__doc__ = """
Name:
    Weighted Moving Average (WMA)

Description:
    The Weighted Moving Average (WMA) gives more weight to recent data points and
    less weight to older data points.

More info:
    https://www.investopedia.com/articles/technical/060401.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - column (str): The column to calculate the WMA on.
    - period (int): The period for the WMA calculation.

Call with:
    df['wma'] = bta.weighted_moving_average(df, 'close', 10)['wma']

Returns:
    pd.DataFrame: DataFrame with 'wma' column.
"""


def test():
    """
    Test function for the weighted_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the weighted_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(weighted_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
