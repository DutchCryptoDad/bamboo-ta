# -*- coding: utf-8 -*-
# acceleration_bands.py

import pandas as pd
import numpy as np


def acceleration_bands(
    df: pd.DataFrame, length: int = 20, c: float = 4.0, ma_type: str = "SMA"
) -> pd.DataFrame:
    """Acceleration Bands (ACCBANDS)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 20
    c = float(c) if c > 0 else 4.0
    
    # Calculate high-low range and ratio
    high_low_range = df_copy["high"] - df_copy["low"]
    high_low_range = high_low_range.where(high_low_range > 0, 0.0001)  # Avoid division by zero
    hl_ratio = high_low_range / (df_copy["high"] + df_copy["low"])
    hl_ratio *= c
    
    # Calculate base values for bands
    lower_base = df_copy["low"] * (1 - hl_ratio)
    upper_base = df_copy["high"] * (1 + hl_ratio)
    
    # Apply moving average based on type
    if ma_type.upper() == "EMA":
        lower = lower_base.ewm(span=length, adjust=False).mean()
        middle = df_copy["close"].ewm(span=length, adjust=False).mean()
        upper = upper_base.ewm(span=length, adjust=False).mean()
    elif ma_type.upper() == "SMA":
        lower = lower_base.rolling(window=length).mean()
        middle = df_copy["close"].rolling(window=length).mean()
        upper = upper_base.rolling(window=length).mean()
    else:
        raise ValueError(f"Invalid ma_type: {ma_type}. Use 'EMA' or 'SMA'.")
    
    # Store results in DataFrame
    df_copy["accbands_lower"] = lower
    df_copy["accbands_middle"] = middle
    df_copy["accbands_upper"] = upper
    
    return df_copy[["accbands_lower", "accbands_middle", "accbands_upper"]]


acceleration_bands.__doc__ = \
"""
Name:
    Acceleration Bands (ACCBANDS)

Description:
    Acceleration Bands, created by Price Headley, are volatility-based envelopes
    plotted above and below a simple moving average. The bands are based on a multiple
    of the high-low range, adjusted by the sum of the high and low.
    
    The bands widen and narrow based on market volatility, providing potential
    overbought and oversold levels. They can be used to identify potential
    price targets for trending markets or potential reversal points when the price
    reaches the upper or lower bands.

More info:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/acceleration-bands-abands/
    https://library.tradingtechnologies.com/trade/chrt-ti-acceleration-bands.html

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for the moving average calculation. Default is 20.
    - c (float): The multiplier for the high-low ratio. Default is 4.0.
    - ma_type (str): The type of moving average to use ('SMA' or 'EMA'). Default is 'SMA'.

Call with:
    result = bta.acceleration_bands(df)
    df['accbands_lower'] = result['accbands_lower']
    df['accbands_middle'] = result['accbands_middle']
    df['accbands_upper'] = result['accbands_upper']

Returns:
    pd.DataFrame: DataFrame with 'accbands_lower', 'accbands_middle', and 'accbands_upper' columns.
"""


def test():
    """
    Test function for the acceleration_bands indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the acceleration_bands indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(acceleration_bands)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 