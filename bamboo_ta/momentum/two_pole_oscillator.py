# -*- coding: utf-8 -*-
# two_pole_oscillator.py

import pandas as pd


def two_pole_oscillator(df: pd.DataFrame, 
                       column: str = "close", 
                       filter_length: int = 20, 
                       sma_length: int = 25,
                       area_length: int = 100,
                       lag_periods: int = 4) -> pd.DataFrame:
    """Two-Pole Oscillator"""
    
    df_copy = df.copy()
    
    # Ensure required columns exist
    required_columns = [column, 'high', 'low']
    for col in required_columns:
        if col not in df_copy.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate SMA and standardized momentum exactly as Pine Script
    sma1 = df_copy[column].rolling(window=sma_length).mean()
    close_diff = df_copy[column] - sma1
    sma_diff = close_diff.rolling(window=sma_length).mean()
    
    # CRITICAL: Use biased standard deviation (ddof=0) to match Pine Script ta.stdev()
    stdev_diff = close_diff.rolling(window=sma_length).std(ddof=0)
    
    # Calculate normalized momentum (equivalent to sma_n1 in Pine Script)
    sma_n1 = (close_diff - sma_diff) / stdev_diff
    
    # Apply Pine Script precision rounding (9 decimal places)
    sma_n1 = sma_n1.round(9)
    
    # Calculate area for signal positioning (used in original for plotting levels)
    area = (df_copy['high'] - df_copy['low']).rolling(window=area_length).mean()
    
    # Two-pole smooth filter implementation - ULTRA-PRECISE Pine Script conversion
    # Exact Pine Script f_two_pole_filter(source, length) logic
    alpha = 2.0 / (filter_length + 1)
    
    # Initialize state variables exactly like Pine Script var behavior
    smooth1 = None
    smooth2 = None
    two_p_values = []
    
    for i in range(len(sma_n1)):
        source_value = sma_n1.iloc[i]
        
        if pd.isna(source_value):
            two_p_values.append(None)
            continue
            
        # Exact Pine Script var logic with precision matching
        if smooth1 is None:
            smooth1 = float(source_value)
        else:
            smooth1 = (1.0 - alpha) * smooth1 + alpha * source_value
            # Apply Pine Script precision rounding after each calculation
            smooth1 = round(smooth1, 9)
        
        if smooth2 is None:
            smooth2 = float(smooth1)
        else:
            smooth2 = (1.0 - alpha) * smooth2 + alpha * smooth1
            # Apply Pine Script precision rounding after each calculation
            smooth2 = round(smooth2, 9)
            
        two_p_values.append(smooth2)
    
    # Convert to pandas Series with explicit float64 dtype
    two_p = pd.Series(two_p_values, index=df_copy.index, dtype='float64')
    
    # Create lagged version using historical indexing like Pine Script [4]
    # Pine Script [4] means 4 bars ago, which is different from shift
    two_pp = two_p.shift(lag_periods)
    
    # Generate buy and sell signals using exact crossover logic
    # ta.crossover(a, b) means a > b and a[1] <= b[1]
    # ta.crossunder(a, b) means a < b and a[1] >= b[1]
    
    buy_condition1 = two_p > two_pp  # Current: two_p > two_pp
    buy_condition2 = two_p.shift(1) <= two_pp.shift(1)  # Previous: two_p[1] <= two_pp[1]
    buy_condition3 = two_p < 0  # two_p < 0
    buy_signal = (buy_condition1 & buy_condition2 & buy_condition3).astype(int)
    
    sell_condition1 = two_p < two_pp  # Current: two_p < two_pp
    sell_condition2 = two_p.shift(1) >= two_pp.shift(1)  # Previous: two_p[1] >= two_pp[1]
    sell_condition3 = two_p > 0  # two_p > 0
    sell_signal = (sell_condition1 & sell_condition2 & sell_condition3).astype(int)
    
    # Store results
    df_copy['two_pole'] = two_p
    df_copy['two_pole_lagged'] = two_pp
    df_copy['buy_signal'] = buy_signal
    df_copy['sell_signal'] = sell_signal
    df_copy['area'] = area
    
    return df_copy[['two_pole', 'two_pole_lagged', 'buy_signal', 'sell_signal', 'area']]


two_pole_oscillator.__doc__ = """
Name:
    Two-Pole Oscillator

Description:
    The Two-Pole Oscillator is a momentum indicator that applies a two-stage exponential
    smoothing filter to a standardized price momentum calculation. It creates an oscillator
    that ranges roughly between -1 and +1, with buy signals generated when the oscillator
    crosses above its lagged version while below zero, and sell signals when it crosses
    below its lagged version while above zero.
    
    The indicator uses:
    1. A standardized momentum calculation based on price deviation from SMA
    2. A two-pole (double) exponential smoothing filter for noise reduction
    3. Signal generation using crossovers with a lagged version of the oscillator

More info:
    https://www.tradingview.com/script/2Ssn4yDZ-Two-Pole-Oscillator-BigBeluga/
    (BigBeluga Two-Pole Oscillator)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'close', 'high', 'low'.
    - column (str): The column to use for calculations. Default is 'close'.
    - filter_length (int): Period for the two-pole filter smoothing. Default is 20.
    - sma_length (int): Period for the SMA and standardization calculations. Default is 25.
    - area_length (int): Period for calculating the area (high-low range). Default is 100.
    - lag_periods (int): Number of periods to lag the oscillator for signal generation. Default is 4.

Call with:
    result = bta.two_pole_oscillator(df)
    df['two_pole'] = result['two_pole']
    df['two_pole_lagged'] = result['two_pole_lagged']
    df['buy_signal'] = result['buy_signal']
    df['sell_signal'] = result['sell_signal']

Returns:
    pd.DataFrame: DataFrame with 'two_pole', 'two_pole_lagged', 'buy_signal', 
    'sell_signal', and 'area' columns.
"""


def test():
    """
    Test function for the two_pole_oscillator indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the two_pole_oscillator indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(two_pole_oscillator)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()