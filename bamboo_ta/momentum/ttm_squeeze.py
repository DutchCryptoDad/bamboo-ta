# -*- coding: utf-8 -*-
# ttm_squeeze.py

import pandas as pd
import numpy as np


def ttm_squeeze(df: pd.DataFrame, bb_length: int = 20, bb_std: float = 2.0, 
                kc_length: int = 20, kc_scalar: float = 1.5, 
                mom_length: int = 12, mom_smooth: int = 6,
                use_tr: bool = True, mamode: str = "sma", 
                use_pro: bool = False, detailed: bool = False,
                kc_scalar_wide: float = 2.0, kc_scalar_narrow: float = 1.0) -> pd.DataFrame:
    """TTM Squeeze Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    high = df_copy["high"]
    low = df_copy["low"]
    close = df_copy["close"]
    
    # Calculate Bollinger Bands
    bb_middle = close.rolling(window=bb_length).mean()
    bb_std_dev = close.rolling(window=bb_length).std()
    bb_upper = bb_middle + bb_std * bb_std_dev
    bb_lower = bb_middle - bb_std * bb_std_dev
    
    # Calculate Keltner Channels with True Range if required
    if use_tr:
        tr = pd.DataFrame(index=df_copy.index)
        tr['hl'] = high - low
        tr['hc'] = (high - close.shift(1)).abs()
        tr['lc'] = (low - close.shift(1)).abs()
        true_range = tr[['hl', 'hc', 'lc']].max(axis=1)
        
        if mamode.lower() == "ema":
            kc_middle = close.ewm(span=kc_length, adjust=False).mean()
            atr = true_range.ewm(span=kc_length, adjust=False).mean()
        else:  # sma
            kc_middle = close.rolling(window=kc_length).mean()
            atr = true_range.rolling(window=kc_length).mean()
            
        kc_upper = kc_middle + kc_scalar * atr
        kc_lower = kc_middle - kc_scalar * atr
        
        if use_pro:
            kc_upper_wide = kc_middle + kc_scalar_wide * atr
            kc_lower_wide = kc_middle - kc_scalar_wide * atr
            kc_upper_narrow = kc_middle + kc_scalar_narrow * atr
            kc_lower_narrow = kc_middle - kc_scalar_narrow * atr
    else:
        # Use high-low range instead of True Range
        high_low_range = high - low
        
        if mamode.lower() == "ema":
            kc_middle = close.ewm(span=kc_length, adjust=False).mean()
            avg_range = high_low_range.ewm(span=kc_length, adjust=False).mean()
        else:  # sma
            kc_middle = close.rolling(window=kc_length).mean()
            avg_range = high_low_range.rolling(window=kc_length).mean()
            
        kc_upper = kc_middle + kc_scalar * avg_range
        kc_lower = kc_middle - kc_scalar * avg_range
        
        if use_pro:
            kc_upper_wide = kc_middle + kc_scalar_wide * avg_range
            kc_lower_wide = kc_middle - kc_scalar_wide * avg_range
            kc_upper_narrow = kc_middle + kc_scalar_narrow * avg_range
            kc_lower_narrow = kc_middle - kc_scalar_narrow * avg_range
    
    # Calculate momentum
    momentum = close.diff(mom_length)
    
    # Smooth momentum
    if mamode.lower() == "ema":
        squeeze = momentum.ewm(span=mom_smooth, adjust=False).mean()
    else:  # sma
        squeeze = momentum.rolling(window=mom_smooth).mean()
    
    # Determine squeeze conditions
    if use_pro:
        # Three levels of squeeze for Pro version
        squeeze_on_wide = (bb_lower > kc_lower_wide) & (bb_upper < kc_upper_wide)
        squeeze_on_normal = (bb_lower > kc_lower) & (bb_upper < kc_upper)
        squeeze_on_narrow = (bb_lower > kc_lower_narrow) & (bb_upper < kc_upper_narrow)
        squeeze_off = (bb_lower < kc_lower_wide) & (bb_upper > kc_upper_wide)
        no_squeeze = ~squeeze_on_wide & ~squeeze_off
        
        # Add results to DataFrame
        df_copy["squeeze"] = squeeze
        df_copy["squeeze_on_wide"] = squeeze_on_wide.astype(int)
        df_copy["squeeze_on_normal"] = squeeze_on_normal.astype(int)
        df_copy["squeeze_on_narrow"] = squeeze_on_narrow.astype(int)
        df_copy["squeeze_off"] = squeeze_off.astype(int)
        df_copy["no_squeeze"] = no_squeeze.astype(int)
        
        result_columns = ["squeeze", "squeeze_on_wide", "squeeze_on_normal", "squeeze_on_narrow", "squeeze_off", "no_squeeze"]
    else:
        # Standard squeeze version
        squeeze_on = (bb_lower > kc_lower) & (bb_upper < kc_upper)
        squeeze_off = (bb_lower < kc_lower) & (bb_upper > kc_upper)
        no_squeeze = ~squeeze_on & ~squeeze_off
        
        # Add results to DataFrame
        df_copy["squeeze"] = squeeze
        df_copy["squeeze_on"] = squeeze_on.astype(int)
        df_copy["squeeze_off"] = squeeze_off.astype(int)
        df_copy["no_squeeze"] = no_squeeze.astype(int)
        
        result_columns = ["squeeze", "squeeze_on", "squeeze_off", "no_squeeze"]
    
    # Add detailed columns if requested
    if detailed:
        # Identify increasing and decreasing momentum
        squeeze_inc = squeeze.copy()
        squeeze_dec = squeeze.copy()
        
        for i in range(1, len(squeeze)):
            if squeeze.iloc[i] > squeeze.iloc[i-1]:
                squeeze_dec.iloc[i] = np.nan
            elif squeeze.iloc[i] < squeeze.iloc[i-1]:
                squeeze_inc.iloc[i] = np.nan
            else:
                # No change
                squeeze_inc.iloc[i] = np.nan
                squeeze_dec.iloc[i] = np.nan
        
        # Separate positive and negative momentum
        pos_squeeze = squeeze.copy()
        neg_squeeze = squeeze.copy()
        
        pos_squeeze[pos_squeeze < 0] = np.nan
        neg_squeeze[neg_squeeze >= 0] = np.nan
        
        # Identify increasing and decreasing positive momentum
        pos_inc = pos_squeeze.copy()
        pos_dec = pos_squeeze.copy()
        
        for i in range(1, len(pos_squeeze)):
            if not np.isnan(pos_squeeze.iloc[i]):
                if pos_squeeze.iloc[i] > pos_squeeze.iloc[i-1] if not np.isnan(pos_squeeze.iloc[i-1]) else True:
                    pos_dec.iloc[i] = np.nan
                else:
                    pos_inc.iloc[i] = np.nan
                    
        # Identify increasing and decreasing negative momentum
        neg_inc = neg_squeeze.copy()
        neg_dec = neg_squeeze.copy()
        
        for i in range(1, len(neg_squeeze)):
            if not np.isnan(neg_squeeze.iloc[i]):
                if neg_squeeze.iloc[i] < neg_squeeze.iloc[i-1] if not np.isnan(neg_squeeze.iloc[i-1]) else True:
                    neg_inc.iloc[i] = np.nan
                else:
                    neg_dec.iloc[i] = np.nan
        
        # Add detailed results to DataFrame
        df_copy["squeeze_inc"] = squeeze_inc
        df_copy["squeeze_dec"] = squeeze_dec
        df_copy["pos_inc"] = pos_inc
        df_copy["pos_dec"] = pos_dec
        df_copy["neg_inc"] = neg_inc
        df_copy["neg_dec"] = neg_dec
        
        result_columns.extend(["squeeze_inc", "squeeze_dec", "pos_inc", "pos_dec", "neg_inc", "neg_dec"])
    
    return df_copy[result_columns]


ttm_squeeze.__doc__ = \
"""
Name:
    TTM Squeeze

Description:
    The TTM (Trade the Markets) Squeeze indicator was developed by John Carter and 
    is discussed in his book "Mastering the Trade." It identifies periods of market 
    consolidation and expansion by comparing Bollinger Bands® and Keltner Channels.
    
    When Bollinger Bands are inside Keltner Channels, it indicates a "squeeze" 
    condition (low volatility) that often precedes significant price movements. 
    When Bollinger Bands expand outside Keltner Channels, it indicates the 
    "squeeze" has fired, signaling potential trading opportunities.
    
    This implementation offers both the standard version and a "Pro" version with 
    additional squeeze levels (wide, normal, and narrow). It also includes a momentum 
    component that helps identify the direction and strength of price movement when 
    the squeeze fires.

More info:
    https://www.tradingview.com/support/solutions/43000501971-ttm-squeeze/
    https://usethinkscript.com/threads/john-carters-squeeze-pro-indicator-for-thinkorswim-free.4021/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - bb_length (int): The period for Bollinger Bands calculation. Default is 20.
    - bb_std (float): Number of standard deviations for Bollinger Bands. Default is 2.0.
    - kc_length (int): The period for Keltner Channels calculation. Default is 20.
    - kc_scalar (float): Multiplier for the Keltner Channels. Default is 1.5.
    - mom_length (int): The period for momentum calculation. Default is 12.
    - mom_smooth (int): The period for smoothing momentum. Default is 6.
    - use_tr (bool): If True, use True Range for Keltner Channels; otherwise, use High-Low range. Default is True.
    - mamode (str): Moving average type, either 'sma' or 'ema'. Default is 'sma'.
    - use_pro (bool): If True, use the Pro version with multiple squeeze levels. Default is False.
    - detailed (bool): If True, return additional data for visualization. Default is False.
    - kc_scalar_wide (float): Multiplier for wide Keltner Channels (Pro version only). Default is 2.0.
    - kc_scalar_narrow (float): Multiplier for narrow Keltner Channels (Pro version only). Default is 1.0.

Call with:
    # Basic usage:
    result = bta.ttm_squeeze(df)
    df['squeeze'] = result['squeeze']
    df['squeeze_on'] = result['squeeze_on']
    df['squeeze_off'] = result['squeeze_off']
    
    # Pro version:
    result = bta.ttm_squeeze(df, use_pro=True)
    df['squeeze'] = result['squeeze']
    df['squeeze_on_wide'] = result['squeeze_on_wide']
    df['squeeze_on_normal'] = result['squeeze_on_normal']
    df['squeeze_on_narrow'] = result['squeeze_on_narrow']

Returns:
    pd.DataFrame: DataFrame with various squeeze-related columns.
"""


def test():
    """
    Test function for the ttm_squeeze indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ttm_squeeze indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ttm_squeeze)
        
        # Test the Pro version
        test_indicator(ttm_squeeze, use_pro=True)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 