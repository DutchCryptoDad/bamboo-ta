# -*- coding: utf-8 -*-
# ma_streak.py
import numpy as np
import pandas as pd


def ma_streak(
    df: pd.DataFrame, length: int = 10, src: str = "close", matype: int = 1
) -> pd.DataFrame:
    """MA Streak Indicator"""
    df_copy = df.copy()

    # Calculate different types of moving averages
    df_copy["sma"] = df_copy[src].rolling(window=length).mean()
    df_copy["ema"] = df_copy[src].ewm(span=length, adjust=False).mean()
    df_copy["wma"] = (
        df_copy[src]
        .rolling(window=length)
        .apply(
            lambda prices: np.dot(prices, np.arange(1, length + 1))
            / np.arange(1, length + 1).sum(),
            raw=True,
        )
    )
    df_copy["vwma"] = (df_copy[src] * df_copy["volume"]).rolling(
        window=length
    ).sum() / df_copy["volume"].rolling(window=length).sum()

    # Calculate Hull Moving Average (HMA)
    half_length = int(length / 2)
    sqrt_length = int(np.sqrt(length))
    df_copy["hma"] = df_copy[src].rolling(window=half_length).mean()
    df_copy["hma"] = 2 * df_copy["hma"] - df_copy[src].rolling(window=length).mean()
    df_copy["hma"] = df_copy["hma"].rolling(window=sqrt_length).mean()

    # Select the appropriate moving average
    if matype == 1:
        df_copy["avgval"] = df_copy["sma"]
    elif matype == 2:
        df_copy["avgval"] = df_copy["ema"]
    elif matype == 3:
        df_copy["avgval"] = df_copy["hma"]
    elif matype == 4:
        df_copy["avgval"] = df_copy["wma"]
    elif matype == 5:
        df_copy["avgval"] = df_copy["vwma"]
    else:
        raise ValueError("Invalid moving average type. Choose a value between 1 and 5.")

    # Initialize the streak columns
    df_copy["upcount"] = 0
    df_copy["dncount"] = 0
    df_copy["ma_streak"] = 0

    # Calculate the streak
    for i in range(1, len(df_copy)):
        if df_copy["avgval"].iloc[i] > df_copy["avgval"].iloc[i - 1]:
            df_copy.at[i, "upcount"] = df_copy.at[i - 1, "upcount"] + 1
            df_copy.at[i, "dncount"] = 0
        elif df_copy["avgval"].iloc[i] < df_copy["avgval"].iloc[i - 1]:
            df_copy.at[i, "dncount"] = df_copy.at[i - 1, "dncount"] - 1
            df_copy.at[i, "upcount"] = 0
        df_copy.at[i, "ma_streak"] = df_copy.at[i, "upcount"] + df_copy.at[i, "dncount"]

    return df_copy[["ma_streak"]]


ma_streak.__doc__ = """
Name:
    MA Streak Indicator

Description:
    This indicator tracks how many bars a given moving average is rising or falling.
    It's color-coded green (positive) or red (negative).

More info:
    https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/

Call with:
    df['ma_streak'] = bta.ma_streak(df, length=10, src='close', matype=1)['ma_streak']

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the moving average calculation. Default is 10.
    - src (str): The column name to use for the moving average calculation. Default is 'close'.
    - matype (int): Type of moving average to use. Default is 1 (SMA).

    MA types:
    1 - Simple Moving Average (SMA)
    2 - Exponential Moving Average (EMA)
    3 - Hull Moving Average (HMA)
    4 - Weighted Moving Average (WMA)
    5 - Volume Weighted Moving Average (VWMA)

Returns:
    pd.DataFrame: DataFrame with 'ma_streak' column.
"""


def test():
    """
    Test function for the ma_streak indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ma_streak indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ma_streak)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
