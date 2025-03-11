# -*- coding: utf-8 -*-
# bbw_expansion.py
import numpy as np
import pandas as pd


def bbw_expansion(
    df: pd.DataFrame,
    upper_band: str = "bb_upper",
    lower_band: str = "bb_lower",
    middle_band: str = "bb_middle",
    mult: float = 1.05,
    rolling_window: int = 20,
) -> pd.DataFrame:
    """Bollinger Band Width Expansion Detector"""
    # Create a copy of the DataFrame to prevent modifying the original
    df_copy = df.copy()

    # Calculate the Bollinger Band Width (BBW)
    df_copy["bb_width"] = (df_copy[upper_band] - df_copy[lower_band]) / df_copy[
        middle_band
    ]

    # Calculate the rolling maximum of BBW
    df_copy["rolling_max"] = df_copy["bb_width"].rolling(window=rolling_window).max()

    # Detect expansion where the BBW exceeds the rolling max by the multiplier
    df_copy["bbw_expansion"] = (
        df_copy["bb_width"] > (df_copy["rolling_max"] * mult)
    ).astype(int)

    # Return the DataFrame with the calculated columns
    return df_copy[["bb_width", "bbw_expansion"]]


bbw_expansion.__doc__ = """
Name:
    Bollinger Band Width (BBW) Expansion Detector

Description:
    Detects if the Bollinger Band Width (BBW) of the last observation exceeds a 
    rolling maximum by a specified multiplier. This can signal a potential increase 
    in market volatility. The Bollinger Band Width is calculated as 
    (Upper Band - Lower Band) / Middle Band, and is a measure of volatility.
    This indicator requires the bta.bollinger_bands function to be used in the dataframe too.

More info:
    https://tradingview.com/support/solutions/43000501971-bollinger-bands-width/

Parameters:
    - df (pd.DataFrame): Input DataFrame containing Bollinger Band columns.
    - upper_band (str): Column name for the upper Bollinger Band. Default is 'bb_upper'.
    - lower_band (str): Column name for the lower Bollinger Band. Default is 'bb_lower'.
    - middle_band (str): Column name for the middle Bollinger Band. Default is 'bb_middle'.
    - mult (float): Multiplier to compare the last BBW value against the rolling maximum. Default is 1.05.
    - rolling_window (int): Rolling window size for calculating the maximum BBW. Default is 20.

Call with:
    df['bbw_expansion'] = bta.bbw_expansion(df, upper_band='bb_upper', lower_band='bb_lower', 
                                           middle_band='bb_middle', mult=1.05, rolling_window=20)['bbw_expansion']

Returns:
    pd.DataFrame: DataFrame with additional columns:
        - 'bb_width': Bollinger Band Width values.
        - 'bbw_expansion': Indicator for expansion (1 if condition met, 0 otherwise).

Important Notes:
    - This function REQUIRES that your DataFrame already contains Bollinger Bands columns:
      * Upper band column (default name: 'bb_upper')
      * Lower band column (default name: 'bb_lower')
      * Middle band column (default name: 'bb_middle')
    
    - These columns must be generated first using the bollinger_bands function:
      ```
      bb_df = bta.bollinger_bands(df)
      df['bb_upper'] = bb_df['upper']
      df['bb_middle'] = bb_df['middle']
      df['bb_lower'] = bb_df['lower']
      ```
    
    - The function will fail with a KeyError if the required Bollinger Band columns are missing.
    
    - For testing purposes, you might need to create a wrapper that calculates
      Bollinger Bands before calling this function.
"""


def test():
    """
    Test function for the bbw_expansion indicator.

    This function uses the generic test_indicator function from bamboo_ta.py
    to test the bbw_expansion indicator.

    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator

        # Test the indicator
        test_indicator(bbw_expansion)

    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
