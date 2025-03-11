# -*- coding: utf-8 -*-
# increasing.py

import pandas as pd
import numpy as np


def increasing(
    df: pd.DataFrame,
    length: int = 1,
    strict: bool = False,
    as_int: bool = True,
    percent: float = None,
    drift: int = 1,
    column: str = "close"
) -> pd.DataFrame:
    """Increasing Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 1
    drift = int(drift) if drift > 0 else 1
    
    # Get price series
    close = df_copy[column]
    
    # Apply percentage adjustment if specified
    if percent is not None and percent > 0:
        close_adjusted = (1 + 0.01 * percent) * close
    else:
        close_adjusted = close
        percent = None
    
    # Calculate increasing condition
    if strict:
        # Check if strictly increasing over the entire period
        increasing_series = close > close_adjusted.shift(drift)
        
        # Add additional conditions for strict increasing
        for i in range(2, length + 1):
            increasing_series = increasing_series & (close.shift(i - 1 - drift) > close_adjusted.shift(i - drift))
        
        # Fill NaN values
        increasing_series = increasing_series.fillna(False)
    else:
        # Simple check if current value is greater than value 'length' periods ago
        increasing_series = close.diff(length) > 0
    
    # Convert to integer if specified
    if as_int:
        increasing_series = increasing_series.astype(int)
    
    # Add result to DataFrame with appropriate naming
    percent_suffix = f"_{percent}pct" if percent is not None else ""
    strict_prefix = "strict_" if strict else ""
    df_copy[f"{strict_prefix}increasing{percent_suffix}"] = increasing_series
    
    # Return the result
    return df_copy[[f"{strict_prefix}increasing{percent_suffix}"]]


increasing.__doc__ = \
"""
Name:
    Increasing Indicator

Description:
    The Increasing indicator identifies when a series is increasing over a specified period.
    It returns True (or 1) if the series is increasing, and False (or 0) otherwise.
    
    The indicator has two modes:
    - Standard: Returns True if the current value is greater than the value 'length' periods ago
    - Strict: Returns True only if the series has been continuously increasing over the entire period
    
    Additionally, a percentage parameter can be used to adjust the comparison threshold,
    allowing for a more flexible definition of what constitutes "increasing."
    
    This indicator is useful for identifying uptrends, determining when to exit short positions,
    or finding potential entry points for long positions.

More info:
    None

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The lookback period for comparison. Default is 1.
    - strict (bool): If True, checks if the series is continuously increasing over the period. Default is False.
    - as_int (bool): If True, returns the result as integers (1 for True, 0 for False). Default is True.
    - percent (float): Optional percentage threshold adjustment. Default is None.
    - drift (int): The lag period for comparison in strict mode. Default is 1.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Standard increasing check
    result = bta.increasing(df)
    df['increasing'] = result['increasing']
    
    # Strict increasing check with longer period
    result = bta.increasing(df, length=5, strict=True)
    df['strict_increasing'] = result['strict_increasing']
    
    # Increasing with percentage threshold
    result = bta.increasing(df, percent=1.5)
    df['increasing_1.5pct'] = result['increasing_1.5pct']

Returns:
    pd.DataFrame: DataFrame with a column indicating increasing status (name varies based on parameters).
"""


def test():
    """
    Test function for the increasing indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the increasing indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(increasing)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 