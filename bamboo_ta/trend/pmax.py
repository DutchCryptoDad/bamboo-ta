# -*- coding: utf-8 -*-
# pmax.py
import numpy as np
import pandas as pd


def pmax(
    df: pd.DataFrame,
    period: int,
    multiplier: float,
    length: int,
    ma_type: str = "EMA",
    src: str = "close",
) -> pd.DataFrame:
    """Pmax Indicator"""
    df_copy = df.copy()

    # Define the source price
    if src == "close":
        masrc = df_copy["close"]
    elif src == "hl2":
        masrc = (df_copy["high"] + df_copy["low"]) / 2
    elif src == "ohlc4":
        masrc = (
            df_copy["open"] + df_copy["high"] + df_copy["low"] + df_copy["close"]
        ) / 4
    else:
        raise ValueError(f"Invalid src value: {src}")

    # Moving average calculations
    if ma_type == "EMA":
        mavalue = masrc.ewm(span=length, adjust=False).mean()
    elif ma_type == "SMA":
        mavalue = masrc.rolling(window=length).mean()
    else:
        raise ValueError(f"Invalid ma_type value: {ma_type}")

    # ATR calculation (self-contained)
    df_copy["tr"] = np.maximum(
        df_copy["high"] - df_copy["low"],
        np.maximum(
            abs(df_copy["high"] - df_copy["close"].shift()),
            abs(df_copy["low"] - df_copy["close"].shift()),
        ),
    )
    df_copy["atr"] = df_copy["tr"].rolling(window=period).mean()

    # Calculate bands
    df_copy["basic_ub"] = mavalue + (multiplier * df_copy["atr"])
    df_copy["basic_lb"] = mavalue - (multiplier * df_copy["atr"])

    # Final upper and lower bands
    final_ub = np.full(len(df_copy), 0.00)
    final_lb = np.full(len(df_copy), 0.00)

    for i in range(period, len(df_copy)):
        final_ub[i] = (
            df_copy["basic_ub"].iloc[i]
            if df_copy["basic_ub"].iloc[i] < final_ub[i - 1]
            or mavalue.iloc[i - 1] > final_ub[i - 1]
            else final_ub[i - 1]
        )
        final_lb[i] = (
            df_copy["basic_lb"].iloc[i]
            if df_copy["basic_lb"].iloc[i] > final_lb[i - 1]
            or mavalue.iloc[i - 1] < final_lb[i - 1]
            else final_lb[i - 1]
        )

    # Determine the Pmax values
    pm_arr = np.full(len(df_copy), 0.00)
    for i in range(period, len(df_copy)):
        pm_arr[i] = (
            final_ub[i]
            if pm_arr[i - 1] == final_ub[i - 1] and mavalue.iloc[i] <= final_ub[i]
            else final_lb[i]
            if pm_arr[i - 1] == final_ub[i - 1] and mavalue.iloc[i] > final_ub[i]
            else final_lb[i]
            if pm_arr[i - 1] == final_lb[i - 1] and mavalue.iloc[i] >= final_lb[i]
            else final_ub[i]
            if pm_arr[i - 1] == final_lb[i - 1] and mavalue.iloc[i] < final_lb[i]
            else 0.00
        )

    # Mark the trend direction
    df_copy["pmax"] = pm_arr
    df_copy["pmax_trend"] = np.where(
        pm_arr > 0.00, np.where(mavalue < pm_arr, "down", "up"), np.NaN
    )

    return df_copy[["pmax", "pmax_trend"]]


pmax.__doc__ = """
Name:
    Pmax Indicator

Description:
    A self-contained implementation of the Pmax indicator that calculates upper and lower
    bands based on a moving average and Average True Range (ATR). The function is independent
    of any external libraries.

More info:
    https://www.tradingview.com/script/sU9molfV/

Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data.
    - period (int): Lookback period for ATR calculation.
    - multiplier (float): ATR multiplier to calculate bands.
    - length (int): Lookback period for the moving average.
    - ma_type (str, default='EMA'): Type of moving average to use. Options are:
        - 'EMA' (Exponential Moving Average)
        - 'SMA' (Simple Moving Average)
    - src (str, default='close'): Source price for calculation. Options are:
        - 'close' (default)
        - 'hl2' (average of high and low)
        - 'ohlc4' (average of open, high, low, and close)

Call with:
    pmax_result = bta.pmax(df, period=14, multiplier=2.0, length=20, ma_type='EMA', src='close')
    df['pmax'] = pmax_result['pmax']
    df['pmax_trend'] = pmax_result['pmax_trend']

Returns:
    pd.DataFrame: DataFrame with the following columns added:
        - 'pmax': Final Pmax values.
        - 'pmax_trend': Trend direction ('up' or 'down').
"""


def test():
    """
    Test function for the pmax indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the pmax indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(pmax)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
