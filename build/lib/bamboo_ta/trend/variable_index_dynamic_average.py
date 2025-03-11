# -*- coding: utf-8 -*-
# variable_index_dynamic_average.py

import pandas as pd
import numpy as np


def variable_index_dynamic_average(df: pd.DataFrame, length: int = 14, 
                                 column: str = "close", drift: int = 1) -> pd.DataFrame:
    """Variable Index Dynamic Average (VIDYA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Calculate the Chande Momentum Oscillator (CMO)
    def calculate_cmo(source: pd.Series, n: int, d: int) -> pd.Series:
        """Calculate Chande Momentum Oscillator (CMO)"""
        # Calculate the momentum (difference between current value and d periods ago)
        mom = source.diff(d)
        
        # Split momentum into positive and negative values
        positive = mom.copy().clip(lower=0)
        negative = mom.copy().clip(upper=0).abs()
        
        # Sum the positive and negative values over n periods
        pos_sum = positive.rolling(n).sum()
        neg_sum = negative.rolling(n).sum()
        
        # Calculate CMO
        cmo = (pos_sum - neg_sum) / (pos_sum + neg_sum)
        return cmo
    
    # Calculate the CMO and get its absolute value
    abs_cmo = calculate_cmo(series, length, drift).abs()
    
    # Calculate the smoothing factor
    alpha = 2 / (length + 1)
    
    # Initialize the VIDYA series
    vidya = pd.Series(np.nan, index=series.index)
    
    # Set the first valid value (at position length)
    if len(series) > length:
        vidya.iloc[length] = series.iloc[length]
    
    # Calculate VIDYA values
    for i in range(length + 1, len(series)):
        if np.isnan(vidya.iloc[i-1]) or np.isnan(abs_cmo.iloc[i]):
            continue
        vidya.iloc[i] = alpha * abs_cmo.iloc[i] * series.iloc[i] + vidya.iloc[i - 1] * (1 - alpha * abs_cmo.iloc[i])
    
    # Add result to DataFrame
    df_copy["vidya"] = vidya
    
    return df_copy[["vidya"]]


variable_index_dynamic_average.__doc__ = \
"""
Name:
    Variable Index Dynamic Average (VIDYA)

Description:
    The Variable Index Dynamic Average (VIDYA) was developed by Tushar Chande in 1992.
    It is an adaptive moving average that adjusts its sensitivity based on market volatility.
    
    VIDYA uses the Chande Momentum Oscillator (CMO) to determine volatility. When volatility 
    is high, VIDYA reacts faster to price changes, making it more responsive than traditional
    moving averages. When volatility is low, it behaves more like a standard exponential 
    moving average.
    
    This indicator can be particularly useful for traders who want a moving average that 
    automatically adjusts to changing market conditions, potentially reducing lag during 
    volatile periods.

More info:
    https://www.tradingview.com/script/hdrf0fXV-Variable-Index-Dynamic-Average-VIDYA/
    https://www.perfecttrendsystem.com/blog_mt4_2/en/vidya-indicator-for-mt4

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the VIDYA calculation. Default is 14.
    - column (str): The column name to use for calculations. Default is 'close'.
    - drift (int): The period for momentum calculation in CMO. Default is 1.

Call with:
    result = bta.variable_index_dynamic_average(df)
    df['vidya'] = result['vidya']

Returns:
    pd.DataFrame: DataFrame with 'vidya' column.
"""


def test():
    """
    Test function for the variable_index_dynamic_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the variable_index_dynamic_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(variable_index_dynamic_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 