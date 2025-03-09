# -*- coding: utf-8 -*-
# keltner_channel.py
import numpy as np
import pandas as pd


def keltner_channel(
    df: pd.DataFrame,
    column: str = "close",
    ema_length: int = 20,
    atr_length: int = 10,
    atr_mult: float = 2.0,
) -> pd.DataFrame:
    """Keltner Channel"""
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate ATR for the channel width
    # Calculate True Range components
    df_copy["high_low"] = df_copy["high"] - df_copy["low"]
    df_copy["high_close"] = (df_copy["high"] - df_copy["close"].shift()).abs()
    df_copy["low_close"] = (df_copy["low"] - df_copy["close"].shift()).abs()

    # Calculate True Range
    df_copy["true_range"] = df_copy[["high_low", "high_close", "low_close"]].max(axis=1)

    # Calculate ATR as the rolling mean of True Range
    df_copy["atr"] = (
        df_copy["true_range"].rolling(window=atr_length, min_periods=1).mean()
    )

    # Calculate the middle line (EMA)
    df_copy["kc_middle"] = df_copy[column].ewm(span=ema_length, adjust=False).mean()

    # Calculate the upper and lower bands
    df_copy["kc_upper"] = df_copy["kc_middle"] + (df_copy["atr"] * atr_mult)
    df_copy["kc_lower"] = df_copy["kc_middle"] - (df_copy["atr"] * atr_mult)

    # Calculate the width of the channel
    df_copy["kc_width"] = (df_copy["kc_upper"] - df_copy["kc_lower"]) / df_copy[
        "kc_middle"
    ]

    return df_copy[["kc_middle", "kc_upper", "kc_lower", "kc_width"]]


keltner_channel.__doc__ = """
Name:
    Keltner Channel

Description:
    The Keltner Channel is a volatility-based indicator that consists of three lines: 
    a middle line (typically an EMA), an upper band, and a lower band. The upper and 
    lower bands are calculated by adding and subtracting a multiple of the Average 
    True Range (ATR) from the middle line. 
    
    Unlike Bollinger Bands which use standard deviation, Keltner Channels use ATR, 
    making them more responsive to volatility changes based on trading ranges 
    rather than closing prices.

More info:
    https://www.investopedia.com/terms/k/keltnerchannel.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high', 'low', and 'close'.
    - column (str): The column name to use for the middle line calculation. Default is 'close'.
    - ema_length (int): Period for the EMA calculation for the middle line. Default is 20.
    - atr_length (int): Period for the ATR calculation. Default is 10.
    - atr_mult (float): Multiplier for the ATR to determine the channel width. Default is 2.0.

Call with:
    kc_result = bta.keltner_channel(df, 'close', 20, 10, 2.0)
    df['kc_middle'] = kc_result['kc_middle']
    df['kc_upper'] = kc_result['kc_upper']
    df['kc_lower'] = kc_result['kc_lower']
    df['kc_width'] = kc_result['kc_width']

Returns:
    pd.DataFrame: DataFrame with 'kc_middle', 'kc_upper', 'kc_lower', and 'kc_width' columns.
"""


def test():
    """
    Test function for the keltner_channel indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the keltner_channel indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(keltner_channel)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
