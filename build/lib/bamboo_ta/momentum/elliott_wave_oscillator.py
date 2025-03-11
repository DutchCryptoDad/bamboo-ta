# -*- coding: utf-8 -*-
# elliott_wave_oscillator.py

import pandas as pd


def elliott_wave_oscillator(
    df: pd.DataFrame, 
    column: str = 'close', 
    sma1_period: int = 5, 
    sma2_period: int = 35
) -> pd.DataFrame:
    """Elliott Wave Oscillator"""
 
    df_copy = df.copy()

    sma1 = df[column].rolling(window=sma1_period).mean()
    sma2 = df[column].rolling(window=sma2_period).mean()
    
    df_copy['ewo'] = ((sma1 - sma2) / df[column] * 100)

    return df_copy[['ewo']]

elliott_wave_oscillator.__doc__ = \
"""
Name:
    Elliott Wave Oscillator

Description:
    The Elliott Wave Oscillator (EWO) is a tool to help identify the trend and 
    overall market pattern, assisting in finding future trading opportunities.
    It is derived by calculating the difference between a short and long period 
    simple moving average, then normalizing the result with the close price.

More info:
    https://www.investopedia.com/terms/e/elliottwavetheory.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the 
      column specified.
    - column (str): The column on which EWO is to be calculated. Default is 'close'.
    - sma1_period (int): The period for the shorter SMA used in EWO calculation. 
      Default is 5.
    - sma2_period (int): The period for the longer SMA used in EWO calculation. 
      Default is 35.

Call with:
    df['ewo'] = bta.elliott_wave_oscillator(df, 'close', 5, 35)

Returns:
    pd.DataFrame: DataFrame with 'ewo' column.
"""

def test():
    """
    Test function for the elliott_wave_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the elliott_wave_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(elliott_wave_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
