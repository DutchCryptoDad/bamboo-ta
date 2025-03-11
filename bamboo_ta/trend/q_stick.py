# -*- coding: utf-8 -*-
# q_stick.py

import pandas as pd
import numpy as np


def q_stick(
    df: pd.DataFrame,
    length: int = 10,
    ma_type: str = "SMA"
) -> pd.DataFrame:
    """Q Stick Indicator"""
    df_copy = df.copy()
    
    # Ensure the DataFrame contains the required columns
    required_columns = ["open", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")
    
    # Validate parameters
    length = int(length) if length > 0 else 10
    
    # Calculate difference between close and open
    diff = df_copy["close"] - df_copy["open"]
    
    # Apply the selected moving average type
    ma_type = ma_type.upper()
    
    if ma_type == "SMA":
        # Simple Moving Average
        q_stick_val = diff.rolling(window=length).mean()
    elif ma_type == "EMA":
        # Exponential Moving Average
        q_stick_val = diff.ewm(span=length, adjust=False).mean()
    elif ma_type == "DEMA":
        # Double Exponential Moving Average
        ema1 = diff.ewm(span=length, adjust=False).mean()
        ema2 = ema1.ewm(span=length, adjust=False).mean()
        q_stick_val = 2 * ema1 - ema2
    elif ma_type == "WMA":
        # Weighted Moving Average
        weights = np.arange(1, length + 1)
        q_stick_val = diff.rolling(window=length).apply(
            lambda x: np.sum(weights * x) / np.sum(weights), 
            raw=True
        )
    elif ma_type == "HMA":
        # Hull Moving Average
        half_length = int(length / 2)
        sqrt_length = int(np.sqrt(length))
        
        # Calculate WMA with half the length
        wma_half = diff.rolling(window=half_length).apply(
            lambda x: np.sum(np.arange(1, len(x) + 1) * x) / np.sum(np.arange(1, len(x) + 1)),
            raw=True
        )
        
        # Calculate WMA with the full length
        wma_full = diff.rolling(window=length).apply(
            lambda x: np.sum(np.arange(1, len(x) + 1) * x) / np.sum(np.arange(1, len(x) + 1)),
            raw=True
        )
        
        # Calculate 2 * WMA(half) - WMA(full)
        h = 2 * wma_half - wma_full
        
        # Calculate WMA of h with length sqrt(original_length)
        q_stick_val = h.rolling(window=sqrt_length).apply(
            lambda x: np.sum(np.arange(1, len(x) + 1) * x) / np.sum(np.arange(1, len(x) + 1)),
            raw=True
        )
    elif ma_type == "RMA":
        # Running/Rolling Moving Average (equivalent to EMA with alpha=1/length)
        alpha = 1.0 / length
        q_stick_val = diff.ewm(alpha=alpha, adjust=False).mean()
    else:
        raise ValueError(f"Unsupported moving average type: {ma_type}")
    
    # Store result in DataFrame
    df_copy["q_stick"] = q_stick_val
    
    return df_copy[["q_stick"]]


q_stick.__doc__ = \
"""
Name:
    Q Stick Indicator

Description:
    The Q Stick indicator, developed by Tushar Chande, attempts to quantify and
    identify trends in candlestick charts by measuring the relationship between
    opening and closing prices over a specified period.
    
    A positive Q Stick value indicates buying pressure (more closes above opens),
    while a negative value indicates selling pressure (more closes below opens).
    Values near zero suggest a balance between buying and selling pressure.
    
    This implementation allows for different types of moving averages to be applied
    to the difference between close and open prices.

More info:
    https://library.tradingtechnologies.com/trade/chrt-ti-qstick.html

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open' and 'close' columns.
    - length (int): Period for the moving average calculation. Default is 10.
    - ma_type (str): The type of moving average to use. Options include:
      'SMA' (Simple), 'EMA' (Exponential), 'DEMA' (Double Exponential),
      'WMA' (Weighted), 'HMA' (Hull), 'RMA' (Running/Rolling). Default is 'SMA'.

Call with:
    result = bta.q_stick(df, length=10, ma_type='EMA')
    df['q_stick'] = result['q_stick']

Returns:
    pd.DataFrame: DataFrame with 'q_stick' column containing the indicator values.
"""


def test():
    """
    Test function for the q_stick indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the q_stick indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(q_stick)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 