# -*- coding: utf-8 -*-
# center_of_gravity.py

import pandas as pd
import numpy as np


def center_of_gravity(df: pd.DataFrame, length: int = 10) -> pd.DataFrame:
    """Center of Gravity Oscillator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate coefficients (length down to 1)
    coefficients = np.array([length - i for i in range(length)])
    
    # Apply the center of gravity formula
    def calculate_cg(window):
        if len(window) < length:
            return np.nan
        # Numerator: -sum(price[i] * (length - i))
        numerator = -np.sum(window * coefficients[:len(window)])
        # Denominator: sum(price)
        denominator = np.sum(window)
        return numerator / denominator if denominator != 0 else np.nan
    
    # Calculate CG
    df_copy["cg"] = df_copy["close"].rolling(window=length).apply(
        calculate_cg, raw=True
    )
    
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
    
    The oscillator calculates a weighted sum where more recent prices have less 
    weight (contrary to typical weighted averages), creating a unique perspective 
    on price momentum.

More info:
    http://www.mesasoftware.com/papers/TheCGOscillator.pdf

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the CG calculation. Default is 10.

Call with:
    df['cg'] = bta.center_of_gravity(df)['cg']

Returns:
    pd.DataFrame: DataFrame with 'cg' column.
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