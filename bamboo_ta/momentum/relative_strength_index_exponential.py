# -*- coding: utf-8 -*-
# relative_strength_index_exponential.py

import pandas as pd
import numpy as np


def relative_strength_index_exponential(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
    """Relative Strength Index Exponential"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    close = df_copy["close"]
    
    # Initialize variables
    vC, v1C = 0, 0
    v4, v8, v10, v14, v18, v20 = 0, 0, 0, 0, 0, 0
    
    f0, f8, f10, f18, f20, f28, f30, f38 = 0, 0, 0, 0, 0, 0, 0, 0
    f40, f48, f50, f58, f60, f68, f70, f78 = 0, 0, 0, 0, 0, 0, 0, 0
    f80, f88, f90 = 0, 0, 0
    
    # Calculate RSX
    m = len(close)
    result = pd.Series(index=close.index)
    result.iloc[:length-1] = np.nan
    result.iloc[length-1] = 0
    
    for i in range(length, m):
        if f90 == 0:
            f90 = 1.0
            f0 = 0.0
            if length - 1.0 >= 5:
                f88 = length - 1.0
            else:
                f88 = 5.0
            f8 = 100.0 * close.iloc[i]
            f18 = 3.0 / (length + 2.0)
            f20 = 1.0 - f18
        else:
            if f88 <= f90:
                f90 = f88 + 1
            else:
                f90 = f90 + 1
            f10 = f8
            f8 = 100 * close.iloc[i]
            v8 = f8 - f10
            f28 = f20 * f28 + f18 * v8
            f30 = f18 * f28 + f20 * f30
            vC = 1.5 * f28 - 0.5 * f30
            f38 = f20 * f38 + f18 * vC
            f40 = f18 * f38 + f20 * f40
            v10 = 1.5 * f38 - 0.5 * f40
            f48 = f20 * f48 + f18 * v10
            f50 = f18 * f48 + f20 * f50
            v14 = 1.5 * f48 - 0.5 * f50
            f58 = f20 * f58 + f18 * abs(v8)
            f60 = f18 * f58 + f20 * f60
            v18 = 1.5 * f58 - 0.5 * f60
            f68 = f20 * f68 + f18 * v18
            f70 = f18 * f68 + f20 * f70
            v1C = 1.5 * f68 - 0.5 * f70
            f78 = f20 * f78 + f18 * v1C
            f80 = f18 * f78 + f20 * f80
            v20 = 1.5 * f78 - 0.5 * f80
            
            if f88 >= f90 and f8 != f10:
                f0 = 1.0
            if f88 == f90 and f0 == 0.0:
                f90 = 0.0
        
        if f88 < f90 and v20 > 0.0000000001:
            v4 = (v14 / v20 + 1.0) * 50.0
            if v4 > 100.0:
                v4 = 100.0
            if v4 < 0.0:
                v4 = 0.0
        else:
            v4 = 50.0
        result.iloc[i] = v4
    
    # Add result to the DataFrame
    df_copy["rsx"] = result
    
    return df_copy[["rsx"]]


relative_strength_index_exponential.__doc__ = \
"""
Name:
    Relative Strength Index Exponential (RSX)

Description:
    The Relative Strength Index Exponential (RSX) is based on the popular RSI indicator 
    and inspired by the work of Jurik Research. This enhanced version of the RSI reduces 
    noise and provides a clearer, only slightly delayed insight on momentum and velocity 
    of price movements.
    
    Like the traditional RSI, it's an oscillator that ranges from 0 to 100, with values 
    above 70 typically considered overbought and values below 30 considered oversold. 
    However, the RSX's smoother line can provide more reliable signals with less whipsaws.

More info:
    http://www.jurikres.com/catalog1/ms_rsx.htm
    https://www.prorealcode.com/prorealtime-indicators/jurik-rsx/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the RSX calculation. Default is 14.

Call with:
    df['rsx'] = bta.relative_strength_index_exponential(df)['rsx']

Returns:
    pd.DataFrame: DataFrame with 'rsx' column.
"""


def test():
    """
    Test function for the relative_strength_index_exponential indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the relative_strength_index_exponential indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(relative_strength_index_exponential)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 