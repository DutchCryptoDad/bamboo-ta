# -*- coding: utf-8 -*-
# two_pole_oscillator_fixed.py

import pandas as pd


def two_pole_oscillator_fixed(df: pd.DataFrame, 
                             column: str = "close", 
                             filter_length: int = 20, 
                             sma_length: int = 25,
                             area_length: int = 100,
                             lag_periods: int = 4) -> pd.DataFrame:
    """Two-Pole Oscillator - EXACT Pine Script Conversion"""
    
    df_copy = df.copy()
    
    # Ensure required columns exist
    required_columns = [column, 'high', 'low']
    for col in required_columns:
        if col not in df_copy.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # EXACT Pine Script calculation:
    # float sma1   = ta.sma(close, 25)
    # float sma_n1 = ((close - sma1) - ta.sma(close - sma1, 25)) / ta.stdev(close - sma1, 25)
    
    sma1 = df_copy[column].rolling(window=sma_length).mean()
    close_minus_sma1 = df_copy[column] - sma1
    sma_of_diff = close_minus_sma1.rolling(window=sma_length).mean()
    stdev_of_diff = close_minus_sma1.rolling(window=sma_length).std()
    
    # This is the exact Pine Script calculation
    sma_n1 = (close_minus_sma1 - sma_of_diff) / stdev_of_diff
    
    # Calculate area (ta.sma(high-low, 100))
    area = (df_copy['high'] - df_copy['low']).rolling(window=area_length).mean()
    
    # EXACT Pine Script two-pole filter
    # f_two_pole_filter(source, length) =>
    #     var float smooth1 = na
    #     var float smooth2 = na
    #     alpha = 2.0 / (length + 1)
    #     if na(smooth1)
    #         smooth1 := source
    #     else
    #         smooth1 := (1 - alpha) * smooth1 + alpha * source
    #     if na(smooth2)
    #         smooth2 := smooth1
    #     else
    #         smooth2 := (1 - alpha) * smooth2 + alpha * smooth1
    
    alpha = 2.0 / (filter_length + 1)
    smooth1 = None
    smooth2 = None
    two_p_values = []
    
    for i in range(len(sma_n1)):
        source_val = sma_n1.iloc[i]
        
        if pd.isna(source_val):
            two_p_values.append(None)
            continue
            
        # Apply Pine Script logic exactly
        if smooth1 is None:
            smooth1 = source_val
        else:
            smooth1 = (1 - alpha) * smooth1 + alpha * source_val
            
        if smooth2 is None:
            smooth2 = smooth1
        else:
            smooth2 = (1 - alpha) * smooth2 + alpha * smooth1
            
        two_p_values.append(smooth2)
    
    two_p = pd.Series(two_p_values, index=df_copy.index)
    
    # two_pp = two_p[4] - Pine Script historical reference
    two_pp = two_p.shift(lag_periods)
    
    # Pine Script signal logic:
    # bool buy  = ta.crossover(two_p, two_pp) and two_p < 0 and barstate.isconfirmed
    # bool sell = ta.crossunder(two_p, two_pp) and two_p > 0 and barstate.isconfirmed
    
    # ta.crossover(a, b) = a > b AND a[1] <= b[1]
    buy_crossover = (two_p > two_pp) & (two_p.shift(1) <= two_pp.shift(1))
    buy_condition = buy_crossover & (two_p < 0)
    buy_signal = buy_condition.astype(int)
    
    # ta.crossunder(a, b) = a < b AND a[1] >= b[1]  
    sell_crossunder = (two_p < two_pp) & (two_p.shift(1) >= two_pp.shift(1))
    sell_condition = sell_crossunder & (two_p > 0)
    sell_signal = sell_condition.astype(int)
    
    # Store results
    df_copy['two_pole'] = two_p
    df_copy['two_pole_lagged'] = two_pp
    df_copy['buy_signal'] = buy_signal
    df_copy['sell_signal'] = sell_signal
    df_copy['area'] = area
    
    return df_copy[['two_pole', 'two_pole_lagged', 'buy_signal', 'sell_signal', 'area']]


# Test the new implementation
if __name__ == "__main__":
    import numpy as np
    
    np.random.seed(42)
    data = {
        'close': np.random.randn(100).cumsum() + 50000,
        'high': np.random.randn(100).cumsum() + 50100,
        'low': np.random.randn(100).cumsum() + 49900,
    }
    df = pd.DataFrame(data)
    df['high'] = pd.concat([df['high'], df['close']], axis=1).max(axis=1)
    df['low'] = pd.concat([df['low'], df['close']], axis=1).min(axis=1)
    
    result = two_pole_oscillator_fixed(df)
    print("Fixed implementation test:")
    print(result.dropna().tail())