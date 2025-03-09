# -*- coding: utf-8 -*-
# rolling_moving_average.py
import pandas as pd


def rolling_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 14
) -> pd.DataFrame:
    """Rolling Moving Average (RMA) calculation."""
    df_copy = df.copy()
    df_copy["rma"] = df_copy[column].ewm(alpha=1 / period, adjust=False).mean()

    return df_copy[["rma"]]


rolling_moving_average.__doc__ = """
Name:
    Rolling Moving Average (RMA)

Description:
    The RMA function calculates the Rolling Moving Average (RMA) of a specified column
    in a DataFrame over a given period. It uses an exponential moving average (EMA)
    calculation with a specified smoothing factor (alpha) and returns a DataFrame
    containing the RMA values. This function allows for flexible moving average
    calculations based on any column in the input DataFrame.

More info:
    The RMA is similar to an EMA but with a different smoothing factor calculation.
    It's used in indicators like RSI.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which RMA is to be calculated.
    - period (int): The period over which RMA is to be calculated.

Call with:
    df['rma'] = bta.rolling_moving_average(df, 'close', 14)['rma']

Returns:
    pd.DataFrame: DataFrame with 'rma' column.
"""


def test():
    """
    Test function for the rolling_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the rolling_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(rolling_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
