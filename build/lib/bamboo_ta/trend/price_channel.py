# -*- coding: utf-8 -*-
# price_channel.py
import pandas as pd


def price_channel(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """Price Channel (PPC)"""
    df_copy = df.copy()

    # Calculate highest high and lowest low over period
    df_copy["highest_high"] = (
        df_copy["high"].rolling(window=period, min_periods=1).max()
    )
    df_copy["lowest_low"] = df_copy["low"].rolling(window=period, min_periods=1).min()

    # Calculate upper, middle, and lower bands
    df_copy["ppc_upper"] = df_copy["highest_high"]
    df_copy["ppc_lower"] = df_copy["lowest_low"]
    df_copy["ppc_mid"] = (df_copy["ppc_upper"] + df_copy["ppc_lower"]) / 2

    # Calculate percentage position within the channel
    df_copy["percent_p"] = (
        (df_copy["close"] - df_copy["ppc_lower"])
        / (df_copy["ppc_upper"] - df_copy["ppc_lower"])
        * 100
    )

    return df_copy[["ppc_upper", "ppc_mid", "ppc_lower", "percent_p"]]


price_channel.__doc__ = """
Name:
    Price Channel (PPC)

Description:
    The Price Channel % PC indicator calculates the percent change of the price channel.
    It calculates the highest high and lowest low of the trailing number of bars specified
    by the input period. The price channel calculates the highest high and lowest low of
    the trailing number of bars specified by the input period.

    When a market moves above the upper band, it is a sign of market strength. Conversely,
    when a market moves below the lower band, it is a sign of market weakness. A sustained
    move above or below the channel lines may indicate a significant breakout.

    The `percent_p` column represents the percentage position of the current closing price
    within the price channel defined by the highest high and lowest low over a specified
    period. It shows where the current closing price stands relative to the recent highest
    and lowest prices.

More info:
    https://www.investopedia.com/terms/p/price-channel.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - period (int): Period for the highest high and lowest low calculation. Default is 20.

Call with:
    ppc_result = bta.price_channel(df, period=20)
    df['ppc_upper'] = ppc_result['ppc_upper']
    df['ppc_mid'] = ppc_result['ppc_mid']
    df['ppc_lower'] = ppc_result['ppc_lower']
    df['percent_p'] = ppc_result['percent_p']

Returns:
    pd.DataFrame: DataFrame with 'ppc_upper', 'ppc_mid', 'ppc_lower', and 'percent_p' columns.
"""


def test():
    """
    Test function for the price_channel indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the price_channel indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(price_channel)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
