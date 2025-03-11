# -*- coding: utf-8 -*-
# commodity_channel_index.py

import pandas as pd
import numpy as np


def commodity_channel_index(df: pd.DataFrame, length: int = 14, constant: float = 0.015) -> pd.DataFrame:
    """Commodity Channel Index"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate typical price
    df_copy["tp"] = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3
    
    # Calculate the mean of typical price over the specified length
    mean_tp = df_copy["tp"].rolling(window=length).mean()
    
    # Calculate the mean absolute deviation
    # MAD is the average distance between each value and the average
    mad_tp = df_copy["tp"].rolling(window=length).apply(
        lambda x: np.mean(np.abs(x - np.mean(x))), raw=True
    )
    
    # Calculate CCI
    df_copy["cci"] = (df_copy["tp"] - mean_tp) / (constant * mad_tp)
    
    return df_copy[["cci"]]


commodity_channel_index.__doc__ = \
"""
Name:
    Commodity Channel Index

Description:
    The Commodity Channel Index (CCI) is a momentum-based oscillator used to help determine 
    when an investment vehicle is reaching a condition of being overbought or oversold. 
    It is also used to assess price trend direction and strength. This information 
    helps traders and investors make buy/sell decisions.
    
    CCI measures the current price level relative to an average price level over a 
    given period of time. The indicator fluctuates above or below zero, moving 
    between overbought and oversold conditions.

More info:
    https://www.investopedia.com/terms/c/commoditychannelindex.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - length (int): The period for calculating CCI. Default is 14.
    - constant (float): Scaling factor. Default is 0.015.

Call with:
    df['cci'] = bta.commodity_channel_index(df)['cci']

Returns:
    pd.DataFrame: DataFrame with 'cci' column.
"""


def test():
    """
    Test function for the commodity_channel_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the commodity_channel_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(commodity_channel_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 