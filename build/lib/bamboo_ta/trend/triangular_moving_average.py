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
    
    # Validate parameters
    length = int(length) if length > 0 else 10
    
    # Calculate half length
    half_length = round(0.5 * (length + 1))
    
    # Calculate first SMA
    sma1 = df_copy[column].rolling(window=half_length).mean()
    
    # Calculate TRIMA (SMA of the first SMA)
    trima = sma1.rolling(window=half_length).mean()
    
    # Add result to DataFrame
    df_copy["trima"] = trima
    
    return df_copy[["trima"]]


triangular_moving_average.__doc__ = \
"""
Name:
    Triangular Moving Average (TRIMA)

Description:
    A Triangular Moving Average (TRIMA) is a weighted moving average where the weights
    form a triangular pattern, with the greatest weight given to the middle of the period.
    This is accomplished by calculating a Simple Moving Average (SMA) of another SMA.
    
    The TRIMA provides a smoother representation of price action compared to a standard
    Simple Moving Average, making it useful for identifying the underlying trend while
    filtering out short-term price fluctuations and noise.

More info:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triangular-moving-average-trima/
    https://www.investopedia.com/terms/t/triangularMovingAverage.asp

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