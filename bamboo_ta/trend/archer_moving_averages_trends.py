# -*- coding: utf-8 -*-
# archer_moving_averages_trends.py

import pandas as pd
import numpy as np


def archer_moving_averages_trends(
    df: pd.DataFrame,
    fast_length: int = 8,
    slow_length: int = 21,
    lookback: int = 2,
    ma_type: str = "EMA",
    column: str = "close"
) -> pd.DataFrame:
    """Archer Moving Averages Trends (AMAT)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    fast_length = int(fast_length) if fast_length > 0 else 8
    slow_length = int(slow_length) if slow_length > 0 else 21
    lookback = int(lookback) if lookback > 0 else 2
    ma_type = ma_type.upper()
    
    # Calculate the fast and slow moving averages
    if ma_type == "SMA":
        # Simple Moving Average
        fast_ma = df_copy[column].rolling(window=fast_length).mean()
        slow_ma = df_copy[column].rolling(window=slow_length).mean()
    elif ma_type == "EMA":
        # Exponential Moving Average
        fast_ma = df_copy[column].ewm(span=fast_length, adjust=False).mean()
        slow_ma = df_copy[column].ewm(span=slow_length, adjust=False).mean()
    elif ma_type == "WMA":
        # Weighted Moving Average
        weights_fast = np.arange(1, fast_length + 1)
        weights_slow = np.arange(1, slow_length + 1)
        
        fast_ma = df_copy[column].rolling(window=fast_length).apply(
            lambda x: np.sum(weights_fast * x) / np.sum(weights_fast), 
            raw=True
        )
        
        slow_ma = df_copy[column].rolling(window=slow_length).apply(
            lambda x: np.sum(weights_slow * x) / np.sum(weights_slow), 
            raw=True
        )
    else:
        raise ValueError(f"Unsupported moving average type: {ma_type}")
    
    # Calculate long_run: both MAs are increasing for 'lookback' periods
    fast_increasing = fast_ma.diff(lookback) > 0
    slow_increasing = slow_ma.diff(lookback) > 0
    fast_above_slow = fast_ma > slow_ma
    
    long_run = (fast_increasing & slow_increasing & fast_above_slow).astype(int)
    
    # Calculate short_run: both MAs are decreasing for 'lookback' periods
    fast_decreasing = fast_ma.diff(lookback) < 0
    slow_decreasing = slow_ma.diff(lookback) < 0
    fast_below_slow = fast_ma < slow_ma
    
    short_run = (fast_decreasing & slow_decreasing & fast_below_slow).astype(int)
    
    # Store results in DataFrame
    df_copy["amat_long"] = long_run
    df_copy["amat_short"] = short_run
    
    return df_copy[["amat_long", "amat_short"]]


archer_moving_averages_trends.__doc__ = \
"""
Name:
    Archer Moving Averages Trends (AMAT)

Description:
    The Archer Moving Averages Trends indicator identifies potential trend conditions
    by analyzing the relationship between fast and slow moving averages.
    
    The indicator generates two signals:
    - Long Run: Identifies potential bullish trends when both fast and slow moving
      averages are increasing over the lookback period, and the fast MA is above the slow MA.
    - Short Run: Identifies potential bearish trends when both fast and slow moving
      averages are decreasing over the lookback period, and the fast MA is below the slow MA.
    
    This indicator can be useful for trend identification, filtering trading signals,
    or as a component in more complex trading strategies.

More info:
    N/A (Original implementation by Kevin Johnson for Pandas TA)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - fast_length (int): The period for the fast moving average. Default is 8.
    - slow_length (int): The period for the slow moving average. Default is 21.
    - lookback (int): The period to check for consistent movement in the MAs. Default is 2.
    - ma_type (str): The type of moving average to use ('SMA', 'EMA', 'WMA'). Default is 'EMA'.
    - column (str): Name of the column to use for calculations. Default is 'close'.

Call with:
    result = bta.archer_moving_averages_trends(df, fast_length=8, slow_length=21, ma_type='EMA')
    df['amat_long'] = result['amat_long']  # Long trend signals (1 or 0)
    df['amat_short'] = result['amat_short']  # Short trend signals (1 or 0)

Returns:
    pd.DataFrame: DataFrame with 'amat_long' and 'amat_short' columns containing the indicator values.
"""


def test():
    """
    Test function for the archer_moving_averages_trends indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the archer_moving_averages_trends indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(archer_moving_averages_trends)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 