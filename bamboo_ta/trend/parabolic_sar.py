# -*- coding: utf-8 -*-
# parabolic_sar.py

import pandas as pd
import numpy as np


def parabolic_sar(
    df: pd.DataFrame,
    initial_af: float = 0.02,
    af_step: float = 0.02,
    max_af: float = 0.2,
    use_close: bool = False
) -> pd.DataFrame:
    """Parabolic Stop and Reverse (PSAR)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low"]
    if use_close:
        required_columns.append("close")
    
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    initial_af = float(initial_af) if initial_af > 0 else 0.02
    af_step = float(af_step) if af_step > 0 else 0.02
    max_af = float(max_af) if max_af > 0 else 0.2
    
    # Get price series
    high = df_copy["high"]
    low = df_copy["low"]
    
    # Helper function to determine if price is falling at the start
    def is_falling(high_vals, low_vals):
        """Returns True if -DM is positive (indicating falling)"""
        h_diff = high_vals[1] - high_vals[0]
        l_diff = low_vals[0] - low_vals[1]
        return l_diff > h_diff and l_diff > 0
    
    # Initialize series for results
    psar_long = pd.Series(np.nan, index=df_copy.index)
    psar_short = pd.Series(np.nan, index=df_copy.index)
    psar_af = pd.Series(np.nan, index=df_copy.index)
    psar_reversal = pd.Series(0, index=df_copy.index)
    
    # Check initial trend direction (falling?)
    falling = is_falling(high.iloc[:2].values, low.iloc[:2].values)
    
    # Set initial values
    if use_close and len(df_copy) > 0:
        sar = df_copy["close"].iloc[0]
    else:
        sar = high.iloc[0] if falling else low.iloc[0]
    
    # Set initial extreme point
    ep = low.iloc[0] if falling else high.iloc[0]
    
    # Set initial acceleration factor
    af = initial_af
    psar_af.iloc[0] = af
    
    # Fill first value in appropriate series
    if falling:
        psar_short.iloc[0] = sar
    else:
        psar_long.iloc[0] = sar
    
    # Calculate PSAR for the rest of the series
    for i in range(1, len(df_copy)):
        high_val = high.iloc[i]
        low_val = low.iloc[i]
        
        # Calculate SAR value for this period
        sar_val = sar + af * (ep - sar)
        
        # Check for trend reversal
        if falling:
            # In downtrend, SAR must not be above prior two highs
            sar_val = max(sar_val, high.iloc[i-1])
            if i >= 2:
                sar_val = max(sar_val, high.iloc[i-2])
            
            # Check for reversal (price above SAR)
            reverse = high_val > sar_val
            
            # Update extreme point and acceleration factor if trend continues
            if low_val < ep:
                ep = low_val
                af = min(af + af_step, max_af)
        else:
            # In uptrend, SAR must not be below prior two lows
            sar_val = min(sar_val, low.iloc[i-1])
            if i >= 2:
                sar_val = min(sar_val, low.iloc[i-2])
            
            # Check for reversal (price below SAR)
            reverse = low_val < sar_val
            
            # Update extreme point and acceleration factor if trend continues
            if high_val > ep:
                ep = high_val
                af = min(af + af_step, max_af)
        
        # Handle reversal if it occurred
        if reverse:
            # Reset SAR and AF, switch trend direction
            sar_val = ep
            af = initial_af
            falling = not falling
            # Reset extreme point
            ep = low_val if falling else high_val
            # Record reversal
            psar_reversal.iloc[i] = 1
        
        # Update SAR for next iteration
        sar = sar_val
        
        # Store current AF value
        psar_af.iloc[i] = af
        
        # Store SAR value in appropriate series based on trend direction
        if falling:
            psar_short.iloc[i] = sar
        else:
            psar_long.iloc[i] = sar
    
    # Store results in DataFrame
    df_copy["psar_long"] = psar_long
    df_copy["psar_short"] = psar_short
    df_copy["psar_af"] = psar_af
    df_copy["psar_reversal"] = psar_reversal
    
    return df_copy[["psar_long", "psar_short", "psar_af", "psar_reversal"]]


parabolic_sar.__doc__ = \
"""
Name:
    Parabolic Stop and Reverse (PSAR)

Description:
    The Parabolic SAR (Stop and Reverse) is a trend-following indicator developed by 
    J. Welles Wilder. It is used to determine the direction of a trend and identify 
    potential reversal points in price.
    
    The indicator appears as a series of dots placed either above or below the price, 
    depending on the trend direction:
    - Dots below the price indicate an uptrend (stored in 'psar_long')
    - Dots above the price indicate a downtrend (stored in 'psar_short')
    
    The distance between the price and the dots gradually decreases as the trend continues,
    eventually causing a reversal when the price crosses the SAR value. At this point, the
    SAR "stops and reverses" to the other side of the price.
    
    The indicator uses an acceleration factor (AF) that increases as the trend continues
    in the same direction, causing the SAR to accelerate toward the price.
    
    This implementation returns four components:
    - psar_long: SAR values during uptrends (appears below price)
    - psar_short: SAR values during downtrends (appears above price)
    - psar_af: Current acceleration factor value
    - psar_reversal: Binary indicator (1/0) showing when SAR reversals occur

More info:
    https://www.investopedia.com/trading/introduction-to-parabolic-sar/
    https://school.stockcharts.com/doku.php?id=technical_indicators:parabolic_sar

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns, 
      and optionally 'close' if use_close is True.
    - initial_af (float): Initial acceleration factor. Default is 0.02.
    - af_step (float): Acceleration factor increment. Default is 0.02.
    - max_af (float): Maximum acceleration factor. Default is 0.2.
    - use_close (bool): Whether to use close price for initial SAR calculation. Default is False.

Call with:
    result = bta.parabolic_sar(df)
    df['psar_long'] = result['psar_long']  # SAR values during uptrends (below price)
    df['psar_short'] = result['psar_short']  # SAR values during downtrends (above price)
    df['psar_af'] = result['psar_af']  # Current acceleration factor
    df['psar_reversal'] = result['psar_reversal']  # Binary indicator for SAR reversals

Returns:
    pd.DataFrame: DataFrame with 'psar_long', 'psar_short', 'psar_af', and 'psar_reversal' columns.
"""


def test():
    """
    Test function for the parabolic_sar indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the parabolic_sar indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(parabolic_sar)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 