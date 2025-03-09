# -*- coding: utf-8 -*-
# relative_volume.py
import numpy as np
import pandas as pd


def relative_volume(
    df: pd.DataFrame, volume_col: str = "volume", window: int = 24
) -> pd.DataFrame:
    """Relative Volume"""
    # Create a copy of the DataFrame to prevent modifying the original
    df_copy = df.copy()

    # Calculate the SMA of the volume
    df_copy["volume_sma"] = df_copy[volume_col].rolling(window=window).mean()

    # Calculate Relative Volume
    df_copy["rvol"] = df_copy[volume_col] / df_copy["volume_sma"]

    # Return the DataFrame with the RVOL column
    return df_copy[["rvol"]]


relative_volume.__doc__ = """
Name:
    Relative Volume (RVOL)

Description:
    Computes the Relative Volume (RVOL) indicator, which compares the current volume
    to a moving average of volume over a specified window. This helps identify periods
    of unusually high or low trading activity. Values greater than 1 indicate above-average 
    volume, while values less than 1 indicate below-average volume. Traders often look for 
    high relative volume to confirm breakouts or significant price movements.

More info:
    https://www.investopedia.com/terms/r/relative-volume.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing a volume column.
    - volume_col (str): Name of the column containing volume data. Default is 'volume'.
    - window (int): Lookback window for calculating the Simple Moving Average (SMA) of volume. Default is 24.

Call with:
    df['rvol'] = bta.relative_volume(df, volume_col='volume', window=24)['rvol']

Returns:
    pd.DataFrame: DataFrame with an additional column:
        - 'rvol': The Relative Volume values.
"""


def test():
    """
    Test function for the relative_volume indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the relative_volume indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(relative_volume)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
