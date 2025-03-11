# -*- coding: utf-8 -*-
# detrended_price_oscillator.py

import pandas as pd
import numpy as np


def detrended_price_oscillator(
    df: pd.DataFrame, 
    length: int = 20, 
    centered: bool = True,
    column: str = "close"
) -> pd.DataFrame:
    """Detrended Price Oscillator (DPO)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 20
    
    # Get price series
    close = df_copy[column]
    
    # Calculate displacement period
    t = int(0.5 * length) + 1
    
    # Calculate moving average
    ma = close.rolling(window=length).mean()
    
    # Calculate DPO
    if centered:
        # Centered version - shifts the price backward and the MA forward
        # This is the traditional implementation but requires knowing future prices
        # Final result is shifted back to align with current time
        df_copy["dpo"] = (close.shift(t) - ma).shift(-t)
    else:
        # Non-centered version - compares current price with a displaced MA
        # This is more practical for real-time analysis as it doesn't use future prices
        df_copy["dpo"] = close - ma.shift(t)
    
    return df_copy[["dpo"]]


detrended_price_oscillator.__doc__ = \
"""
Name:
    Detrended Price Oscillator (DPO)

Description:
    The Detrended Price Oscillator (DPO) is an indicator designed to remove trend from 
    price and make it easier to identify cycles. Unlike other oscillators, the DPO is 
    not a momentum indicator. It instead highlights cycles by removing the underlying 
    trend from the price data.
    
    The DPO accomplishes this by comparing the current price (or a displaced price) to 
    a moving average from a displaced period in the past. By doing this, it attempts to 
    eliminate the trend component from the price action, leaving the cyclical components.
    
    The indicator can be calculated in two modes:
    - Centered (default): Uses future data for alignment, suitable for historical analysis
    - Non-centered: Uses only historical data, suitable for real-time trading
    
    When the DPO is above zero, it indicates that price is above the displaced moving average.
    When it's below zero, price is below the displaced moving average.

More info:
    https://www.tradingview.com/scripts/detrendedpriceoscillator/
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dpo
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:detrended_price_osci

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the moving average calculation. Default is 20.
    - centered (bool): Whether to center the calculation (shifts result for better alignment). 
                      True is for historical analysis, False for real-time. Default is True.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.detrended_price_oscillator(df)
    df['dpo'] = result['dpo']

Returns:
    pd.DataFrame: DataFrame with 'dpo' column.
"""


def test():
    """
    Test function for the detrended_price_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the detrended_price_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(detrended_price_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 