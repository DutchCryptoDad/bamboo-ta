# -*- coding: utf-8 -*-
# trend_signals.py

import pandas as pd
import numpy as np


def trend_signals(
    df: pd.DataFrame,
    trend_column: str,
    as_bool: bool = False,
    trade_offset: int = 0,
    drift: int = 1
) -> pd.DataFrame:
    """Trend Signals Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if trend_column not in df.columns:
        raise KeyError(f"DataFrame must contain '{trend_column}' column")
    
    # Validate parameters
    as_bool = bool(as_bool)
    trade_offset = int(trade_offset) if trade_offset != 0 else 0
    drift = int(drift) if drift > 0 else 1
    
    # Get the trend series
    trend = df_copy[trend_column].astype(int)
    
    # Calculate trades, entries, and exits
    trades = trend.diff(drift).shift(trade_offset).fillna(0).astype(int)
    entries = (trades > 0).astype(int)
    exits = (trades < 0).abs().astype(int)
    
    # Convert to boolean if requested
    if as_bool:
        trend = trend.astype(bool)
        entries = entries.astype(bool)
        exits = exits.astype(bool)
    
    # Store results in DataFrame
    df_copy["trend"] = trend
    df_copy["trades"] = trades
    df_copy["entries"] = entries
    df_copy["exits"] = exits
    
    return df_copy[["trend", "trades", "entries", "exits"]]


trend_signals.__doc__ = \
"""
Name:
    Trend Signals

Description:
    Given a trend column, Trend Signals returns the trend, trades, entries, and exits
    as a set of columns that can be used for analysis or trading signal generation.
    
    A trend can be as simple as a boolean series where True represents an uptrend
    (e.g., 'close' > 'moving average'), or something more complex that results in
    a boolean or integer (0 or 1) series.
    
    This indicator is particularly useful for converting technical indicators or
    conditions into actionable trading signals. When 'as_bool=True', it returns
    trend, entries, and exits as boolean values, which can be helpful for backtesting.
    
    The function calculates:
    - trend: The input trend (0 or 1, or True/False if as_bool=True)
    - trades: Change in trend (1 for entry, -1 for exit, 0 otherwise)
    - entries: Points where trades change to positive (1 or True, 0 or False otherwise)
    - exits: Points where trades change to negative (1 or True, 0 or False otherwise)

More info:
    N/A (Original implementation by Kevin Johnson for Pandas TA)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified trend column.
    - trend_column (str): Name of the column containing the trend values (must be 0/1 or True/False).
    - as_bool (bool): If True, converts the trend, entries, and exits to boolean values. Default is False.
    - trade_offset (int): Value used to shift the trade entries/exits. Use 1 for backtesting 
      and 0 for live trading. Default is 0.
    - drift (int): The difference period for calculating changes in trend. Default is 1.

Call with:
    # Assuming you have a DataFrame with a trend column (e.g., 'sma_trend' = close > sma)
    result = bta.trend_signals(df, trend_column='sma_trend', as_bool=False)
    df['trend'] = result['trend']  # The trend (0 or 1)
    df['trades'] = result['trades']  # Trade signals (1: entry, -1: exit, 0: no change)
    df['entries'] = result['entries']  # Entry points (1 or 0)
    df['exits'] = result['exits']  # Exit points (1 or 0)

Returns:
    pd.DataFrame: DataFrame with 'trend', 'trades', 'entries', and 'exits' columns.
"""


def test():
    """
    Test function for the trend_signals indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the trend_signals indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(trend_signals)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 