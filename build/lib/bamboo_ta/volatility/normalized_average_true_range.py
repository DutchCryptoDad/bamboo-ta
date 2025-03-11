# -*- coding: utf-8 -*-
# normalized_average_true_range.py

import pandas as pd
import numpy as np


def normalized_average_true_range(df: pd.DataFrame, length: int = 14, scalar: float = 100, column: str = "close") -> pd.DataFrame:
    """Normalized Average True Range (NATR)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 14
    scalar = float(scalar) if scalar > 0 else 100
    
    # Calculate True Range
    tr1 = df_copy["high"] - df_copy["low"]
    tr2 = abs(df_copy["high"] - df_copy["close"].shift(1))
    tr3 = abs(df_copy["low"] - df_copy["close"].shift(1))
    
    # True Range is the maximum of the three
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate ATR (Average True Range) using EMA
    atr = true_range.ewm(span=length, adjust=False).mean()
    
    # Calculate NATR by normalizing with close price
    df_copy["natr"] = scalar * atr / df_copy[column]
    
    return df_copy[["natr"]]


normalized_average_true_range.__doc__ = \
"""
Name:
    Normalized Average True Range (NATR)

Description:
    The Normalized Average True Range (NATR) is a modification of the Average True Range
    (ATR) indicator that attempts to normalize the average true range by dividing it by 
    the closing price and multiplying by a scalar (usually 100).
    
    Unlike the ATR, which is an absolute value that can vary significantly across different
    securities based on their price, the NATR expresses volatility as a percentage of the
    closing price. This makes it easier to compare volatility across different securities
    regardless of their price levels.
    
    The NATR is useful for:
    - Comparing volatility across different securities
    - Setting position sizes based on volatility
    - Identifying periods of high or low volatility

More info:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/normalized-average-true-range-natr/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for calculating ATR. Default is 14.
    - scalar (float): Multiplier to scale the result (typically 100 for percentage). Default is 100.
    - column (str): The column name to use for normalization. Default is 'close'.

Call with:
    result = bta.normalized_average_true_range(df)
    df['natr'] = result['natr']

Returns:
    pd.DataFrame: DataFrame with 'natr' column.
"""


def test():
    """
    Test function for the normalized_average_true_range indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the normalized_average_true_range indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(normalized_average_true_range)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 