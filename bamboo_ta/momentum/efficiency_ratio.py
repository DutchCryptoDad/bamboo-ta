# -*- coding: utf-8 -*-
# efficiency_ratio.py

import pandas as pd
import numpy as np


def efficiency_ratio(df: pd.DataFrame, length: int = 10, drift: int = 1) -> pd.DataFrame:
    """Efficiency Ratio"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate the absolute price change over the specified length
    abs_diff = df_copy["close"].diff(length).abs()
    
    # Calculate the sum of absolute price changes over the specified length
    abs_volatility = df_copy["close"].diff(drift).abs()
    volatility_sum = abs_volatility.rolling(window=length).sum()
    
    # Calculate the Efficiency Ratio
    df_copy["er"] = abs_diff / volatility_sum
    
    return df_copy[["er"]]


efficiency_ratio.__doc__ = \
"""
Name:
    Efficiency Ratio

Description:
    The Efficiency Ratio (ER) was developed by Perry J. Kaufman to measure market noise 
    or volatility. It quantifies the efficiency of price movement by comparing the net 
    directional movement to the total volatility over a specified period.
    
    The indicator ranges from 0 to 1, where values close to 1 indicate a strong trend 
    with minimal noise, and values close to 0 indicate a choppy market with high noise. 
    It's often used to adjust the responsiveness of other indicators based on market 
    conditions.

More info:
    https://www.investopedia.com/terms/k/kaufman-efficiency-ratio.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the efficiency calculation. Default is 10.
    - drift (int): The period for calculating price changes. Default is 1.

Call with:
    df['er'] = bta.efficiency_ratio(df)['er']

Returns:
    pd.DataFrame: DataFrame with 'er' column.
"""


def test():
    """
    Test function for the efficiency_ratio indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the efficiency_ratio indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(efficiency_ratio)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 