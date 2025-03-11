# -*- coding: utf-8 -*-
# cross_signals.py

import pandas as pd
import numpy as np


def cross_signals(
    df: pd.DataFrame,
    signal_column: str,
    level_a: float,
    level_b: float,
    above: bool = True,
    long: bool = True,
    as_bool: bool = False,
    trade_offset: int = 0
) -> pd.DataFrame:
    """Cross Signals Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if signal_column not in df.columns:
        raise KeyError(f"DataFrame must contain '{signal_column}' column")
    
    # Validate parameters
    above = bool(above)
    long = bool(long)
    as_bool = bool(as_bool)
    trade_offset = int(trade_offset) if trade_offset != 0 else 0
    
    # Get the signal series
    signal = df_copy[signal_column]
    
    # Helper function to identify crossovers
    def cross_value(series, value, direction=True):
        """
        Identify where a series crosses a value.
        
        Args:
            series: The data series
            value: The threshold value
            direction: True for crossover (series crosses above value), 
                       False for crossunder (series crosses below value)
        
        Returns:
            Series containing 1 where crossover/under occurs, otherwise 0
        """
        if direction:
            # Crossover (series crosses above value)
            cross = ((series.shift(1) <= value) & (series > value)).astype(int)
        else:
            # Crossunder (series crosses below value)
            cross = ((series.shift(1) >= value) & (series < value)).astype(int)
        return cross
    
    # Calculate entries and exits based on crossovers/crossunders
    if above:
        # Mode 1: Signal crosses above level_a (entry) and below level_b (exit)
        entries = cross_value(signal, level_a, direction=True)  # Cross above level_a
        exits = -cross_value(signal, level_b, direction=False)  # Cross below level_b
    else:
        # Mode 2: Signal crosses below level_a (entry) and above level_b (exit)
        entries = cross_value(signal, level_a, direction=False)  # Cross below level_a
        exits = -cross_value(signal, level_b, direction=True)  # Cross above level_b
    
    # Combine entries and exits
    trades = entries + exits
    
    # Fill gaps for trend determination
    trades_filled = trades.replace({0: np.nan})
    trades_filled = trades_filled.ffill()
    trades_filled = trades_filled.fillna(0)
    
    # Determine the trend (1 for in trend, 0 for not in trend)
    trends = (trades_filled > 0).astype(int)
    
    # Handle short trends if requested
    if not long:
        trends = 1 - trends
    
    # Create temporary column for the trend
    trend_col = "__temp_trend"
    df_copy[trend_col] = trends
    
    # Use trend_signals to generate the final signals
    try:
        from bamboo_ta.trend.trend_signals import trend_signals
        
        # Apply trend_signals
        result = trend_signals(
            df=df_copy,
            trend_column=trend_col,
            as_bool=as_bool,
            trade_offset=trade_offset,
            drift=1
        )
        
        # Rename columns for clarity
        result = result.rename(columns={
            "trend": "cross_trend",
            "trades": "cross_trades",
            "entries": "cross_entries",
            "exits": "cross_exits"
        })
        
        # Also add long and short trends
        if as_bool:
            result["cross_long"] = result["cross_trend"]
            result["cross_short"] = ~result["cross_trend"]
        else:
            result["cross_long"] = result["cross_trend"]
            result["cross_short"] = 1 - result["cross_trend"]
        
        # Remove temporary column
        result = result.drop(trend_col, axis=1, errors='ignore')
        
        return result[["cross_trend", "cross_trades", "cross_entries", "cross_exits", "cross_long", "cross_short"]]
        
    except ImportError:
        # If trend_signals is not available, do a simplified calculation
        print("Warning: trend_signals not available, using simplified calculation")
        
        # Calculate trades, entries and exits directly
        trades = trends.diff().shift(trade_offset).fillna(0).astype(int)
        entries = (trades > 0).astype(int)
        exits = (trades < 0).abs().astype(int)
        
        # Convert to boolean if requested
        if as_bool:
            trends = trends.astype(bool)
            entries = entries.astype(bool)
            exits = exits.astype(bool)
            long_trends = trends
            short_trends = ~trends
        else:
            long_trends = trends
            short_trends = 1 - trends
        
        # Store results in DataFrame
        df_copy["cross_trend"] = trends
        df_copy["cross_trades"] = trades
        df_copy["cross_entries"] = entries
        df_copy["cross_exits"] = exits
        df_copy["cross_long"] = long_trends
        df_copy["cross_short"] = short_trends
        
        # Remove temporary column
        df_copy = df_copy.drop(trend_col, axis=1, errors='ignore')
        
        return df_copy[["cross_trend", "cross_trades", "cross_entries", "cross_exits", "cross_long", "cross_short"]]


cross_signals.__doc__ = \
"""
Name:
    Cross Signals

Description:
    Cross Signals generates trading signals based on a signal series crossing specific levels.
    It returns the trend, trades, entries, and exits as a set of columns that can be used 
    for analysis or trading signal generation.
    
    The indicator has two primary modes controlled by the 'above' parameter:
    - When above=True (default): Generates entry signals when the signal crosses above level_a,
      and exit signals when it crosses below level_b.
    - When above=False: Generates entry signals when the signal crosses below level_a,
      and exit signals when it crosses above level_b.
    
    This is particularly useful for oscillators like RSI, Stochastic, or Z-Score where
    crossing specific thresholds can indicate potential trade opportunities.
    
    The 'long' parameter determines whether to interpret the signals as long positions (true)
    or short positions (false).

More info:
    N/A (Original implementation by Kevin Johnson for Pandas TA)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified signal column.
    - signal_column (str): Name of the column containing the signal series to evaluate.
    - level_a (float): The first threshold level for generating entry signals.
    - level_b (float): The second threshold level for generating exit signals.
    - above (bool): Determines the signal crossing mode. Default is True.
    - long (bool): Whether to interpret signals as long positions. When False,
      interprets signals as short positions. Default is True.
    - as_bool (bool): If True, converts the trends, entries, and exits to boolean values.
      Default is False.
    - trade_offset (int): Value used to shift the trade entries/exits. Use 1 for backtesting
      and 0 for live trading. Default is 0.

Call with:
    # Example for RSI crossing above 30 (entry) and below 70 (exit)
    result = bta.cross_signals(df, signal_column='rsi', level_a=30, level_b=70, above=True)
    df['cross_trend'] = result['cross_trend']
    df['cross_entries'] = result['cross_entries']
    df['cross_exits'] = result['cross_exits']
    df['cross_long'] = result['cross_long']
    df['cross_short'] = result['cross_short']

Returns:
    pd.DataFrame: DataFrame with 'cross_trend', 'cross_trades', 'cross_entries', 'cross_exits',
    'cross_long', and 'cross_short' columns.
"""


def test():
    """
    Test function for the cross_signals indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the cross_signals indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(cross_signals)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 