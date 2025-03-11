# -*- coding: utf-8 -*-
# price_volume.py

import pandas as pd
import numpy as np


def price_volume(df: pd.DataFrame, signed: bool = False, column: str = "close") -> pd.DataFrame:
    """Price-Volume (PVOL)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = [column, "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate price volume
    pvol = df_copy[column] * df_copy["volume"]
    
    # Apply sign if requested
    if signed:
        # Calculate price change direction
        price_change = df_copy[column].diff()
        sign = np.where(price_change >= 0, 1, -1)
        pvol = pvol * sign
    
    # Add result to DataFrame
    df_copy["pvol"] = pvol
    
    return df_copy[["pvol"]]


price_volume.__doc__ = \
"""
Name:
    Price-Volume (PVOL)

Description:
    The Price-Volume indicator is a simple measure that calculates the product of price 
    and volume. This gives a measure of the monetary value of transactions at each time period.
    
    When the 'signed' parameter is set to True, the indicator also takes into account 
    the direction of price movement, multiplying by +1 for price increases and -1 for 
    price decreases, which can help identify buying and selling pressure.

More info:
    https://www.investopedia.com/articles/technical/02/082702.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain specified price column and 'volume' column.
    - signed (bool): Whether to apply the sign of price changes to the result. Default is False.
    - column (str): The price column to use for calculations. Default is 'close'.

Call with:
    result = bta.price_volume(df)
    df['pvol'] = result['pvol']

Returns:
    pd.DataFrame: DataFrame with 'pvol' column.
"""


def test():
    """
    Test function for the price_volume indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the price_volume indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(price_volume)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 