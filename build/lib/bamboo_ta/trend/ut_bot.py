# -*- coding: utf-8 -*-
# ut_bot.py
import numpy as np
import pandas as pd


def ut_bot(
    df: pd.DataFrame,
    column: str = "close",
    key_value: float = 3.0,
    atr_period: int = 10,
) -> pd.DataFrame:
    """UT Bot Indicator"""
    df_copy = df.copy()
    src = df_copy[column]

    # Calculate ATR
    df_copy["tr"] = np.maximum(
        df_copy["high"] - df_copy["low"],
        np.maximum(
            abs(df_copy["high"] - df_copy["close"].shift()),
            abs(df_copy["low"] - df_copy["close"].shift()),
        ),
    )
    x_atr = df_copy["tr"].rolling(window=atr_period).mean()
    n_loss = key_value * x_atr

    # Initialize trailing stop array
    x_atr_trailing_stop = pd.Series(index=df_copy.index, dtype=float)

    # Calculate trailing stop
    for i in range(len(df_copy)):
        if i == 0:
            x_atr_trailing_stop.iloc[i] = src.iloc[i]
            continue

        prev_stop = x_atr_trailing_stop.iloc[i - 1]
        curr_src = src.iloc[i]
        prev_src = src.iloc[i - 1]

        if curr_src > prev_stop and prev_src > prev_stop:
            x_atr_trailing_stop.iloc[i] = max(prev_stop, curr_src - n_loss.iloc[i])
        elif curr_src < prev_stop and prev_src < prev_stop:
            x_atr_trailing_stop.iloc[i] = min(prev_stop, curr_src + n_loss.iloc[i])
        elif curr_src > prev_stop:
            x_atr_trailing_stop.iloc[i] = curr_src - n_loss.iloc[i]
        else:
            x_atr_trailing_stop.iloc[i] = curr_src + n_loss.iloc[i]

    # Calculate position
    position = pd.Series(0, index=df_copy.index)
    for i in range(1, len(df_copy)):
        prev_src = src.iloc[i - 1]
        curr_src = src.iloc[i]
        prev_stop = x_atr_trailing_stop.iloc[i - 1]

        if prev_src < prev_stop and curr_src > prev_stop:
            position.iloc[i] = 1
        elif prev_src > prev_stop and curr_src < prev_stop:
            position.iloc[i] = -1
        else:
            position.iloc[i] = position.iloc[i - 1]

    # Calculate buy/sell signals
    buy_signal = (src > x_atr_trailing_stop) & (
        src.shift(1) <= x_atr_trailing_stop.shift(1)
    )
    sell_signal = (src < x_atr_trailing_stop) & (
        src.shift(1) >= x_atr_trailing_stop.shift(1)
    )

    df_copy["ut_bot_stop"] = x_atr_trailing_stop
    df_copy["ut_bot_position"] = position
    df_copy["ut_bot_buy"] = buy_signal
    df_copy["ut_bot_sell"] = sell_signal

    return df_copy[["ut_bot_stop", "ut_bot_position", "ut_bot_buy", "ut_bot_sell"]]


ut_bot.__doc__ = """
Name:
    UT Bot Indicator

Description:
    A trend-following indicator that uses ATR to create a trailing stop that helps identify trend changes
    and potential entry/exit points. Originally created by HPotter.

More info:
    https://www.tradingview.com/script/jKqk8tWu-UT-BOT-1-3/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain OHLC data
    - column (str): The column name to use for calculations. Default is 'close'
    - key_value (float): Sensitivity multiplier for the ATR. Default is 3.0
    - atr_period (int): Period for ATR calculation. Default is 10

Call with:
    result = bta.ut_bot(df, 'close', 3.0, 10)
    df['ut_bot_stop'] = result['ut_bot_stop']
    df['ut_bot_position'] = result['ut_bot_position']
    df['ut_bot_buy'] = result['ut_bot_buy']
    df['ut_bot_sell'] = result['ut_bot_sell']

Returns:
    pd.DataFrame: DataFrame with 'ut_bot_stop', 'ut_bot_position', 'ut_bot_buy', and 'ut_bot_sell' columns
"""


def test():
    """
    Test function for the ut_bot indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the ut_bot indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(ut_bot)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
