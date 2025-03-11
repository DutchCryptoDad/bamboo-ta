# -*- coding: utf-8 -*-
# mass_index.py

import pandas as pd
import numpy as np


def mass_index(df: pd.DataFrame, fast_length: int = 9, slow_length: int = 25) -> pd.DataFrame:
    """Mass Index (MASSI)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    fast_length = int(fast_length) if fast_length > 0 else 9
    slow_length = int(slow_length) if slow_length > 0 else 25
    
    # Swap if necessary
    if slow_length < fast_length:
        fast_length, slow_length = slow_length, fast_length
    
    # Calculate high-low range
    high_low_range = df_copy["high"] - df_copy["low"]
    
    # First EMA of high-low range
    hl_ema1 = high_low_range.ewm(span=fast_length, adjust=False).mean()
    
    # Second EMA (EMA of the first EMA)
    hl_ema2 = hl_ema1.ewm(span=fast_length, adjust=False).mean()
    
    # Calculate ratio
    hl_ratio = hl_ema1 / hl_ema2
    
    # Sum the ratio over the slow period
    df_copy["mass_index"] = hl_ratio.rolling(window=slow_length, min_periods=slow_length).sum()
    
    return df_copy[["mass_index"]]


mass_index.__doc__ = \
"""
Name:
    Mass Index (MASSI)

Description:
    The Mass Index is a non-directional volatility indicator that utilizes the
    High-Low Range to identify trend reversals based on range expansions.
    
    Unlike many other technical indicators, the Mass Index doesn't follow price
    direction but instead identifies reversals by tracking changes in the range 
    between high and low prices. A Mass Index above 27 followed by a drop below 
    26.5 is often considered a "reversal bulge" signaling a potential trend change.
    
    The indicator is based on the idea that reversals are often preceded by 
    widening ranges as volatility increases, followed by narrowing ranges as 
    the market prepares to reverse.

More info:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:mass_index

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - fast_length (int): The period for the first and second EMA calculations. Default is 9.
    - slow_length (int): The period for summing the EMA ratio. Default is 25.

Call with:
    result = bta.mass_index(df)
    df['mass_index'] = result['mass_index']

Returns:
    pd.DataFrame: DataFrame with 'mass_index' column.
"""


def test():
    """
    Test function for the mass_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the mass_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(mass_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 