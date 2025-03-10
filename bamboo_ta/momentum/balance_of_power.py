# -*- coding: utf-8 -*-
# balance_of_power.py

import pandas as pd
import numpy as np


def balance_of_power(df: pd.DataFrame, scalar: float = 1.0) -> pd.DataFrame:
    """Balance of Power"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate non-zero high-low range to avoid division by zero
    high_low_range = df_copy["high"] - df_copy["low"]
    high_low_range = high_low_range.replace(0, np.nan)  # Replace zeros with NaN to avoid division by zero
    
    # Calculate close-open range
    close_open_range = df_copy["close"] - df_copy["open"]
    
    # Calculate Balance of Power
    df_copy["bop"] = scalar * close_open_range / high_low_range
    
    return df_copy[["bop"]]


balance_of_power.__doc__ = \
"""
Name:
    Balance of Power

Description:
    The Balance of Power (BOP) indicator measures the strength of buyers vs sellers
    by assessing the ability of each to push price to an extreme level. It is calculated
    by comparing the close and open prices relative to the high and low prices.
    
    Positive BOP values indicate buying pressure, while negative values indicate
    selling pressure. A zero line crossing can signal a potential shift in control
    between buyers and sellers.

More info:
    http://www.worden.com/TeleChartHelp/Content/Indicators/Balance_of_Power.htm

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low',
      and 'close' columns.
    - scalar (float): Factor to magnify the values. Default is 1.0.

Call with:
    df['bop'] = bta.balance_of_power(df)['bop']

For Signal line:
    df['bop_signal'] = df['bop'].rolling(window=14).mean()  # Using SMA for signal

Returns:
    pd.DataFrame: DataFrame with 'bop' column.
"""


def test():
    """
    Test function for the balance_of_power indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the balance_of_power indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(balance_of_power)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 