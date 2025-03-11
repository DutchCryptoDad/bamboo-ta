# -*- coding: utf-8 -*-
# percentage_distance.py

import pandas as pd
import numpy as np


def percentage_distance(df: pd.DataFrame, drift: int = 1) -> pd.DataFrame:
    """Price Distance (PDIST)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    drift = int(drift) if drift > 0 else 1
    
    # Calculate non-zero ranges
    high_low_range = np.maximum(df_copy["high"] - df_copy["low"], 0.0001)  # Avoid zero values
    open_close_range = np.abs(df_copy["open"] - df_copy["close"])
    open_close_shifted_range = np.abs(df_copy["open"] - df_copy["close"].shift(drift))
    
    # Calculate Price Distance
    df_copy["pdist"] = 2 * high_low_range + open_close_shifted_range - open_close_range
    
    return df_copy[["pdist"]]


percentage_distance.__doc__ = \
"""
Name:
    Price Distance (PDIST)

Description:
    The Price Distance indicator measures the "distance" covered by price movements.
    It considers not only the high-low range, but also the relationship between opening
    and closing prices, both current and from a previous period (drift).
    
    This indicator is useful for analyzing volatility and understanding the magnitude
    of price movements within a given period. High PDIST values indicate more significant
    price movement or volatility, while low values indicate more stable or range-bound
    price action.
    
    The calculation weighs the high-low range more heavily (multiplier of 2) to emphasize
    the overall range of the period.

More info:
    https://www.prorealcode.com/prorealtime-indicators/pricedistance/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low', and 'close' columns.
    - drift (int): The difference period for comparing with previous closes. Default is 1.

Call with:
    result = bta.percentage_distance(df)
    df['pdist'] = result['pdist']

Returns:
    pd.DataFrame: DataFrame with 'pdist' column.
"""


def test():
    """
    Test function for the percentage_distance indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the percentage_distance indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(percentage_distance)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 