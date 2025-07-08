# -*- coding: utf-8 -*-
# williams_vix_fix.py
import pandas as pd
import numpy as np


def williams_vix_fix(df, vix_length=22, mult=2.0, bbl=20, ph=0.85):
    """Williams VIX Fix"""
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    df_copy = df.copy()
    
    # Calculate the highest high over the lookback period
    highest_high = df_copy['high'].rolling(window=vix_length).max()
    
    # Calculate Williams VIX Fix (WVF) - Original Formula
    # WVF = ((Highest(High, Period) - Low) / Highest(High, Period)) * 100
    wvf = ((highest_high - df_copy['low']) / highest_high) * 100
    
    # Calculate Bollinger Bands for VIX Fix
    wvf_sma = wvf.rolling(window=bbl).mean()
    wvf_stdev = wvf.rolling(window=bbl).std()
    
    # Upper and Lower Bollinger Bands
    upper_band = wvf_sma + (mult * wvf_stdev)
    lower_band = wvf_sma - (mult * wvf_stdev)
    mid_line = wvf_sma
    
    # Percentile calculations
    # Range High based on percentile of VIX Fix values
    range_high = wvf.rolling(window=bbl).max() * ph
    
    # Upper range calculation (alternative signal method) - NOT USED in signals but calculated
    upper_range = highest_high * ph
    
    # VIX Fix signal conditions (green flash criteria)
    # Signal when VIX Fix >= upper_band OR VIX Fix >= range_high
    vix_signal = ((wvf >= upper_band) | (wvf >= range_high)).astype(int)
    
    # Green flash signal - triggers when signal goes from 0 to 1
    green_flash = (
        (vix_signal == 1) & (vix_signal.shift(1) == 0)
    ).astype(int)
    
    # Store results in the copy DataFrame
    df_copy['williams_vix_fix'] = wvf
    df_copy['williams_vix_fix_upper_band'] = upper_band
    df_copy['williams_vix_fix_lower_band'] = lower_band
    df_copy['williams_vix_fix_mid_line'] = mid_line
    df_copy['williams_vix_fix_range_high'] = range_high
    df_copy['williams_vix_fix_signal'] = vix_signal
    df_copy['williams_vix_fix_green_flash'] = green_flash
    
    return df_copy[['williams_vix_fix', 'williams_vix_fix_upper_band', 'williams_vix_fix_lower_band', 
                    'williams_vix_fix_mid_line', 'williams_vix_fix_range_high', 
                    'williams_vix_fix_signal', 'williams_vix_fix_green_flash']]


williams_vix_fix.__doc__ = """
Name:
    Williams VIX Fix

Description:
    The Williams VIX Fix indicator, developed by Larry Williams, measures market volatility 
    and identifies potential market bottoms when volatility spikes indicate oversold conditions.
    
    The indicator calculates the percentage difference between the highest high over a 
    specified period and the current low, relative to the highest high. This creates 
    a volatility measure that spikes during market stress and can signal potential 
    reversal points.
    
    The indicator includes:
    - Williams VIX Fix: The main volatility measure
    - Midline: Upper band (mean + standard deviation)
    - Lower Band: Lower band (mean - standard deviation)
    - Signal: Binary signal when VIX exceeds thresholds
    - Green Flash: Signal for potential market bottoms

More info:
    https://www.tradingview.com/script/xqJvYkWE-Williams-VIX-Fix-Finds-Market-Bottoms/
    https://www.stockcharts.com/school/doku.php?id=chart_school:technical_indicators:williams_vix_fix_fix

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - vix_length (int): Period for calculating the highest high. Default is 22.
    - mult (float): Multiplier for standard deviation bands. Default is 2.0.
    - bbl (int): Period for calculating Bollinger Band levels. Default is 20.
    - ph (float): Percentile threshold for range high signals. Default is 0.85.

Call with:
    vix_result = bta.williams_vix_fix(df, vix_length=22, mult=2.0, bbl=20, ph=0.85)
    df['williams_vix_fix'] = vix_result['williams_vix_fix']
    df['williams_vix_fix_upper_band'] = vix_result['williams_vix_fix_upper_band']
    df['williams_vix_fix_lower_band'] = vix_result['williams_vix_fix_lower_band']
    df['williams_vix_fix_mid_line'] = vix_result['williams_vix_fix_mid_line']
    df['williams_vix_fix_range_high'] = vix_result['williams_vix_fix_range_high']
    df['williams_vix_fix_signal'] = vix_result['williams_vix_fix_signal']
    df['williams_vix_fix_green_flash'] = vix_result['williams_vix_fix_green_flash']

Returns:
    pd.DataFrame: DataFrame with 'williams_vix_fix', 'williams_vix_fix_upper_band', 'williams_vix_fix_lower_band',
    'williams_vix_fix_mid_line', 'williams_vix_fix_range_high', 'williams_vix_fix_signal', and 'williams_vix_fix_green_flash' columns.
"""


def test():
    """
    Test function for the williams_vix_fix indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the williams_vix_fix indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(williams_vix_fix)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()