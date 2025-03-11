# -*- coding: utf-8 -*-
# bollinger_bands.py
import numpy as np
import pandas as pd


def bollinger_bands(
    df: pd.DataFrame,
    column: str = "close",
    period: int = 20,
    std_dev: float = 2.0,
    ddof: int = 0,
) -> pd.DataFrame:
    """Bollinger Bands"""
    df_copy = df.copy()

    # Calculate middle band (SMA)
    sma = df_copy[column].rolling(window=period).mean()

    # Calculate standard deviation of the specified column
    rolling_std = df_copy[column].rolling(window=period).std(ddof=ddof)

    # Calculate upper and lower bands
    df_copy["bb_upper"] = sma + (rolling_std * std_dev)
    df_copy["bb_middle"] = sma
    df_copy["bb_lower"] = sma - (rolling_std * std_dev)

    return df_copy[["bb_upper", "bb_middle", "bb_lower"]]


bollinger_bands.__doc__ = """
Name:
    Bollinger Bands (BBANDS)

Description:
    Bollinger Bands are a type of statistical chart characterizing the prices and 
    volatility over time of a financial instrument or commodity. Bollinger Bands 
    consist of three lines: a middle band (SMA), an upper band, and a lower band.
    The upper and lower bands are calculated by adding and subtracting a standard
    deviation multiple from the middle band.

More info:
    https://www.investopedia.com/terms/b/bollingerbands.asp

Parameters:
    - df (pandas.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the BBANDS is to be applied. Default is 'close'.
    - period (int): Look-back period to compute the moving average. Default is 20.
    - std_dev (float): Number of standard deviations to compute the upper and lower bands. Default is 2.0.
    - ddof (int): Degrees of Freedom to use in standard deviation calculation. Default is 0.

Call with:
    bb_result = bta.bollinger_bands(df, 'close', 20, 2, 0)
    df['bb_upper'] = bb_result['bb_upper']
    df['bb_middle'] = bb_result['bb_middle']
    df['bb_lower'] = bb_result['bb_lower']

Returns:
    pd.DataFrame: DataFrame with 'bb_upper', 'bb_middle', 'bb_lower' columns.
"""


def test():
    """
    Test function for the bollinger_bands indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the bollinger_bands indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(bollinger_bands)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
