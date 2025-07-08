# -*- coding: utf-8 -*-
# volumatic_variable_index_dynamic_average.py
import numpy as np
import pandas as pd


def volumatic_variable_index_dynamic_average(
    df: pd.DataFrame,
    vidya_length: int = 10,
    vidya_momentum: int = 20,
    band_distance: float = 2.0,
    atr_length: int = 200,
    pivot_left_bars: int = 3,
    pivot_right_bars: int = 3,
    smooth_length: int = 15,
    column: str = 'close'
) -> pd.DataFrame:
    """Volumatic Variable Index Dynamic Average (VIDYA)"""
    
    df_copy = df.copy()
    
    # Ensure required columns exist
    required_columns = ['open', 'high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate momentum for VIDYA
    momentum = df_copy[column].diff()
    
    # Calculate positive and negative momentum sums
    pos_momentum = np.where(momentum >= 0, momentum, 0.0)
    neg_momentum = np.where(momentum >= 0, 0.0, -momentum)
    
    sum_pos_momentum = pd.Series(pos_momentum).rolling(window=vidya_momentum).sum()
    sum_neg_momentum = pd.Series(neg_momentum).rolling(window=vidya_momentum).sum()
    
    # Calculate CMO (Chande Momentum Oscillator) component
    cmo = 100 * (sum_pos_momentum - sum_neg_momentum) / (sum_pos_momentum + sum_neg_momentum)
    abs_cmo = np.abs(cmo)
    
    # Calculate VIDYA
    alpha = 2 / (vidya_length + 1)
    vidya_value = pd.Series(index=df_copy.index, dtype=float)
    vidya_value.iloc[0] = df_copy[column].iloc[0]
    
    for i in range(1, len(df_copy)):
        if pd.notna(abs_cmo.iloc[i]):
            adaptive_alpha = alpha * abs_cmo.iloc[i] / 100
            vidya_value.iloc[i] = (adaptive_alpha * df_copy[column].iloc[i] + 
                                 (1 - adaptive_alpha) * vidya_value.iloc[i-1])
        else:
            vidya_value.iloc[i] = vidya_value.iloc[i-1]
    
    # Apply smoothing to VIDYA
    vidya_smoothed = vidya_value.rolling(window=smooth_length).mean()
    
    # Calculate Average True Range (ATR) - TradingView compatible
    high_low = df_copy['high'] - df_copy['low']
    high_close = np.abs(df_copy['high'] - df_copy['close'].shift(1))
    low_close = np.abs(df_copy['low'] - df_copy['close'].shift(1))
    
    true_range = np.maximum(high_low, np.maximum(high_close, low_close))
    
    # Use RMA (Wilder's smoothing) instead of SMA - this is what TradingView uses
    atr = pd.Series(index=df_copy.index, dtype=float)
    atr.iloc[0] = true_range.iloc[0] if not pd.isna(true_range.iloc[0]) else 0
    
    alpha = 1.0 / atr_length  # Wilder's smoothing factor
    for i in range(1, len(df_copy)):
        if pd.notna(true_range.iloc[i]):
            atr.iloc[i] = alpha * true_range.iloc[i] + (1 - alpha) * atr.iloc[i-1]
        else:
            atr.iloc[i] = atr.iloc[i-1]
    
    # Calculate upper and lower bands
    upper_band = vidya_smoothed + atr * band_distance
    lower_band = vidya_smoothed - atr * band_distance
    
    # Detect trend direction using crossovers
    trend_up = pd.Series(False, index=df_copy.index)
    smoothed_value = pd.Series(np.nan, index=df_copy.index)
    
    for i in range(1, len(df_copy)):
        # Check for crossover above upper band (uptrend start)
        if (df_copy[column].iloc[i] > upper_band.iloc[i] and 
            df_copy[column].iloc[i-1] <= upper_band.iloc[i-1]):
            trend_up.iloc[i] = True
        # Check for crossunder below lower band (downtrend start)
        elif (df_copy[column].iloc[i] < lower_band.iloc[i] and 
              df_copy[column].iloc[i-1] >= lower_band.iloc[i-1]):
            trend_up.iloc[i] = False
        else:
            trend_up.iloc[i] = trend_up.iloc[i-1]
    
    # Set smoothed value based on trend
    for i in range(len(df_copy)):
        if trend_up.iloc[i]:
            smoothed_value.iloc[i] = lower_band.iloc[i]
        else:
            smoothed_value.iloc[i] = upper_band.iloc[i]
    
    # Detect pivot highs and lows
    pivot_highs = pd.Series(False, index=df_copy.index)
    pivot_lows = pd.Series(False, index=df_copy.index)
    
    for i in range(pivot_left_bars, len(df_copy) - pivot_right_bars):
        # Check for pivot high
        window_high = df_copy['high'].iloc[i-pivot_left_bars:i+pivot_right_bars+1]
        if df_copy['high'].iloc[i] == window_high.max():
            pivot_highs.iloc[i] = True
            
        # Check for pivot low
        window_low = df_copy['low'].iloc[i-pivot_left_bars:i+pivot_right_bars+1]
        if df_copy['low'].iloc[i] == window_low.min():
            pivot_lows.iloc[i] = True
    
    # Calculate volume analysis
    up_volume = np.where(df_copy['close'] > df_copy['open'], df_copy['volume'], 0)
    down_volume = np.where(df_copy['close'] < df_copy['open'], df_copy['volume'], 0)
    
    # Calculate trend change signals
    trend_up_prev = trend_up.shift(1).fillna(False)
    trend_change_up = trend_up & ~trend_up_prev
    trend_change_down = ~trend_up & trend_up_prev
    
    # Calculate cumulative volume during trends
    cumulative_up_volume = pd.Series(0.0, index=df_copy.index)
    cumulative_down_volume = pd.Series(0.0, index=df_copy.index)
    
    current_up_vol = 0
    current_down_vol = 0
    
    for i in range(1, len(df_copy)):
        if trend_change_up.iloc[i] or trend_change_down.iloc[i]:
            current_up_vol = 0
            current_down_vol = 0
        
        current_up_vol += up_volume[i]
        current_down_vol += down_volume[i]
        
        cumulative_up_volume.iloc[i] = current_up_vol
        cumulative_down_volume.iloc[i] = current_down_vol
    
    # Calculate volume delta percentage
    avg_volume = (cumulative_up_volume + cumulative_down_volume) / 2
    volume_delta_pct = np.where(avg_volume > 0, 
                               (cumulative_up_volume - cumulative_down_volume) / avg_volume * 100, 
                               0)
    
    # Store results
    df_copy['vidya'] = vidya_value
    df_copy['vidya_smoothed'] = vidya_smoothed
    df_copy['upper_band'] = upper_band
    df_copy['lower_band'] = lower_band
    df_copy['smoothed_value'] = smoothed_value
    df_copy['trend_up'] = trend_up.astype(int)
    df_copy['trend_change_up'] = trend_change_up.astype(int)
    df_copy['trend_change_down'] = trend_change_down.astype(int)
    df_copy['pivot_high'] = pivot_highs.astype(int)
    df_copy['pivot_low'] = pivot_lows.astype(int)
    df_copy['up_volume'] = cumulative_up_volume
    df_copy['down_volume'] = cumulative_down_volume
    df_copy['volume_delta_pct'] = volume_delta_pct
    df_copy['atr'] = atr
    
    return df_copy[['vidya', 'vidya_smoothed', 'upper_band', 'lower_band', 'smoothed_value', 
                    'trend_up', 'trend_change_up', 'trend_change_down', 'pivot_high', 'pivot_low',
                    'up_volume', 'down_volume', 'volume_delta_pct', 'atr']]


volumatic_variable_index_dynamic_average.__doc__ = """
Name:
    Volumatic Variable Index Dynamic Average (VIDYA)

Description:
    The Volumatic Variable Index Dynamic Average (VIDYA) is an advanced indicator that combines
    the Variable Index Dynamic Average with volume analysis and support/resistance detection.
    
    This indicator uses the Chande Momentum Oscillator (CMO) to determine volatility and adapts
    the moving average sensitivity accordingly. When volatility is high, VIDYA reacts faster to
    price changes. The indicator also incorporates volume analysis to identify buying and selling
    pressure, and detects pivot points for support and resistance levels.
    
    Key features:
    - Adaptive moving average based on market volatility
    - Volume-weighted trend analysis
    - Automatic support and resistance detection via pivot points
    - Dynamic upper and lower bands based on ATR
    - Trend change signals with volume confirmation

More info:
    Based on the Volumatic VIDYA indicator by BigBeluga
    Original PineScript: https://creativecommons.org/licenses/by-nc-sa/4.0/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low', 'close', 'volume' columns.
    - vidya_length (int): Length of the VIDYA calculation. Default is 10.
    - vidya_momentum (int): Momentum length for VIDYA calculation. Default is 20.
    - band_distance (float): Distance factor for upper/lower bands. Default is 2.0.
    - atr_length (int): Period for ATR calculation. Default is 200.
    - pivot_left_bars (int): Left side bars for pivot detection. Default is 3.
    - pivot_right_bars (int): Right side bars for pivot detection. Default is 3.
    - smooth_length (int): Smoothing period for VIDYA. Default is 15.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.volumatic_variable_index_dynamic_average(df)
    df['vidya'] = result['vidya']
    df['vidya_smoothed'] = result['vidya_smoothed']
    df['upper_band'] = result['upper_band']
    df['lower_band'] = result['lower_band']
    df['smoothed_value'] = result['smoothed_value']
    df['trend_up'] = result['trend_up']
    df['trend_change_up'] = result['trend_change_up']
    df['trend_change_down'] = result['trend_change_down']
    df['pivot_high'] = result['pivot_high']
    df['pivot_low'] = result['pivot_low']
    df['up_volume'] = result['up_volume']
    df['down_volume'] = result['down_volume']
    df['volume_delta_pct'] = result['volume_delta_pct']
    df['atr'] = result['atr']

Returns:
    pd.DataFrame: DataFrame with columns:
        - 'vidya': Raw VIDYA values
        - 'vidya_smoothed': Smoothed VIDYA values
        - 'upper_band': Upper band (VIDYA + ATR * distance)
        - 'lower_band': Lower band (VIDYA - ATR * distance)
        - 'smoothed_value': Trend-based smoothed value
        - 'trend_up': Binary indicator for uptrend (1) or downtrend (0)
        - 'trend_change_up': Binary indicator for trend change to up
        - 'trend_change_down': Binary indicator for trend change to down
        - 'pivot_high': Binary indicator for pivot high points
        - 'pivot_low': Binary indicator for pivot low points
        - 'up_volume': Cumulative volume during uptrends
        - 'down_volume': Cumulative volume during downtrends
        - 'volume_delta_pct': Volume delta as percentage
        - 'atr': Average True Range values
"""


def test():
    """
    Test function for the volumatic_variable_index_dynamic_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the volumatic_variable_index_dynamic_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(volumatic_variable_index_dynamic_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()