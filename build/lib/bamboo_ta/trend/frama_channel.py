# -*- coding: utf-8 -*-
# frama_channel.py
import numpy as np
import pandas as pd
import math


def frama_channel(
    df: pd.DataFrame,
    length: int = 26,
    distance: float = 1.5,
    volatility_period: int = 200,
    smoothing: int = 5,
    color_candles: bool = True,
    signals_data: str = "Price",  # "Price" or "Average Volume"
    debug: bool = False
) -> pd.DataFrame:
    """FRAMA Channel"""
    
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    if signals_data == "Average Volume" and "volume" not in df.columns:
        required_columns.append("volume")
    
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Length must be even for FRAMA calculation
    N = length
    if N % 2 != 0:
        N = N + 1
    
    # Source price (hl2 equivalent)
    price = (df_copy['high'] + df_copy['low']) / 2
    
    # Calculate volatility using SMA of (high - low)
    volatility = (df_copy['high'] - df_copy['low']).rolling(window=volatility_period).mean()
    
    # Initialize FRAMA calculation
    frama_raw = []
    
    # Debug storage
    if debug:
        debug_info = []
    
    for i in range(len(df_copy)):
        current_price = price.iloc[i]
        
        if i == 0:
            # First bar: initialize with price
            frama_val = current_price
        elif i < N:
            # Early bars: simple initialization
            if len(frama_raw) > 0:
                alpha = 2.0 / (i + 1)
                frama_val = alpha * current_price + (1 - alpha) * frama_raw[-1]
            else:
                frama_val = current_price
        else:
            # Full FRAMA calculation for bars >= N
            window_start = i - N + 1
            highs = df_copy['high'].iloc[window_start:i+1].values
            lows = df_copy['low'].iloc[window_start:i+1].values
            
            # Calculate N3 (price range over entire period divided by N)
            highest_high = np.max(highs)
            lowest_low = np.min(lows)
            n3 = (highest_high - lowest_low) / N
            
            # Calculate N1 (first half range)
            half_n = N // 2
            hh1 = highs[0]
            ll1 = lows[0]
            
            for count in range(half_n):
                if highs[count] > hh1:
                    hh1 = highs[count]
                if lows[count] < ll1:
                    ll1 = lows[count]
            
            n1 = (hh1 - ll1) / half_n
            
            # Calculate N2 (second half range)
            hh2 = highs[half_n]
            ll2 = lows[half_n]
            
            for count in range(half_n, N):
                if highs[count] > hh2:
                    hh2 = highs[count]
                if lows[count] < ll2:
                    ll2 = lows[count]
            
            n2 = (hh2 - ll2) / half_n
            
            # Calculate fractal dimension
            if n1 > 0 and n2 > 0 and n3 > 0:
                try:
                    dimen = (math.log(n1 + n2) - math.log(n3)) / math.log(2)
                except (ValueError, ZeroDivisionError):
                    dimen = 1.0
            else:
                dimen = 1.0
            
            # Calculate alpha
            alpha = math.exp(-4.6 * (dimen - 1))
            alpha = max(min(alpha, 1.0), 0.01)
            
            # Calculate FRAMA
            prev_frama = frama_raw[-1] if frama_raw else current_price
            frama_val = alpha * current_price + (1 - alpha) * prev_frama
            
            # Store debug info for key periods
            if debug and i >= len(df_copy) - 5:  # Last 5 values
                debug_info.append({
                    'index': i,
                    'bar_index': i,
                    'price': current_price,
                    'n1': n1,
                    'n2': n2,
                    'n3': n3,
                    'dimen': dimen,
                    'alpha': alpha,
                    'frama_raw': frama_val,
                    'prev_frama': prev_frama
                })
        
        frama_raw.append(frama_val)
    
    # Convert to pandas Series
    frama_raw_series = pd.Series(frama_raw, index=df_copy.index)
    
    # Apply Pine Script smoothing logic:
    # ta.sma((bar_index < N + 1) ? price : Filt, 5)
    pre_smooth_series = []
    for i in range(len(df_copy)):
        if i < N + 1:  # bar_index < N + 1
            pre_smooth_series.append(price.iloc[i])
        else:
            pre_smooth_series.append(frama_raw_series.iloc[i])
    
    # Apply SMA(5)
    pre_smooth = pd.Series(pre_smooth_series, index=df_copy.index)
    frama_final = pre_smooth.rolling(window=smoothing, min_periods=1).mean()
    
    # Calculate channel bands
    upper_band = frama_final + volatility * distance
    lower_band = frama_final - volatility * distance
    
    # Calculate signals data based on user choice
    if signals_data == "Average Volume" and "volume" in df_copy.columns:
        signal_values = df_copy['volume'].rolling(window=10).mean()
    else:
        signal_values = df_copy['close']
    
    # Calculate hlc3 for breakout detection
    hlc3 = (df_copy['high'] + df_copy['low'] + df_copy['close']) / 3
    
    # Breakout conditions
    break_up = (hlc3 > upper_band) & (hlc3.shift(1) <= upper_band.shift(1))
    break_down = (hlc3 < lower_band) & (hlc3.shift(1) >= lower_band.shift(1))
    
    # Cross detection for neutral state
    close_cross_frama = ((df_copy['close'] > frama_final) & (df_copy['close'].shift(1) <= frama_final.shift(1))) | \
                       ((df_copy['close'] < frama_final) & (df_copy['close'].shift(1) >= frama_final.shift(1)))
    
    # Color logic
    color_state = pd.Series(index=df_copy.index, dtype='object')
    color_state[:] = 'neutral'
    
    for i in range(len(df_copy)):
        if i == 0:
            color_state.iloc[i] = 'neutral'
        else:
            color_state.iloc[i] = color_state.iloc[i-1]
            
            if close_cross_frama.iloc[i]:
                color_state.iloc[i] = 'neutral'
            
            if break_up.iloc[i]:
                color_state.iloc[i] = 'up'
            elif break_down.iloc[i]:
                color_state.iloc[i] = 'down'
    
    # Signal labels with counting logic
    signal_up = pd.Series(0, index=df_copy.index)
    signal_down = pd.Series(0, index=df_copy.index)
    signal_up_value = pd.Series(np.nan, index=df_copy.index)
    signal_down_value = pd.Series(np.nan, index=df_copy.index)
    
    count1 = 0
    count2 = 0
    
    for i in range(len(df_copy)):
        if break_up.iloc[i]:
            count2 = 0
            count1 += 1
            if count1 == 1:
                signal_up.iloc[i] = 1
                signal_up_value.iloc[i] = signal_values.iloc[i]
        
        if break_down.iloc[i]:
            count1 = 0
            count2 += 1
            if count2 == 1:
                signal_down.iloc[i] = 1
                signal_down_value.iloc[i] = signal_values.iloc[i]
    
    # Debug output
    if debug:
        print("=== FRAMA Channel Debug Information ===")
        print(f"Length (N): {N}")
        print(f"Distance: {distance}")
        print(f"Volatility Period: {volatility_period}")
        print(f"Smoothing: {smoothing}")
        print(f"Signals Data: {signals_data}")
        
        print("\nLast few FRAMA calculations:")
        for info in debug_info:
            print(f"Bar Index {info['bar_index']}: Price={info['price']:.2f}, "
                  f"N1={info['n1']:.6f}, N2={info['n2']:.6f}, N3={info['n3']:.6f}, "
                  f"Dimen={info['dimen']:.6f}, Alpha={info['alpha']:.6f}, "
                  f"FRAMA Raw={info['frama_raw']:.2f}")
        
        # Show final values comparison
        print(f"\nFinal FRAMA values (last 5):")
        for i in range(max(0, len(frama_final)-5), len(frama_final)):
            print(f"Index {i}: Raw FRAMA={frama_raw_series.iloc[i]:.2f}, "
                  f"Final FRAMA={frama_final.iloc[i]:.2f}")
    
    # Create result DataFrame
    result = pd.DataFrame(index=df_copy.index)
    result['frama'] = frama_final
    result['frama_upper'] = upper_band
    result['frama_lower'] = lower_band
    result['frama_volatility'] = volatility
    result['frama_breakout_up'] = break_up.astype(int)
    result['frama_breakout_down'] = break_down.astype(int)
    result['frama_signal_up'] = signal_up
    result['frama_signal_down'] = signal_down
    result['frama_signal_up_value'] = signal_up_value
    result['frama_signal_down_value'] = signal_down_value
    result['frama_color'] = color_state
    result['frama_raw'] = frama_raw_series
    result['frama_pre_smooth'] = pre_smooth
    result['hlc3'] = hlc3
    result['close_cross_frama'] = close_cross_frama.astype(int)
    
    if color_candles:
        result['candle_color'] = color_state
    
    return result


frama_channel.__doc__ = """
Name:
    FRAMA Channel

Description:
    The FRAMA Channel is a trend-following indicator that utilizes the Fractal Adaptive 
    Moving Average (FRAMA) to create a dynamic channel around the price. The indicator 
    helps identify uptrends, downtrends, and ranging markets by examining the relationship 
    between the price and the channel's boundaries.
    
    Key Features:
    - Dynamic FRAMA Channel with adaptive sensitivity based on market fractal dimension
    - Trend change signals with arrows showing price or average volume
    - Ranging market detection when price stays within channel bounds
    - Color-coded candles and channel bands for visual trend identification
    - Customizable display of price or average volume at trend change points
    
    The indicator adapts to market conditions:
    - In trending markets: Less sensitive to reduce noise
    - In ranging markets: More sensitive to capture price movements
    - Neutral detection: When price crosses the FRAMA line without band breakout

More info:
    Based on BigBeluga's FRAMA Channel indicator for TradingView
    https://www.tradingview.com/script/frama-channel-bigbeluga/
    
    The core idea uses the fractal nature of markets to adapt to different conditions.
    When price crosses upper/lower bands, it signals trend shifts. If price remains
    within the channel, the market is likely in a ranging phase with low momentum.

Parameters:
    - df (pandas.DataFrame): Input DataFrame with 'open', 'high', 'low', 'close' columns.
        If signals_data="Average Volume", 'volume' column is also required.
    - length (int): Period for FRAMA calculation. Will be made even if odd. Default is 26.
    - distance (float): Multiplier for channel band distance from FRAMA line. Default is 1.5.
    - volatility_period (int): Period for volatility calculation (SMA of high-low). Default is 200.
    - smoothing (int): Period for final SMA smoothing of FRAMA line. Default is 5.
    - color_candles (bool): Whether to include candle coloring information. Default is True.
    - signals_data (str): Display "Price" or "Average Volume" in signals. Default is "Price".
    - debug (bool): If True, prints detailed calculation information. Default is False.

Call with:
    frama_result = bta.frama_channel(df, length=26, distance=1.5, signals_data="Price")
    df['frama'] = frama_result['frama']
    df['frama_upper'] = frama_result['frama_upper']
    df['frama_lower'] = frama_result['frama_lower']
    df['frama_color'] = frama_result['frama_color']  # 'up', 'down', 'neutral'
    df['frama_signal_up'] = frama_result['frama_signal_up']
    df['frama_signal_down'] = frama_result['frama_signal_down']

Returns:
    pd.DataFrame: DataFrame with the following columns:
        - 'frama': Main FRAMA line (adaptive moving average with smoothing)
        - 'frama_upper': Upper channel band
        - 'frama_lower': Lower channel band  
        - 'frama_volatility': Volatility values used for bands
        - 'frama_breakout_up': All upward breakouts (1/0)
        - 'frama_breakout_down': All downward breakouts (1/0)
        - 'frama_signal_up': First upward signal in sequence (1/0)
        - 'frama_signal_down': First downward signal in sequence (1/0)
        - 'frama_signal_up_value': Price/volume value at up signals
        - 'frama_signal_down_value': Price/volume value at down signals
        - 'frama_color': Trend state ('up'/'down'/'neutral')
        - 'frama_raw': Raw FRAMA before final smoothing
        - 'frama_pre_smooth': Series before SMA smoothing
        - 'hlc3': Typical price used for breakout detection
        - 'close_cross_frama': Close crossing FRAMA line (1/0)
        - 'candle_color': Candle coloring info (if color_candles=True)
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