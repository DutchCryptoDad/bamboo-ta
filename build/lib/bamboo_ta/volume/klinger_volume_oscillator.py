# -*- coding: utf-8 -*-
# klinger_volume_oscillator.py

import pandas as pd
import numpy as np


def klinger_volume_oscillator(df: pd.DataFrame, fast_length: int = 34, 
                           slow_length: int = 55, signal_length: int = 13) -> pd.DataFrame:
    """Klinger Volume Oscillator (KVO)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    fast_length = int(fast_length) if fast_length > 0 else 34
    slow_length = int(slow_length) if slow_length > 0 else 55
    signal_length = int(signal_length) if signal_length > 0 else 13
    
    # Calculate HLC3 (Typical Price)
    df_copy["hlc3"] = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3
    
    # Calculate trend direction
    df_copy["trend"] = np.where(df_copy["hlc3"].diff() > 0, 1, -1)
    
    # Calculate signed volume
    df_copy["signed_volume"] = df_copy["volume"] * df_copy["trend"]
    
    # Calculate KVO
    fast_ema = df_copy["signed_volume"].ewm(span=fast_length, adjust=False).mean()
    slow_ema = df_copy["signed_volume"].ewm(span=slow_length, adjust=False).mean()
    df_copy["kvo"] = fast_ema - slow_ema
    
    # Calculate KVO signal line
    df_copy["kvo_signal"] = df_copy["kvo"].ewm(span=signal_length, adjust=False).mean()
    
    # Calculate KVO histogram
    df_copy["kvo_hist"] = df_copy["kvo"] - df_copy["kvo_signal"]
    
    return df_copy[["kvo", "kvo_signal", "kvo_hist"]]


klinger_volume_oscillator.__doc__ = \
"""
Name:
    Klinger Volume Oscillator (KVO)

Description:
    The Klinger Volume Oscillator (KVO) was developed by Stephen J. Klinger. It is designed 
    to predict price reversals in a market by comparing volume to price. The KVO attempts to 
    determine long-term trends of money flow while remaining sensitive enough to detect 
    short-term fluctuations.
    
    The oscillator does this by using volume to emphasize price movements and divergences.
    It uses two EMAs of a volume force, which is calculated using volume and price changes,
    then finds the difference between these EMAs.

More info:
    https://www.investopedia.com/terms/k/klingeroscillator.asp
    https://www.daytrading.com/klinger-volume-oscillator

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - fast_length (int): The fast period for the EMA calculation. Default is 34.
    - slow_length (int): The slow period for the EMA calculation. Default is 55.
    - signal_length (int): The period for the signal line EMA calculation. Default is 13.

Call with:
    result = bta.klinger_volume_oscillator(df)
    df['kvo'] = result['kvo']
    df['kvo_signal'] = result['kvo_signal']
    df['kvo_hist'] = result['kvo_hist']

Returns:
    pd.DataFrame: DataFrame with 'kvo', 'kvo_signal', and 'kvo_hist' columns.
"""


def test():
    """
    Test function for the klinger_volume_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the klinger_volume_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(klinger_volume_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 