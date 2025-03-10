# -*- coding: utf-8 -*-
# smi_ergodic_indicator.py

import pandas as pd
import numpy as np


def smi_ergodic_indicator(df: pd.DataFrame, fast: int = 5, slow: int = 20, signal: int = 5, scalar: float = 1.0) -> pd.DataFrame:
    """SMI Ergodic Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # First, we need to calculate the True Strength Index (TSI)
    # The TSI uses momentum and its EMA to identify overbought/oversold conditions
    
    # Calculate momentum (close - previous close)
    momentum = df_copy["close"].diff()
    
    # Calculate absolute momentum
    abs_momentum = momentum.abs()
    
    # Double smoothing of momentum
    smooth1 = momentum.ewm(span=slow, adjust=False).mean()
    smooth2 = smooth1.ewm(span=fast, adjust=False).mean()
    
    # Double smoothing of absolute momentum
    abs_smooth1 = abs_momentum.ewm(span=slow, adjust=False).mean()
    abs_smooth2 = abs_smooth1.ewm(span=fast, adjust=False).mean()
    
    # Calculate TSI
    tsi = scalar * (smooth2 / abs_smooth2)
    
    # Calculate signal line (EMA of TSI)
    tsi_signal = tsi.ewm(span=signal, adjust=False).mean()
    
    # Calculate oscillator (TSI - signal)
    tsi_osc = tsi - tsi_signal
    
    # Add results to the DataFrame
    df_copy["smi"] = tsi * 100  # Multiply by 100 to get percentage
    df_copy["smi_signal"] = tsi_signal * 100
    df_copy["smi_histogram"] = tsi_osc * 100
    
    return df_copy[["smi", "smi_signal", "smi_histogram"]]


smi_ergodic_indicator.__doc__ = \
"""
Name:
    SMI Ergodic Indicator

Description:
    The SMI Ergodic Indicator is essentially the True Strength Index (TSI) developed 
    by William Blau, with the addition of a signal line. It uses double moving averages 
    of price changes over two time frames to identify momentum trends and potential 
    reversals.
    
    The indicator consists of three lines:
    - SMI: The main line, representing the smoothed ratio of momentum to absolute momentum
    - Signal: An EMA of the SMI line, used to generate potential trading signals
    - Histogram: The difference between SMI and Signal, which helps identify momentum shifts
    
    The trend is considered bullish when the SMI crosses above zero and bearish when it 
    crosses below zero. Trading signals can be generated when the SMI crosses its signal line.

More info:
    https://www.motivewave.com/studies/smi_ergodic_indicator.htm
    https://traderpedia.net/indicators/smi-ergodic-indicator/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - fast (int): The short smoothing period. Default is 5.
    - slow (int): The long smoothing period. Default is 20.
    - signal (int): The signal line period. Default is 5.
    - scalar (float): Multiplier for the result. Default is 1.0.

Call with:
    result = bta.smi_ergodic_indicator(df)
    df['smi'] = result['smi']
    df['smi_signal'] = result['smi_signal']
    df['smi_histogram'] = result['smi_histogram']

Returns:
    pd.DataFrame: DataFrame with 'smi', 'smi_signal', and 'smi_histogram' columns.
"""


def test():
    """
    Test function for the smi_ergodic_indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the smi_ergodic_indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(smi_ergodic_indicator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 