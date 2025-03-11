# -*- coding: utf-8 -*-
# calculate_stop_loss_take_profit.py
import numpy as np
import pandas as pd


def calculate_stop_loss_take_profit(
    df: pd.DataFrame,
    signal_column: str = "trade_signal",
    long_trade_signal: str = "long_trade",
    short_trade_signal: str = "short_trade",
    no_trade_signal: str = "no_trade",
    lookback_period: int = 5,
    long_reward_ratio: float = 2,
    short_reward_ratio: float = 2,
    buffer: float = 0.0,
) -> pd.DataFrame:
    """
    Calculate stop loss, take profit, and entry price based on customizable trade signals.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing trading data and trade signals.
    - signal_column (str): Column name where trade signals ('long_trade', 'short_trade', etc.) are stored. Default is 'trade_signal'.
    - long_trade_signal (str): The value in signal_column that represents a long trade. Default is 'long_trade'.
    - short_trade_signal (str): The value in signal_column that represents a short trade. Default is 'short_trade'.
    - no_trade_signal (str): The value in signal_column that represents no trade. Default is 'no_trade'.
    - lookback_period (int): The lookback period for calculating stop loss. Default is 5.
    - long_reward_ratio (float): Reward-risk ratio for long trades. Default is 2.
    - short_reward_ratio (float): Reward-risk ratio for short trades. Default is 2.
    - buffer (float): Buffer added to the stop loss. Default is 0.0.

    Call with:
        stop_loss_take_profit = bta.calculate_stop_loss_take_profit(df,
                                                                   signal_column='trade_signal',
                                                                   long_trade_signal='long_trade',
                                                                   short_trade_signal='short_trade',
                                                                   no_trade_signal='no_trade',
                                                                   lookback_period=5,
                                                                   long_reward_ratio=2,
                                                                   short_reward_ratio=1.5,
                                                                   buffer=0.5)

    Add the new columns to the original DataFrame:
        df['stop_loss'] = stop_loss_take_profit['stop_loss']
        df['entry_price'] = stop_loss_take_profit['entry_price']
        df['take_profit'] = stop_loss_take_profit['take_profit']
        df['exit_reason'] = stop_loss_take_profit['exit_reason']

    Returns:
    - pd.DataFrame: Updated DataFrame with new columns: 'stop_loss', 'take_profit', 'entry_price', and 'exit_reason'.
    """
    stop_loss = []
    take_profit = []
    entry_price = []
    exit_reason = []

    current_signal = None
    current_stop_loss = None
    current_take_profit = None
    current_entry_price = None

    for i, row in df.iterrows():
        signal = row[signal_column]

        if signal == long_trade_signal:
            if current_signal != long_trade_signal:  # New long trade signal
                low_window = df["low"].iloc[max(0, i - lookback_period) : i + 1]
                lowest_low = low_window.min()
                stop_loss_price = lowest_low - buffer
                current_entry_price = row["close"]
                risk = current_entry_price - stop_loss_price
                take_profit_price = current_entry_price + risk * long_reward_ratio

                current_stop_loss = stop_loss_price
                current_take_profit = take_profit_price
                current_signal = long_trade_signal

            stop_loss.append(
                float(current_stop_loss) if current_stop_loss is not None else np.nan
            )
            take_profit.append(
                float(current_take_profit)
                if current_take_profit is not None
                else np.nan
            )
            entry_price.append(
                float(current_entry_price)
                if current_entry_price is not None
                else np.nan
            )

            # Determine exit reason
            if row["close"] < current_stop_loss:
                exit_reason.append("stop_loss_exit")
            elif row["close"] > current_take_profit:
                exit_reason.append("take_profit_hit")
            else:
                exit_reason.append("")

        elif signal == short_trade_signal:
            if current_signal != short_trade_signal:  # New short trade signal
                high_window = df["high"].iloc[max(0, i - lookback_period) : i + 1]
                highest_high = high_window.max()
                stop_loss_price = highest_high + buffer
                current_entry_price = row["close"]
                risk = stop_loss_price - current_entry_price
                take_profit_price = current_entry_price - risk * short_reward_ratio

                current_stop_loss = stop_loss_price
                current_take_profit = take_profit_price
                current_signal = short_trade_signal

            stop_loss.append(
                float(current_stop_loss) if current_stop_loss is not None else np.nan
            )
            take_profit.append(
                float(current_take_profit)
                if current_take_profit is not None
                else np.nan
            )
            entry_price.append(
                float(current_entry_price)
                if current_entry_price is not None
                else np.nan
            )

            # Determine exit reason
            if row["close"] > current_stop_loss:
                exit_reason.append("stop_loss_exit")
            elif row["close"] < current_take_profit:
                exit_reason.append("take_profit_hit")
            else:
                exit_reason.append("")

        elif signal == no_trade_signal:
            # No trade signal, reset values
            current_signal = None
            current_stop_loss = None
            current_take_profit = None
            current_entry_price = None
            stop_loss.append(np.nan)
            take_profit.append(np.nan)
            entry_price.append(np.nan)
            exit_reason.append("trade_signal_lost")

    # Create a new DataFrame with only the calculated columns
    result_df = pd.DataFrame(
        {
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "entry_price": entry_price,
            "exit_reason": exit_reason,
        }
    )

    return result_df


calculate_stop_loss_take_profit.__doc__ = """
Name:
    Calculate Stop-Loss and Take-Profit

Description:
    This function calculates dynamic stop-loss and take-profit levels based on recent price action
    and customizable trade signals. It implements a swing-based risk management approach that 
    uses the lowest low (for long trades) or highest high (for short trades) within a lookback 
    period to establish stop-loss levels. Take-profit levels are then calculated based on 
    configurable reward-to-risk ratios.
    
    The function also tracks the status of trades, identifying when stop-loss or take-profit 
    levels have been hit, and provides exit reason information.

More info:
    This implementation follows a common risk management practice in trading:
    - For long trades: Stop-loss is placed below a recent swing low
    - For short trades: Stop-loss is placed above a recent swing high
    - Take-profit is calculated as a multiple of the risk (the distance to stop-loss)
    
    This approach adapts to market conditions by using actual price swings rather than 
    fixed percentages or arbitrary levels.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing price data and trade signals.
    - signal_column (str): Column name with trade signals. Default is 'trade_signal'.
    - long_trade_signal (str): Value indicating a long trade. Default is 'long_trade'.
    - short_trade_signal (str): Value indicating a short trade. Default is 'short_trade'.
    - no_trade_signal (str): Value indicating no trade. Default is 'no_trade'.
    - lookback_period (int): Period for finding swing highs/lows. Default is 5.
    - long_reward_ratio (float): Reward-risk ratio for long trades. Default is 2.
    - short_reward_ratio (float): Reward-risk ratio for short trades. Default is 2.
    - buffer (float): Additional buffer added to stop-loss. Default is 0.0.

Call with:
    # After generating trade signals
    risk_mgmt = bta.calculate_stop_loss_take_profit(
        df,
        signal_column='my_signal',
        long_trade_signal='buy',
        short_trade_signal='sell',
        no_trade_signal='neutral',
        lookback_period=10,
        long_reward_ratio=2.5,
        short_reward_ratio=2.0,
        buffer=0.2
    )
    
    # Add results to the original dataframe
    df['sl'] = risk_mgmt['stop_loss']
    df['tp'] = risk_mgmt['take_profit']
    df['entry'] = risk_mgmt['entry_price']
    df['exit_type'] = risk_mgmt['exit_reason']

Returns:
    pd.DataFrame: A DataFrame with four columns:
    - 'stop_loss': The calculated stop-loss prices
    - 'take_profit': The calculated take-profit prices
    - 'entry_price': The trade entry prices
    - 'exit_reason': The reason for exit ('stop_loss_exit', 'take_profit_hit', etc.)

Important Notes:
    - This function REQUIRES that your DataFrame already contains specific columns:
      * A trade signal column (default name: 'trade_signal') with values matching 
        those specified in long_trade_signal, short_trade_signal, and no_trade_signal
      * 'high', 'low', and 'close' price columns
    
    - The function will fail with a KeyError if these required columns are missing.
    
    - Before using this function, make sure to:
      1. Generate trading signals and assign them to a column (default: 'trade_signal')
      2. Ensure your signal column contains the expected values (by default: 'long_trade',
         'short_trade', and 'no_trade')
    
    - For testing purposes, you might need to create a wrapper that adds these
      required columns before calling this function.
"""


def test():
    """
    Test function for the calculate_stop_loss_take_profit indicator.

    This function uses the generic test_indicator function from bamboo_ta.py
    to test the calculate_stop_loss_take_profit indicator.

    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator

        # Test the indicator
        test_indicator(calculate_stop_loss_take_profit)

    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
