# -*- coding: utf-8 -*-
# ssl_channels_atr.py
import numpy as np
import pandas as pd


def ssl_channels_atr(
    df: pd.DataFrame, column: str = "close", length: int = 21, atr_period: int = 14
) -> pd.DataFrame:
    """SSL Channels with ATR"""
    df_copy = df.copy()

    # Internal ATR calculation
    def calculate_atr(df, period):
        high_low = df["high"] - df["low"]
        high_close = np.abs(df["high"] - df["close"].shift())
        low_close = np.abs(df["low"] - df["close"].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period, min_periods=1).mean()
        return atr

    # Calculate ATR and adjusted SMAs
    df_copy["atr"] = calculate_atr(df_copy, atr_period)
    df_copy["sma_high"] = df_copy["high"].rolling(length).mean() + df_copy["atr"]
    df_copy["sma_low"] = df_copy["low"].rolling(length).mean() - df_copy["atr"]

    # Determine trend direction
    df_copy["hlv"] = np.where(
        df_copy[column] > df_copy["sma_high"],
        1,
        np.where(df_copy[column] < df_copy["sma_low"], -1, np.nan),
    )
    df_copy["hlv"] = df_copy["hlv"].ffill()

    # Calculate SSL ATR channels
    df_copy["ssl_atr_down"] = np.where(
        df_copy["hlv"] < 0, df_copy["sma_high"], df_copy["sma_low"]
    )
    df_copy["ssl_atr_up"] = np.where(
        df_copy["hlv"] < 0, df_copy["sma_low"], df_copy["sma_high"]
    )

    return df_copy[["ssl_atr_down", "ssl_atr_up"]]


ssl_channels_atr.__doc__ = """
Name:
    SSL Channels with ATR

Description:
    The ssl_channels_atr function calculates the SSL (Safe and Secure Levels) channels using
    the Average True Range (ATR) to adjust the Simple Moving Averages (SMA) of the high
    and low prices over a specified period. It determines the trend direction based on
    the comparison of a chosen price column with these adjusted SMAs and generates the
    SSL ATR Down and Up levels accordingly.

    This indicator helps identify potential trend reversals and continuations by providing
    dynamic support and resistance levels.

More info:
    https://www.tradingview.com/script/xl7XbPTM-SSL-Channel-Chart/

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the SMA calculation. Default is 21.
    - atr_period (int): Period for the ATR calculation. Default is 14.
    - column (str): The column to use for the moving average calculations. Default is 'close'.

Call with:
    ssl_result = bta.ssl_channels_atr(df, column='close', length=14, atr_period=7)
    df['ssl_atr_down'] = ssl_result['ssl_atr_down']
    df['ssl_atr_up'] = ssl_result['ssl_atr_up']

Returns:
    pd.DataFrame: DataFrame with 'ssl_atr_down' and 'ssl_atr_up' columns.
"""


def test():
    """
    Test function for the ssl_channels_atr indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ssl_channels_atr indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ssl_channels_atr)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
