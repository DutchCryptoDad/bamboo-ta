# -*- coding: utf-8 -*-
# triple_exponential_average.py

import pandas as pd
import numpy as np


def triple_exponential_average(df: pd.DataFrame, length: int = 30, signal: int = 9, scalar: float = 100, drift: int = 1) -> pd.DataFrame:
    """Triple Exponential Average (TRIX) Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate first EMA
    ema1 = df_copy["close"].ewm(span=length, adjust=False).mean()
    
    # Calculate second EMA (EMA of first EMA)
    ema2 = ema1.ewm(span=length, adjust=False).mean()
    
    # Calculate third EMA (EMA of second EMA)
    ema3 = ema2.ewm(span=length, adjust=False).mean()
    
    # Calculate TRIX (rate of change of triple EMA)
    trix = scalar * ema3.pct_change(drift)
    
    # Calculate signal line (SMA of TRIX)
    trix_signal = trix.rolling(window=signal).mean()
    
    # Add results to the DataFrame
    df_copy["trix"] = trix
    df_copy["trix_signal"] = trix_signal
    
    return df_copy[["trix", "trix_signal"]]


triple_exponential_average.__doc__ = \
"""
Name:
    Triple Exponential Average (TRIX)

Description:
    TRIX is a momentum oscillator developed by Jack Hutson in the early 1980s. 
    It calculates the rate of change of a triple exponentially smoothed moving 
    average, filtering out minor price movements to identify the major trend direction.
    
    The indicator oscillates around a zero line. Positive values suggest bullish 
    momentum, while negative values indicate bearish momentum. Trading signals 
    can be generated when TRIX crosses above or below the zero line, or when it 
    crosses its signal line.
    
    The triple smoothing helps to eliminate noise and identify the underlying trend 
    more clearly than simpler rate of change indicators.

More info:
    https://www.investopedia.com/terms/t/trix.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the exponential moving averages. Default is 30.
    - signal (int): The period for the signal line. Default is 9.
    - scalar (float): Multiplier to scale the values. Default is 100.
    - drift (int): The difference period for rate of change calculation. Default is 1.

Call with:
    result = bta.triple_exponential_average(df)
    df['trix'] = result['trix']
    df['trix_signal'] = result['trix_signal']

Returns:
    pd.DataFrame: DataFrame with 'trix' and 'trix_signal' columns.
"""


def test():
    """
    Test function for the triple_exponential_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the triple_exponential_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(triple_exponential_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 