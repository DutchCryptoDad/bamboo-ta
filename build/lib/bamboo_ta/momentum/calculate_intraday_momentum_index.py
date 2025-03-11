# -*- coding: utf-8 -*-
# calculate_intraday_momentum_index.py

import pandas as pd
import numpy as np


def calculate_intraday_momentum_index(df: pd.DataFrame, length: int = 14) -> pd.Series:
    """Calculate Intraday Momentum Index"""
    # Ensure the DataFrame contains the required columns
    if not {'open', 'close'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'open' and 'close' columns.")

    # Calculate gains and losses
    gain = np.where(df['close'] > df['open'], df['close'] - df['open'], 0)
    loss = np.where(df['close'] < df['open'], df['open'] - df['close'], 0)

    # Calculate rolling sums of gains and losses
    up_sum = pd.Series(gain).rolling(window=length).sum()
    down_sum = pd.Series(loss).rolling(window=length).sum()

    # Calculate IMI
    imi = 100 * up_sum / (up_sum + down_sum)

    # Return the IMI as a Pandas Series
    return imi

calculate_intraday_momentum_index.__doc__ = \
"""
Name:
    Intraday Momentum Index (IMI)

Description:
    The Intraday Momentum Index combines candlestick analysis with relative strength index (RSI)
    principles to measure intraday momentum based on the relationship between the open and close prices.

More info:
    https://www.investopedia.com/terms/i/intraday-momentum-index.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the following columns:
        - 'open': Opening price.
        - 'close': Closing price.
    - length (int, default=14): Lookback period for calculating the IMI.

Call with:
    df['imi'] = bta.calculate_intraday_momentum_index(df, length=14)

Returns:
    pd.Series: A Series representing the Intraday Momentum Index (IMI) values.
"""


def test():
    """
    Test function for the calculate_intraday_momentum_index indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the calculate_intraday_momentum_index indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(calculate_intraday_momentum_index)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
