# -*- coding: utf-8 -*-
# schaff_trend_cycle.py

import pandas as pd
import numpy as np


def schaff_trend_cycle(df: pd.DataFrame, tc_length: int = 10, fast: int = 12, 
                       slow: int = 26, factor: float = 0.5) -> pd.DataFrame:
    """Schaff Trend Cycle (STC)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if "close" not in df.columns:
        raise KeyError("DataFrame must contain 'close' column")
    
    close = df_copy["close"]
    
    # Swap fast and slow if slow < fast to ensure correct calculation
    if slow < fast:
        fast, slow = slow, fast
    
    # Calculate MACD
    fast_ma = close.ewm(span=fast, adjust=False).mean()
    slow_ma = close.ewm(span=slow, adjust=False).mean()
    xmacd = fast_ma - slow_ma
    
    # Calculate Schaff Trend Cycle
    pff, pf = _schaff_tc_calculation(close, xmacd, tc_length, factor)
    
    # Create output DataFrame
    df_copy["stc"] = pff
    df_copy["stc_macd"] = xmacd
    df_copy["stc_stoch"] = pf
    
    return df_copy[["stc", "stc_macd", "stc_stoch"]]


def _schaff_tc_calculation(close: pd.Series, xmacd: pd.Series, tc_length: int, factor: float) -> tuple:
    """
    Internal function to calculate the Schaff Trend Cycle values.
    
    Args:
        close (pd.Series): Series of close prices, used for indexing.
        xmacd (pd.Series): MACD or other oscillator values.
        tc_length (int): Trend cycle length.
        factor (float): Smoothing factor.
        
    Returns:
        tuple: (pff, pf) where pff is the final STC values and pf is the intermediate stochastic.
    """
    # First stochastic of MACD
    lowest_xmacd = xmacd.rolling(window=tc_length).min()
    highest_xmacd = xmacd.rolling(window=tc_length).max()
    
    # Non-zero range calculation
    xmacd_range = highest_xmacd - lowest_xmacd
    xmacd_range = xmacd_range.where(xmacd_range != 0, 1)  # Replace zeros with 1 to avoid division by zero
    
    # Initialize arrays
    m = len(xmacd)
    stoch1 = np.zeros(m)
    pf = np.zeros(m)
    
    # Calculate first stochastic
    for i in range(1, m):
        if pd.notna(lowest_xmacd.iloc[i]) and pd.notna(xmacd_range.iloc[i]):
            stoch1[i] = 100 * ((xmacd.iloc[i] - lowest_xmacd.iloc[i]) / xmacd_range.iloc[i])
        else:
            stoch1[i] = stoch1[i - 1]
            
        # Smoothed calculation for Fast D of MACD
        pf[i] = pf[i - 1] + (factor * (stoch1[i] - pf[i - 1]))
    
    # Convert to Series for further calculations
    pf_series = pd.Series(pf, index=close.index)
    
    # Second stochastic of smoothed Percent Fast D (PF)
    lowest_pf = pf_series.rolling(window=tc_length).min()
    highest_pf = pf_series.rolling(window=tc_length).max()
    
    # Non-zero range calculation
    pf_range = highest_pf - lowest_pf
    pf_range = pf_range.where(pf_range != 0, 1)  # Replace zeros with 1 to avoid division by zero
    
    # Initialize arrays for second stochastic
    stoch2 = np.zeros(m)
    pff = np.zeros(m)
    
    # Calculate second stochastic
    for i in range(1, m):
        if pd.notna(pf_range.iloc[i]) and pd.notna(lowest_pf.iloc[i]):
            stoch2[i] = 100 * ((pf_series.iloc[i] - lowest_pf.iloc[i]) / pf_range.iloc[i])
        else:
            stoch2[i] = stoch2[i - 1]
            
        # Smoothed calculation for Fast D of PF
        pff[i] = pff[i - 1] + (factor * (stoch2[i] - pff[i - 1]))
    
    return pff, pf


schaff_trend_cycle.__doc__ = \
"""
Name:
    Schaff Trend Cycle

Description:
    The Schaff Trend Cycle (STC) is an evolution of the Moving Average Convergence
    Divergence (MACD) indicator, incorporating two cascaded stochastic calculations
    with additional smoothing.
    
    Developed by Doug Schaff, this indicator attempts to improve upon the MACD by
    reducing lag and generating clearer buy/sell signals. The STC combines the 
    trend-following aspects of MACD with the cyclical properties of stochastics,
    making it potentially more responsive to price changes.

More info:
    https://school.stockcharts.com/doku.php?id=technical_indicators:schaff_trend_cycle

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - tc_length (int): SchaffTC signal-line length. Default is 10 (typically set to 
      half of the expected market cycle length).
    - fast (int): The short period for MACD calculation. Default is 12.
    - slow (int): The long period for MACD calculation. Default is 26.
    - factor (float): Smoothing factor for the final stochastic calculation. Default is 0.5.

Call with:
    result = bta.schaff_trend_cycle(df)
    df['stc'] = result['stc']  # Main indicator
    df['stc_macd'] = result['stc_macd']  # Underlying MACD line
    df['stc_stoch'] = result['stc_stoch']  # Intermediate stochastic calculation

Returns:
    pd.DataFrame: DataFrame with 'stc', 'stc_macd', and 'stc_stoch' columns.
"""


def test():
    """
    Test function for the schaff_trend_cycle indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the schaff_trend_cycle indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(schaff_trend_cycle)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 