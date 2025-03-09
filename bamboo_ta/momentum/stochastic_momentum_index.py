# -*- coding: utf-8 -*-
# stochastic_momentum_index.py

import pandas as pd
import numpy as np


def stochastic_momentum_index(
    df: pd.DataFrame, k_length: int = 9, d_length: int = 3
) -> pd.DataFrame:
    """Stochastic Momentum Index (SMI)"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    ll = df_copy["low"].rolling(window=k_length).min()
    hh = df_copy["high"].rolling(window=k_length).max()

    diff = hh - ll
    rdiff = df_copy["close"] - (hh + ll) / 2

    avgrel = rdiff.ewm(span=d_length).mean().ewm(span=d_length).mean()
    avgdiff = diff.ewm(span=d_length).mean().ewm(span=d_length).mean()

    df_copy["smi"] = np.where(avgdiff != 0, (avgrel / (avgdiff / 2) * 100), 0)

    return df_copy[["smi"]]


stochastic_momentum_index.__doc__ = """
Name:
    Stochastic Momentum Index (SMI)

Description:
    The Stochastic Momentum Index (SMI) Indicator was developed by William Blau
    in 1993 and is considered to be a momentum indicator that can help identify
    trend reversal points.

More info:
    

Call with:
    df['smi'] = bta.stochastic_momentum_index(df, k_length=9, d_length=3)['smi']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - k_length (int): Period for %K. Default is 9.
    - d_length (int): Period for %D. Default is 3.

Returns:
    pd.DataFrame: DataFrame with 'smi' column populated.
"""


def test():
    """
    Test function for the stochastic_momentum_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the stochastic_momentum_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(stochastic_momentum_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
