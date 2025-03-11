# -*- coding: utf-8 -*-
# ehlers_ray_index.py

import pandas as pd
import numpy as np


def ehlers_ray_index(df: pd.DataFrame, length: int = 13) -> pd.DataFrame:
    """Ehlers Ray Index"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate the exponential moving average of the close
    ema = df_copy["close"].ewm(span=length, adjust=False).mean()
    
    # Calculate Bull Power (high - EMA)
    df_copy["bull_power"] = df_copy["high"] - ema
    
    # Calculate Bear Power (low - EMA)
    df_copy["bear_power"] = df_copy["low"] - ema
    
    return df_copy[["bull_power", "bear_power"]]


ehlers_ray_index.__doc__ = \
"""
Name:
    Ehlers Ray Index

Description:
    The Ehlers Ray Index, also known as Elder Ray Index, was developed by Dr. Alexander 
    Elder. It consists of two separate indicators: Bull Power and Bear Power, which 
    are designed to measure the strength of buyers and sellers in the market.
    
    Bull Power measures the ability of buyers to push prices above an average consensus 
    value (the EMA). Positive values indicate buying pressure, with higher values 
    showing stronger buying pressure.
    
    Bear Power measures the ability of sellers to push prices below the same average 
    consensus value. Negative values indicate selling pressure, with lower values 
    showing stronger selling pressure.
    
    Both indicators are typically used together with trend analysis to identify 
    favorable entry points.

More info:
    https://www.investopedia.com/terms/e/elderray.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - length (int): The period for the EMA calculation. Default is 13.

Call with:
    result = bta.ehlers_ray_index(df)
    df['bull_power'] = result['bull_power']
    df['bear_power'] = result['bear_power']

Returns:
    pd.DataFrame: DataFrame with 'bull_power' and 'bear_power' columns.
"""


def test():
    """
    Test function for the ehlers_ray_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ehlers_ray_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ehlers_ray_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 