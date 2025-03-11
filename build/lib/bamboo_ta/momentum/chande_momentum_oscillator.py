# -*- coding: utf-8 -*-
# chande_momentum_oscillator.py

import pandas as pd


def chande_momentum_oscillator(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
    """Chande Momentum Oscillator"""
    df_copy = df.copy()

    mom = df['close'].diff()
    pos_mom = mom.where(mom > 0, 0)
    neg_mom = -mom.where(mom < 0, 0)
    
    sm1 = pos_mom.rolling(window=length).sum()
    sm2 = neg_mom.rolling(window=length).sum()
    
    df_copy['cmo'] = 100 * (sm1 - sm2) / (sm1 + sm2)

    return df_copy[['cmo']]

chande_momentum_oscillator.__doc__ = \
"""
Name:
    Chande Momentum Oscillator

Description:
    The Chande Momentum Oscillator (CMO) is a technical momentum indicator developed 
    by Tushar Chande. It measures the amount that an asset's price has changed over 
    a specified period of time.

More info:
    https://www.investopedia.com/terms/c/chandemomentumoscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Length for the CMO calculation. Default is 14.

Call with:
        df['cmo'] = bta.chande_momentum_oscillator(df)

For Signal line:
        df['cmo_signal'] = df['cmo'].rolling(window=10).mean()  # Using SMA for signal

Returns:
    pd.DataFrame: DataFrame with 'cmo' column.
"""


def test():
    """
    Test function for the chande_momentum_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the chande_momentum_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(chande_momentum_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
