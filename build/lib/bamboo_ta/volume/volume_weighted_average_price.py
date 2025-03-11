# -*- coding: utf-8 -*-
# volume_weighted_average_price.py
import numpy as np
import pandas as pd


def volume_weighted_average_price(
    df: pd.DataFrame, window: int = 14, fillna: bool = False
) -> pd.DataFrame:
    """Volume Weighted Average Price"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate typical price
    typical_price = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3.0
    typical_price_volume = typical_price * df_copy["volume"]

    # Calculate VWAP over the rolling window
    min_periods = 0 if fillna else window
    total_pv = typical_price_volume.rolling(window, min_periods=min_periods).sum()
    total_volume = df_copy["volume"].rolling(window, min_periods=min_periods).sum()

    # VWAP calculation
    vwap = total_pv / total_volume
    if fillna:
        vwap = vwap.fillna(0)

    # Add the VWAP to the DataFrame
    df_copy["vwap"] = vwap

    return df_copy[["vwap"]]


volume_weighted_average_price.__doc__ = """
Name:
    Volume Weighted Average Price (VWAP)

Description:
    The Volume Weighted Average Price (VWAP) equals the dollar value of all trading periods 
    divided by the total trading volume for the current day. VWAP is often used by institutional 
    traders to determine the quality of execution. This implementation provides a rolling VWAP 
    over a specified window period, making it usable across multiple timeframes.

More info:
    https://www.investopedia.com/terms/v/vwap.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): n period for rolling calculation. Default is 14.
    - fillna (bool): If True, fill nan values.

Call with:
    df['vwap'] = bta.volume_weighted_average_price(df, window=14, fillna=True)['vwap']

Returns:
    pd.DataFrame: DataFrame with 'vwap' column.
"""


def test():
    """
    Test function for the volume_weighted_average_price indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the volume_weighted_average_price indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(volume_weighted_average_price)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
