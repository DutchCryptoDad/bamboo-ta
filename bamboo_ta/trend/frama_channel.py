# -*- coding: utf-8 -*-
# frama_channel.py
import numpy as np
import pandas as pd


def frama_channel(df, length=26, distance=1.5, volatility_period=200, smooth_period=5, fillna=False):
    """FRAMA Channel Indicator"""
    
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df_copy.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate price source (hl2)
    price = (df_copy["high"] + df_copy["low"]) / 2
    hlc3 = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3
    
    # Calculate volatility using SMA of high-low range
    volatility = (df_copy["high"] - df_copy["low"]).rolling(window=volatility_period).mean()
    
    # Initialize arrays for FRAMA calculation
    frama_values = np.full(len(df_copy), np.nan)
    
    # Calculate FRAMA
    for i in range(length, len(df_copy)):
        # Get the data window
        high_window = df_copy["high"].iloc[i-length+1:i+1]
        low_window = df_copy["low"].iloc[i-length+1:i+1]
        
        # Calculate N3: (highest high - lowest low) / length
        HH = high_window.max()
        LL = low_window.min()
        N3 = (HH - LL) / length if (HH - LL) > 0 else 0.001
        
        # Calculate N1: first half range
        half_length = length // 2
        high_first_half = high_window.iloc[:half_length]
        low_first_half = low_window.iloc[:half_length]
        HH1 = high_first_half.max()
        LL1 = low_first_half.min()
        N1 = (HH1 - LL1) / half_length if (HH1 - LL1) > 0 else 0.001
        
        # Calculate N2: second half range
        high_second_half = high_window.iloc[half_length:]
        low_second_half = low_window.iloc[half_length:]
        HH2 = high_second_half.max()
        LL2 = low_second_half.min()
        N2 = (HH2 - LL2) / half_length if (HH2 - LL2) > 0 else 0.001
        
        # Calculate fractal dimension
        if N1 > 0 and N2 > 0 and N3 > 0:
            try:
                dimension = (np.log(N1 + N2) - np.log(N3)) / np.log(2)
            except:
                dimension = 1.5  # Default fallback
        else:
            dimension = 1.5
        
        # Calculate alpha for FRAMA
        alpha = np.exp(-4.6 * (dimension - 1))
        alpha = np.clip(alpha, 0.01, 1.0)  # Clamp between 0.01 and 1
        
        # Calculate FRAMA value
        if i == length:
            # Initialize first value
            frama_values[i] = price.iloc[i]
        else:
            # FRAMA calculation: alpha * price + (1 - alpha) * previous_frama
            frama_values[i] = alpha * price.iloc[i] + (1 - alpha) * frama_values[i-1]
    
    # Convert to pandas Series
    frama_series = pd.Series(frama_values, index=df_copy.index)
    
    # Apply SMA smoothing to FRAMA
    frama_smoothed = frama_series.rolling(window=smooth_period).mean()
    
    # For early values (before we have enough data), use the price
    for i in range(length):
        if pd.isna(frama_smoothed.iloc[i]):
            frama_smoothed.iloc[i] = price.iloc[i]
    
    # Calculate channel bands
    upper_band = frama_smoothed + volatility * distance
    lower_band = frama_smoothed - volatility * distance
    
    # Generate breakout signals
    breakout_up = np.full(len(df_copy), False)
    breakout_down = np.full(len(df_copy), False)
    
    for i in range(1, len(df_copy)):
        # Check for crossover above upper band
        if (hlc3.iloc[i] > upper_band.iloc[i] and 
            hlc3.iloc[i-1] <= upper_band.iloc[i-1] and 
            not pd.isna(upper_band.iloc[i])):
            breakout_up[i] = True
            
        # Check for crossunder below lower band
        if (hlc3.iloc[i] < lower_band.iloc[i] and 
            hlc3.iloc[i-1] >= lower_band.iloc[i-1] and 
            not pd.isna(lower_band.iloc[i])):
            breakout_down[i] = True
    
    # Generate trend direction
    trend_direction = np.full(len(df_copy), 0)  # 0 = neutral, 1 = up, -1 = down
    
    for i in range(1, len(df_copy)):
        if breakout_up[i]:
            trend_direction[i] = 1
        elif breakout_down[i]:
            trend_direction[i] = -1
        else:
            # Check if price crosses FRAMA line for neutral state
            if (df_copy["close"].iloc[i] > frama_smoothed.iloc[i] and 
                df_copy["close"].iloc[i-1] <= frama_smoothed.iloc[i-1]):
                trend_direction[i] = 0
            elif (df_copy["close"].iloc[i] < frama_smoothed.iloc[i] and 
                  df_copy["close"].iloc[i-1] >= frama_smoothed.iloc[i-1]):
                trend_direction[i] = 0
            else:
                trend_direction[i] = trend_direction[i-1]
    
    # Fill NaN values if requested
    if fillna:
        frama_smoothed = frama_smoothed.fillna(method='bfill').fillna(method='ffill')
        upper_band = upper_band.fillna(method='bfill').fillna(method='ffill')
        lower_band = lower_band.fillna(method='bfill').fillna(method='ffill')
    
    # Prepare result
    df_copy["frama"] = frama_smoothed
    df_copy["frama_upper"] = upper_band
    df_copy["frama_lower"] = lower_band
    df_copy["breakout_up"] = breakout_up.astype(int)
    df_copy["breakout_down"] = breakout_down.astype(int)
    df_copy["trend_direction"] = trend_direction
    
    return df_copy[["frama", "frama_upper", "frama_lower", "breakout_up", "breakout_down", "trend_direction"]]


frama_channel.__doc__ = """
Name:
    FRAMA Channel

Description:
    The FRAMA (Fractal Adaptive Moving Average) Channel is an advanced trend-following
    indicator that adapts to market volatility using fractal geometry. It calculates
    a fractal dimension to determine the optimal smoothing factor, making it more
    responsive during trending markets and smoother during ranging markets.
    
    The indicator creates a channel around the FRAMA line using volatility-based bands
    and generates breakout signals when price crosses above the upper band (bullish)
    or below the lower band (bearish).

More info:
    https://www.mesasoftware.com/papers/FRAMA.pdf
    https://www.tradingview.com/script/frama-channel-bigbeluga/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low', and 'close' columns.
    - length (int): Length for FRAMA calculation. Must be even number. Default is 26.
    - distance (float): Multiplier for channel bands distance from FRAMA line. Default is 1.5.
    - volatility_period (int): Period for calculating volatility (high-low range). Default is 200.
    - smooth_period (int): Period for SMA smoothing of FRAMA values. Default is 5.
    - fillna (bool): If True, fills NaN values using forward/backward fill. Default is False.

Call with:
    frama_result = bta.frama_channel(df, length=26, distance=1.5)
    df["frama"] = frama_result["frama"]
    df["frama_upper"] = frama_result["frama_upper"]
    df["frama_lower"] = frama_result["frama_lower"]
    df["breakout_up"] = frama_result["breakout_up"]
    df["breakout_down"] = frama_result["breakout_down"]
    df["trend_direction"] = frama_result["trend_direction"]

Returns:
    pd.DataFrame: DataFrame with 'frama', 'frama_upper', 'frama_lower', 'breakout_up', 
    'breakout_down', and 'trend_direction' columns.
"""


def test():
    """
    Test function for the frama_channel indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the frama_channel indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(frama_channel)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()