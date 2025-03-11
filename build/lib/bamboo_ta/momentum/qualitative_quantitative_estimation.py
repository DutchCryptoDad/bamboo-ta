# -*- coding: utf-8 -*-
# qualitative_quantitative_estimation.py

import pandas as pd
import numpy as np


def qqe_mod(
    df: pd.DataFrame,
    rsi_period: int = 6,
    rsi_smoothing: int = 5,
    qqe_factor: int = 3,
    threshold: int = 3,
    bollinger_length: int = 50,
    bb_multiplier: float = 0.35,
    rsi_period2: int = 6,
    rsi_smoothing2: int = 5,
    qqe_factor2: float = 1.61,
    threshold2: int = 3,
) -> pd.DataFrame:
    """Qualitative Quantitative Estimation"""

    # Define internal helper functions to make the QQE self-contained
    def wilders_ema(series, period):
        return series.ewm(alpha=1 / period, adjust=False).mean()

    def relative_strength_index(df_local, column="close", period=14):
        """Calculate Relative Strength Index"""
        df_rsi = df_local.copy()
        delta = df_rsi[column].diff(1)
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()

        # Apply the Wilder's smoothing technique for gain and loss averages
        for i in range(period, len(df_rsi)):
            avg_gain.iloc[i] = (
                avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]
            ) / period
            avg_loss.iloc[i] = (
                avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]
            ) / period

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def exponential_moving_average(df_local, column="close", period=21):
        """Calculate Exponential Moving Average"""
        ema = df_local[column].ewm(span=period, adjust=False).mean()
        return ema

    def simple_moving_average(df_local, column="close", period=21):
        """Calculate Simple Moving Average"""
        sma = df_local[column].rolling(window=period).mean()
        return sma

    df_copy = df.copy()

    # First QQE Calculation
    wilders_period = rsi_period * 2 - 1

    rsi = relative_strength_index(df_copy, column="close", period=rsi_period)
    rsi_ma = exponential_moving_average(
        df_copy.assign(rsi=rsi), column="rsi", period=rsi_smoothing
    )
    atr_rsi = abs(rsi_ma.shift(1) - rsi_ma)
    ma_atr_rsi = wilders_ema(atr_rsi, wilders_period)
    dar = wilders_ema(ma_atr_rsi, wilders_period) * qqe_factor

    longband = np.zeros(len(df_copy))
    shortband = np.zeros(len(df_copy))
    trend = np.zeros(len(df_copy))

    delta_fast_atr_rsi = dar
    rsindex = rsi_ma

    for i in range(1, len(df_copy)):
        if i > 1:
            if rsindex[i - 1] > longband[i - 1] and rsindex[i] > longband[i - 1]:
                longband[i] = max(longband[i - 1], rsindex[i] - delta_fast_atr_rsi[i])
            else:
                longband[i] = rsindex[i] - delta_fast_atr_rsi[i]

            if rsindex[i - 1] < shortband[i - 1] and rsindex[i] < shortband[i - 1]:
                shortband[i] = min(shortband[i - 1], rsindex[i] + delta_fast_atr_rsi[i])
            else:
                shortband[i] = rsindex[i] + delta_fast_atr_rsi[i]

        else:
            longband[i] = rsindex[i] - delta_fast_atr_rsi[i]
            shortband[i] = rsindex[i] + delta_fast_atr_rsi[i]

        if rsindex[i] > shortband[i - 1]:
            trend[i] = 1
        elif rsindex[i] < longband[i - 1]:
            trend[i] = 0
        else:
            trend[i] = trend[i - 1]

    fast_atr_rsi_tl = np.where(trend == 1, longband, shortband)

    # Bollinger Bands on FastATRRSI TL
    basis = simple_moving_average(
        pd.DataFrame(fast_atr_rsi_tl - 50), column=0, period=bollinger_length
    )
    dev = bb_multiplier * (
        pd.DataFrame(fast_atr_rsi_tl - 50)[0]
        .rolling(window=bollinger_length)
        .std(ddof=0)
    )
    upper = basis + dev
    lower = basis - dev

    # Second QQE Calculation
    wilders_period2 = rsi_period2 * 2 - 1

    rsi2 = relative_strength_index(df_copy, column="close", period=rsi_period2)
    rsi_ma2 = exponential_moving_average(
        df_copy.assign(rsi2=rsi2), column="rsi2", period=rsi_smoothing2
    )
    atr_rsi2 = abs(rsi_ma2.shift(1) - rsi_ma2)
    ma_atr_rsi2 = wilders_ema(atr_rsi2, wilders_period2)
    dar2 = wilders_ema(ma_atr_rsi2, wilders_period2) * qqe_factor2

    longband2 = np.zeros(len(df_copy))
    shortband2 = np.zeros(len(df_copy))
    trend2 = np.zeros(len(df_copy))

    delta_fast_atr_rsi2 = dar2
    rsindex2 = rsi_ma2

    for i in range(1, len(df_copy)):
        if i > 1:
            if rsindex2[i - 1] > longband2[i - 1] and rsindex2[i] > longband2[i - 1]:
                longband2[i] = max(
                    longband2[i - 1], rsindex2[i] - delta_fast_atr_rsi2[i]
                )
            else:
                longband2[i] = rsindex2[i] - delta_fast_atr_rsi2[i]

            if rsindex2[i - 1] < shortband2[i - 1] and rsindex2[i] < shortband2[i - 1]:
                shortband2[i] = min(
                    shortband2[i - 1], rsindex2[i] + delta_fast_atr_rsi2[i]
                )
            else:
                shortband2[i] = rsindex2[i] + delta_fast_atr_rsi2[i]
        else:
            longband2[i] = rsindex2[i] - delta_fast_atr_rsi2[i]
            shortband2[i] = rsindex2[i] + delta_fast_atr_rsi2[i]

        if rsindex2[i] > shortband2[i - 1]:
            trend2[i] = 1
        elif rsindex2[i] < longband2[i - 1]:
            trend2[i] = 0
        else:
            trend2[i] = trend2[i - 1]

    fast_atr_rsi2_tl = np.where(trend2 == 1, longband2, shortband2)

    df_copy["qqe_line"] = fast_atr_rsi2_tl - 50
    df_copy["hist"] = rsi_ma2 - 50

    # Final Calculations
    greenbar1 = rsi_ma - 50 > upper
    redbar1 = rsi_ma - 50 < lower
    greenbar2 = rsi_ma2 - 50 > upper
    redbar2 = rsi_ma - 50 < lower

    df_copy["qqe_up"] = np.where(greenbar1 & greenbar2, rsi_ma2 - 50, np.nan)
    df_copy["qqe_down"] = np.where(redbar1 & redbar2, rsi_ma2 - 50, np.nan)

    return df_copy[["qqe_line", "hist", "qqe_up", "qqe_down"]]


qqe_mod.__doc__ = """
Name:
    Qualitative Quantitative Estimation Modified (QQE Mod)

Description:
    The Qualitative Quantitative Estimation (QQE) is a technical indicator based on RSI 
    with a dynamic volatility-based trailing stop line. The modified version (QQE Mod) 
    incorporates two QQE calculations with different parameters and Bollinger Bands to 
    provide additional trading signals.

More info:
    https://www.tradingview.com/script/TpUW4muw-QQE-MOD/

Call with:
    qqe_df = bta.qqe_mod(df)
    df['qqe_line'] = qqe_df['qqe_line']
    df['hist'] = qqe_df['hist']
    df['qqe_up'] = qqe_df['qqe_up']
    df['qqe_down'] = qqe_df['qqe_down']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain a 'close' column.
    - rsi_period (int): Period for the first RSI calculation. Default is 6.
    - rsi_smoothing (int): Smoothing period for the first RSI. Default is 5.
    - qqe_factor (int): Multiplication factor for the first QQE ATR. Default is 3.
    - threshold (int): Threshold for the first QQE. Default is 3.
    - bollinger_length (int): Length for Bollinger Bands calculation. Default is 50.
    - bb_multiplier (float): Multiplier for Bollinger Bands standard deviation. Default is 0.35.
    - rsi_period2 (int): Period for the second RSI calculation. Default is 6.
    - rsi_smoothing2 (int): Smoothing period for the second RSI. Default is 5.
    - qqe_factor2 (float): Multiplication factor for the second QQE ATR. Default is 1.61.
    - threshold2 (int): Threshold for the second QQE. Default is 3.

Returns:
    pd.DataFrame: DataFrame with 'qqe_line', 'hist', 'qqe_up', and 'qqe_down' columns.
"""


def test():
    """
    Test function for the qqe_mod indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the qqe_mod indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(qqe_mod)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
