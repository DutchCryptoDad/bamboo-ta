# -*- coding: utf-8 -*-
# candlestick_patterns.py
import pandas as pd
import numpy as np

def safe_divide(a, b, default=0):
    """Safely divide a by b, returning default if b is 0 or if result is NaN."""
    if np.isscalar(b):
        return default if b == 0 else a / b
    else:
        result = a / b
        result[b == 0] = default
        return result

def safe_compare(a, b, comparison='<', tolerance=0):
    """Safely compare a and b, handling NaN values."""
    if comparison == '<':
        return (a < b) & ~np.isnan(a) & ~np.isnan(b)
    elif comparison == '>':
        return (a > b) & ~np.isnan(a) & ~np.isnan(b)
    elif comparison == '==':
        if tolerance > 0:
            return (np.abs(a - b) < tolerance) & ~np.isnan(a) & ~np.isnan(b)
        else:
            return (a == b) & ~np.isnan(a) & ~np.isnan(b)
    # Add more comparisons as needed

def candlestick_patterns(df, include_indicators=False):
    """Detects candlestick types and patterns"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Add volume column check for volume-based patterns
    has_volume = "volume" in df.columns
    
    # Calculate basic candlestick properties
    df_copy['body_size'] = abs(df_copy["close"] - df_copy["open"])
    df_copy['total_range'] = df_copy["high"] - df_copy["low"]
    # Avoid division by zero
    df_copy['total_range'] = df_copy['total_range'].replace(0, np.nan)
    
    # Calculate shadows
    df_copy['lower_shadow'] = df_copy[["open", "close"]].min(axis=1) - df_copy["low"]
    df_copy['upper_shadow'] = df_copy["high"] - df_copy[["open", "close"]].max(axis=1)
    
    # Calculate relative sizes
    df_copy['body_percent'] = df_copy['body_size'] / df_copy['total_range']
    df_copy['upper_shadow_percent'] = df_copy['upper_shadow'] / df_copy['total_range']
    df_copy['lower_shadow_percent'] = df_copy['lower_shadow'] / df_copy['total_range']
    
    # Bullish/Bearish basic classification
    df_copy['is_bullish'] = df_copy["close"] > df_copy["open"]
    df_copy['is_bearish'] = df_copy["close"] < df_copy["open"]
    
    # Previous candle data
    df_copy['prev_open'] = df_copy["open"].shift(1)
    df_copy['prev_high'] = df_copy["high"].shift(1)
    df_copy['prev_low'] = df_copy["low"].shift(1)
    df_copy['prev_close'] = df_copy["close"].shift(1)
    df_copy['prev_body_size'] = df_copy['body_size'].shift(1)
    df_copy['prev_total_range'] = df_copy['total_range'].shift(1)
    df_copy['prev_is_bullish'] = df_copy['is_bullish'].shift(1)
    df_copy['prev_is_bearish'] = df_copy['is_bearish'].shift(1)
    df_copy['prev_body_percent'] = df_copy['body_percent'].shift(1)
    df_copy['prev_upper_shadow_percent'] = df_copy['upper_shadow_percent'].shift(1)
    df_copy['prev_lower_shadow_percent'] = df_copy['lower_shadow_percent'].shift(1)
    
    # Two candles back
    df_copy['prev2_open'] = df_copy["open"].shift(2)
    df_copy['prev2_high'] = df_copy["high"].shift(2)
    df_copy['prev2_low'] = df_copy["low"].shift(2)
    df_copy['prev2_close'] = df_copy["close"].shift(2)
    df_copy['prev2_is_bullish'] = df_copy['is_bullish'].shift(2)
    df_copy['prev2_is_bearish'] = df_copy['is_bearish'].shift(2)
    df_copy['prev2_body_percent'] = df_copy['body_percent'].shift(2)
    df_copy['prev2_body_size'] = df_copy['body_size'].shift(2)  # Add this line
    
    # Three candles back
    df_copy['prev3_open'] = df_copy["open"].shift(3)
    df_copy['prev3_high'] = df_copy["high"].shift(3)
    df_copy['prev3_low'] = df_copy["low"].shift(3)
    df_copy['prev3_close'] = df_copy["close"].shift(3)
    df_copy['prev3_is_bullish'] = df_copy['is_bullish'].shift(3)
    df_copy['prev3_is_bearish'] = df_copy['is_bearish'].shift(3)
    df_copy['prev3_body_size'] = df_copy['body_size'].shift(3)
    df_copy['prev3_body_percent'] = df_copy['body_percent'].shift(3)
    
    # Four candles back
    df_copy['prev4_open'] = df_copy["open"].shift(4)
    df_copy['prev4_high'] = df_copy["high"].shift(4)
    df_copy['prev4_low'] = df_copy["low"].shift(4)
    df_copy['prev4_close'] = df_copy["close"].shift(4)
    df_copy['prev4_is_bullish'] = df_copy['is_bullish'].shift(4)
    df_copy['prev4_is_bearish'] = df_copy['is_bearish'].shift(4)
    df_copy['prev4_body_size'] = df_copy['body_size'].shift(4)
    df_copy['prev4_body_percent'] = df_copy['body_percent'].shift(4)
    
    # Five candles back
    df_copy['prev5_open'] = df_copy["open"].shift(5)
    df_copy['prev5_high'] = df_copy["high"].shift(5)
    df_copy['prev5_low'] = df_copy["low"].shift(5)
    df_copy['prev5_close'] = df_copy["close"].shift(5)
    df_copy['prev5_is_bullish'] = df_copy['is_bullish'].shift(5)
    df_copy['prev5_is_bearish'] = df_copy['is_bearish'].shift(5)
    df_copy['prev5_body_size'] = df_copy['body_size'].shift(5)
    df_copy['prev5_body_percent'] = df_copy['body_percent'].shift(5)
    
    # Initialize result columns
    candle_type = pd.Series("", index=df_copy.index)
    candle_pattern = pd.Series("", index=df_copy.index)
    
    #---------------------------------------------------------------------------
    # 1. SINGLE CANDLESTICK PATTERNS
    #---------------------------------------------------------------------------
    
    # DOJI VARIATIONS
    
    # Standard Doji - very small body
    doji_condition = (df_copy['body_percent'] < 0.1)
    
    # Long-legged Doji - small body with long upper and lower shadows
    long_legged_doji_condition = (
        doji_condition & 
        (df_copy['upper_shadow_percent'] > 0.3) & 
        (df_copy['lower_shadow_percent'] > 0.3)
    )
    
    # Dragonfly Doji - small body at the top with long lower shadow
    dragonfly_doji_condition = (
        doji_condition & 
        (df_copy['lower_shadow_percent'] > 0.6) & 
        (df_copy['upper_shadow_percent'] < 0.1)
    )
    
    # Gravestone Doji - small body at the bottom with long upper shadow
    gravestone_doji_condition = (
        doji_condition & 
        (df_copy['upper_shadow_percent'] > 0.6) & 
        (df_copy['lower_shadow_percent'] < 0.1)
    )
    
    # Four-Price Doji - open, high, low, and close are all equal (or very close)
    four_price_doji_condition = (
        (df_copy['total_range'] / df_copy['close'] < 0.0005) &  # Range is less than 0.05% of price
        (df_copy['body_size'] / df_copy['close'] < 0.0001)      # Body is less than 0.01% of price
    )
    
    # STRONG TREND CANDLES
    
    # Marubozu - candle with no or very small shadows
    bullish_marubozu_condition = (
        df_copy['is_bullish'] &
        (df_copy['body_percent'] > 0.9) &  # Large body
        (df_copy['lower_shadow_percent'] < 0.05) &  # Very small or no lower shadow
        (df_copy['upper_shadow_percent'] < 0.05)    # Very small or no upper shadow
    )
    
    bearish_marubozu_condition = (
        df_copy['is_bearish'] &
        (df_copy['body_percent'] > 0.9) &  # Large body
        (df_copy['lower_shadow_percent'] < 0.05) &  # Very small or no lower shadow
        (df_copy['upper_shadow_percent'] < 0.05)    # Very small or no upper shadow
    )
    
    # Spinning Top - small body with significant upper and lower shadows
    spinning_top_condition = (
        (df_copy['body_percent'] < 0.3) &  # Small body
        (df_copy['lower_shadow_percent'] > 0.2) &  # Significant lower shadow
        (df_copy['upper_shadow_percent'] > 0.2)    # Significant upper shadow
    )
    
    # REVERSAL CANDLES
    
    # Hammer - small body at the top with long lower shadow
    hammer_condition = (
        df_copy['is_bullish'] &
        (df_copy['body_percent'] < 0.3) &  # Small body
        (df_copy['lower_shadow_percent'] > 0.6) &  # Long lower shadow
        (df_copy['upper_shadow_percent'] < 0.1)    # Very short upper shadow
    )
    
    # Inverted Hammer - small body at the bottom with long upper shadow
    inverted_hammer_condition = (
        df_copy['is_bullish'] &
        (df_copy['body_percent'] < 0.3) &  # Small body
        (df_copy['upper_shadow_percent'] > 0.6) &  # Long upper shadow
        (df_copy['lower_shadow_percent'] < 0.1)    # Very short lower shadow
    )
    
    # Hanging Man - small body at the top with long lower shadow (bearish)
    hanging_man_condition = (
        df_copy['is_bearish'] &
        (df_copy['body_percent'] < 0.3) &  # Small body
        (df_copy['lower_shadow_percent'] > 0.6) &  # Long lower shadow
        (df_copy['upper_shadow_percent'] < 0.1)    # Very short upper shadow
    )
    
    # Shooting Star - small body at the bottom with long upper shadow (bearish)
    shooting_star_condition = (
        df_copy['is_bearish'] &
        (df_copy['body_percent'] < 0.3) &  # Small body
        (df_copy['upper_shadow_percent'] > 0.6) &  # Long upper shadow
        (df_copy['lower_shadow_percent'] < 0.1)    # Very short lower shadow
    )
    
    # Belt Hold - long body with no or very small shadow on one side
    bullish_belt_hold_condition = (
        df_copy['is_bullish'] &
        (df_copy['body_percent'] > 0.7) &  # Large body
        (df_copy['lower_shadow_percent'] < 0.05)  # Very small or no lower shadow
    )
    
    bearish_belt_hold_condition = (
        df_copy['is_bearish'] &
        (df_copy['body_percent'] > 0.7) &  # Large body
        (df_copy['upper_shadow_percent'] < 0.05)  # Very small or no upper shadow
    )
    
    # High Wave Candle - extreme volatility with small body and very long shadows
    high_wave_condition = (
        (df_copy['body_percent'] < 0.2) &  # Very small body
        (df_copy['upper_shadow_percent'] > 0.4) &  # Very long upper shadow
        (df_copy['lower_shadow_percent'] > 0.4)    # Very long lower shadow
    )
    
    #---------------------------------------------------------------------------
    # 2. TWO-CANDLESTICK PATTERNS
    #---------------------------------------------------------------------------
    
    # REVERSAL PATTERNS
    
    # Bullish Engulfing
    bullish_engulfing_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (df_copy["open"] < df_copy["prev_close"]) &  # Current open below previous close
        (df_copy["close"] > df_copy["prev_open"])    # Current close above previous open
    )
    
    # Bearish Engulfing
    bearish_engulfing_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        (df_copy["open"] > df_copy["prev_close"]) &  # Current open above previous close
        (df_copy["close"] < df_copy["prev_open"])    # Current close below previous open
    )
    
    # Piercing Line - bullish reversal after downtrend
    piercing_line_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (df_copy["open"] < df_copy["prev_low"]) &  # Current open below previous low
        (df_copy["close"] > (df_copy["prev_open"] + df_copy["prev_close"]) / 2) &  # Close above midpoint
        (df_copy["close"] < df_copy["prev_open"])  # But not above previous open
    )
    
    # Dark Cloud Cover - bearish reversal after uptrend
    dark_cloud_cover_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        (df_copy["open"] > df_copy["prev_high"]) &  # Current open above previous high
        (df_copy["close"] < (df_copy["prev_open"] + df_copy["prev_close"]) / 2) &  # Close below midpoint
        (df_copy["close"] > df_copy["prev_open"])  # But not below previous open
    )
    
    # Bullish Harami - small bullish candle contained within previous bearish candle
    bullish_harami_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (df_copy["open"] > df_copy["prev_close"]) &  # Current open above previous close
        (df_copy["close"] < df_copy["prev_open"]) &  # Current close below previous open
        (df_copy['body_size'] < df_copy['prev_body_size'] * 0.6)  # Current body smaller than previous
    )
    
    # Bearish Harami - small bearish candle contained within previous bullish candle
    bearish_harami_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        (df_copy["open"] < df_copy["prev_close"]) &  # Current open below previous close
        (df_copy["close"] > df_copy["prev_open"]) &  # Current close above previous open
        (df_copy['body_size'] < df_copy['prev_body_size'] * 0.6)  # Current body smaller than previous
    )
    
    # Harami Cross - harami with doji as the second candle (stronger signal)
    bullish_harami_cross_condition = (
        bullish_harami_condition &
        doji_condition  # Second candle is a doji
    )
    
    bearish_harami_cross_condition = (
        bearish_harami_condition &
        doji_condition  # Second candle is a doji
    )
    
    # Tweezer Tops - bearish reversal with two candles having same/similar highs
    tweezer_tops_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        (abs(df_copy["high"] - df_copy["prev_high"]) / df_copy["high"] < 0.001)  # Same/similar highs
    )
    
    # Tweezer Bottoms - bullish reversal with two candles having same/similar lows
    tweezer_bottoms_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (abs(df_copy["low"] - df_copy["prev_low"]) / df_copy["low"] < 0.001)  # Same/similar lows
    )
    
    # GAP-BASED PATTERNS
    
    # Up Gap Side-by-Side White Lines - bullish continuation
    up_gap_side_by_side_white_lines_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        (df_copy["low"] > df_copy["prev_high"]) &  # Gap up
        (abs(df_copy['body_size'] - df_copy['prev_body_size']) / df_copy['body_size'] < 0.1)  # Similar body sizes
    )
    
    # Down Gap Side-by-Side White Lines - bearish continuation
    down_gap_side_by_side_white_lines_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (df_copy["high"] < df_copy["prev_low"]) &  # Gap down
        (abs(df_copy['body_size'] - df_copy['prev_body_size']) / df_copy['body_size'] < 0.1)  # Similar body sizes
    )
    
    #---------------------------------------------------------------------------
    # 3. THREE-CANDLESTICK PATTERNS
    #---------------------------------------------------------------------------
    
    # STRONG REVERSAL PATTERNS
    
    # Morning Star - bullish reversal
    morning_star_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev2_is_bearish'] &  # First candle is bearish
        (df_copy['prev_body_percent'] < 0.3) &  # Second candle has small body
        (df_copy["prev_high"] < df_copy["prev2_low"]) &  # Gap down between first and second
        (df_copy["close"] > (df_copy["prev2_open"] + df_copy["prev2_close"]) / 2)  # Close into first candle body
    )
    
    # Evening Star - bearish reversal
    evening_star_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev2_is_bullish'] &  # First candle is bullish
        (df_copy['prev_body_percent'] < 0.3) &  # Second candle has small body
        (df_copy["prev_low"] > df_copy["prev2_high"]) &  # Gap up between first and second
        (df_copy["close"] < (df_copy["prev2_open"] + df_copy["prev2_close"]) / 2)  # Close into first candle body
    )
    
    # Three White Soldiers - strong bullish reversal
    three_white_soldiers_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        df_copy['prev2_is_bullish'] &  # Two candles back is bullish
        (df_copy["open"] > df_copy["prev_open"]) &  # Each open higher than previous
        (df_copy["prev_open"] > df_copy["prev2_open"]) &
        (df_copy["close"] > df_copy["prev_close"]) &  # Each close higher than previous
        (df_copy["prev_close"] > df_copy["prev2_close"]) &
        (df_copy['body_percent'] > 0.6) &  # All have large bodies
        (df_copy['prev_body_percent'] > 0.6) &
        (df_copy['prev2_body_percent'] > 0.6)
    )
    
    # Three Black Crows - strong bearish reversal
    three_black_crows_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        df_copy['prev2_is_bearish'] &  # Two candles back is bearish
        (df_copy["open"] < df_copy["prev_open"]) &  # Each open lower than previous
        (df_copy["prev_open"] < df_copy["prev2_open"]) &
        (df_copy["close"] < df_copy["prev_close"]) &  # Each close lower than previous
        (df_copy["prev_close"] < df_copy["prev2_close"]) &
        (df_copy['body_percent'] > 0.6) &  # All have large bodies
        (df_copy['prev_body_percent'] > 0.6) &
        (df_copy['prev2_body_percent'] > 0.6)
    )
    
    # Three Inside Up - bullish reversal
    three_inside_up_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        bullish_harami_condition.shift(1) &  # Previous two candles form a bullish harami
        (df_copy["close"] > df_copy["prev_close"])  # Current close higher than previous
    )
    
    # Three Inside Down - bearish reversal
    three_inside_down_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        bearish_harami_condition.shift(1) &  # Previous two candles form a bearish harami
        (df_copy["close"] < df_copy["prev_close"])  # Current close lower than previous
    )
    
    # Three Outside Up - bullish reversal
    three_outside_up_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        bullish_engulfing_condition.shift(1) &  # Previous two candles form a bullish engulfing
        (df_copy["close"] > df_copy["prev_close"])  # Current close higher than previous
    )
    
    # Three Outside Down - bearish reversal
    three_outside_down_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        bearish_engulfing_condition.shift(1) &  # Previous two candles form a bearish engulfing
        (df_copy["close"] < df_copy["prev_close"])  # Current close lower than previous
    )
    
    # CONTINUATION PATTERNS
    
    # Rising Three Methods - bullish continuation
    rising_three_methods_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish (5th)
        df_copy['prev4_is_bullish'] &  # First candle is bullish
        df_copy['prev_is_bearish'] &  # 4th candle is bearish
        df_copy['prev2_is_bearish'] &  # 3rd candle is bearish
        df_copy['prev3_is_bearish'] &  # 2nd candle is bearish
        (df_copy["prev4_body_size"] > df_copy["prev3_body_size"]) &  # First candle has larger body
        (df_copy["prev4_body_size"] > df_copy["prev2_body_size"]) &
        (df_copy["prev4_body_size"] > df_copy["prev_body_size"]) &
        (df_copy["prev_high"] < df_copy["prev4_high"]) &  # Middle candles stay within first candle's range
        (df_copy["prev2_high"] < df_copy["prev4_high"]) &
        (df_copy["prev3_high"] < df_copy["prev4_high"]) &
        (df_copy["prev_low"] > df_copy["prev4_low"]) &
        (df_copy["prev2_low"] > df_copy["prev4_low"]) &
        (df_copy["prev3_low"] > df_copy["prev4_low"]) &
        (df_copy["close"] > df_copy["prev4_high"])  # Current close above first candle's high
    )
    
    # Falling Three Methods - bearish continuation
    falling_three_methods_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish (5th)
        df_copy['prev4_is_bearish'] &  # First candle is bearish
        df_copy['prev_is_bullish'] &  # 4th candle is bullish
        df_copy['prev2_is_bullish'] &  # 3rd candle is bullish
        df_copy['prev3_is_bullish'] &  # 2nd candle is bullish
        (df_copy["prev4_body_size"] > df_copy["prev3_body_size"]) &  # First candle has larger body
        (df_copy["prev4_body_size"] > df_copy["prev2_body_size"]) &
        (df_copy["prev4_body_size"] > df_copy["prev_body_size"]) &
        (df_copy["prev_high"] < df_copy["prev4_high"]) &  # Middle candles stay within first candle's range
        (df_copy["prev2_high"] < df_copy["prev4_high"]) &
        (df_copy["prev3_high"] < df_copy["prev4_high"]) &
        (df_copy["prev_low"] > df_copy["prev4_low"]) &
        (df_copy["prev2_low"] > df_copy["prev4_low"]) &
        (df_copy["prev3_low"] > df_copy["prev4_low"]) &
        (df_copy["close"] < df_copy["prev4_low"])  # Current close below first candle's low
    )
    
    # Advance Block - weakening bullish trend
    advance_block_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        df_copy['prev2_is_bullish'] &  # Two candles back is bullish
        (df_copy["close"] > df_copy["prev_close"]) &  # Each close higher than previous
        (df_copy["prev_close"] > df_copy["prev2_close"]) &
        (df_copy['body_percent'] < df_copy['prev_body_percent']) &  # Decreasing body size
        (df_copy['prev_body_percent'] < df_copy['prev2_body_percent']) &
        (df_copy['upper_shadow_percent'] > df_copy['prev_upper_shadow_percent'])  # Increasing upper shadows
    )
    
    # Deliberation - reversal warning after uptrend
    deliberation_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish or doji
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        df_copy['prev2_is_bullish'] &  # Two candles back is bullish
        (df_copy["close"] > df_copy["prev_close"]) &  # Each close higher than previous
        (df_copy["prev_close"] > df_copy["prev2_close"]) &
        (df_copy['body_percent'] < 0.3) &  # Current candle has small body
        (df_copy['prev_body_percent'] > 0.5) &  # Previous candles have larger bodies
        (df_copy['prev2_body_percent'] > 0.5)
    )
    
    #---------------------------------------------------------------------------
    # 4. RARE & ADVANCED CANDLESTICK PATTERNS
    #---------------------------------------------------------------------------
    
    # MULTI-CANDLE TREND REVERSAL PATTERNS
    
    # Abandoned Baby Bullish - bullish reversal with gaps
    abandoned_baby_bullish_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        doji_condition.shift(1) &  # Middle candle is doji
        df_copy['prev2_is_bearish'] &  # First candle is bearish
        (df_copy["prev_high"] < df_copy["prev2_low"]) &  # Gap down between first and doji
        (df_copy["low"] > df_copy["prev_high"])  # Gap up between doji and current
    )
    
    # Abandoned Baby Bearish - bearish reversal with gaps
    abandoned_baby_bearish_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        doji_condition.shift(1) &  # Middle candle is doji
        df_copy['prev2_is_bullish'] &  # First candle is bullish
        (df_copy["prev_low"] > df_copy["prev2_high"]) &  # Gap up between first and doji
        (df_copy["high"] < df_copy["prev_low"])  # Gap down between doji and current
    )
    
    # Island Reversal Bullish - isolated low with gaps on both sides
    island_reversal_bullish_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        (df_copy["low"] > df_copy["prev_high"]) &  # Gap up from previous
        (df_copy["prev2_low"] > df_copy["prev_high"])  # Previous candle gapped down and is isolated
    )
    
    # Island Reversal Bearish - isolated high with gaps on both sides
    island_reversal_bearish_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        (df_copy["high"] < df_copy["prev_low"]) &  # Gap down from previous
        (df_copy["prev2_high"] < df_copy["prev_low"])  # Previous candle gapped up and is isolated
    )
    
    # Unique Three River Bottom - bullish reversal
    unique_three_river_bottom_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish with small body
        (df_copy['body_percent'] < 0.3) &
        df_copy['prev_is_bearish'] &  # Previous candle is bearish with low below first candle
        (df_copy["prev_low"] < df_copy["prev2_low"]) &
        df_copy['prev2_is_bearish'] &  # First candle is bearish with long body
        (df_copy['prev2_body_percent'] > 0.6) &
        (df_copy["close"] < df_copy["prev_open"])  # Current close below previous open
    )
    
    # Concealing Baby Swallow - rare bearish reversal
    concealing_baby_swallow_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish and engulfs previous
        (df_copy["high"] > df_copy["prev_high"]) &
        (df_copy["low"] < df_copy["prev_low"]) &
        df_copy['prev_is_bearish'] &  # Previous candle is bearish with upper shadow inside first candle
        (df_copy["prev_high"] > df_copy["prev2_open"]) &
        (df_copy["prev_high"] < df_copy["prev2_close"]) &
        df_copy['prev2_is_bearish'] &  # First candle is bearish
        df_copy['prev3_is_bearish']  # Candle before first is bearish (confirming downtrend)
    )
    
    # Hook Reversal Bullish - bullish reversal after downtrend
    hook_reversal_bullish_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (df_copy["open"] < df_copy["prev_close"]) &  # Open below previous close
        (df_copy["close"] > df_copy["prev_close"]) &  # Close above previous close
        (df_copy["close"] < df_copy["prev_open"])  # But not above previous open
    )
    
    # Hook Reversal Bearish - bearish reversal after uptrend
    hook_reversal_bearish_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        (df_copy["open"] > df_copy["prev_close"]) &  # Open above previous close
        (df_copy["close"] < df_copy["prev_close"]) &  # Close below previous close
        (df_copy["close"] > df_copy["prev_open"])  # But not below previous open
    )
    
    # Fry Pan Bottom (Rounded Bottom) - bullish reversal
    # This is a complex pattern typically spanning 10+ candles
    # Simplified detection looking for key characteristics
    fry_pan_bottom_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish with strong body
        (df_copy['body_percent'] > 0.6) &
        (df_copy["close"] > df_copy["prev_high"]) &  # Breakout above previous high
        (df_copy["prev_low"] < df_copy["prev2_low"]) &  # Previous formed a higher low
        (df_copy["prev2_low"] < df_copy["prev3_low"]) &  # Series of higher lows
        (df_copy["prev3_low"] < df_copy["prev4_low"]) &
        (df_copy["prev4_low"] < df_copy["prev5_low"])
    )
    
    # Dumpling Top (Rounded Top) - bearish reversal
    # This is a complex pattern typically spanning 10+ candles
    # Simplified detection looking for key characteristics
    dumpling_top_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish with strong body
        (df_copy['body_percent'] > 0.6) &
        (df_copy["close"] < df_copy["prev_low"]) &  # Breakout below previous low
        (df_copy["prev_high"] > df_copy["prev2_high"]) &  # Previous formed a lower high
        (df_copy["prev2_high"] > df_copy["prev3_high"]) &  # Series of lower highs
        (df_copy["prev3_high"] > df_copy["prev4_high"]) &
        (df_copy["prev4_high"] > df_copy["prev5_high"])
    )
    
    # MULTI-CANDLE CONTINUATION PATTERNS
    
    # Separating Lines Bullish - bullish continuation
    separating_lines_bullish_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (abs(df_copy["open"] - df_copy["prev_open"]) / df_copy["open"] < 0.001) &  # Same/similar opens
        (df_copy["close"] > df_copy["prev_open"])  # Current close above open
    )
    
    # Separating Lines Bearish - bearish continuation
    separating_lines_bearish_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        (abs(df_copy["open"] - df_copy["prev_open"]) / df_copy["open"] < 0.001) &  # Same/similar opens
        (df_copy["close"] < df_copy["prev_open"])  # Current close below open
    )
    
    # On Neck Line - bearish continuation
    on_neck_line_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (abs(df_copy["close"] - df_copy["prev_low"]) / df_copy["close"] < 0.001)  # Close at previous low
    )
    
    # In Neck Line - weak bearish continuation
    in_neck_line_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (df_copy["close"] > df_copy["prev_low"]) &  # Close slightly above previous low
        (df_copy["close"] < df_copy["prev_low"] * 1.01)  # But not more than 1% above
    )
    
    # Thrusting Pattern - weak bearish continuation
    thrusting_pattern_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (df_copy["close"] > df_copy["prev_low"]) &  # Close above previous low
        (df_copy["close"] < (df_copy["prev_open"] + df_copy["prev_close"]) / 2) &  # But below midpoint
        (df_copy["close"] > (df_copy["prev_open"] + df_copy["prev_close"]) / 2 * 0.9)  # Not too far below
    )
    
    # EXOTIC PATTERNS
    
    # Tower Top - bearish reversal
    tower_top_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        (df_copy['body_percent'] > 0.5) &  # With substantial body
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        (df_copy['prev_body_percent'] > 0.5) &  # Also with substantial body
        (df_copy["high"] > df_copy["prev2_high"]) &  # Current and previous made new highs
        (df_copy["prev_high"] > df_copy["prev2_high"]) &
        (df_copy["prev2_high"] > df_copy["prev3_high"]) &  # After a series of rising candles
        (df_copy["prev3_high"] > df_copy["prev4_high"])
    )
    
    # Tower Bottom - bullish reversal
    tower_bottom_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        (df_copy['body_percent'] > 0.5) &  # With substantial body
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        (df_copy['prev_body_percent'] > 0.5) &  # Also with substantial body
        (df_copy["low"] < df_copy["prev2_low"]) &  # Current and previous made new lows
        (df_copy["prev_low"] < df_copy["prev2_low"]) &
        (df_copy["prev2_low"] < df_copy["prev3_low"]) &  # After a series of falling candles
        (df_copy["prev3_low"] < df_copy["prev4_low"])
    )
    
    # Ladder Bottom - bullish reversal
    ladder_bottom_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        (df_copy['body_percent'] > 0.5) &  # With substantial body
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        df_copy['prev2_is_bearish'] &  # Two candles back is bearish
        df_copy['prev3_is_bearish'] &  # Three candles back is bearish
        (df_copy["prev_low"] < df_copy["prev2_low"]) &  # Consecutively lower lows
        (df_copy["prev2_low"] < df_copy["prev3_low"]) &
        (df_copy["prev_high"] < df_copy["prev2_high"]) &  # Consecutively lower highs
        (df_copy["prev2_high"] < df_copy["prev3_high"]) &
        (df_copy["close"] > df_copy["prev_open"])  # Current close above previous open
    )
    
    # Ladder Top - bearish reversal
    ladder_top_condition = (
        df_copy['is_bearish'] &  # Current candle is bearish
        (df_copy['body_percent'] > 0.5) &  # With substantial body
        df_copy['prev_is_bullish'] &  # Previous candle is bullish
        df_copy['prev2_is_bullish'] &  # Two candles back is bullish
        df_copy['prev3_is_bullish'] &  # Three candles back is bullish
        (df_copy["prev_high"] > df_copy["prev2_high"]) &  # Consecutively higher highs
        (df_copy["prev2_high"] > df_copy["prev3_high"]) &
        (df_copy["prev_low"] > df_copy["prev2_low"]) &  # Consecutively higher lows
        (df_copy["prev2_low"] > df_copy["prev3_low"]) &
        (df_copy["close"] < df_copy["prev_open"])  # Current close below previous open
    )
    
    # Tri-Star - rare doji-based reversal
    tri_star_bullish_condition = (
        doji_condition &  # Current candle is doji
        doji_condition.shift(1) &  # Previous candle is doji
        doji_condition.shift(2) &  # Two candles back is doji
        (df_copy["prev_low"] < df_copy["prev2_low"]) &  # Middle doji lower than first
        (df_copy["low"] > df_copy["prev_low"])  # Current doji higher than middle
    )
    
    tri_star_bearish_condition = (
        doji_condition &  # Current candle is doji
        doji_condition.shift(1) &  # Previous candle is doji
        doji_condition.shift(2) &  # Two candles back is doji
        (df_copy["prev_high"] > df_copy["prev2_high"]) &  # Middle doji higher than first
        (df_copy["high"] < df_copy["prev_high"])  # Current doji lower than middle
    )
    
    # Mat Hold - bullish continuation
    mat_hold_condition = (
        df_copy['is_bullish'] &  # Current candle is bullish
        (df_copy['body_percent'] > 0.5) &  # With substantial body
        df_copy['prev_is_bearish'] &  # Previous candle is bearish
        df_copy['prev2_is_bearish'] &  # Two candles back is bearish
        df_copy['prev3_is_bearish'] &  # Three candles back is bearish
        df_copy['prev4_is_bullish'] &  # Four candles back is bullish
        (df_copy['prev4_body_percent'] > 0.5) &  # First candle has large body
        (df_copy["prev3_high"] < df_copy["prev4_high"]) &  # Middle candles stay within first candle's range
        (df_copy["prev2_high"] < df_copy["prev4_high"]) &
        (df_copy["prev_high"] < df_copy["prev4_high"]) &
        (df_copy["close"] > df_copy["prev4_close"])  # Current close above first candle's close
    )
    
    #---------------------------------------------------------------------------
    # ASSIGN CANDLE TYPES AND PATTERNS
    #---------------------------------------------------------------------------
    
    # Replace NaN values with False in all condition Series to avoid propagation
    for condition_var in locals().copy():
        if isinstance(locals()[condition_var], pd.Series) and condition_var.endswith('_condition'):
            locals()[condition_var] = locals()[condition_var].fillna(False)
    
    # Assign candle types based on conditions (order matters - more specific types first)
    for idx in df_copy.index:
        try:
            # SINGLE CANDLE TYPES
            if four_price_doji_condition.loc[idx]:
                candle_type.loc[idx] = "four_price_doji"
            elif dragonfly_doji_condition.loc[idx]:
                candle_type.loc[idx] = "dragonfly_doji"
            elif gravestone_doji_condition.loc[idx]:
                candle_type.loc[idx] = "gravestone_doji"
            elif long_legged_doji_condition.loc[idx]:
                candle_type.loc[idx] = "long_legged_doji"
            elif doji_condition.loc[idx]:
                candle_type.loc[idx] = "doji"
            elif hammer_condition.loc[idx]:
                candle_type.loc[idx] = "hammer"
            elif inverted_hammer_condition.loc[idx]:
                candle_type.loc[idx] = "inverted_hammer"
            elif hanging_man_condition.loc[idx]:
                candle_type.loc[idx] = "hanging_man"
            elif shooting_star_condition.loc[idx]:
                candle_type.loc[idx] = "shooting_star"
            elif bullish_belt_hold_condition.loc[idx]:
                candle_type.loc[idx] = "bullish_belt_hold"
            elif bearish_belt_hold_condition.loc[idx]:
                candle_type.loc[idx] = "bearish_belt_hold"
            elif bullish_marubozu_condition.loc[idx]:
                candle_type.loc[idx] = "bullish_marubozu"
            elif bearish_marubozu_condition.loc[idx]:
                candle_type.loc[idx] = "bearish_marubozu"
            elif high_wave_condition.loc[idx]:
                candle_type.loc[idx] = "high_wave"
            elif spinning_top_condition.loc[idx]:
                if df_copy['is_bullish'].loc[idx]:
                    candle_type.loc[idx] = "bullish_spinning_top"
                else:
                    candle_type.loc[idx] = "bearish_spinning_top"
            elif df_copy['is_bullish'].loc[idx]:
                candle_type.loc[idx] = "bullish"
            elif df_copy['is_bearish'].loc[idx]:
                candle_type.loc[idx] = "bearish"
            
            # MULTI-CANDLE PATTERNS (order by significance and specificity)
            
            # Three-candle patterns (strongest signals)
            if morning_star_condition.loc[idx]:
                candle_pattern.loc[idx] = "morning_star"
            elif evening_star_condition.loc[idx]:
                candle_pattern.loc[idx] = "evening_star"
            elif abandoned_baby_bullish_condition.loc[idx]:
                candle_pattern.loc[idx] = "abandoned_baby_bullish"
            elif abandoned_baby_bearish_condition.loc[idx]:
                candle_pattern.loc[idx] = "abandoned_baby_bearish"
            elif three_white_soldiers_condition.loc[idx]:
                candle_pattern.loc[idx] = "three_white_soldiers"
            elif three_black_crows_condition.loc[idx]:
                candle_pattern.loc[idx] = "three_black_crows"
            elif three_inside_up_condition.loc[idx]:
                candle_pattern.loc[idx] = "three_inside_up"
            elif three_inside_down_condition.loc[idx]:
                candle_pattern.loc[idx] = "three_inside_down"
            elif three_outside_up_condition.loc[idx]:
                candle_pattern.loc[idx] = "three_outside_up"
            elif three_outside_down_condition.loc[idx]:
                candle_pattern.loc[idx] = "three_outside_down"
            elif rising_three_methods_condition.loc[idx]:
                candle_pattern.loc[idx] = "rising_three_methods"
            elif falling_three_methods_condition.loc[idx]:
                candle_pattern.loc[idx] = "falling_three_methods"
            elif mat_hold_condition.loc[idx]:
                candle_pattern.loc[idx] = "mat_hold"
            elif tri_star_bullish_condition.loc[idx]:
                candle_pattern.loc[idx] = "tri_star_bullish"
            elif tri_star_bearish_condition.loc[idx]:
                candle_pattern.loc[idx] = "tri_star_bearish"
            elif unique_three_river_bottom_condition.loc[idx]:
                candle_pattern.loc[idx] = "unique_three_river_bottom"
            elif concealing_baby_swallow_condition.loc[idx]:
                candle_pattern.loc[idx] = "concealing_baby_swallow"
            elif advance_block_condition.loc[idx]:
                candle_pattern.loc[idx] = "advance_block"
            elif deliberation_condition.loc[idx]:
                candle_pattern.loc[idx] = "deliberation"
            
            # Two-candle patterns
            elif bullish_engulfing_condition.loc[idx]:
                candle_pattern.loc[idx] = "bullish_engulfing"
            elif bearish_engulfing_condition.loc[idx]:
                candle_pattern.loc[idx] = "bearish_engulfing"
            elif bullish_harami_cross_condition.loc[idx]:
                candle_pattern.loc[idx] = "bullish_harami_cross"
            elif bearish_harami_cross_condition.loc[idx]:
                candle_pattern.loc[idx] = "bearish_harami_cross"
            elif bullish_harami_condition.loc[idx]:
                candle_pattern.loc[idx] = "bullish_harami"
            elif bearish_harami_condition.loc[idx]:
                candle_pattern.loc[idx] = "bearish_harami"
            elif piercing_line_condition.loc[idx]:
                candle_pattern.loc[idx] = "piercing_line"
            elif dark_cloud_cover_condition.loc[idx]:
                candle_pattern.loc[idx] = "dark_cloud_cover"
            elif tweezer_tops_condition.loc[idx]:
                candle_pattern.loc[idx] = "tweezer_tops"
            elif tweezer_bottoms_condition.loc[idx]:
                candle_pattern.loc[idx] = "tweezer_bottoms"
            elif up_gap_side_by_side_white_lines_condition.loc[idx]:
                candle_pattern.loc[idx] = "up_gap_side_by_side_white_lines"
            elif down_gap_side_by_side_white_lines_condition.loc[idx]:
                candle_pattern.loc[idx] = "down_gap_side_by_side_white_lines"
            elif separating_lines_bullish_condition.loc[idx]:
                candle_pattern.loc[idx] = "separating_lines_bullish"
            elif separating_lines_bearish_condition.loc[idx]:
                candle_pattern.loc[idx] = "separating_lines_bearish"
            elif hook_reversal_bullish_condition.loc[idx]:
                candle_pattern.loc[idx] = "hook_reversal_bullish"
            elif hook_reversal_bearish_condition.loc[idx]:
                candle_pattern.loc[idx] = "hook_reversal_bearish"
            elif on_neck_line_condition.loc[idx]:
                candle_pattern.loc[idx] = "on_neck_line"
            elif in_neck_line_condition.loc[idx]:
                candle_pattern.loc[idx] = "in_neck_line"
            elif thrusting_pattern_condition.loc[idx]:
                candle_pattern.loc[idx] = "thrusting_pattern"
            
            # Complex patterns
            elif tower_top_condition.loc[idx]:
                candle_pattern.loc[idx] = "tower_top"
            elif tower_bottom_condition.loc[idx]:
                candle_pattern.loc[idx] = "tower_bottom"
            elif ladder_bottom_condition.loc[idx]:
                candle_pattern.loc[idx] = "ladder_bottom"
            elif ladder_top_condition.loc[idx]:
                candle_pattern.loc[idx] = "ladder_top"
            elif fry_pan_bottom_condition.loc[idx]:
                candle_pattern.loc[idx] = "fry_pan_bottom"
            elif dumpling_top_condition.loc[idx]:
                candle_pattern.loc[idx] = "dumpling_top"
            elif island_reversal_bullish_condition.loc[idx]:
                candle_pattern.loc[idx] = "island_reversal_bullish"
            elif island_reversal_bearish_condition.loc[idx]:
                candle_pattern.loc[idx] = "island_reversal_bearish"
            
        except (KeyError, ValueError, TypeError) as e:
            # Skip problematic rows but log the error
            import warnings
            warnings.warn(f"Error processing row at index {idx}: {str(e)}")
            continue
    
    # Create result DataFrame without indicator patterns
    result_df = pd.DataFrame({
        'type': candle_type,
        'pattern': candle_pattern
    }, index=df_copy.index)
    
    # Warning if include_indicators is True
    if include_indicators:
        import warnings
        warnings.warn("The 'include_indicators' parameter is set to True, but indicator-based pattern detection has been removed.")
    
    return result_df

candlestick_patterns.__doc__ = """
    Name:
        Comprehensive Candlestick Patterns Detection

    Description:
        Detects a wide range of candlestick patterns, from basic single-candle types to complex
        multi-candle formations. This function analyzes price data to identify both individual
        candlestick types and pattern formations that may indicate trend continuations or reversals.
        
        The function categorizes patterns into:
        1. Single Candlestick Patterns (e.g., doji, hammer, marubozu)
        2. Two-Candlestick Patterns (e.g., engulfing, harami)
        3. Three-Candlestick Patterns (e.g., morning star, three white soldiers)
        4. Rare & Advanced Patterns (e.g., abandoned baby, island reversal)

    More info:
        https://www.investopedia.com/trading/candlestick-charting-what-is-it/
        https://www.babypips.com/learn/forex/japanese-candlesticks

    Parameters:
        - df (pandas.DataFrame): Input DataFrame which should contain columns:
            'open', 'high', 'low', and 'close'.
        - include_indicators (bool, optional): If True, provides a warning that indicator-based
            pattern detection has been removed. Default is False.

    Single Candlestick Types:
        - "doji": A candle with a very small body, indicating indecision.
        - "long_legged_doji": A doji with long upper and lower shadows, showing extreme indecision.
        - "dragonfly_doji": A doji with a long lower shadow and no upper shadow, often a bullish reversal signal.
        - "gravestone_doji": A doji with a long upper shadow and no lower shadow, often a bearish reversal signal.
        - "four_price_doji": An extremely rare doji where open, high, low, and close are virtually identical.
        - "hammer": A bullish reversal candle with a small body at the top and a long lower shadow.
        - "inverted_hammer": A bullish reversal candle with a small body at the bottom and a long upper shadow.
        - "hanging_man": A bearish reversal candle with a small body at the top and a long lower shadow.
        - "shooting_star": A bearish reversal candle with a small body at the bottom and a long upper shadow.
        - "bullish_belt_hold": A bullish candle with a large body and no or minimal lower shadow.
        - "bearish_belt_hold": A bearish candle with a large body and no or minimal upper shadow.
        - "bullish_marubozu": A bullish candle with a large body and no or minimal shadows.
        - "bearish_marubozu": A bearish candle with a large body and no or minimal shadows.
        - "high_wave": A candle with a small body and very long upper and lower shadows, indicating volatility.
        - "bullish_spinning_top": A bullish candle with a small body and significant upper and lower shadows.
        - "bearish_spinning_top": A bearish candle with a small body and significant upper and lower shadows.
        - "bullish": A standard bullish candle (close > open) that doesn't match any specific pattern.
        - "bearish": A standard bearish candle (close < open) that doesn't match any specific pattern.

    Multi-Candle Patterns:
        Two-Candle Patterns:
        - "bullish_engulfing": A bullish reversal pattern where a large bullish candle engulfs the previous bearish candle.
        - "bearish_engulfing": A bearish reversal pattern where a large bearish candle engulfs the previous bullish candle.
        - "bullish_harami": A bullish reversal pattern where a small bullish candle is contained within the previous bearish candle.
        - "bearish_harami": A bearish reversal pattern where a small bearish candle is contained within the previous bullish candle.
        - "bullish_harami_cross": A stronger bullish harami where the second candle is a doji.
        - "bearish_harami_cross": A stronger bearish harami where the second candle is a doji.
        - "piercing_line": A bullish reversal pattern where a bullish candle closes above the midpoint of the previous bearish candle.
        - "dark_cloud_cover": A bearish reversal pattern where a bearish candle opens above the previous high and closes below the midpoint.
        - "tweezer_tops": A bearish reversal pattern with two candles having the same or similar highs.
        - "tweezer_bottoms": A bullish reversal pattern with two candles having the same or similar lows.
        - "up_gap_side_by_side_white_lines": A bullish continuation pattern with two bullish candles separated by a gap up.
        - "down_gap_side_by_side_white_lines": A bearish continuation pattern with two bearish candles separated by a gap down.
        - "separating_lines_bullish": A bullish continuation pattern where a bullish candle follows a bearish one with the same open.
        - "separating_lines_bearish": A bearish continuation pattern where a bearish candle follows a bullish one with the same open.
        - "hook_reversal_bullish": A bullish reversal pattern similar to piercing line but less strong.
        - "hook_reversal_bearish": A bearish reversal pattern similar to dark cloud cover but less strong.
        - "on_neck_line": A bearish continuation pattern where a bullish candle closes at the previous low.
        - "in_neck_line": A bearish continuation pattern where a bullish candle closes slightly above the previous low.
        - "thrusting_pattern": A weak bearish continuation pattern where a bullish candle closes below the midpoint of the previous bearish candle.

        Three-Candle Patterns:
        - "morning_star": A bullish reversal pattern with a bearish candle, a small-bodied candle, and a bullish candle.
        - "evening_star": A bearish reversal pattern with a bullish candle, a small-bodied candle, and a bearish candle.
        - "abandoned_baby_bullish": A strong bullish reversal with a bearish candle, a gapped-down doji, and a gapped-up bullish candle.
        - "abandoned_baby_bearish": A strong bearish reversal with a bullish candle, a gapped-up doji, and a gapped-down bearish candle.
        - "three_white_soldiers": A strong bullish reversal with three consecutive bullish candles, each closing higher.
        - "three_black_crows": A strong bearish reversal with three consecutive bearish candles, each closing lower.
        - "three_inside_up": A bullish reversal starting with a bullish harami and followed by a confirming bullish candle.
        - "three_inside_down": A bearish reversal starting with a bearish harami and followed by a confirming bearish candle.
        - "three_outside_up": A bullish reversal starting with a bullish engulfing and followed by a confirming bullish candle.
        - "three_outside_down": A bearish reversal starting with a bearish engulfing and followed by a confirming bearish candle.
        - "rising_three_methods": A bullish continuation with a large bullish candle, three small bearish candles, and a final bullish candle.
        - "falling_three_methods": A bearish continuation with a large bearish candle, three small bullish candles, and a final bearish candle.
        - "mat_hold": A bullish continuation similar to rising three methods but with a gap.
        - "tri_star_bullish": A bullish reversal with three consecutive doji candles forming a bottom.
        - "tri_star_bearish": A bearish reversal with three consecutive doji candles forming a top.
        - "unique_three_river_bottom": A bullish reversal with a long bearish candle, a bearish candle with a new low, and a small bullish candle.
        - "concealing_baby_swallow": A rare bearish reversal pattern with four bearish candles.
        - "advance_block": A weakening bullish trend with three bullish candles of decreasing size and increasing upper shadows.
        - "deliberation": A warning of potential reversal after an uptrend, with two strong bullish candles followed by a small bullish candle.

        Complex Patterns:
        - "tower_top": A bearish reversal after an uptrend, with a series of rising candles followed by a strong bearish candle.
        - "tower_bottom": A bullish reversal after a downtrend, with a series of falling candles followed by a strong bullish candle.
        - "ladder_bottom": A bullish reversal after a downtrend, with three bearish candles followed by a strong bullish candle.
        - "ladder_top": A bearish reversal after an uptrend, with three bullish candles followed by a strong bearish candle.
        - "fry_pan_bottom": A bullish reversal forming a rounded bottom pattern.
        - "dumpling_top": A bearish reversal forming a rounded top pattern.
        - "island_reversal_bullish": A bullish reversal with an isolated low surrounded by gaps.
        - "island_reversal_bearish": A bearish reversal with an isolated high surrounded by gaps.

    Pattern Interpretation Guide:
        Bullish Reversal Patterns:
        - Hammer, Dragonfly Doji: Potential reversal after downtrend, shows buyers stepping in at lows
        - Bullish Engulfing, Morning Star: Strong reversal signals, especially after extended downtrends
        - Piercing Line: Moderate reversal signal, needs confirmation
        - Bullish Harami: Indicates indecision after downtrend, weaker signal than engulfing
        - Three White Soldiers: Very strong reversal signal, especially after a prolonged downtrend
        - Abandoned Baby Bullish: Rare but extremely strong reversal signal

        Bearish Reversal Patterns:
        - Shooting Star, Gravestone Doji: Potential reversal after uptrend, shows sellers stepping in at highs
        - Bearish Engulfing, Evening Star: Strong reversal signals, especially after extended uptrends
        - Dark Cloud Cover: Moderate reversal signal, needs confirmation
        - Bearish Harami: Indicates indecision after uptrend, weaker signal than engulfing
        - Three Black Crows: Very strong reversal signal, especially after a prolonged uptrend
        - Abandoned Baby Bearish: Rare but extremely strong reversal signal

        Continuation Patterns:
        - Rising/Falling Three Methods: Strong continuation signals during trends
        - Separating Lines: Moderate continuation signals
        - On Neck Line, In Neck Line, Thrusting Pattern: Weak bearish continuation signals

        Indecision Patterns:
        - Doji, Long-legged Doji: Market indecision, potential reversal if at support/resistance
        - Spinning Tops: Weak indecision signals, less significant than doji

    Trading Strategies:
        1. Reversal Trading:
           - Look for strong reversal patterns (Morning Star, Engulfing) at support/resistance levels
           - Confirm with volume increase and/or other technical indicators
           - Set stop loss below/above the pattern's low/high point

        2. Trend Continuation:
           - Use patterns like Three Methods during established trends
           - Enter in the direction of the primary trend when continuation patterns form
           - Tighter stop losses can be used compared to reversal trades

        3. Volatility Breakout:
           - Look for indecision patterns (Doji) followed by strong momentum candles
           - Enter in the direction of the breakout candle
           - Place stop loss below/above the Doji's low/high

        4. Multiple Timeframe Confirmation:
           - Confirm patterns on higher timeframes before trading on lower timeframes
           - Higher probability setups occur when patterns align across multiple timeframes

    Call with:
        # Detect candlestick types and patterns
        candlestick_df = bta.candlestick_patterns(df)
        
        # Add type and pattern columns to original DataFrame
        df['candlestick_type'] = candlestick_df['type']
        df['candlestick_pattern'] = candlestick_df['pattern']

    Returns:
        pd.DataFrame: DataFrame with 'type' column for individual candle types and 'pattern' column
        for multi-candle patterns.
"""

def test():
    """
    Test function for the candlestick_patterns indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the candlestick_patterns indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(candlestick_patterns)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()