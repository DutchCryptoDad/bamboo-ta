# -*- coding: utf-8 -*-
# zero_lag_exponential_moving_average.py
import pandas as pd


def zero_lag_exponential_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """Zero Lag Exponential Moving Average (ZLEMA)"""
    df_copy = df.copy()

    # Calculate lag
    lag = int((period - 1) / 2)

    # Calculating the adjusted data series
    ema_data = df[column] + (df[column] - df[column].shift(lag))

    # Computing the EMA of the adjusted data series
    zlema = ema_data.ewm(span=period, adjust=False).mean()

    df_copy["zlema"] = zlema

    return df_copy[["zlema"]]


zero_lag_exponential_moving_average.__doc__ = """
Name:
    Zero Lag Exponential Moving Average (ZLEMA)

Description:
    ZLEMA is an Exponential Moving Average (EMA) that adjusts for lag, making it more responsive
    to recent price changes. It uses lagged data differences to adjust the EMA calculation,
    thereby reducing the inherent lag of EMA.

More info:
    Created by John Ehlers, the ZLEMA removes lag by subtracting older data from current data.
    https://en.wikipedia.org/wiki/Zero_lag_exponential_moving_average

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZLEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZLEMA is to be calculated. Default is 21.

Call with:
    df['zlema'] = bta.zero_lag_exponential_moving_average(df, 'close', 21)['zlema']

Returns:
    pd.DataFrame: DataFrame with 'zlema' column.
"""


def test():
    """
    Test function for the zero_lag_exponential_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the zero_lag_exponential_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(zero_lag_exponential_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
