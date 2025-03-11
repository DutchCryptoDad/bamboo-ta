# -*- coding: utf-8 -*-
# decreasing.py

import pandas as pd
import numpy as np


def decreasing(
    df: pd.DataFrame,
    length: int = 1,
    strict: bool = False,
    as_int: bool = True,
    percent: float = None,
    drift: int = 1,
    column: str = "close"
) -> pd.DataFrame:
    """Decreasing Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 1
    strict = bool(strict)
    as_int = bool(as_int)
    drift = int(drift) if drift > 0 else 1
    
    # Get the series to check
    close = df_copy[column]
    
    # Apply percentage adjustment if specified
    if percent is not None and percent > 0:
        close_adjusted = (1 - 0.01 * percent) * close
    else:
        close_adjusted = close
    
    # Calculate the decreasing condition
    if strict:
        # Initialize with the first condition
        decreasing = close < close_adjusted.shift(drift)
        
        # Add additional conditions for each period in the length
        for i in range(2, length + 1):
            prev_idx = i - (drift + 1)
            curr_idx = i - drift
            decreasing = decreasing & (close.shift(prev_idx) < close_adjusted.shift(curr_idx))
        
        # Fill NaN values with False
        decreasing = decreasing.fillna(False)
    else:
        # Simple check if the series has decreased over the entire length
        decreasing = close_adjusted.diff(length) < 0
    
    # Convert to int if requested
    if as_int:
        decreasing = decreasing.astype(int)
    
    # Store results in DataFrame
    df_copy["decreasing"] = decreasing
    
    return df_copy[["decreasing"]]


decreasing.__doc__ = \
"""
Name:
    Decreasing Indicator

Description:
    The Decreasing indicator identifies whether a series is decreasing over a specified period.
    It returns True (or 1 if as_int=True) if the series is decreasing, False (or 0) otherwise.
    
    When strict=True, it checks if the series is continuously decreasing over each period
    within the specified length. When strict=False (default), it simply checks if the
    value has decreased over the entire length period.
    
    The percent parameter allows for a percentage-based adjustment to the series, which
    can be useful for filtering out minor fluctuations.
    
    This indicator can be useful for trend identification, filtering trading signals,
    or as a component in more complex trading strategies.

More info:
    N/A (Original implementation by Kevin Johnson for Pandas TA)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The period over which to check for decreasing values. Default is 1.
    - strict (bool): If True, checks if the series is continuously decreasing over each
      period within the length. Default is False.
    - as_int (bool): If True, returns 1 for decreasing, 0 otherwise. If False, returns
      boolean values. Default is True.
    - percent (float): Percentage adjustment to apply to the series. If specified, compares
      against (1 - 0.01 * percent) * series. Default is None.
    - drift (int): The difference period for comparison. Default is 1.
    - column (str): Name of the column to check. Default is 'close'.

Call with:
    result = bta.decreasing(df, length=5, strict=True)
    df['decreasing'] = result['decreasing']

Returns:
    pd.DataFrame: DataFrame with 'decreasing' column containing the indicator values.
"""


def test():
    """
    Test function for the decreasing indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the decreasing indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(decreasing)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 