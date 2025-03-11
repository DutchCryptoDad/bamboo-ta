# -*- coding: utf-8 -*-
# psychological_line.py

import pandas as pd
import numpy as np


def psychological_line(df: pd.DataFrame, length: int = 12, scalar: float = 100, drift: int = 1) -> pd.DataFrame:
    """Psychological Line"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains at least the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    # Calculate difference based on available columns
    if "open" in df.columns:
        # If open is available, use close - open
        diff = np.sign(df_copy["close"] - df_copy["open"])
    else:
        # Otherwise use close - previous close
        diff = np.sign(df_copy["close"].diff(drift))
    
    # Fill NA values with 0 and zero negative values
    diff = diff.fillna(0)
    diff = diff.where(diff > 0, 0)
    
    # Calculate PSL
    psl = scalar * diff.rolling(window=length).sum() / length
    
    # Add result to the DataFrame
    df_copy["psl"] = psl
    
    return df_copy[["psl"]]


psychological_line.__doc__ = \
"""
Name:
    Psychological Line

Description:
    The Psychological Line (PSL) is an oscillator-type indicator that calculates
    the percentage of bars that close higher over a given period. It measures the 
    buying pressure or market optimism by comparing the number of rising periods 
    to the total number of periods.
    
    When using the close-open mode, it calculates the percentage of bars where the 
    close is higher than the open. When using the close-close mode, it calculates 
    the percentage of bars where the close is higher than the previous close.
    
    Values range from 0 to 100. High values (typically above 70-80) indicate 
    potential overbought conditions, while low values (typically below 20-30) 
    indicate potential oversold conditions.

More info:
    https://www.quantshare.com/item-851-psychological-line

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column,
      and optionally the 'open' column.
    - length (int): The period for the calculation. Default is 12.
    - scalar (float): Multiplier for the result. Default is 100.
    - drift (int): The difference period for the close-close calculation. Default is 1.

Call with:
    df['psl'] = bta.psychological_line(df)['psl']

Returns:
    pd.DataFrame: DataFrame with 'psl' column.
"""


def test():
    """
    Test function for the psychological_line indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the psychological_line indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(psychological_line)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 