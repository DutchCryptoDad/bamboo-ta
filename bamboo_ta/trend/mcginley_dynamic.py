# -*- coding: utf-8 -*-
# mcginley_dynamic.py

import pandas as pd
import numpy as np


def mcginley_dynamic(df: pd.DataFrame, length: int = 10, constant: float = 1.0, 
                   column: str = "close") -> pd.DataFrame:
    """McGinley Dynamic Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Extract the series we'll be working with
    series = df_copy[column]
    
    # Validate parameters
    length = int(length) if length > 0 else 10
    constant = float(constant) if 0 < constant <= 1 else 1.0
    
    # Initialize result series
    mcgd = pd.Series(np.nan, index=series.index)
    
    # Set first value equal to the first price
    mcgd.iloc[0] = series.iloc[0]
    
    # Calculate McGinley Dynamic
    for i in range(1, len(series)):
        denom = constant * length * (series.iloc[i] / mcgd.iloc[i-1]) ** 4
        mcgd.iloc[i] = mcgd.iloc[i-1] + ((series.iloc[i] - mcgd.iloc[i-1]) / denom)
    
    # Add result to DataFrame
    df_copy["mcgd"] = mcgd
    
    return df_copy[["mcgd"]]


mcginley_dynamic.__doc__ = \
"""
Name:
    McGinley Dynamic Indicator

Description:
    The McGinley Dynamic indicator was developed by John R. McGinley, a Certified Market
    Technician, as an improved moving average that minimizes price separation, reduces
    whipsaws, and hugs prices more closely than traditional moving averages.
    
    What makes the McGinley Dynamic unique is its adaptive nature. It speeds up in downtrends
    to follow prices more closely, yet moves more slowly in uptrends. This is achieved by
    incorporating a dynamic smoothing factor that adjusts based on the relationship between
    the current price and the indicator's previous value.
    
    The constant parameter allows for additional fine-tuning, with lower values (e.g., 0.6)
    making the indicator more responsive to price changes.

More info:
    https://www.investopedia.com/articles/forex/09/mcginley-dynamic-indicator.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:mcginley_dynamic

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the calculation. Default is 10.
    - constant (float): Multiplier for the denominator, sometimes set to 0.6 for more
      responsiveness. Default is 1.0.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.mcginley_dynamic(df)
    df['mcgd'] = result['mcgd']

Returns:
    pd.DataFrame: DataFrame with 'mcgd' column.
"""


def test():
    """
    Test function for the mcginley_dynamic indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the mcginley_dynamic indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(mcginley_dynamic)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 