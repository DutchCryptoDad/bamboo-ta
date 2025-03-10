# -*- coding: utf-8 -*-
# triangular_moving_average.py

import pandas as pd
import numpy as np


def triangular_moving_average(df: pd.DataFrame, length: int = 10, 
                           column: str = "close") -> pd.DataFrame:
    """Triangular Moving Average (TRIMA)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Calculate half-length for triangular weighting
    half_length = round(0.5 * (length + 1))
    
    # Calculate first SMA
    sma1 = df_copy[column].rolling(window=half_length).mean()
    
    # Calculate final TRIMA (SMA of first SMA)
    trima = sma1.rolling(window=half_length).mean()
    
    # Add result to DataFrame
    df_copy["trima"] = trima
    
    return df_copy[["trima"]]


triangular_moving_average.__doc__ = \
"""
Name:
    Triangular Moving Average (TRIMA)

Description:
    The Triangular Moving Average (TRIMA) is a weighted moving average where the weights 
    form a triangular pattern, with the greatest weight given to the middle of the period.
    
    Unlike a simple moving average where all data points are weighted equally, or an 
    exponential moving average where more recent data points are weighted more heavily,
    the TRIMA gives more weight to the middle of the period. This results in a smoother
    moving average with reduced lag compared to a simple moving average.
    
    The TRIMA is essentially a double-smoothed simple moving average, calculated by
    taking a simple moving average of a simple moving average.

More info:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/triangular-ma
    https://www.tradingview.com/support/solutions/43000502589/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the TRIMA calculation. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.triangular_moving_average(df)
    df['trima'] = result['trima']

Returns:
    pd.DataFrame: DataFrame with 'trima' column.
"""


def test():
    """
    Test function for the triangular_moving_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the triangular_moving_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(triangular_moving_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 