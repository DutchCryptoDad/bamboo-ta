# -*- coding: utf-8 -*-
# know_sure_thing.py

import pandas as pd
import numpy as np


def know_sure_thing(df: pd.DataFrame, roc1: int = 10, roc2: int = 15, roc3: int = 20, roc4: int = 30, 
                    sma1: int = 10, sma2: int = 10, sma3: int = 10, sma4: int = 15, signal: int = 9) -> pd.DataFrame:
    """Know Sure Thing Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate ROC (Rate of Change) for different periods
    def calculate_roc(series, length):
        return 100 * (series / series.shift(length) - 1)
    
    # Calculate ROC values
    roc_1 = calculate_roc(df_copy["close"], roc1)
    roc_2 = calculate_roc(df_copy["close"], roc2)
    roc_3 = calculate_roc(df_copy["close"], roc3)
    roc_4 = calculate_roc(df_copy["close"], roc4)
    
    # Calculate moving averages of ROC values
    rocma1 = roc_1.rolling(window=sma1).mean()
    rocma2 = roc_2.rolling(window=sma2).mean()
    rocma3 = roc_3.rolling(window=sma3).mean()
    rocma4 = roc_4.rolling(window=sma4).mean()
    
    # Calculate KST
    kst = 100 * (rocma1 + 2 * rocma2 + 3 * rocma3 + 4 * rocma4)
    
    # Calculate KST signal line
    kst_signal = kst.rolling(window=signal).mean()
    
    # Add results to the DataFrame
    df_copy["kst"] = kst
    df_copy["kst_signal"] = kst_signal
    
    return df_copy[["kst", "kst_signal"]]


know_sure_thing.__doc__ = \
"""
Name:
    Know Sure Thing

Description:
    The Know Sure Thing (KST) is a momentum oscillator developed by Martin Pring. 
    It is based on the Rate of Change (ROC) of different time periods, which are 
    then smoothed and weighted to create a composite momentum indicator.
    
    The KST uses four different ROC periods, each smoothed with a simple moving 
    average (SMA) and assigned different weights. These weighted values are then 
    summed to create the KST line. A signal line (typically a 9-period SMA of the KST) 
    is used to identify potential buy and sell signals.
    
    The indicator is designed to capture momentum across different timeframes, 
    making it potentially more responsive and less prone to false signals than 
    simpler momentum indicators.

More info:
    https://www.investopedia.com/terms/k/know-sure-thing-kst.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - roc1 (int): First ROC period. Default is 10.
    - roc2 (int): Second ROC period. Default is 15.
    - roc3 (int): Third ROC period. Default is 20.
    - roc4 (int): Fourth ROC period. Default is 30.
    - sma1 (int): SMA period for the first ROC. Default is 10.
    - sma2 (int): SMA period for the second ROC. Default is 10.
    - sma3 (int): SMA period for the third ROC. Default is 10.
    - sma4 (int): SMA period for the fourth ROC. Default is 15.
    - signal (int): Period for the signal line. Default is 9.

Call with:
    result = bta.know_sure_thing(df)
    df['kst'] = result['kst']
    df['kst_signal'] = result['kst_signal']

Returns:
    pd.DataFrame: DataFrame with 'kst' and 'kst_signal' columns.
"""


def test():
    """
    Test function for the know_sure_thing indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the know_sure_thing indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(know_sure_thing)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 