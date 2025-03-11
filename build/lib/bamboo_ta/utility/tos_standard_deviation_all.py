# -*- coding: utf-8 -*-
# tos_standard_deviation_all.py

import pandas as pd
import numpy as np


def tos_standard_deviation_all(
    df: pd.DataFrame,
    length: int = None,
    stds: list = None,
    ddof: int = 1,
    column: str = "close"
) -> pd.DataFrame:
    """TD Ameritrade's Think or Swim Standard Deviation All Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    if stds is None:
        stds = [1, 2, 3]
    elif not isinstance(stds, list) or len(stds) == 0:
        raise ValueError("stds must be a non-empty list")
    
    # Ensure stds are positive and in ascending order
    if min(stds) <= 0:
        raise ValueError("All standard deviations must be positive")
    
    # Sort stds in ascending order
    stds = sorted(stds)
    
    # Validate ddof
    if not isinstance(ddof, int) or ddof < 0:
        raise ValueError("ddof must be a non-negative integer")
    
    # Set up result DataFrame
    result = pd.DataFrame(index=df.index)
    
    # Determine the calculation length
    if length is None:
        # Use all available data
        calc_df = df_copy
        prop_name = "TOS_STDEVALL"
    else:
        # Validate length
        if not isinstance(length, int) or length <= 2:
            length = 30
        
        # Use only the specified length of data
        calc_df = df_copy.iloc[-length:]
        prop_name = f"TOS_STDEVALL_{length}"
    
    # Extract price series
    price = calc_df[column]
    
    # Create X indices for linear regression
    if isinstance(calc_df.index, pd.DatetimeIndex):
        X = np.arange(len(price))
    else:
        X = np.arange(len(price))
    
    # Calculate linear regression
    m, b = np.polyfit(X, price.values, 1)
    lr = pd.Series(m * X + b, index=price.index)
    
    # Calculate standard deviation
    stdev_val = np.std(price.values, ddof=ddof)
    
    # Set up result DataFrame with the linear regression line
    result[f"{prop_name}_LR"] = np.nan
    result.loc[lr.index, f"{prop_name}_LR"] = lr
    
    # Create upper and lower bands for each standard deviation level
    for i in stds:
        lower_col = f"{prop_name}_L_{i}"
        upper_col = f"{prop_name}_U_{i}"
        
        result[lower_col] = np.nan
        result[upper_col] = np.nan
        
        result.loc[lr.index, lower_col] = lr - i * stdev_val
        result.loc[lr.index, upper_col] = lr + i * stdev_val
    
    # Create a list of column names to return
    cols = [f"{prop_name}_LR"]
    for i in stds:
        cols.append(f"{prop_name}_L_{i}")
        cols.append(f"{prop_name}_U_{i}")
    
    return result[cols]


tos_standard_deviation_all.__doc__ = """
Name:
    TD Ameritrade's Think or Swim Standard Deviation All

Description:
    A port of TD Ameritrade's Think or Swim Standard Deviation All indicator which
    returns the standard deviation of data for the entire plot or for the interval
    of the last bars defined by the length parameter.
    
    This indicator creates a linear regression line along with upper and lower bands
    at specified standard deviation levels. It can be used to identify potential
    price targets and areas of support and resistance.

More info:
    https://tlc.thinkorswim.com/center/reference/thinkScript/Functions/Statistical/StDevAll

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int, optional): Number of bars from current bar to use for calculations.
      If None, all available data is used. Default is None.
    - stds (list, optional): List of Standard Deviations in ascending order from the
      central Linear Regression line. Default is [1, 2, 3].
    - ddof (int): Delta Degrees of Freedom. The divisor used in calculations is N - ddof,
      where N represents the number of elements. Default is 1.
    - column (str): The column to calculate on. Default is 'close'.

Call with:
    tos_sd = bta.tos_standard_deviation_all(df)
    df['tos_lr'] = tos_sd['TOS_STDEVALL_LR']
    df['tos_lower_1'] = tos_sd['TOS_STDEVALL_L_1']
    df['tos_upper_1'] = tos_sd['TOS_STDEVALL_U_1']
    # ...and so on for other bands

Returns:
    pd.DataFrame: DataFrame with columns for the central linear regression line and
    pairs of lower and upper bands based on multiples of the standard deviation.
"""


def test():
    """
    Test function for the tos_standard_deviation_all indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the tos_standard_deviation_all indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(tos_standard_deviation_all)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 