# -*- coding: utf-8 -*-
# choppiness_index.py

import pandas as pd
import numpy as np


def choppiness_index(
    df: pd.DataFrame,
    length: int = 14,
    atr_length: int = 1,
    use_natural_log: bool = False,
    scalar: float = 100
) -> pd.DataFrame:
    """Choppiness Index (CHOP)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 14
    atr_length = int(atr_length) if atr_length > 0 else 1
    scalar = float(scalar) if scalar > 0 else 100
    
    # Calculate True Range
    tr1 = df_copy["high"] - df_copy["low"]
    tr2 = abs(df_copy["high"] - df_copy["close"].shift(1))
    tr3 = abs(df_copy["low"] - df_copy["close"].shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate ATR (Average True Range)
    atr = true_range.rolling(window=atr_length).mean()
    
    # Calculate sum of ATR over the specified length
    atr_sum = atr.rolling(window=length).sum()
    
    # Calculate highest high and lowest low over the specified length
    highest_high = df_copy["high"].rolling(window=length).max()
    lowest_low = df_copy["low"].rolling(window=length).min()
    
    # Calculate range difference
    range_diff = highest_high - lowest_low
    
    # Calculate Choppiness Index
    if use_natural_log:
        df_copy["chop"] = scalar * (np.log(atr_sum) - np.log(range_diff)) / np.log(length)
    else:
        df_copy["chop"] = scalar * (np.log10(atr_sum) - np.log10(range_diff)) / np.log10(length)
    
    return df_copy[["chop"]]


choppiness_index.__doc__ = \
"""
Name:
    Choppiness Index (CHOP)

Description:
    The Choppiness Index was created by Australian commodity trader E.W. Dreiss and is 
    designed to determine if the market is choppy (trading sideways) or not choppy 
    (trading within a trend in either direction).
    
    The indicator oscillates between 0 and 100, where:
    - Values closer to 100 indicate a choppy, sideways market with no clear trend
    - Values closer to 0 indicate a trending market (either up or down)
    
    This indicator is useful for determining whether to use trend-following strategies 
    or range-bound strategies. It can also help identify potential breakouts when transitioning 
    from a choppy to a trending market.
    
    Note that this is a non-directional indicator; it does not indicate whether the trend is 
    up or down, only the degree to which the market is trending or not trending.

More info:
    https://www.tradingview.com/scripts/choppinessindex/
    https://www.motivewave.com/studies/choppiness_index.htm

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for the Choppiness Index calculation. Default is 14.
    - atr_length (int): The period for the ATR calculation. Default is 1.
    - use_natural_log (bool): If True, natural logarithm (ln) is used instead of log base 10. Default is False.
    - scalar (float): Scaling factor for the indicator. Default is 100.

Call with:
    result = bta.choppiness_index(df)
    df['chop'] = result['chop']

Returns:
    pd.DataFrame: DataFrame with 'chop' column.
"""


def test():
    """
    Test function for the choppiness_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the choppiness_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(choppiness_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 