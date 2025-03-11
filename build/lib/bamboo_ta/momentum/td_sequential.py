# -*- coding: utf-8 -*-
# td_sequential.py

import pandas as pd
import numpy as np


def td_sequential(df: pd.DataFrame, asint: bool = False, show_all: bool = True) -> pd.DataFrame:
    """TD Sequential Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    close = df_copy["close"]
    
    def true_sequence_count(series: pd.Series):
        """Count the consecutive True values until the last False value"""
        # Find the index of the last False value
        index = series.where(series == False).last_valid_index()
        
        if index is None:
            # If no False values, count all True values
            return series.count()
        else:
            # Count True values after the last False
            s = series[series.index > index]
            return s.count()
    
    def calc_td(series: pd.Series, direction: str, show_all: bool):
        """Calculate TD Sequential values for a given direction"""
        # Determine if price is higher or lower than 4 periods ago
        td_bool = series.diff(4) > 0 if direction == "up" else series.diff(4) < 0
        
        # Calculate TD Sequential values
        td_num = np.where(
            td_bool, 
            td_bool.rolling(13, min_periods=0).apply(true_sequence_count), 
            0
        )
        td_num = pd.Series(td_num, index=series.index)
        
        # Filter values based on show_all parameter
        if show_all:
            td_num = td_num.mask(td_num == 0)
        else:
            td_num = td_num.mask(~td_num.between(6, 9))
        
        return td_num
    
    # Calculate TD Sequential for up and down trends
    up_seq = calc_td(close, "up", show_all)
    down_seq = calc_td(close, "down", show_all)
    
    # Convert to integers if required
    if asint:
        if up_seq.hasnans and down_seq.hasnans:
            up_seq = up_seq.fillna(0)
            down_seq = down_seq.fillna(0)
        up_seq = up_seq.astype(int)
        down_seq = down_seq.astype(int)
    
    # Add results to the DataFrame
    df_copy["td_up"] = up_seq
    df_copy["td_down"] = down_seq
    
    return df_copy[["td_up", "td_down"]]


td_sequential.__doc__ = \
"""
Name:
    TD Sequential

Description:
    Tom DeMark's Sequential indicator (TD Sequential) is a technical analysis tool 
    designed to identify potential price exhaustion points and trend reversals. 
    It counts specific price patterns to determine when a trend might be overextended.
    
    The indicator consists of two components:
    - TD Setup: A sequence of 9 consecutive closes higher (for sell setup) or 
      lower (for buy setup) than the close 4 bars earlier.
    - TD Countdown: Begins after a completed setup and identifies potential 
      exhaustion points through a 13-bar countdown process.
    
    This implementation displays the count of consecutive price bars meeting 
    the criteria for both bullish (td_up) and bearish (td_down) setups.

More info:
    https://www.tradingview.com/support/solutions/43000588817-td-sequential/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - asint (bool): If True, fills NaN values with 0 and converts to integers. Default is False.
    - show_all (bool): If True, shows all counts; if False, only shows counts between 6-9. Default is True.

Call with:
    result = bta.td_sequential(df)
    df['td_up'] = result['td_up']
    df['td_down'] = result['td_down']

Returns:
    pd.DataFrame: DataFrame with 'td_up' and 'td_down' columns.
"""


def test():
    """
    Test function for the td_sequential indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the td_sequential indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(td_sequential)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 