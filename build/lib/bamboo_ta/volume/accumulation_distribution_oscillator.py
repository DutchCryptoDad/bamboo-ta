# -*- coding: utf-8 -*-
# accumulation_distribution_oscillator.py

import pandas as pd
import numpy as np


def accumulation_distribution_oscillator(
    df: pd.DataFrame, fast_length: int = 3, slow_length: int = 10, fillna: bool = False
) -> pd.DataFrame:
    """Accumulation/Distribution Oscillator (ADOSC)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    fast_length = int(fast_length) if fast_length > 0 else 3
    slow_length = int(slow_length) if slow_length > 0 else 10
    
    # Calculate Accumulation/Distribution Index
    clv = (
        (df_copy["close"] - df_copy["low"]) - (df_copy["high"] - df_copy["close"])
    ) / (df_copy["high"] - df_copy["low"])
    clv = clv.fillna(0.0)  # Handling division by zero
    ad = clv * df_copy["volume"]
    ad = ad.cumsum()
    
    # Calculate fast and slow EMAs of AD
    fast_ad = ad.ewm(span=fast_length, adjust=False).mean()
    slow_ad = ad.ewm(span=slow_length, adjust=False).mean()
    
    # Calculate ADOSC
    adosc = fast_ad - slow_ad
    
    # Handle NaN values
    if fillna:
        adosc = adosc.fillna(0)
    
    # Add result to DataFrame
    df_copy["adosc"] = adosc
    
    return df_copy[["adosc"]]


accumulation_distribution_oscillator.__doc__ = \
"""
Name:
    Accumulation/Distribution Oscillator (ADOSC)

Description:
    The Accumulation/Distribution Oscillator, also known as the Chaikin Oscillator, 
    measures the momentum of the Accumulation/Distribution Index (ADI) using the 
    difference between fast and slow exponential moving averages of the ADI.
    
    The indicator helps identify when the Accumulation/Distribution Index is 
    changing direction, which can signal potential price reversals. It's particularly 
    useful for spotting divergences between price and volume flow.

More info:
    https://www.investopedia.com/articles/active-trading/031914/understanding-chaikin-oscillator.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:chaikin_oscillator

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - fast_length (int): The period for the fast EMA calculation. Default is 3.
    - slow_length (int): The period for the slow EMA calculation. Default is 10.
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    result = bta.accumulation_distribution_oscillator(df)
    df['adosc'] = result['adosc']

Returns:
    pd.DataFrame: DataFrame with 'adosc' column.
"""


def test():
    """
    Test function for the accumulation_distribution_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the accumulation_distribution_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(accumulation_distribution_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 