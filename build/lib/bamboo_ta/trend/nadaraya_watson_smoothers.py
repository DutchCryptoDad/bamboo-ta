# -*- coding: utf-8 -*-
# nadaraya_watson_smoothers.py
import numpy as np
import pandas as pd


def nadaraya_watson_smoothers(df, src='close', bandwidth=8.0, repaint=True, lookback=500):
    """Nadaraya-Watson Smoothers"""
    
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required column
    if src not in df.columns:
        raise KeyError(f"DataFrame must contain '{src}' column")
    
    # Get the source data
    source = df_copy[src].values
    n = len(source)
    
    # Initialize output arrays
    nwe_values = np.full(n, np.nan)
    trend_direction = np.full(n, np.nan)
    reversal_signals = np.full(n, 0)
    
    def gaussian_kernel(x, h):
        """Gaussian window function"""
        return np.exp(-(x**2) / (h**2 * 2))
    
    if repaint:
        # Repainting mode - recalculates all historical values
        for i in range(n):
            sum_weighted = 0.0
            sum_weights = 0.0
            
            # Calculate weighted mean using all available data up to current point
            max_lookback = min(lookback, i + 1)
            for j in range(max_lookback):
                if i - j >= 0:
                    weight = gaussian_kernel(j, bandwidth)
                    sum_weighted += source[i - j] * weight
                    sum_weights += weight
            
            if sum_weights > 0:
                nwe_values[i] = sum_weighted / sum_weights
    else:
        # Non-repainting mode - endpoint method
        # Pre-calculate coefficients
        coefs = np.array([gaussian_kernel(i, bandwidth) for i in range(lookback)])
        den = np.sum(coefs)
        
        for i in range(n):
            sum_weighted = 0.0
            max_lookback = min(lookback, i + 1)
            
            for j in range(max_lookback):
                if i - j >= 0:
                    sum_weighted += source[i - j] * coefs[j]
            
            if den > 0:
                nwe_values[i] = sum_weighted / den
    
    # Calculate trend direction (1 for up, -1 for down, 0 for no trend)
    for i in range(1, n):
        if not np.isnan(nwe_values[i]) and not np.isnan(nwe_values[i-1]):
            if nwe_values[i] > nwe_values[i-1]:
                trend_direction[i] = 1
            elif nwe_values[i] < nwe_values[i-1]:
                trend_direction[i] = -1
            else:
                trend_direction[i] = 0
    
    # Detect reversal signals (trend direction changes)
    prev_direction = 0
    for i in range(1, n):
        if not np.isnan(trend_direction[i]):
            current_direction = trend_direction[i]
            
            # Check for trend reversal
            if prev_direction != 0 and current_direction != 0:
                if prev_direction != current_direction:
                    if current_direction == 1:  # Bullish reversal
                        reversal_signals[i] = 1
                    else:  # Bearish reversal
                        reversal_signals[i] = -1
            
            prev_direction = current_direction
    
    # Store results in the dataframe
    df_copy['nwe'] = nwe_values
    df_copy['nwe_trend'] = trend_direction
    df_copy['nwe_reversal'] = reversal_signals
    
    # Create additional helper columns for trend coloring
    df_copy['nwe_bullish'] = np.where(df_copy['nwe_trend'] == 1, df_copy['nwe'], np.nan)
    df_copy['nwe_bearish'] = np.where(df_copy['nwe_trend'] == -1, df_copy['nwe'], np.nan)
    
    return df_copy[['nwe', 'nwe_trend', 'nwe_reversal', 'nwe_bullish', 'nwe_bearish']]


nadaraya_watson_smoothers.__doc__ = """
Name:
    Nadaraya-Watson Smoothers

Description:
    The Nadaraya-Watson Smoothers indicator is a sophisticated smoothing technique that uses 
    Gaussian kernel regression to create a smooth representation of price action. It applies 
    a Gaussian weight function to nearby data points, giving more weight to closer points 
    and less weight to farther points.
    
    This indicator can operate in two modes:
    - Repainting mode: Recalculates all historical values as new data arrives, providing 
      the smoothest possible curve but changing historical values
    - Non-repainting mode: Uses an endpoint method that doesn't change historical values, 
      making it suitable for backtesting and live trading
    
    The indicator also identifies trend direction changes and potential reversal points,
    making it useful for trend following strategies and entry/exit timing.

More info:
    The Nadaraya-Watson estimator is a non-parametric regression technique that estimates
    the conditional expectation of a random variable. In trading applications, it creates
    a smooth trend line that adapts to price movements while filtering out noise.
    
    https://en.wikipedia.org/wiki/Kernel_regression

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - bandwidth (float): Controls the smoothness of the estimator. Higher values create 
      smoother lines but with more lag. Default is 8.0.
    - repaint (bool): If True, uses repainting mode for smoothest results. If False, 
      uses non-repainting endpoint method. Default is True.
    - lookback (int): Maximum number of bars to look back for calculations. Default is 500.

Call with:
    nw_result = bta.nadaraya_watson_smoothers(df, src='close', bandwidth=8.0, repaint=True)
    df['nwe'] = nw_result['nwe']
    df['nwe_trend'] = nw_result['nwe_trend']
    df['nwe_reversal'] = nw_result['nwe_reversal']
    df['nwe_bullish'] = nw_result['nwe_bullish']
    df['nwe_bearish'] = nw_result['nwe_bearish']

Returns:
    pd.DataFrame: DataFrame with the following columns:
    - 'nwe': The Nadaraya-Watson Estimator values
    - 'nwe_trend': Trend direction (1 for up, -1 for down, 0 for sideways)
    - 'nwe_reversal': Reversal signals (1 for bullish reversal, -1 for bearish reversal, 0 for no reversal)
    - 'nwe_bullish': NWE values when trend is bullish (for plotting in green)
    - 'nwe_bearish': NWE values when trend is bearish (for plotting in red)
"""


def test():
    """
    Test function for the nadaraya_watson_smoothers indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the nadaraya_watson_smoothers indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(nadaraya_watson_smoothers)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()