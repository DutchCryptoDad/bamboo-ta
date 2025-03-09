# -*- coding: utf-8 -*-
# zero_exponential_moving_average.py
import pandas as pd


def zero_exponential_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """Zero Exponential Moving Average (ZEMA)"""
    df_copy = df.copy()

    # Calculate EMA components
    ema1 = df_copy[column].ewm(span=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, adjust=False).mean()

    # ZEMA calculation
    df_copy["zema"] = 2 * ema1 - ema2

    return df_copy[["zema"]]


zero_exponential_moving_average.__doc__ = """
Name:
    Zero Exponential Moving Average (ZEMA)

Description:
    The Zero Exponential Moving Average (ZEMA) is an improved version of the Exponential
    Moving Average (EMA) that reduces lag by incorporating a zero-lag component.

More info:
    The ZEMA applies the formula: 2 * EMA(period) - EMA(EMA(period)) to reduce lag.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZEMA is to be calculated. Default is 21.

Call with:
    df['zema'] = bta.zero_exponential_moving_average(df, 'close', 21)['zema']

Returns:
    pd.DataFrame: DataFrame with 'zema' column.
"""


def test():
    """
    Test function for the zero_exponential_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the zero_exponential_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(zero_exponential_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
