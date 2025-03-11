# -*- coding: utf-8 -*-
# hurst_winter_channel.py

import pandas as pd
import numpy as np


def hurst_winter_channel(
    df: pd.DataFrame, 
    na: float = 0.2, 
    nb: float = 0.1, 
    nc: float = 0.1, 
    nd: float = 0.1, 
    scalar: float = 1.0,
    channel_eval: bool = False,
    column: str = "close"
) -> pd.DataFrame:
    """Hurst-Winter Channel (HWC)"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Validate parameters
    na = float(na) if na > 0 else 0.2
    nb = float(nb) if nb > 0 else 0.1
    nc = float(nc) if nc > 0 else 0.1
    nd = float(nd) if nd > 0 else 0.1
    scalar = float(scalar) if scalar > 0 else 1.0
    
    # Get price series
    close = df_copy[column]
    
    # Initialize result arrays
    result = np.zeros(len(close))
    upper = np.zeros(len(close))
    lower = np.zeros(len(close))
    
    if channel_eval:
        chan_width = np.zeros(len(close))
        chan_pct_width = np.zeros(len(close))
    
    # Initialize variables
    last_a = last_v = last_var = 0
    last_f = last_price = last_result = close.iloc[0]
    
    # Calculate HWC values
    for i in range(len(close)):
        # Calculate Holt-Winter components
        F = (1.0 - na) * (last_f + last_v + 0.5 * last_a) + na * close.iloc[i]
        V = (1.0 - nb) * (last_v + last_a) + nb * (F - last_f)
        A = (1.0 - nc) * last_a + nc * (V - last_v)
        
        # Calculate middle line
        result[i] = F + V + 0.5 * A
        
        # Calculate variance and standard deviation
        var = (1.0 - nd) * last_var + nd * (last_price - last_result) * (last_price - last_result)
        stddev = np.sqrt(var)
        
        # Calculate upper and lower bands
        upper[i] = result[i] + scalar * stddev
        lower[i] = result[i] - scalar * stddev
        
        # Calculate channel metrics if requested
        if channel_eval:
            chan_width[i] = upper[i] - lower[i]
            if chan_width[i] > 0:  # Avoid division by zero
                chan_pct_width[i] = (close.iloc[i] - lower[i]) / chan_width[i]
            else:
                chan_pct_width[i] = 0.5  # Default to middle if zero width
        
        # Update values for next iteration
        last_price = close.iloc[i]
        last_a = A
        last_f = F
        last_v = V
        last_var = var
        last_result = result[i]
    
    # Store results in DataFrame
    df_copy["hwc_middle"] = result
    df_copy["hwc_upper"] = upper
    df_copy["hwc_lower"] = lower
    
    # Include channel evaluation metrics if requested
    if channel_eval:
        df_copy["hwc_width"] = chan_width
        df_copy["hwc_pct_width"] = chan_pct_width
        return df_copy[["hwc_middle", "hwc_upper", "hwc_lower", "hwc_width", "hwc_pct_width"]]
    else:
        return df_copy[["hwc_middle", "hwc_upper", "hwc_lower"]]


hurst_winter_channel.__doc__ = \
"""
Name:
    Hurst-Winter Channel (HWC)

Description:
    The Hurst-Winter Channel (HWC) is a volatility-based channel indicator based on 
    the Holt-Winters triple exponential smoothing method. It creates a middle line using 
    the Holt-Winters Moving Average (HWMA) and upper/lower bands based on price deviation.
    
    The channel adapts to price movements using four smoothing parameters (na, nb, nc, nd)
    and can be adjusted with a scalar multiplier. It can also provide channel width and
    relative price position information for additional analysis.
    
    The Holt-Winters method is particularly good at capturing trends, seasonality, and
    adapting to changes in volatility, making this channel useful for identifying potential
    support/resistance levels and overbought/oversold conditions.

More info:
    https://www.mql5.com/en/code/20857
    https://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - na (float): Parameter of the equation that describes a smoothed series (from 0 to 1). Default is 0.2.
    - nb (float): Parameter of the equation to assess the trend (from 0 to 1). Default is 0.1.
    - nc (float): Parameter of the equation to assess seasonality (from 0 to 1). Default is 0.1.
    - nd (float): Parameter of the channel equation (from 0 to 1). Default is 0.1.
    - scalar (float): Multiplier for the width of the channel calculated. Default is 1.0.
    - channel_eval (bool): Whether to return width and percentage price position metrics. Default is False.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.hurst_winter_channel(df)
    df['hwc_middle'] = result['hwc_middle']
    df['hwc_upper'] = result['hwc_upper']
    df['hwc_lower'] = result['hwc_lower']
    
    # If channel_eval is True:
    df['hwc_width'] = result['hwc_width']
    df['hwc_pct_width'] = result['hwc_pct_width']

Returns:
    pd.DataFrame: DataFrame with 'hwc_middle', 'hwc_upper', 'hwc_lower' columns,
                  and optionally 'hwc_width' and 'hwc_pct_width' if channel_eval is True.
"""


def test():
    """
    Test function for the hurst_winter_channel indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the hurst_winter_channel indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(hurst_winter_channel)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 