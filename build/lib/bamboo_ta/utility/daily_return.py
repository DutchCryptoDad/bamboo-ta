# -*- coding: utf-8 -*-
# daily_return.py
import numpy as np
import pandas as pd


def daily_return(
    df: pd.DataFrame, column: str = "close", fillna: bool = False
) -> pd.Series:
    """
    Calculate the Daily Return (DR) of a specified column in a DataFrame.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

    Call with:
        df['daily_return'] = bta.daily_return(df)

    Returns:
    - pd.Series: Series of daily return values.
    """
    # Copy the DataFrame to avoid modifying the original data
    df_copy = df.copy()

    # Calculate the daily return as a percentage
    df_copy["daily_return"] = (df_copy[column] / df_copy[column].shift(1)) - 1
    df_copy["daily_return"] *= 100

    # Handle NaN values if requested
    if fillna:
        df_copy["daily_return"] = df_copy["daily_return"].fillna(0)

    return df_copy["daily_return"].rename("daily_return")


daily_return.__doc__ = """
Name:
    Daily Return

Description:
    Daily Return (also known as simple return) calculates the percentage change in price
    between consecutive periods. It's a fundamental measure in financial analysis that
    shows how much an investment has gained or lost over a single period, expressed as
    a percentage of the initial investment.

More info:
    The formula for daily return is: ((Pt/Pt-1) - 1) * 100, where Pt is the price at time t.
    
    This is the standard measure of return used in many financial applications. Unlike
    logarithmic returns, simple returns directly represent the actual percentage gain or
    loss experienced by an investor.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    df['daily_ret'] = bta.daily_return(df)
    
    # Using a different price column:
    df['daily_ret'] = bta.daily_return(df, column='adjusted_close')

Returns:
    pd.Series: Series of daily return values expressed as percentages.

Important Notes:
    - This function returns a pandas Series, not a DataFrame.
    
    - When used with bamboo_ta's test_indicator function, it will fail with
      "Error: daily_return did not return a DataFrame" because the test system
      expects a DataFrame return type.
    
    - For testing within the bamboo_ta framework, a wrapper function could be created:
      ```python
      def daily_return_wrapper(df):
          return_series = daily_return(df)
          # Convert the Series to a DataFrame for test_indicator compatibility
          return pd.DataFrame({'daily_return': return_series})
      ```
    
    - In actual usage, the Series return type is more convenient as it can be directly
      assigned to a DataFrame column as shown in the "Call with" examples.
"""


def test():
    """
    Test function for the daily_return indicator.

    This function uses the generic test_indicator function from bamboo_ta.py
    to test the daily_return indicator.

    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator

        # Test the indicator
        test_indicator(daily_return)

    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
