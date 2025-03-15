# -*- coding: utf-8 -*-
# center_of_gravity.py

import pandas as pd
import numpy as np


def center_of_gravity(df: pd.DataFrame, length: int = 10, include_shifted: bool = True) -> pd.DataFrame:
    """Center of Gravity Oscillator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate weighted moving average (WMA)
    weights = np.arange(1, length + 1)
    weight_sum = weights.sum()
    
    # Apply the weighted moving average calculation
    def calculate_wma(window):
        if len(window) < length:
            return np.nan
        # Apply weights with more weight to recent prices
        return np.sum(window * weights[:len(window)]) / weight_sum
    
    # Calculate WMA
    wma_values = df_copy["close"].rolling(window=length).apply(
        calculate_wma, raw=True
    )
    
    # Calculate the Center of Gravity according to Ehlers' formula
    numerator = wma_values * length * (length + 1) / 2
    denominator = df_copy["close"].rolling(window=length).sum()
    
    df_copy["cg"] = numerator / denominator
    
    # Add the shifted CG value (previous bar's CG value)
    if include_shifted:
        df_copy["cg_prev"] = df_copy["cg"].shift(1)
        return df_copy[["cg", "cg_prev"]]
    
    return df_copy[["cg"]]


center_of_gravity.__doc__ = \
"""
Name:
    Center of Gravity

Description:
    The Center of Gravity (CG) oscillator was developed by John Ehlers to identify 
    turning points in price with minimal lag. Unlike many other momentum oscillators, 
    the CG aims to be more responsive to price changes while maintaining some 
    smoothing characteristics.
    
    The implementation follows Ehlers' formula:
    CG = WMA(close, length) * length * (length + 1) / 2 / SUM(close, length)
    
    Where WMA is a weighted moving average that assigns more weight to recent prices.

More info:
    http://www.mesasoftware.com/papers/TheCGOscillator.pdf
    https://www.tradingview.com/script/yhhunbyq/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the CG calculation. Default is 10.
    - include_shifted (bool): If True, includes the CG value from the previous bar
      as a separate column. Default is True.

Call with:
    # Get both current and previous CG values
    cg_df = bta.center_of_gravity(df)
    df['cg'] = cg_df['cg']
    df['cg_prev'] = cg_df['cg_prev']
    
    # Or just the current CG value
    df['cg'] = bta.center_of_gravity(df, include_shifted=False)['cg']

Returns:
    pd.DataFrame: DataFrame with 'cg' column and optionally 'cg_prev' column.
"""


def test():
    """
    Test function for the center_of_gravity indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the center_of_gravity indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(center_of_gravity)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 