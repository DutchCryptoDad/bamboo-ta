# -*- coding: utf-8 -*-
# calculate_atr_stop_loss_take_profit.py
import numpy as np
import pandas as pd


def calculate_atr_stop_loss_take_profit(
    df: pd.DataFrame,
    signal_column: str = "signal",
    atr_column: str = "atr",
    atr_sl_mult: float = 1,
    atr_tp_mult: float = 2,
) -> pd.DataFrame:
    """
    Calculate take profit, stop loss, and buy price based on ATR, signal, and advice changes.

    This version includes an internal logic that calculates 'advice_changed' based on whether
    the current signal differs from the previous signal.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame with columns 'signal', 'close', and 'atr'.
    - signal_column (str): Column with buy/sell signals. Default is 'signal'.
    - atr_column (str): Column with ATR values. Default is 'atr'.
    - atr_sl_mult (float): Multiplier for stop loss based on ATR. Default is 1.
    - atr_tp_mult (float): Multiplier for take profit based on ATR. Default is 2.

    Call with:
        atr_sl_tp_df = bta.calculate_atr_stop_loss_take_profit(df, signal_column='signal')
        df['takeprofit'] = atr_sl_tp_df['takeprofit']
        df['stoploss'] = atr_sl_tp_df['stoploss']
        df['buyprice'] = atr_sl_tp_df['buyprice']

    Returns:
    - pd.DataFrame: DataFrame with 'takeprofit', 'stoploss', and 'buyprice' columns.
    """
    # Create a new column for advice_changed if it does not exist
    df["advice_changed"] = df[signal_column] != df[signal_column].shift(1)

    # Initialize new columns for take profit, stop loss, and buy price
    takeprofit = np.full(len(df), np.nan)
    stoploss = np.full(len(df), np.nan)
    buyprice = np.full(len(df), np.nan)

    # Logic for when the advice has changed and signal is 'buy'
    buy_mask = (df["advice_changed"]) & (df[signal_column] == "buy")
    takeprofit[buy_mask] = df["close"][buy_mask] + (
        df[atr_column][buy_mask] * atr_tp_mult
    )
    stoploss[buy_mask] = df["close"][buy_mask] - (
        df[atr_column][buy_mask] * atr_sl_mult
    )
    buyprice[buy_mask] = df["close"][buy_mask]

    # Logic for carrying forward the previous values if the advice has not changed
    no_change_mask = ~df["advice_changed"]
    takeprofit[no_change_mask] = pd.Series(takeprofit).shift(1)
    stoploss[no_change_mask] = pd.Series(stoploss).shift(1)
    buyprice[no_change_mask] = pd.Series(buyprice).shift(1)

    # Return the result as a DataFrame
    result_df = pd.DataFrame(
        {"takeprofit": takeprofit, "stoploss": stoploss, "buyprice": buyprice}
    )

    return result_df


calculate_atr_stop_loss_take_profit.__doc__ = """
Name:
    Calculate ATR Stop-Loss and Take-Profit

Description:
    This function calculates take-profit, stop-loss, and entry price levels based on the
    Average True Range (ATR) indicator and trading signals. The ATR is a volatility indicator
    that measures market volatility by decomposing the entire range of an asset price for
    a specific period.
    
    The function identifies when a trade signal changes (e.g., from neutral to buy) and
    calculates appropriate risk management levels based on the current ATR value. It uses
    configurable multipliers to determine the distance from entry for stop-loss and take-profit.

More info:
    Using ATR for stop-loss and take-profit placement is a common volatility-based risk
    management technique. The ATR helps adapt these levels to current market conditions:
    - In volatile markets, the ATR increases, resulting in wider stops to avoid premature exits
    - In calm markets, the ATR decreases, allowing for tighter stops to lock in profits

Parameters:
    - df (pd.DataFrame): Input DataFrame with required columns:
        - The signal column (by default 'signal')
        - 'close' price column
        - The ATR column (by default 'atr')
    - signal_column (str): Column with buy/sell signals. Default is 'signal'.
    - atr_column (str): Column containing ATR values. Default is 'atr'.
    - atr_sl_mult (float): Multiplier for stop-loss calculation. Default is 1.
    - atr_tp_mult (float): Multiplier for take-profit calculation. Default is 2.

Call with:
    # After calculating ATR and generating signals
    atr_sl_tp = bta.calculate_atr_stop_loss_take_profit(
        df, 
        signal_column='signal', 
        atr_column='atr_14',
        atr_sl_mult=1.5,
        atr_tp_mult=3.0
    )
    
    # Add results to original dataframe
    df['tp'] = atr_sl_tp['takeprofit']
    df['sl'] = atr_sl_tp['stoploss']
    df['entry'] = atr_sl_tp['buyprice']

Returns:
    pd.DataFrame: A DataFrame with three columns:
    - 'takeprofit': The price levels for taking profit
    - 'stoploss': The price levels for stop-loss
    - 'buyprice': The entry price levels

Important Notes:
    - This function REQUIRES that your DataFrame already contains specific columns:
      * A signal column (default name: 'signal') with values including 'buy'
      * An ATR column (default name: 'atr') with numeric ATR values
      * A 'close' column with the closing prices
    
    - The function will fail with a KeyError if these required columns are missing.
    
    - Before using this function, make sure to:
      1. Calculate the ATR indicator using the average_true_range() function
      2. Generate trading signals and assign them to a column named 'signal' (or specify
         a different column name using the signal_column parameter)
      3. Ensure your 'signal' column contains 'buy' values for entries (other values
         like 'sell' or 'neutral' can be used for non-entry conditions)
    
    - For testing purposes, you might need to create a wrapper that adds these
      required columns before calling this function.
"""


def test():
    """
    Test function for the calculate_atr_stop_loss_take_profit indicator.

    This function uses the generic test_indicator function from bamboo_ta.py
    to test the calculate_atr_stop_loss_take_profit indicator.

    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator

        # Test the indicator
        test_indicator(calculate_atr_stop_loss_take_profit)

    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
