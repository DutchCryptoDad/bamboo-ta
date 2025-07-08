# -*- coding: utf-8 -*-
# bollinger_bands_nadaraya_smoothed.py
import numpy as np
import pandas as pd


def bollinger_bands_nadaraya_smoothed(
    df: pd.DataFrame,
    h: float = 6.0,
    short_period: int = 20,
    short_stdev: float = 3.0,
    med_period: int = 75,
    med_stdev: float = 4.0,
    long_period: int = 100,
    long_stdev: float = 4.25,
    n: int = 100  # Reduced default for better performance
) -> pd.DataFrame:
    """Bollinger Bands (Nadaraya Smoothed)"""
    
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate typical price (HLC3) - matches Pine Script exactly
    tp = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3
    
    def gaussian_weight(x, h):
        """
        Gaussian kernel function - matches Pine Script guass_w exactly
        Pine Script: math.exp (-1 *( (x*x) / (2*(h*h)) ))
        """
        return np.exp(-1 * (x * x) / (2 * (h * h)))
    
    def calculate_bollinger_bands(src, period, stdev_factor):
        """
        Calculate standard Bollinger Bands exactly like Pine Script bollingers function
        Pine Script: 
        bolu = ta.sma(tp, n) + (factor * ta.stdev(tp, n))
        bold = ta.sma(tp, n) - (factor * ta.stdev(tp, n))
        """
        sma = src.rolling(window=period, min_periods=period).mean()
        std = src.rolling(window=period, min_periods=period).std()
        upper = sma + (stdev_factor * std)
        lower = sma - (stdev_factor * std)
        return upper, lower
    
    def running_nadaraya_watson(src, n, h):
        """
        Optimized Nadaraya-Watson implementation - vectorized for speed
        """
        # Convert to numpy for faster computation
        src_values = src.values
        result = np.full(len(src_values), np.nan)
        
        # Pre-calculate all weights once
        weights = np.array([gaussian_weight(i, h) for i in range(n + 1)])
        weights_sum = np.sum(weights)
        normalized_weights = weights / weights_sum if weights_sum > 0 else weights
        
        # Vectorized computation
        for i in range(len(src_values)):
            if not np.isnan(src_values[i]):
                # Determine available lookback
                lookback = min(i + 1, n + 1)
                
                if lookback > 0:
                    # Get the data slice (going backwards from current position)
                    start_idx = max(0, i - lookback + 1)
                    data_slice = src_values[start_idx:i + 1]
                    weights_slice = normalized_weights[:len(data_slice)]
                    
                    # Vectorized calculation - much faster than loop
                    valid_mask = ~np.isnan(data_slice)
                    if np.any(valid_mask):
                        # Reverse the data slice to match Pine Script indexing
                        data_reversed = data_slice[::-1]
                        valid_mask_reversed = valid_mask[::-1]
                        
                        result[i] = np.sum(data_reversed[valid_mask_reversed] * 
                                         weights_slice[valid_mask_reversed])
        
        return pd.Series(result, index=src.index)
    
    # Step 1: Calculate standard Bollinger Bands on typical price
    # Pine Script variable names: n_first=20, n_second=75, n_third=100
    n_first = short_period
    n_second = med_period  
    n_third = long_period
    
    # Pine Script: [BOLU_FIRST, BOLD_FIRST] = bollingers(n_first, short_stdev)
    bolu_first, bold_first = calculate_bollinger_bands(tp, n_first, short_stdev)
    
    # Pine Script: [BOLU_SECOND, BOLD_SECOND] = bollingers(n_second, short_stdev)
    bolu_second, bold_second = calculate_bollinger_bands(tp, n_second, short_stdev)
    
    # Pine Script: [BOLU_THIRD, BOLD_THIRD] = bollingers(n_third, med_stdev)
    bolu_third, bold_third = calculate_bollinger_bands(tp, n_third, med_stdev)
    
    # Pine Script: [BOLU_FOURTH, BOLD_FOURTH] = bollingers(n_third, long_stdev)
    bolu_fourth, bold_fourth = calculate_bollinger_bands(tp, n_third, long_stdev)
    
    # Step 2: Apply Nadaraya-Watson smoothing to the calculated bands
    # Pine Script: smoothed_bolu_1 = running_nadaraya(BOLU_FIRST, n)
    smoothed_bolu_1 = running_nadaraya_watson(bolu_first, n, h)
    smoothed_bold_1 = running_nadaraya_watson(bold_first, n, h)
    smoothed_bolu_2 = running_nadaraya_watson(bolu_second, n, h)
    smoothed_bold_2 = running_nadaraya_watson(bold_second, n, h)
    smoothed_bolu_3 = running_nadaraya_watson(bolu_third, n, h)
    smoothed_bold_3 = running_nadaraya_watson(bold_third, n, h)
    smoothed_bolu_4 = running_nadaraya_watson(bolu_fourth, n, h)
    smoothed_bold_4 = running_nadaraya_watson(bold_fourth, n, h)
    
    # Create result DataFrame
    result = pd.DataFrame(index=df_copy.index)
    
    # All bands
    result['bb_upper_1'] = smoothed_bolu_1
    result['bb_lower_1'] = smoothed_bold_1
    result['bb_upper_2'] = smoothed_bolu_2
    result['bb_lower_2'] = smoothed_bold_2
    result['bb_upper_3'] = smoothed_bolu_3
    result['bb_lower_3'] = smoothed_bold_3
    result['bb_upper_4'] = smoothed_bolu_4
    result['bb_lower_4'] = smoothed_bold_4
    
    # Calculate band break signals
    result['upper_band_break'] = (
        (df_copy['close'] > result['bb_upper_1']) & 
        (df_copy['close'].shift(1) <= result['bb_upper_1'].shift(1))
    ).astype(int)
    
    result['lower_band_break'] = (
        (df_copy['close'] < result['bb_lower_1']) & 
        (df_copy['close'].shift(1) >= result['bb_lower_1'].shift(1))
    ).astype(int)
    
    # Add typical price for reference
    result['typical_price'] = tp
    
    return result


bollinger_bands_nadaraya_smoothed.__doc__ = """
Name:
    Bollinger Bands (Nadaraya Smoothed)

Description:
    This indicator implements Bollinger Bands with Nadaraya-Watson kernel smoothing.
    It creates multiple levels of Bollinger Bands using different periods and standard
    deviation multipliers, then applies Gaussian kernel smoothing to create smoother,
    less noisy band lines.
    
    The Nadaraya-Watson estimator is a non-parametric regression technique that uses
    a Gaussian kernel to weight nearby observations. This creates smoother bands that
    are less prone to whipsaws while maintaining responsiveness to price changes.
    
    The indicator provides four levels of bands:
    - Level 1: Short-term bands (default: 20 period, 3 std dev)
    - Level 2: Medium-term bands (default: 75 period, 3 std dev) 
    - Level 3: Long-term bands (default: 100 period, 4 std dev)
    - Level 4: Extended bands (default: 100 period, 4.25 std dev)
    
    **Note on TradingView Differences:**
    The calculations in this Python implementation may produce slightly different 
    values compared to the original TradingView Pine Script version due to differences 
    in floating-point precision, rounding methods, and internal mathematical libraries 
    between Python (NumPy/Pandas) and Pine Script. Additionally, the default lookback 
    period has been reduced from 499 to 100 bars for improved performance, which may 
    result in less smoothing compared to the TradingView version. For exact TradingView 
    matching, use n=499, though this will significantly increase computation time.

More info:
    Based on Flux Charts' TradingView indicator
    https://www.tradingview.com/script/v/bollinger-bands-nadaraya-smoothed/
    
    Nadaraya-Watson Estimator:
    https://en.wikipedia.org/wiki/Kernel_regression

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close' columns.
    - h (float): Smoothing factor (bandwidth) for the Nadaraya-Watson estimator. Higher values = more smoothing. Default is 6.0.
    - short_period (int): Period for short-term Bollinger Bands. Default is 20.
    - short_stdev (float): Standard deviation multiplier for short-term bands. Default is 3.0.
    - med_period (int): Period for medium-term Bollinger Bands. Default is 75.
    - med_stdev (float): Standard deviation multiplier for medium-term bands. Default is 4.0.
    - long_period (int): Period for long-term Bollinger Bands. Default is 100.
    - long_stdev (float): Standard deviation multiplier for long-term bands. Default is 4.25.
    - n (int): Number of historical bars to consider for smoothing. Default is 100 (reduced from 499 for performance).

Call with:
    result = bta.bollinger_bands_nadaraya_smoothed(df)
    df['bb_upper_1'] = result['bb_upper_1']
    df['bb_lower_1'] = result['bb_lower_1']
    df['bb_upper_2'] = result['bb_upper_2']
    df['bb_lower_2'] = result['bb_lower_2']
    df['bb_upper_3'] = result['bb_upper_3']
    df['bb_lower_3'] = result['bb_lower_3']
    df['bb_upper_4'] = result['bb_upper_4']
    df['bb_lower_4'] = result['bb_lower_4']
    df['upper_band_break'] = result['upper_band_break']
    df['lower_band_break'] = result['lower_band_break']

Returns:
    pd.DataFrame: DataFrame with the following columns:
    - 'bb_upper_1', 'bb_lower_1': Level 1 smoothed Bollinger Bands (main bands)
    - 'bb_upper_2', 'bb_lower_2': Level 2 smoothed Bollinger Bands
    - 'bb_upper_3', 'bb_lower_3': Level 3 smoothed Bollinger Bands
    - 'bb_upper_4', 'bb_lower_4': Level 4 smoothed Bollinger Bands
    - 'upper_band_break': Signal when price breaks above main upper band (1/0)
    - 'lower_band_break': Signal when price breaks below main lower band (1/0)
    - 'typical_price': HLC3 typical price used for calculations
"""


def test():
    """
    Test function for the bollinger_bands_nadaraya_smoothed indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the bollinger_bands_nadaraya_smoothed indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(bollinger_bands_nadaraya_smoothed)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()