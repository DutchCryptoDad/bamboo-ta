# -*- coding: utf-8 -*-
# st_dev.py
import pandas as pd


def st_dev(series: pd.Series, period: int) -> pd.Series:
    """
    Calculate the rolling standard deviation over a specified period.

    Parameters:
    - series (pd.Series): The data series to calculate the standard deviation for.
    - period (int): The period over which to calculate the standard deviation.

    Call with:
        df['std_dev'] = bta.st_dev(df['column_name'], period=14)

    Like:
        df['std_dev'] = bta.st_dev(df['close'], period=14)

    Returns:
    - pd.Series: The rolling standard deviation of the series over the specified period.
    """
    if not isinstance(series, pd.Series):
        raise ValueError("Input must be a pandas Series.")
    if period <= 0:
        raise ValueError("Period must be a positive integer.")

    return series.rolling(window=period).std()


st_dev.__doc__ = """
Name:
    Standard Deviation

Description:
    Standard Deviation is a statistical measure of volatility or dispersion from a central value (mean).
    In finance, it's used to measure market volatility and asset price dispersion.
    Higher values indicate greater volatility and potentially higher risk.

More info:
    https://www.investopedia.com/terms/s/standarddeviation.asp

Parameters:
    - series (pd.Series): The data series to calculate the standard deviation for.
    - period (int): The period over which to calculate the standard deviation.

Call with:
    df['std_dev'] = bta.st_dev(df['close'], period=14)

Returns:
    pd.Series: The rolling standard deviation of the series over the specified period.
"""


def test():
    """
    Test function for the st_dev indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the st_dev indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(st_dev)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
