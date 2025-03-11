# -*- coding: utf-8 -*-
# arnaud_legoux_moving_average.py

import pandas as pd
import numpy as np


def arnaud_legoux_moving_average(df: pd.DataFrame, length: int = 10, sigma: float = 6.0, 
                              distribution_offset: float = 0.85, column: str = "close") -> pd.DataFrame:
    """Arnaud Legoux Moving Average (ALMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Pre-calculations
    m = distribution_offset * (length - 1)  # Center of the Gaussian distribution
    s = length / sigma  # Standard deviation of the Gaussian distribution
    
    # Calculate Gaussian weights
    weights = np.zeros(length)
    for i in range(length):
        weights[i] = np.exp(-1 * ((i - m) ** 2) / (2 * s ** 2))
    
    # Normalize weights to sum to 1
    weights = weights / weights.sum()
    
    # Initialize result series
    alma = pd.Series(np.nan, index=series.index)
    
    # Calculate ALMA
    for i in range(length - 1, len(series)):
        window = series.iloc[i - length + 1 : i + 1].values
        
        # Reverse window to match the implementation in the original code
        window = window[::-1]
        
        # Calculate weighted sum
        alma.iloc[i] = np.sum(window * weights)
    
    # Add result to DataFrame
    df_copy["alma"] = alma
    
    return df_copy[["alma"]]


arnaud_legoux_moving_average.__doc__ = \
"""
Name:
    Arnaud Legoux Moving Average (ALMA)

Description:
    The Arnaud Legoux Moving Average (ALMA) was developed by Arnaud Legoux and Dimitrios Kouzis-Loukas.
    It uses the curve of the Normal (Gaussian) distribution to create a moving average with reduced lag
    while maintaining smoothness to filter out market noise.
    
    ALMA applies a Gaussian distribution curve across the moving average period, which can be shifted
    (using distribution_offset) to control the balance between smoothness and responsiveness. The sigma
    parameter controls the shape of the curve and the overall smoothness.
    
    This moving average excels at reducing the lag typically associated with traditional moving averages
    while still providing effective noise reduction.

More info:
    https://medium.com/analytics-vidhya/arnaud-legoux-moving-average-alma-7e1f35fc0b8e
    https://www.prorealcode.com/prorealtime-indicators/alma-arnaud-legoux-moving-average/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the ALMA calculation. Default is 10.
    - sigma (float): Controls the smoothness of the curve. Higher values = smoother. Default is 6.0.
    - distribution_offset (float): Controls the shape symmetry of the curve. 
      Range is 0-1, where 0 gives more smoothing and 1 provides more responsiveness. Default is 0.85.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.arnaud_legoux_moving_average(df)
    df['alma'] = result['alma']

Returns:
    pd.DataFrame: DataFrame with 'alma' column.
"""


def test():
    """
    Test function for the arnaud_legoux_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the arnaud_legoux_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(arnaud_legoux_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 