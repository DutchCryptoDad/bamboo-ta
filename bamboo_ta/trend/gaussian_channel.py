# -*- coding: utf-8 -*-
# gaussian_channel.py
import numpy as np
import pandas as pd


def gaussian_channel(
    df: pd.DataFrame,
    source: str = "hlc3",
    poles: int = 4,
    period: int = 144,
    multiplier: float = 1.414,
    reduced_lag: bool = False,
    fast_response: bool = False
) -> pd.DataFrame:
    """Gaussian Channel"""
    
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Calculate source data based on input
    if source == "hlc3":
        src_data = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3
    elif source == "close":
        src_data = df_copy["close"]
    elif source == "open":
        if "open" not in df.columns:
            raise KeyError("DataFrame must contain 'open' column for open source")
        src_data = df_copy["open"]
    elif source == "hl2":
        src_data = (df_copy["high"] + df_copy["low"]) / 2
    elif source == "ohlc4":
        if "open" not in df.columns:
            raise KeyError("DataFrame must contain 'open' column for ohlc4 source")
        src_data = (df_copy["open"] + df_copy["high"] + df_copy["low"] + df_copy["close"]) / 4
    else:
        # Assume it's a column name
        if source not in df.columns:
            raise KeyError(f"DataFrame must contain '{source}' column")
        src_data = df_copy[source]
    
    # Calculate True Range exactly like Pine Script tr(true)
    high = df_copy["high"]
    low = df_copy["low"]
    close = df_copy["close"]
    
    # Pine Script tr(true) calculation - vectorized
    tr_data = pd.Series(index=df_copy.index, dtype=float)
    prev_close = close.shift(1)
    
    # For the first bar, Pine Script tr(true) returns high - low
    tr_data.iloc[0] = high.iloc[0] - low.iloc[0]
    
    # For subsequent bars
    for i in range(1, len(df_copy)):
        tr1 = high.iloc[i] - low.iloc[i]
        tr2 = abs(high.iloc[i] - prev_close.iloc[i])
        tr3 = abs(low.iloc[i] - prev_close.iloc[i])
        tr_data.iloc[i] = max(tr1, tr2, tr3)
    
    # CRITICAL: Beta and Alpha calculation - rechecking the Pine Script
    # beta = (1 - cos(4*asin(1)/per)) / (pow(1.414, 2/N) - 1)
    # alpha = -beta + sqrt(pow(beta, 2) + 2*beta)
    
    # Pine Script uses asin(1) which equals π/2, so 4*asin(1) = 2π
    # This is different from my previous calculation!
    asin_1 = np.arcsin(1.0)  # This is π/2
    four_asin_1 = 4 * asin_1  # This is 2π
    
    beta = (1 - np.cos(four_asin_1 / period)) / (np.power(1.414, 2.0 / poles) - 1)
    alpha = -beta + np.sqrt(beta * beta + 2 * beta)
    
    print(f"Debug: asin(1)={asin_1}, 4*asin(1)={four_asin_1}")
    print(f"Debug: beta={beta}, alpha={alpha}")
    
    # Lag calculation
    lag = int((period - 1) / (2 * poles))
    
    # Data preprocessing for lag reduction
    if reduced_lag and lag > 0:
        src_processed = src_data + (src_data - src_data.shift(lag))
        tr_processed = tr_data + (tr_data - tr_data.shift(lag))
        # Fill NaN values for the first 'lag' periods
        src_processed.iloc[:lag] = src_data.iloc[:lag]
        tr_processed.iloc[:lag] = tr_data.iloc[:lag]
    else:
        src_processed = src_data.copy()
        tr_processed = tr_data.copy()
    
    def f_filt9x(a, s, i):
        """
        Exact Pine Script f_filt9x implementation with proper var behavior
        """
        x = 1 - a
        
        # Initialize result array - this simulates Pine Script's 'var float _f = na'
        # In Pine Script, var variables retain their values across bars
        result = np.zeros(len(s))
        
        # Weight mappings exactly as in Pine Script
        m2 = 0
        m3 = 0
        m4 = 0
        m5 = 0
        m6 = 0
        m7 = 0
        m8 = 0
        m9 = 0
        
        if i >= 2:
            m2_map = {9: 36, 8: 28, 7: 21, 6: 15, 5: 10, 4: 6, 3: 3, 2: 1}
            m2 = m2_map.get(i, 0)
        if i >= 3:
            m3_map = {9: 84, 8: 56, 7: 35, 6: 20, 5: 10, 4: 4, 3: 1}
            m3 = m3_map.get(i, 0)
        if i >= 4:
            m4_map = {9: 126, 8: 70, 7: 35, 6: 15, 5: 5, 4: 1}
            m4 = m4_map.get(i, 0)
        if i >= 5:
            m5_map = {9: 126, 8: 56, 7: 21, 6: 6, 5: 1}
            m5 = m5_map.get(i, 0)
        if i >= 6:
            m6_map = {9: 84, 8: 28, 7: 7, 6: 1}
            m6 = m6_map.get(i, 0)
        if i >= 7:
            m7_map = {9: 36, 8: 8, 7: 1}
            m7 = m7_map.get(i, 0)
        if i >= 8:
            m8_map = {9: 9, 8: 1}
            m8 = m8_map.get(i, 0)
        if i == 9:
            m9 = 1
        
        # Process each bar sequentially (this is critical for recursive filters)
        for idx in range(len(s)):
            if pd.isna(s.iloc[idx]):
                result[idx] = 0  # Pine Script behavior for NaN
                continue
            
            # Exact Pine Script formula:
            filter_val = (
                np.power(a, i) * s.iloc[idx] +
                i * x * (result[idx-1] if idx >= 1 else 0) -
                (m2 * np.power(x, 2) * (result[idx-2] if idx >= 2 else 0)) +
                (m3 * np.power(x, 3) * (result[idx-3] if idx >= 3 else 0)) -
                (m4 * np.power(x, 4) * (result[idx-4] if idx >= 4 else 0)) +
                (m5 * np.power(x, 5) * (result[idx-5] if idx >= 5 else 0)) -
                (m6 * np.power(x, 6) * (result[idx-6] if idx >= 6 else 0)) +
                (m7 * np.power(x, 7) * (result[idx-7] if idx >= 7 else 0)) -
                (m8 * np.power(x, 8) * (result[idx-8] if idx >= 8 else 0)) +
                (m9 * np.power(x, 9) * (result[idx-9] if idx >= 9 else 0))
            )
            
            result[idx] = filter_val
        
        return pd.Series(result, index=s.index)
    
    def f_pole(a, s, i):
        """Pine Script f_pole implementation"""
        # Calculate all required filters
        f1 = f_filt9x(a, s, 1)
        f2 = f_filt9x(a, s, 2) if i >= 2 else pd.Series(0, index=s.index)
        f3 = f_filt9x(a, s, 3) if i >= 3 else pd.Series(0, index=s.index)
        f4 = f_filt9x(a, s, 4) if i >= 4 else pd.Series(0, index=s.index)
        f5 = f_filt9x(a, s, 5) if i >= 5 else pd.Series(0, index=s.index)
        f6 = f_filt9x(a, s, 6) if i >= 6 else pd.Series(0, index=s.index)
        f7 = f_filt9x(a, s, 7) if i >= 7 else pd.Series(0, index=s.index)
        f8 = f_filt9x(a, s, 8) if i >= 8 else pd.Series(0, index=s.index)
        f9 = f_filt9x(a, s, 9) if i == 9 else pd.Series(0, index=s.index)
        
        # Select the appropriate filter
        if i == 1:
            fn = f1
        elif i == 2:
            fn = f2
        elif i == 3:
            fn = f3
        elif i == 4:
            fn = f4
        elif i == 5:
            fn = f5
        elif i == 6:
            fn = f6
        elif i == 7:
            fn = f7
        elif i == 8:
            fn = f8
        elif i == 9:
            fn = f9
        else:
            fn = f1  # Fallback
        
        return fn, f1
    
    # Calculate Gaussian filters for source and true range
    filt_n, filt_1 = f_pole(alpha, src_processed, poles)
    filt_n_tr, filt_1_tr = f_pole(alpha, tr_processed, poles)
    
    print(f"Debug: First few filt_n values: {filt_n.head()}")
    print(f"Debug: First few filt_n_tr values: {filt_n_tr.head()}")
    
    # Apply fast response mode if enabled
    if fast_response:
        filt = (filt_n + filt_1) / 2
        filt_tr = (filt_n_tr + filt_1_tr) / 2
    else:
        filt = filt_n
        filt_tr = filt_n_tr
    
    # Calculate bands
    upper_band = filt + filt_tr * multiplier
    lower_band = filt - filt_tr * multiplier
    
    # Determine filter direction
    filter_direction = pd.Series(index=df_copy.index, dtype=float)
    filter_direction.iloc[0] = 0
    
    for i in range(1, len(filt)):
        if filt.iloc[i] > filt.iloc[i-1]:
            filter_direction.iloc[i] = 1  # Uptrend
        elif filt.iloc[i] < filt.iloc[i-1]:
            filter_direction.iloc[i] = -1  # Downtrend
        else:
            filter_direction.iloc[i] = 0  # Neutral
    
    # Filter color for reference (from Pine Script)
    # fcolor = filt > filt[1] ? #0aff68 : filt < filt[1] ? #ff0a5a : #cccccc
    
    # Bar color logic - exact Pine Script implementation
    bar_signal = pd.Series(index=df_copy.index, dtype=float)
    bar_signal.iloc[0] = 0
    
    for i in range(1, len(src_data)):
        current_src = src_data.iloc[i]
        previous_src = src_data.iloc[i-1]
        current_filt = filt.iloc[i]
        current_upper = upper_band.iloc[i]
        current_lower = lower_band.iloc[i]
        
        # Pine Script bar color logic:
        # barcolor = (src > src[1]) and (src > filt) and (src < hband) ? #0aff68 : 
        #            (src > src[1]) and (src >= hband) ? #0aff1b : 
        #            (src <= src[1]) and (src > filt) ? #00752d : 
        #            (src < src[1]) and (src < filt) and (src > lband) ? #ff0a5a : 
        #            (src < src[1]) and (src <= lband) ? #ff0a11 : 
        #            (src >= src[1]) and (src < filt) ? #990032 : #cccccc
        
        if (current_src > previous_src) and (current_src > current_filt) and (current_src < current_upper):
            bar_signal.iloc[i] = 1  # #0aff68 - bright green
        elif (current_src > previous_src) and (current_src >= current_upper):
            bar_signal.iloc[i] = 2  # #0aff1b - brighter green
        elif (current_src <= previous_src) and (current_src > current_filt):
            bar_signal.iloc[i] = 3  # #00752d - dark green
        elif (current_src < previous_src) and (current_src < current_filt) and (current_src > current_lower):
            bar_signal.iloc[i] = -1  # #ff0a5a - red
        elif (current_src < previous_src) and (current_src <= current_lower):
            bar_signal.iloc[i] = -2  # #ff0a11 - bright red
        elif (current_src >= previous_src) and (current_src < current_filt):
            bar_signal.iloc[i] = -3  # #990032 - dark red
        else:
            bar_signal.iloc[i] = 0  # #cccccc - gray
    
    # Create result DataFrame
    result = pd.DataFrame(index=df_copy.index)
    result["gc_middle"] = filt  # The main Gaussian filter line (centerline)
    result["gc_upper"] = upper_band
    result["gc_lower"] = lower_band
    result["gc_direction"] = filter_direction
    result["gc_bar_signal"] = bar_signal
    
    return result


gaussian_channel.__doc__ = """
Name:
    Gaussian Channel

Description:
    The Gaussian Channel is an experimental indicator utilizing the Ehlers Gaussian Filter 
    technique combined with lag reduction techniques and true range to analyze trend activity.
    Gaussian filters are exponential moving averages applied multiple times.
    
    The indicator calculates beta and alpha based on the sampling period and number of poles 
    specified. The data can be given a truncation option for reduced lag. Then the alpha 
    and source values are used to calculate the filter and filtered true range of the dataset.
    Filtered true range with a specified multiplier is then added to and subtracted from the 
    filter, generating a channel.
    
    A one pole filter with an N pole alpha can be averaged with the filter to generate a 
    faster filter (Fast Response Mode).

More info:
    Original Pine Script by DonovanWall
    Based on John Ehlers' Gaussian Filter technique
    https://www.tradingview.com/script/NaN/ (Pine Script reference)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
      For 'ohlc4' source, 'open' column is also required.
    - source (str): Price source to use. Options: 'hlc3', 'close', 'open', 'hl2', 'ohlc4', 
      or any column name. Default is 'hlc3'.
    - poles (int): Number of poles for the Gaussian filter (1-9). Higher values create smoother 
      output with more lag. Default is 4.
    - period (int): Sampling period for the filter. Larger values result in smoother outputs 
      with increased lag. Default is 144.
    - multiplier (float): Multiplier for the filtered true range to create channel bands. 
      Default is 1.414.
    - reduced_lag (bool): Enable reduced lag mode for faster response. Default is False.
    - fast_response (bool): Enable fast response mode by averaging N-pole and 1-pole filters. 
      Default is False.

Call with:
    gc_result = bta.gaussian_channel(df, source='hlc3', poles=4, period=144, multiplier=1.414)
    df['gc_middle'] = gc_result['gc_middle']
    df['gc_upper'] = gc_result['gc_upper']
    df['gc_lower'] = gc_result['gc_lower']
    df['gc_direction'] = gc_result['gc_direction']
    df['gc_bar_signal'] = gc_result['gc_bar_signal']

Returns:
    pd.DataFrame: DataFrame with the following columns:
        - 'gc_middle': The main Gaussian filter line (centerline/middle of channel)
        - 'gc_upper': Upper channel band (middle + filtered_tr * multiplier)
        - 'gc_lower': Lower channel band (middle - filtered_tr * multiplier)
        - 'gc_direction': Filter direction (1=up, -1=down, 0=neutral)
        - 'gc_bar_signal': Bar color signal based on price position relative to filter and bands:
            2: Strong bullish (price rising above upper band)
            1: Bullish (price rising above filter, within channel)
            3: Weak bullish (price above filter but declining)
            -2: Strong bearish (price falling below lower band)
            -1: Bearish (price falling below filter, within channel)
            -3: Weak bearish (price below filter but rising)
            0: Neutral/choppy (sideways movement)
"""


def test():
    """
    Test function for the gaussian_channel indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the gaussian_channel indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(gaussian_channel)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()