# -*- coding: utf-8 -*-
# volume_weighted_moving_average.py

import pandas as pd
import numpy as np


def volume_weighted_moving_average(df: pd.DataFrame, length: int = 10) -> pd.DataFrame:
    """Volume Weighted Moving Average (VWMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 10
    
    # Calculate price * volume
    pv = df_copy["close"] * df_copy["volume"]
    
    # Calculate VWMA
    vwma = (pv.rolling(window=length).sum() / 
            df_copy["volume"].rolling(window=length).sum())
    
    # Add result to DataFrame
    df_copy["vwma"] = vwma
    
    return df_copy[["vwma"]]


volume_weighted_moving_average.__doc__ = \
"""
Name:
    Volume Weighted Moving Average (VWMA)

Description:
    The Volume Weighted Moving Average (VWMA) is a technical analysis indicator that
    combines price and volume data to provide a more accurate representation of a
    security's average price over time. Unlike a simple moving average that gives
    equal weight to each price point, the VWMA gives more weight to price points
    with higher trading volumes.
    
    This weighting method can provide a more accurate representation of a security's
    true average price, as it accounts for the significance of price movements based
    on their trading volume. High-volume price movements are considered more significant
    and thus have a greater impact on the VWMA.

More info:
    https://www.investopedia.com/articles/trading/11/trading-with-vwap-mvwap.asp
    https://www.motivewave.com/studies/volume_weighted_moving_average.htm

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - length (int): The period for the VWMA calculation. Default is 10.

Call with:
    result = bta.volume_weighted_moving_average(df)
    df['vwma'] = result['vwma']

Returns:
    pd.DataFrame: DataFrame with 'vwma' column.
"""


def test():
    """
    Test function for the volume_weighted_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the volume_weighted_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(volume_weighted_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 