# -*- coding: utf-8 -*-
# least_squares_moving_average.py
import numpy as np
import pandas as pd


def least_squares_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """Least Squares Moving Average (LSMA)"""
    df_copy = df.copy()

    lsma_values = []

    for i in range(period - 1, len(df)):
        # Extract the most recent N df points
        subset = df.iloc[i + 1 - period : i + 1]

        # Perform linear regression to fit a line
        x = np.arange(len(subset))
        y = subset[column].values
        slope, intercept = np.polyfit(x, y, 1)

        # Calculate the LSMA value using the linear equation
        lsma = intercept + slope * (period - 1)
        lsma_values.append(lsma)

    lsma_series = pd.Series(lsma_values, index=df.index[period - 1 :])

    df_copy["lsma"] = lsma_series

    return df_copy[["lsma"]]


least_squares_moving_average.__doc__ = """
Name:
    Least Squares Moving Average (LSMA)

Description:
    LSMA uses linear regression to compute the trend of the data over a specified period.
    It fits a straight line to the data points using the method of least squares to depict
    the direction of movement.

More info:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/lsma

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which LSMA is to be calculated. Default is 'close'.
    - period (int): The period over which LSMA is to be calculated. Default is 21.

Call with:
    df['lsma'] = bta.least_squares_moving_average(df, 'close', 50)['lsma']

Returns:
    pd.DataFrame: DataFrame with 'lsma' column.
"""


def test():
    """
    Test function for the least_squares_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the least_squares_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(least_squares_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
