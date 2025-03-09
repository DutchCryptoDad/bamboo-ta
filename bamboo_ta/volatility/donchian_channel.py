# -*- coding: utf-8 -*-
# donchian_channel.py
import numpy as np
import pandas as pd


def donchian_channel(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """Donchian Channel"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate Donchian Channel components
    df_copy["dc_upper"] = df_copy["high"].rolling(window=period).max()
    df_copy["dc_lower"] = df_copy["low"].rolling(window=period).min()
    df_copy["dc_middle"] = (df_copy["dc_upper"] + df_copy["dc_lower"]) / 2

    # Calculate the width of the channel
    if "close" in df.columns:
        df_copy["dc_width"] = (df_copy["dc_upper"] - df_copy["dc_lower"]) / df_copy[
            "close"
        ]
    else:
        df_copy["dc_width"] = (df_copy["dc_upper"] - df_copy["dc_lower"]) / df_copy[
            "dc_middle"
        ]

    return df_copy[["dc_upper", "dc_middle", "dc_lower", "dc_width"]]


donchian_channel.__doc__ = """
Name:
    Donchian Channel

Description:
    The Donchian Channel is a volatility indicator composed of three lines: 
    an upper band, a middle band, and a lower band. The upper band represents 
    the highest price of a security over a specified period, while the lower band 
    represents the lowest price. The middle band is simply the average of the 
    upper and lower bands.
    
    Donchian Channels are used to identify potential breakouts, determine market 
    volatility, and identify trend strength. They are particularly popular in trend-following 
    systems like the Turtle Trading system.

More info:
    https://www.investopedia.com/terms/d/donchianchannels.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high' and 'low'.
    - period (int): The lookback period to calculate the highest high and lowest low. Default is 20.

Call with:
    dc_result = bta.donchian_channel(df, 20)
    df['dc_upper'] = dc_result['dc_upper']
    df['dc_middle'] = dc_result['dc_middle']
    df['dc_lower'] = dc_result['dc_lower']
    df['dc_width'] = dc_result['dc_width']

Returns:
    pd.DataFrame: DataFrame with 'dc_upper', 'dc_middle', 'dc_lower', and 'dc_width' columns.
"""


def test():
    """
    Test function for the donchian_channel indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the donchian_channel indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(donchian_channel)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
