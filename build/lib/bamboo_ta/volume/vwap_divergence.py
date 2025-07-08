# -*- coding: utf-8 -*-
# vwap_divergence.py
import numpy as np
import pandas as pd


def vwap_divergence(
    df: pd.DataFrame,
    divergence_lookback: int = 5,
    divergence_atr_multiplier: float = 3.0,
    atr_length: int = 14,
    min_bars_between_signals: int = 15,
    gap_threshold_multiplier: float = 1.0,
    anchor: str = "session",
    source: str = "hlc3",
    volume_col: str = "volume"
) -> pd.DataFrame:
    """VWAP Divergence Indicator"""
    
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "open", volume_col]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate source price based on input
    if source == "hlc3":
        src = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3
    elif source == "hl2":
        src = (df_copy["high"] + df_copy["low"]) / 2
    elif source == "ohlc4":
        src = (df_copy["open"] + df_copy["high"] + df_copy["low"] + df_copy["close"]) / 4
    elif source == "close":
        src = df_copy["close"]
    else:
        raise ValueError("Invalid source. Use 'hlc3', 'hl2', 'ohlc4', or 'close'")
    
    # Calculate ATR (Average True Range)
    def calculate_atr(df, length):
        """Calculate Average True Range"""
        high_low = df["high"] - df["low"]
        high_close_prev = np.abs(df["high"] - df["close"].shift(1))
        low_close_prev = np.abs(df["low"] - df["close"].shift(1))
        
        true_range = np.maximum(high_low, np.maximum(high_close_prev, low_close_prev))
        atr = true_range.rolling(window=length).mean()
        return atr
    
    # Calculate VWAP
    def calculate_vwap(price, volume, anchor_type="session"):
        """Calculate Volume Weighted Average Price"""
        # For simplicity, we'll calculate VWAP for the entire period
        # In a real implementation, you might want to reset VWAP based on anchor periods
        if anchor_type == "session":
            # Reset VWAP daily (simplified approach)
            if 'date' in df.columns or df.index.name == 'date':
                # Group by date and calculate VWAP for each day
                if 'date' in df.columns:
                    df_temp = df.copy()
                    df_temp['date_only'] = pd.to_datetime(df_temp['date']).dt.date
                else:
                    df_temp = df.copy()
                    df_temp['date_only'] = df.index.date
                
                def calc_group_vwap(group, price_series, vol_series):
                    group_price = price_series.loc[group.index]
                    group_vol = vol_series.loc[group.index]
                    return (group_price * group_vol).cumsum() / group_vol.cumsum()
                
                vwap = df_temp.groupby('date_only').apply(
                    lambda x: calc_group_vwap(x, src, df_copy[volume_col])
                ).reset_index(level=0, drop=True).sort_index()
            else:
                # Simple cumulative VWAP
                vwap = (price * volume).cumsum() / volume.cumsum()
        else:
            # Simple cumulative VWAP for other anchor types
            vwap = (price * volume).cumsum() / volume.cumsum()
        
        return vwap
    
    # Calculate indicators
    atr = calculate_atr(df_copy, atr_length)
    vwap = calculate_vwap(src, df_copy[volume_col], anchor)
    
    # Initialize output columns
    df_copy["vwap"] = vwap
    df_copy["atr"] = atr
    df_copy["bullish_divergence"] = False
    df_copy["bearish_divergence"] = False
    df_copy["vwap_trend"] = 0  # 1 for up, -1 for down, 0 for neutral
    
    # Calculate trend based on VWAP direction
    df_copy["vwap_trend"] = np.where(
        vwap > vwap.shift(1), 1,
        np.where(vwap < vwap.shift(1), -1, 0)
    )
    
    # Track last divergence signals to avoid clustering
    last_bullish_divergence = -min_bars_between_signals - 1
    last_bearish_divergence = -min_bars_between_signals - 1
    
    # Calculate divergences
    for i in range(divergence_lookback, len(df_copy)):
        current_close = df_copy["close"].iloc[i]
        prev_close = df_copy["close"].iloc[i-1]
        current_vwap = vwap.iloc[i]
        prev_vwap = vwap.iloc[i-1]
        current_atr = atr.iloc[i]
        
        if pd.isna(current_atr) or current_atr == 0:
            continue
        
        # Calculate price movement over lookback period
        high_current = df_copy["high"].iloc[i]
        low_lookback = df_copy["low"].iloc[i - divergence_lookback]
        last5gain = high_current - low_lookback
        
        high_lookback = df_copy["high"].iloc[i - divergence_lookback]
        low_current = df_copy["low"].iloc[i]
        last5loss = high_lookback - low_current
        
        # Check for gaps (simplified gap detection)
        gaps = False
        for j in range(divergence_lookback + 1):
            if i - j > 0:
                open_curr = df_copy["open"].iloc[i - j]
                close_prev = df_copy["close"].iloc[i - j - 1]
                if abs(open_curr - close_prev) > current_atr * gap_threshold_multiplier:
                    gaps = True
                    break
        
        # Calculate range for additional filtering
        high_20 = df_copy["high"].iloc[max(0, i-19):i+1].max()
        low_20 = df_copy["low"].iloc[max(0, i-19):i+1].min()
        range_20 = high_20 - low_20
        
        # Bullish divergence conditions
        bullish_condition = (
            current_close > prev_close and  # Price going up
            current_vwap < prev_vwap and   # VWAP going down (divergence)
            last5gain > current_atr * divergence_atr_multiplier and  # Significant price movement
            not gaps and  # No significant gaps
            (i - last_bullish_divergence > min_bars_between_signals or 
             (range_20 > current_atr * 2 and i - last_bullish_divergence > 10))
        )
        
        if bullish_condition:
            df_copy.loc[df_copy.index[i], "bullish_divergence"] = True
            last_bullish_divergence = i
        
        # Bearish divergence conditions
        bearish_condition = (
            current_close < prev_close and  # Price going down
            current_vwap > prev_vwap and   # VWAP going up (divergence)
            last5loss > current_atr * divergence_atr_multiplier and  # Significant price movement
            not gaps and  # No significant gaps
            (i - last_bearish_divergence > min_bars_between_signals or 
             (range_20 > current_atr * 2 and i - last_bearish_divergence > 10))
        )
        
        if bearish_condition:
            df_copy.loc[df_copy.index[i], "bearish_divergence"] = True
            last_bearish_divergence = i
    
    return df_copy[["vwap", "atr", "vwap_trend", "bullish_divergence", "bearish_divergence"]]


vwap_divergence.__doc__ = """
Name:
    VWAP Divergence

Description:
    The VWAP Divergence indicator identifies potential bullish and bearish divergences 
    between price action and the Volume Weighted Average Price (VWAP). A bullish 
    divergence occurs when price moves higher while VWAP moves lower, suggesting 
    potential upward momentum. A bearish divergence occurs when price moves lower 
    while VWAP moves higher, suggesting potential downward momentum.
    
    The indicator uses ATR (Average True Range) to filter out insignificant movements 
    and includes gap detection to avoid false signals during market gaps. It also 
    implements a minimum bar spacing between signals to prevent clustering of alerts.

More info:
    https://www.investopedia.com/terms/v/vwap.asp
    https://www.tradingview.com/script/fluxchart-vwap-divergence/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      'close', 'open', and volume columns.
    - divergence_lookback (int): Lookback period to determine price movement significance. 
      Default is 5.
    - divergence_atr_multiplier (float): ATR multiplier to determine minimum movement 
      threshold for divergence signals. Default is 3.0.
    - atr_length (int): Period for ATR calculation. Default is 14.
    - min_bars_between_signals (int): Minimum bars between divergence signals to 
      prevent clustering. Default is 15.
    - gap_threshold_multiplier (float): ATR multiplier for gap detection threshold. 
      Default is 1.0.
    - anchor (str): VWAP anchor period. Options: 'session', 'week', 'month'. 
      Default is 'session'.
    - source (str): Price source for VWAP calculation. Options: 'hlc3', 'hl2', 
      'ohlc4', 'close'. Default is 'hlc3'.
    - volume_col (str): Name of the volume column. Default is 'volume'.

Call with:
    result = bta.vwap_divergence(df)
    df['vwap'] = result['vwap']
    df['vwap_trend'] = result['vwap_trend']
    df['bullish_divergence'] = result['bullish_divergence']
    df['bearish_divergence'] = result['bearish_divergence']
    df['atr'] = result['atr']

Returns:
    pd.DataFrame: DataFrame with 'vwap', 'atr', 'vwap_trend', 'bullish_divergence', 
    and 'bearish_divergence' columns.
"""


def test():
    """
    Test function for the vwap_divergence indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the vwap_divergence indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(vwap_divergence)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()