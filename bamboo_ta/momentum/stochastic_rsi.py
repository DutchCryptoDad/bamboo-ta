# -*- coding: utf-8 -*-
# stochastic_rsi.py

import pandas as pd
import numpy as np


def stochastic_rsi(
    df: pd.DataFrame,
    length_rsi: int = 14,
    length_stoch: int = 14,
    smooth_k: int = 3,
    smooth_d: int = 3,
    mamode: str = "sma",
) -> pd.DataFrame:
    """Stochastic RSI"""

    df_copy = df.copy()

    # Step 1: Calculate RSI using Wilder's smoothing method (same as TradingView)
    delta = df_copy["close"].diff()

    # Create upMove and downMove arrays
    up_move = pd.Series(0.0, index=delta.index)
    down_move = pd.Series(0.0, index=delta.index)

    # Populate upMove and downMove
    up_move[delta > 0] = delta[delta > 0]
    down_move[delta < 0] = -delta[delta < 0]

    # Calculate Wilder's Smoothing
    # First values are simple moving averages
    avg_up = up_move.rolling(window=length_rsi, min_periods=length_rsi).mean()
    avg_down = down_move.rolling(window=length_rsi, min_periods=length_rsi).mean()

    # Apply Wilder's smoothing for subsequent values
    for i in range(length_rsi, len(up_move)):
        avg_up[i] = ((avg_up[i - 1] * (length_rsi - 1)) + up_move[i]) / length_rsi
        avg_down[i] = ((avg_down[i - 1] * (length_rsi - 1)) + down_move[i]) / length_rsi

    # Calculate RSI
    rs = avg_up / np.maximum(avg_down, 1e-10)  # Prevent division by zero
    df_copy["rsi"] = 100 - (100 / (1 + rs))

    # Step 2: Calculate the Stochastic Oscillator on RSI
    # This matches TradingView's ta.stoch(rsi1, rsi1, rsi1, lengthStoch)
    lowest_rsi = df_copy["rsi"].rolling(window=length_stoch).min()
    highest_rsi = df_copy["rsi"].rolling(window=length_stoch).max()

    # Handle division by zero using numpy
    rsi_range = np.maximum(highest_rsi - lowest_rsi, 1e-10)  # Avoid division by zero
    stoch = 100 * (df_copy["rsi"] - lowest_rsi) / rsi_range

    # Step 3: Apply smoothing according to mamode (TradingView uses SMA by default)
    if mamode.lower() == "sma":
        stoch_k = stoch.rolling(window=smooth_k).mean()
        stoch_d = stoch_k.rolling(window=smooth_d).mean()
    elif mamode.lower() == "ema":
        stoch_k = stoch.ewm(span=smooth_k, adjust=False).mean()
        stoch_d = stoch_k.ewm(span=smooth_d, adjust=False).mean()
    else:
        # Default to SMA if unknown mode
        stoch_k = stoch.rolling(window=smooth_k).mean()
        stoch_d = stoch_k.rolling(window=smooth_d).mean()

    df_copy["stoch_rsi_k"] = stoch_k
    df_copy["stoch_rsi_d"] = stoch_d

    return df_copy[["stoch_rsi_k", "stoch_rsi_d"]]


stochastic_rsi.__doc__ = """
Name:
    Stochastic RSI (StochasticRSI)

Description:
    The Stochastic RSI is a technical momentum oscillator that combines Stochastic Oscillator
    and Relative Strength Index (RSI). It is used to identify overbought and oversold conditions
    in the market by applying the Stochastic formula to RSI values rather than price data.
    
    Originally developed by Tushar Chande and Stanley Kroll, it provides a more sensitive indicator
    than standard RSI or Stochastic oscillators alone, operating within a 0-100 range.

More info:
    https://www.investopedia.com/terms/s/stochrsi.asp

Calculation:
    - Calculate RSI for the given period (length_rsi) using Wilder's smoothing method
    - Find lowest and highest RSI values over the stochastic period (length_stoch)
    - Apply the Stochastic formula to RSI: 100 * (RSI - MinRSI) / (MaxRSI - MinRSI)
    - Smooth the %K line using SMA with period (smooth_k)
    - Smooth the %D line using SMA with period (smooth_d) on the %K line

Parameters:
    - df (pd.DataFrame): DataFrame containing the data with a 'close' column.
    - length_rsi (int): Period for the RSI calculation. Default is 14.
    - length_stoch (int): Period for the Stochastic calculation. Default is 14.
    - smooth_k (int): Smoothing period for %K line. Default is 3.
    - smooth_d (int): Smoothing period for %D line. Default is 3.
    - mamode (str): Moving average type for smoothing ('sma' or 'ema'). Default is 'sma'.

Call with:
    stoch_rsi = bta.stochastic_rsi(df, length_rsi=14, length_stoch=14, smooth_k=3, smooth_d=3)
    df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
    df["stoch_rsi_d"] = stoch_rsi["stoch_rsi_d"]

Returns:
    pd.DataFrame: DataFrame with 'stoch_rsi_k' and 'stoch_rsi_d' columns.
"""


def test():
    """
    Test function for the stochastic_rsi indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the stochastic_rsi indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(stochastic_rsi)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
