# -*- coding: utf-8 -*-
# awesome_oscillator.py
import pandas as pd 

def awesome_oscillator(
    df: pd.DataFrame, 
    high_col: str = 'high', 
    low_col: str = 'low', 
    window1: int = 5, 
    window2: int = 34, 
    fillna: bool = False
) -> pd.DataFrame:
    """Awesome Oscillator (AO)"""
    df_copy = df.copy()

    median_price = 0.5 * (df_copy[high_col] + df_copy[low_col])
    min_periods_s = 0 if fillna else window1
    min_periods_l = 0 if fillna else window2

    df_copy['ao'] = (
        median_price.rolling(window1, min_periods=min_periods_s).mean()
        - median_price.rolling(window2, min_periods=min_periods_l).mean()
    )
    
    if fillna:
        df_copy['ao'] = df_copy['ao'].fillna(0)

    return df_copy[['ao']]

awesome_oscillator.__doc__ = \
"""
Name:
    Awesome Oscillator

Description:
    The Awesome Oscillator is a momentum indicator used to measure market momentum.
    It is calculated by subtracting a 34-period simple moving average (SMA) of the
    median price from a 5-period SMA of the median price.

More info:
    https://www.investopedia.com/terms/a/awesomeoscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing 'high' and 'low' columns.
    - high_col (str): The name of the 'high' column. Default is 'high'.
    - low_col (str): The name of the 'low' column. Default is 'low'.
    - window1 (int, optional): Short period. Default is 5.
    - window2 (int, optional): Long period. Default is 34.
    - fillna (bool, optional): If True, fill nan values with 0. Default is False.

Call with:
    df['ao'] = bta.awesome_oscillator(df, 'high', 'low', 5, 34)['ao']

Returns:
    pd.DataFrame: DataFrame with the 'ao' column.
"""


def test():
    """
    Test function for the awesome_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the awesome_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(awesome_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
