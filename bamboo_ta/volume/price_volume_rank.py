# -*- coding: utf-8 -*-
# price_volume_rank.py

import pandas as pd
import numpy as np


def price_volume_rank(df: pd.DataFrame) -> pd.DataFrame:
    """Price Volume Rank (PVR)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate price and volume changes
    df_copy["close_diff"] = df_copy["close"].diff().fillna(0)
    df_copy["volume_diff"] = df_copy["volume"].diff().fillna(0)
    
    # Calculate PVR
    conditions = [
        (df_copy["close_diff"] >= 0) & (df_copy["volume_diff"] >= 0),  # Price up, Volume up
        (df_copy["close_diff"] >= 0) & (df_copy["volume_diff"] < 0),   # Price up, Volume down
        (df_copy["close_diff"] < 0) & (df_copy["volume_diff"] >= 0),   # Price down, Volume up
        (df_copy["close_diff"] < 0) & (df_copy["volume_diff"] < 0)     # Price down, Volume down
    ]
    values = [1, 2, 3, 4]
    
    df_copy["pvr"] = np.select(conditions, values, default=np.nan)
    
    return df_copy[["pvr"]]


price_volume_rank.__doc__ = \
"""
Name:
    Price Volume Rank (PVR)

Description:
    The Price Volume Rank indicator was developed by Anthony J. Macek to classify price and 
    volume behavior into four distinct categories. It provides a simple numerical classification 
    that can help identify potential market turning points and trend continuations.
    
    The indicator assigns values from 1 to 4 based on the combination of price change and 
    volume change directions:
    
    1: Price up, Volume up (strong bullish)
    2: Price up, Volume down (weak bullish)
    3: Price down, Volume up (strong bearish)
    4: Price down, Volume down (weak bearish)
    
    The basic interpretation is to consider buying when the PVR is below 2.5 and 
    selling when it is above 2.5.

More info:
    https://www.fmlabs.com/reference/default.htm?url=PVrank.htm
    Technical Analysis of Stocks & Commodities Magazine, June 1994

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.

Call with:
    result = bta.price_volume_rank(df)
    df['pvr'] = result['pvr']

Returns:
    pd.DataFrame: DataFrame with 'pvr' column.
"""


def test():
    """
    Test function for the price_volume_rank indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the price_volume_rank indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(price_volume_rank)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 