# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd
from .bamboo_ta import *
from scipy.signal import argrelextrema
from scipy.stats import linregress
from typing import Tuple


def calculate_atr_stop_loss_take_profit(
    df: pd.DataFrame,
    signal_column: str = 'signal',
    atr_column: str = 'atr',
    atr_sl_mult: float = 1,
    atr_tp_mult: float = 2
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
    df['advice_changed'] = df[signal_column] != df[signal_column].shift(1)

    # Initialize new columns for take profit, stop loss, and buy price
    takeprofit = np.full(len(df), np.nan)
    stoploss = np.full(len(df), np.nan)
    buyprice = np.full(len(df), np.nan)

    # Logic for when the advice has changed and signal is 'buy'
    buy_mask = (df['advice_changed']) & (df[signal_column] == 'buy')
    takeprofit[buy_mask] = df['close'][buy_mask] + (df[atr_column][buy_mask] * atr_tp_mult)
    stoploss[buy_mask] = df['close'][buy_mask] - (df[atr_column][buy_mask] * atr_sl_mult)
    buyprice[buy_mask] = df['close'][buy_mask]

    # Logic for carrying forward the previous values if the advice has not changed
    no_change_mask = ~df['advice_changed']
    takeprofit[no_change_mask] = pd.Series(takeprofit).shift(1)
    stoploss[no_change_mask] = pd.Series(stoploss).shift(1)
    buyprice[no_change_mask] = pd.Series(buyprice).shift(1)

    # Return the result as a DataFrame
    result_df = pd.DataFrame({
        'takeprofit': takeprofit,
        'stoploss': stoploss,
        'buyprice': buyprice
    })
    
    return result_df


def calculate_stop_loss_take_profit(
    df: pd.DataFrame,
    signal_column: str = 'trade_signal',
    long_trade_signal: str = 'long_trade',
    short_trade_signal: str = 'short_trade',
    no_trade_signal: str = 'no_trade',
    lookback_period: int = 5,
    long_reward_ratio: float = 2,
    short_reward_ratio: float = 2,
    buffer: float = 0.0
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
                low_window = df['low'].iloc[max(0, i - lookback_period):i + 1]
                lowest_low = low_window.min()
                stop_loss_price = lowest_low - buffer
                current_entry_price = row['close']
                risk = current_entry_price - stop_loss_price
                take_profit_price = current_entry_price + risk * long_reward_ratio

                current_stop_loss = stop_loss_price
                current_take_profit = take_profit_price
                current_signal = long_trade_signal

            stop_loss.append(float(current_stop_loss) if current_stop_loss is not None else np.nan)
            take_profit.append(float(current_take_profit) if current_take_profit is not None else np.nan)
            entry_price.append(float(current_entry_price) if current_entry_price is not None else np.nan)

            # Determine exit reason
            if row['close'] < current_stop_loss:
                exit_reason.append('stop_loss_exit')
            elif row['close'] > current_take_profit:
                exit_reason.append('take_profit_hit')
            else:
                exit_reason.append('')

        elif signal == short_trade_signal:
            if current_signal != short_trade_signal:  # New short trade signal
                high_window = df['high'].iloc[max(0, i - lookback_period):i + 1]
                highest_high = high_window.max()
                stop_loss_price = highest_high + buffer
                current_entry_price = row['close']
                risk = stop_loss_price - current_entry_price
                take_profit_price = current_entry_price - risk * short_reward_ratio

                current_stop_loss = stop_loss_price
                current_take_profit = take_profit_price
                current_signal = short_trade_signal

            stop_loss.append(float(current_stop_loss) if current_stop_loss is not None else np.nan)
            take_profit.append(float(current_take_profit) if current_take_profit is not None else np.nan)
            entry_price.append(float(current_entry_price) if current_entry_price is not None else np.nan)

            # Determine exit reason
            if row['close'] > current_stop_loss:
                exit_reason.append('stop_loss_exit')
            elif row['close'] < current_take_profit:
                exit_reason.append('take_profit_hit')
            else:
                exit_reason.append('')

        elif signal == no_trade_signal:
            # No trade signal, reset values
            current_signal = None
            current_stop_loss = None
            current_take_profit = None
            current_entry_price = None
            stop_loss.append(np.nan)
            take_profit.append(np.nan)
            entry_price.append(np.nan)
            exit_reason.append('trade_signal_lost')

    # Create a new DataFrame with only the calculated columns
    result_df = pd.DataFrame({
        'stop_loss': stop_loss,
        'take_profit': take_profit,
        'entry_price': entry_price,
        'exit_reason': exit_reason
    })
    
    return result_df


def consecutive_count(consecutive_diff: np.ndarray) -> float:
    """
    Calculate the average consecutive count of non-zero differences.
    
    Parameters:
    - consecutive_diff (np.ndarray): Array of consecutive differences.

    Returns:
    - float: Average consecutive count. If there are fewer than two non-zero differences, returns 0.
    """
    # Find indices of non-zero elements in the array
    non_zero_diff = np.where(consecutive_diff != 0)[0]

    # If fewer than two non-zero elements, return 0 as no valid calculation can be performed
    if len(non_zero_diff) < 2:
        return 0

    # Calculate and return the average distance between consecutive non-zero indices
    return np.mean(np.diff(non_zero_diff))


def first_crossed_above_second(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Check if series1 crosses above series2 in a vectorized manner.

    Parameters:
    - series1 (pd.Series): First input series to check for crossover.
    - series2 (pd.Series): Second input series to compare against.

    Call with:
        df['first_crossed_above_second'] = bta.first_crossed_above_second(series1, series2)

    Returns:
    - pd.Series: Boolean series where True indicates a crossover above.
    """
    # Ensure both series have the same length
    if len(series1) != len(series2):
        raise ValueError("Input series must have the same length")

    # Vectorized check for crossover above
    return (series1 > series2) & (series1.shift(1) <= series2.shift(1))


def first_crossed_below_second(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Check if series1 crosses below series2 in a vectorized manner.

    Parameters:
    - series1 (pd.Series): First input series to check for crossover.
    - series2 (pd.Series): Second input series to compare against.

    Call with:
        df['first_crossed_below_second'] = bta.first_crossed_below_second(series1, series2)

    Returns:
    - pd.Series: Boolean series where True indicates a crossover below.
    """
    # Ensure both series have the same length
    if len(series1) != len(series2):
        raise ValueError("Input series must have the same length")

    # Vectorized check for crossover below
    return (series1 < series2) & (series1.shift(1) >= series2.shift(1))


def cumulative_return(df: pd.DataFrame, column: str = "close", fillna: bool = False) -> pd.Series:
    """
    Calculate the Cumulative Return (CR) of a specified column in a DataFrame.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the specified column.
    - column (str): The column on which the cumulative return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values. Default is False.

    Call with:
        df['cumulative_return'] = bta.cumulative_return(df)

    Returns:
    - pd.Series: Series of cumulative return values.
    """
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Calculate cumulative return
    df_copy['cum_ret'] = (df_copy[column] / df_copy[column].iloc[0]) - 1
    df_copy['cum_ret'] *= 100  # Expressing cumulative return as a percentage

    # Handle NaN values if requested
    if fillna:
        df_copy['cum_ret'] = df_copy['cum_ret'].fillna(-1)

    return df_copy['cum_ret'].rename("cumulative_return")


def daily_log_return(df: pd.DataFrame, column: str = "close", fillna: bool = False) -> pd.Series:
    """
    Calculate the Daily Log Return (DLR) of a specified column in a DataFrame.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily log return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

    Call with:
        df['daily_log_return'] = bta.daily_log_return(df)

    Returns:
    - pd.Series: Series of daily log return values.
    """
    # Copy the DataFrame to avoid modifying the original data
    df_copy = df.copy()

    # Calculate the daily log return
    df_copy['daily_log_return'] = np.log(df_copy[column]).diff() * 100  # Expressing as a percentage

    # Handle NaN values if requested
    if fillna:
        df_copy['daily_log_return'] = df_copy['daily_log_return'].fillna(0)

    return df_copy['daily_log_return'].rename("daily_log_return")


def daily_return(df: pd.DataFrame, column: str = "close", fillna: bool = False) -> pd.Series:
    """
    Calculate the Daily Return (DR) of a specified column in a DataFrame.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

    Call with:
        df['daily_return'] = bta.daily_return(df)

    Returns:
    - pd.Series: Series of daily return values.
    """
    # Copy the DataFrame to avoid modifying the original data
    df_copy = df.copy()

    # Calculate the daily return as a percentage
    df_copy['daily_return'] = (df_copy[column] / df_copy[column].shift(1)) - 1
    df_copy['daily_return'] *= 100

    # Handle NaN values if requested
    if fillna:
        df_copy['daily_return'] = df_copy['daily_return'].fillna(0)

    return df_copy['daily_return'].rename("daily_return")


def exhaustion_candles(df: pd.DataFrame, window: int = 1, multiplier: int = 1) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate the average consecutive length of ups and downs to adjust the exhaustion bands dynamically.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the 'close' price series.
    - window (int): Lookback window for calculation.
    - multiplier (int): Scalar multiplier for both major and minor quality.

    Call with:
        maj_qual, min_qual = exhaustion_candles(df, window, multiplier)
        df['maj_qual'] = maj_qual
        df['min_qual'] = min_qual

    Returns:
    - Tuple[np.ndarray, np.ndarray]: Arrays of major and minor quality values.
    """
    consecutive_diff = np.sign(df['close'].diff())
    maj_qual = np.zeros(len(df))
    min_qual = np.zeros(len(df))

    # Ensure multiplier is applied consistently
    multiplier = np.full(len(df), multiplier)

    for i in range(len(df)):
        idx_range = consecutive_diff[i - window + 1:i + 1] if i >= window else consecutive_diff[:i + 1]
        avg_consecutive = consecutive_count(idx_range)
        
        # Ensure avg_consecutive is a scalar, not an array
        if isinstance(avg_consecutive, np.ndarray):
            avg_consecutive = avg_consecutive.item()

        maj_qual[i] = int(avg_consecutive * (3 * multiplier[i])) if not np.isnan(avg_consecutive) else 0
        min_qual[i] = int(avg_consecutive * (3 * multiplier[i])) if not np.isnan(avg_consecutive) else 0

    return maj_qual, min_qual


import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

def exhaustion_lengths(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Calculate the average length of peaks and valleys to adjust the exhaustion bands dynamically.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing 'high' and 'low' columns.

    Call with:
        maj_len, min_len = exhaustion_lengths(df)
        df['maj_len'] = maj_len
        df['min_len'] = min_len

    Returns:
    - int, int: Average peak distance and average valley distance.
    """
    # Find relative maxima (peaks) and minima (valleys) in the 'high' and 'low' columns
    high_indices = argrelextrema(df['high'].to_numpy(), np.greater)[0]
    low_indices = argrelextrema(df['low'].to_numpy(), np.less)[0]

    # If there are fewer than two peaks or valleys, return zero
    if len(high_indices) < 2 or len(low_indices) < 2:
        return 0, 0

    # Calculate average and standard deviation of distances between peaks and valleys
    avg_peak_distance = np.mean(np.diff(high_indices))
    std_peak_distance = np.std(np.diff(high_indices))
    avg_valley_distance = np.mean(np.diff(low_indices))
    std_valley_distance = np.std(np.diff(low_indices))

    # Determine major and minor lengths using average + standard deviation
    maj_len = int(avg_peak_distance + std_peak_distance)
    min_len = int(avg_valley_distance + std_valley_distance)

    return maj_len, min_len


def get_min_max(series1: pd.Series, series2: pd.Series, function: str = "min") -> pd.Series:
    """
    Find the minimum or maximum value between two series for each index.

    Parameters:
    - series1 (pd.Series): First input series.
    - series2 (pd.Series): Second input series.
    - function (str): Function to apply ("min" or "max"). Default is "min".

    Call with:
        df['min_max'] = bta.get_min_max(series1, series2, function)
    Like:
        df['min_max'] = bta.get_min_max(df['open'], df['open'], 'max')

    Returns:
    - pd.Series: Series with min or max values for each index.
    """
    series1 = np.array(series1)
    series2 = np.array(series2)

    if function == "min":
        output = np.amin([series1, series2], axis=0)
    elif function == "max":
        output = np.amax([series1, series2], axis=0)
    else:
        raise ValueError('"function" variable should be "min" or "max"')

    return pd.Series(output)


def linear_decay(start: float, end: float, start_time: int, 
                 end_time: int, trade_time: int) -> float:
    """
    Simple linear decay function. Decays from start to end after 
    end_time minutes (starts after start_time minutes).

    Parameters:
    - start (float): Starting value.
    - end (float): Ending value.
    - start_time (int): Start time in minutes.
    - end_time (int): End time in minutes.
    - trade_time (int): Current trade time in minutes.

    Call with:
        decayed_value = linear_decay(start, end, start_time, end_time, trade_time)

    Returns:
    - float: Decayed value.
    """
    time = max(0, trade_time - start_time)
    rate = (start - end) / (end_time - start_time)
    return max(end, start - (rate * time))


def linear_growth(start: float, end: float, start_time: int, 
                  end_time: int, trade_time: int) -> float:
    """
    Simple linear growth function. Grows from start to end after 
    end_time minutes (starts after start_time minutes).

    Parameters:
    - start (float): Starting value.
    - end (float): Ending value.
    - start_time (int): Start time in minutes.
    - end_time (int): End time in minutes.
    - trade_time (int): Current trade time in minutes.

    Call with:
        grown_value = linear_growth(start, end, start_time, end_time, trade_time)

    Returns:
    - float: Grown value.
    """
    time = max(0, trade_time - start_time)
    rate = (end - start) / (end_time - start_time)
    return min(end, start + (rate * time))


def overbought_oversold(
    df: pd.DataFrame,
    indicator_col: str,
    overbought_value: float = 75,
    oversold_value: float = 30,
    previous_rows: int = 5
) -> pd.Series:
    """
    Overbought/Oversold (OBOS) Indicator

    Determines overbought, oversold, and trigger conditions based on a specified indicator column.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the indicator column.
    - indicator_col (str): The name of the column containing the indicator values.
    - overbought_value (float, default=75): The overbought threshold.
    - oversold_value (float, default=30): The oversold threshold.
    - previous_rows (int, default=5): Number of previous rows to consider for trigger conditions.

    # Example usage of the obos function
    obos = bta.overbought_oversold(
        df,
        indicator_col='indicator',  # Replace 'indicator' with the column name containing the indicator values
        overbought_value=75,       # Specify the overbought threshold (default: 75)
        oversold_value=30,         # Specify the oversold threshold (default: 30)
        previous_rows=5            # Number of previous rows to consider for trigger conditions (default: 5)
    )

    # Integrate results into the original DataFrame
    df['obos_condition'] = obos

    Returns:
    - pd.Series: A Series containing the OBOS conditions:
        - 'overbought'
        - 'oversold'
        - 'overbought_trigger'
        - 'oversold_trigger'
        - 'neutral'
    """
    if indicator_col not in df.columns:
        raise ValueError(f"Column '{indicator_col}' not found in the DataFrame.")

    # Create arrays for efficiency
    indicator = df[indicator_col].values
    obos_condition = np.full(len(df), "neutral", dtype=object)

    # Determine 'overbought' and 'oversold'
    obos_condition[indicator > overbought_value] = "overbought"
    obos_condition[indicator < oversold_value] = "oversold"

    # Determine 'overbought_trigger' and 'oversold_trigger' conditions
    for i in range(previous_rows, len(df)):
        if obos_condition[i] == "neutral":
            previous_values = indicator[i - previous_rows:i]
            if (previous_values < oversold_value).any():
                obos_condition[i] = "oversold_trigger"
            elif (previous_values > overbought_value).any():
                obos_condition[i] = "overbought_trigger"

    return pd.Series(obos_condition, index=df.index, name="obos_condition")


def populate_leledc_major_minor(df: pd.DataFrame, maj_qual: np.ndarray, 
                                min_qual: np.ndarray, maj_len: int, 
                                min_len: int) -> pd.DataFrame:
    """
    Populate Leledc Major and Minor columns.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - maj_qual (np.ndarray): Array of major quality values.
    - min_qual (np.ndarray): Array of minor quality values.
    - maj_len (int): Major length value.
    - min_len (int): Minor length value.

    Call with:
        leledc_major_minor = bta.populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len)
        df['leledc_major'] = leledc_major_minor['leledc_major']
        df['leledc_minor'] = leledc_major_minor['leledc_minor']

    Returns:
    - pd.DataFrame: DataFrame with 'leledc_major' and 'leledc_minor' columns.
    """
    df_copy = df.copy()
    bindex_maj, sindex_maj, trend_maj = 0, 0, 0
    bindex_min, sindex_min = 0, 0

    df_copy['leledc_major'] = np.nan
    df_copy['leledc_minor'] = 0

    for i in range(1, len(df_copy)):
        close = df_copy['close'][i]
        short_length = i if i < 4 else 4

        if close > df_copy['close'][i - short_length]:
            bindex_maj += 1
            bindex_min += 1
        elif close < df_copy['close'][i - short_length]:
            sindex_maj += 1
            sindex_min += 1

        update_major = False
        if (bindex_maj > maj_qual[i] and close < df_copy['open'][i] and
                df_copy['high'][i] >= df_copy['high'][i - maj_len:i].max()):
            bindex_maj, trend_maj, update_major = 0, 1, True
        elif (sindex_maj > maj_qual[i] and close > df_copy['open'][i] and
              df_copy['low'][i] <= df_copy['low'][i - maj_len:i].min()):
            sindex_maj, trend_maj, update_major = 0, -1, True

        df_copy.at[i, 'leledc_major'] = trend_maj if update_major else np.nan if trend_maj == 0 else trend_maj

        if (bindex_min > min_qual[i] and close < df_copy['open'][i] and
                df_copy['high'][i] >= df_copy['high'][i - min_len:i].max()):
            bindex_min = 0
            df_copy.at[i, 'leledc_minor'] = -1
        elif (sindex_min > min_qual[i] and close > df_copy['open'][i] and
              df_copy['low'][i] <= df_copy['low'][i - min_len:i].min()):
            sindex_min = 0
            df_copy.at[i, 'leledc_minor'] = 1
        else:
            df_copy.at[i, 'leledc_minor'] = 0

    return df_copy[['leledc_major', 'leledc_minor']]



def pump_dump_protection(
    df: pd.DataFrame,
    rsi_period: int = 14,
    short_volume_window: int = 4,
    long_volume_window: int = 48,
    volume_warn_threshold: float = 5.0
) -> pd.DataFrame:
    """
    Pump and Dump Protection Indicator

    This function detects abnormal volume changes and price movements to identify potential pump-and-dump
    scenarios. It eliminates dependency on a specific timeframe, relying only on rolling calculations.

    Parameters:
    - df (pd.DataFrame): Input DataFrame with required columns:
        - 'close': Closing price.
        - 'high': High price for the interval.
        - 'low': Low price for the interval.
        - 'volume': Volume for the interval.
    - rsi_period (int, default=14): Lookback period for RSI calculation.
    - short_volume_window (int, default=4): Rolling window size for short-term volume mean.
    - long_volume_window (int, default=48): Rolling window size for long-term volume mean.
    - volume_warn_threshold (float, default=5.0): Threshold for detecting abnormal short-term volume spikes.

    Call with:
        pd_result = bta.pump_dump_protection_no_timeframe(
            df,
            rsi_period=14,
            short_volume_window=4,
            long_volume_window=48,
            volume_warn_threshold=5.0
        )

        # Add all calculated columns to the original DataFrame
        df['volume_mean_short'] = pd_result['volume_mean_short']
        df['volume_mean_long'] = pd_result['volume_mean_long']
        df['volume_change_percentage'] = pd_result['volume_change_percentage']
        df['rsi'] = pd_result['rsi']
        df['pnd_volume_warn'] = pd_result['pnd_volume_warn']

    Returns:
    - pd.DataFrame: The DataFrame with the following additional columns:
        - 'volume_mean_short': Rolling mean of volume over `short_volume_window` intervals.
        - 'volume_mean_long': Rolling mean of volume over `long_volume_window` intervals.
        - 'volume_change_percentage': Ratio of 'volume_mean_short' to 'volume_mean_long'.
        - 'rsi': Calculated RSI values.
        - 'pnd_volume_warn': Indicator for abnormal volume spikes.
    """
    df_copy = df.copy()

    # Calculate RSI
    delta = df_copy['close'].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=rsi_period).mean()
    avg_loss = pd.Series(loss).rolling(window=rsi_period).mean()
    rs = avg_gain / avg_loss
    df_copy['rsi'] = 100 - (100 / (1 + rs))

    # Calculate rolling volume means
    df_copy['volume_mean_short'] = df_copy['volume'].rolling(short_volume_window).mean()
    df_copy['volume_mean_long'] = df_copy['volume'].rolling(long_volume_window).mean()

    # Calculate volume change percentage
    df_copy['volume_change_percentage'] = df_copy['volume_mean_short'] / df_copy['volume_mean_long']

    # Abnormal volume spike detection
    df_copy['pnd_volume_warn'] = np.where(
        (df_copy['volume_mean_short'] / df_copy['volume_mean_long'] > volume_warn_threshold), -1, 0
    )

    return df_copy[[
        'volume_mean_short',
        'volume_mean_long',
        'volume_change_percentage',
        'rsi',
        'pnd_volume_warn'
    ]]


def regression_slope(df: pd.DataFrame, lookback_period: int = 20) -> pd.Series:
    """
    Calculate the slope of the linear regression for a given lookback period.

    This function computes the slope of a linear regression line (least squares) fitted to the
    'close' prices over the specified lookback period.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the 'close' prices.
    - lookback_period (int): The lookback period for calculating the regression slope. Default is 20.

    Call with:
        df['slope'] = bta.regression_slope(df, 20)

    Returns:
    - pd.Series: Series containing the regression slopes.
    """
    # Ensure the 'close' column exists in the DataFrame
    if 'close' not in df.columns:
        raise KeyError("The input DataFrame must contain a 'close' column.")
    
    # Extract the 'close' prices as a NumPy array for faster processing
    y_values = df['close'].values
    
    # Create an array for the x-values (time steps) for the regression
    x_values = np.arange(lookback_period)
    x_mean = x_values.mean()
    
    # Function to calculate the slope for a given rolling window
    def calculate_slope(window):
        y_mean = window.mean()
        numerator = np.sum((x_values - x_mean) * (window - y_mean))
        denominator = np.sum((x_values - x_mean) ** 2)
        return numerator / denominator

    # Apply the slope calculation to the rolling window on the 'close' prices
    slope_series = df['close'].rolling(window=lookback_period).apply(calculate_slope, raw=True)
    
    return slope_series


def same_length(bigger: np.ndarray, shorter: np.ndarray) -> np.ndarray:
    """
    Ensures the shorter array has the same length as the bigger array by padding with NaN values.

    Parameters:
    - bigger (np.ndarray): The array with the larger size.
    - shorter (np.ndarray): The array with the smaller size.

    Call with:
        padded_array = same_length(bigger_array, shorter_array)

    Returns:
    - np.ndarray: The shorter array padded with NaN values to match the size of the bigger array.
    """
    if not isinstance(bigger, np.ndarray) or not isinstance(shorter, np.ndarray):
        raise ValueError("Both inputs must be NumPy arrays.")
    
    if bigger.shape[0] < shorter.shape[0]:
        raise ValueError("The first array must be bigger or equal in length to the second array.")
    
    # Calculate how many NaN values to add to the shorter array
    pad_size = bigger.shape[0] - shorter.shape[0]
    
    # Return the concatenated array of NaNs followed by the shorter array
    return np.concatenate((np.full(pad_size, np.nan), shorter))


def st_dev(series: pd.Series, period: int) -> pd.Series:
    """
    Calculate the rolling standard deviation over a specified period.

    Parameters:
    - series (pd.Series): The data series to calculate the standard deviation for.
    - period (int): The period over which to calculate the standard deviation.

    Call with:
        df['std_dev'] = bta.st_dev(df['column_name'], period=14)
    
    Like:
        df['std_dev'] = bta.st_dev(df['close'], period=14)

    Returns:
    - pd.Series: The rolling standard deviation of the series over the specified period.
    """
    if not isinstance(series, pd.Series):
        raise ValueError("Input must be a pandas Series.")
    if period <= 0:
        raise ValueError("Period must be a positive integer.")

    return series.rolling(window=period).std()


def top_percent_change(df: pd.DataFrame, length: int = 0) -> pd.Series:
    """
    Calculate the percentage change of the current close price from the range maximum open price.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data with required columns:
        - 'open': Opening price.
        - 'close': Closing price.
    - length (int, default=0): Lookback period for calculating the range maximum. If 0, calculates the percentage 
      change between the current open and close prices.
    
    Call with:
        df['percent_change'] = bta.top_percent_change(df, length=3)
    
    Returns:
    - pd.Series: A Series representing the percentage change for each row in the DataFrame.
    """
    # Ensure the required columns are in the DataFrame
    if not {'open', 'close'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'open' and 'close' columns.")

    if length == 0:
        # Calculate percentage change for the current open and close prices
        percent_change = (df['open'] - df['close']) / df['close']
    else:
        # Calculate percentage change from the range maximum open price
        max_open = df['open'].rolling(window=length).max()
        percent_change = (max_open - df['close']) / df['close']

    return percent_change


def z_score(series: pd.Series, window: int = 500) -> pd.Series:
    """
    Calculate the z-score of a series.

    Parameters:
    - series (pd.Series): Input series.
    - window (int): Lookback window for mean and standard deviation calculation.

    Call with:
        df['zscore']  = bta.z_score(series)
    
    Like:
        df['zscore']  = bta.z_score(df['close'])

    Returns:
    - pd.Series: Z-score series.
    """
    mean = series.rolling(window=window, min_periods=1).mean()
    std = series.rolling(window=window, min_periods=1).std(ddof=0)
    zscore = (series - mean) / std
    zscore = zscore.fillna(0)  # Fill NaN values with 0 to avoid issues with calculations

    return zscore


class IndicatorMixin:
    """Utility mixin class for indicator calculations."""

    _fillna = False

    def _check_fillna(self, series: pd.Series, value: int = 0) -> pd.Series:
        """
        Check if the fillna flag is True and handle NaN values accordingly.

        Parameters:
        - series (pd.Series): Calculated indicator series.
        - value (int): Value to fill gaps; if -1, fill values using 'backfill' mode.

        Returns:
        - pd.Series: Series with NaN values handled.
        """
        if self._fillna:
            series_output = series.copy(deep=False)
            series_output = series_output.replace([np.inf, -np.inf], np.nan)
            if isinstance(value, int) and value == -1:
                series = series_output.ffill().bfill()
            else:
                series = series_output.ffill().fillna(value)
        return series

    @staticmethod
    def _true_range(high: pd.Series, low: pd.Series, prev_close: pd.Series) -> pd.Series:
        """
        Calculate the true range.

        Parameters:
        - high (pd.Series): High price series.
        - low (pd.Series): Low price series.
        - prev_close (pd.Series): Previous close price series.

        Returns:
        - pd.Series: True range series.
        """
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        true_range = pd.DataFrame(data={"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
        return true_range


def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows with 'NaN' values and handle very large numbers and zeros in numeric columns.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.

    Call with:
        df['df_cleaned'] = bta.drop_na(df)

    Returns:
    - pd.DataFrame: DataFrame without NaN values, extremely large values, and zeroes in numeric columns.
    """
    df_copy = df.copy()
    
    # Select numeric columns
    number_cols = df_copy.select_dtypes(include=np.number).columns.tolist()
    
    # Replace extremely large values (greater than exp(709)) with NaN
    df_copy[number_cols] = df_copy[number_cols].where(df_copy[number_cols] < math.exp(709))
    
    # Replace zero values with NaN
    df_copy[number_cols] = df_copy[number_cols].replace(0.0, np.nan)
    
    # Drop rows with any NaN values
    df_cleaned = df_copy.dropna()
    
    return df_cleaned


