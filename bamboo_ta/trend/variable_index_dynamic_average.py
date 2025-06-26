# -*- coding: utf-8 -*-
# variable_index_dynamic_average.py
import numpy as np
import pandas as pd


def variable_index_dynamic_average(
    df: pd.DataFrame,
    length: int = 14,
    column: str = 'close',
    drift: int = 1
) -> pd.DataFrame:
    """Variable Index Dynamic Average (VIDYA)"""
    
    df_copy = df.copy()
    
    # Ensure required column exists
    if column not in df.columns:
        raise KeyError(f"DataFrame must contain '{column}' column")
    
    # Calculate momentum (price changes)
    momentum = df_copy[column].diff(drift)
    
    # Calculate positive and negative momentum
    pos_momentum = momentum.where(momentum >= 0, 0.0)
    neg_momentum = momentum.where(momentum < 0, 0.0).abs()
    
    # Calculate rolling sums for CMO calculation
    sum_pos_momentum = pos_momentum.rolling(window=length).sum()
    sum_neg_momentum = neg_momentum.rolling(window=length).sum()
    
    # Calculate Chande Momentum Oscillator (CMO)
    # CMO = 100 * (sum_pos - sum_neg) / (sum_pos + sum_neg)
    total_momentum = sum_pos_momentum + sum_neg_momentum
    cmo = (100 * (sum_pos_momentum - sum_neg_momentum) / total_momentum).fillna(0)
    
    # Calculate absolute CMO for volatility index
    abs_cmo = cmo.abs()
    
    # Calculate the volatility index (VI) - normalized CMO
    # VI ranges from 0 to 1, where 1 means maximum volatility
    volatility_index = abs_cmo / 100
    
    # Calculate VIDYA using the volatility index
    # VIDYA adapts the smoothing constant based on market volatility
    alpha = 2 / (length + 1)  # Standard EMA smoothing constant
    
    vidya = pd.Series(index=df_copy.index, dtype=float)
    vidya.iloc[0] = df_copy[column].iloc[0]  # Initialize with first price
    
    for i in range(1, len(df_copy)):
        if pd.notna(volatility_index.iloc[i]):
            # Adaptive smoothing constant
            # When volatility is high, VI approaches 1, making VIDYA more responsive
            # When volatility is low, VI approaches 0, making VIDYA smoother
            adaptive_alpha = alpha * volatility_index.iloc[i]
            
            vidya.iloc[i] = (adaptive_alpha * df_copy[column].iloc[i] + 
                           (1 - adaptive_alpha) * vidya.iloc[i-1])
        else:
            # If VI is NaN, use previous VIDYA value
            vidya.iloc[i] = vidya.iloc[i-1]
    
    # Store results
    df_copy['vidya'] = vidya
    
    return df_copy[['vidya']]


variable_index_dynamic_average.__doc__ = """
Name:
    Variable Index Dynamic Average (VIDYA)

Description:
    The Variable Index Dynamic Average (VIDYA) was developed by Tushar Chande in 1992.
    It is an adaptive moving average that adjusts its sensitivity based on market volatility.
    
    VIDYA uses the Chande Momentum Oscillator (CMO) to determine volatility. When volatility 
    is high, VIDYA reacts faster to price changes, making it more responsive than traditional
    moving averages. When volatility is low, it behaves more like a standard exponential 
    moving average.
    
    This indicator can be particularly useful for traders who want a moving average that 
    automatically adjusts to changing market conditions, potentially reducing lag during 
    volatile periods.

More info:
    https://www.tradingview.com/script/hdrf0fXV-Variable-Index-Dynamic-Average-VIDYA/
    https://www.perfecttrendsystem.com/blog_mt4_2/en/vidya-indicator-for-mt4

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the VIDYA calculation. Default is 14.
    - column (str): The column name to use for calculations. Default is 'close'.
    - drift (int): The period for momentum calculation in CMO. Default is 1.

Call with:
    result = bta.variable_index_dynamic_average(df)
    df['vidya'] = result['vidya']

Returns:
    pd.DataFrame: DataFrame with 'vidya' column.
"""


def test():
    """
    Test function for the variable_index_dynamic_average indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the variable_index_dynamic_average indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(variable_index_dynamic_average)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()