# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd
from .bamboo_ta import *
from scipy.signal import argrelextrema
from scipy.stats import linregress


def CalculateATRStopLossTakeProfit(
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
        df = CalculateATRStopLossTakeProfit(df, signal_column='signal')

    Returns:
    - pd.DataFrame: Updated DataFrame with 'takeprofit', 'stoploss', and 'buyprice' columns.
    """
    # Initialize new columns for take profit, stop loss, and buy price if not already present
    if 'takeprofit' not in df.columns:
        df['takeprofit'] = np.nan
    if 'stoploss' not in df.columns:
        df['stoploss'] = np.nan
    if 'buyprice' not in df.columns:
        df['buyprice'] = np.nan

    # Create a new column for advice_changed if it does not exist
    df['advice_changed'] = df[signal_column] != df[signal_column].shift(1)

    # Logic for when the advice has changed and signal is 'buy'
    buy_mask = (df['advice_changed'] == True) & (df[signal_column] == 'buy')
    df.loc[buy_mask, 'takeprofit'] = df.loc[buy_mask, 'close'] + (df.loc[buy_mask, atr_column] * atr_tp_mult)
    df.loc[buy_mask, 'stoploss'] = df.loc[buy_mask, 'close'] - (df.loc[buy_mask, atr_column] * atr_sl_mult)
    df.loc[buy_mask, 'buyprice'] = df.loc[buy_mask, 'close']

    # Logic for when the advice has changed and signal is 'sell'
    sell_mask = (df['advice_changed'] == True) & (df[signal_column] == 'sell')
    df.loc[sell_mask, 'takeprofit'] = np.nan
    df.loc[sell_mask, 'stoploss'] = np.nan
    df.loc[sell_mask, 'buyprice'] = np.nan

    # Logic for carrying forward the previous values if the advice has not changed
    no_change_mask = df['advice_changed'] == False
    df.loc[no_change_mask, 'takeprofit'] = df['takeprofit'].shift(1)
    df.loc[no_change_mask, 'stoploss'] = df['stoploss'].shift(1)
    df.loc[no_change_mask, 'buyprice'] = df['buyprice'].shift(1)

    return df


def CalculateFixedStopLossTakeProfitWithSignal(
    df: pd.DataFrame,
    signal_column: str = 'trade_signal',
    long_trade_signal: str = 'long_trade',
    short_trade_signal: str = 'short_trade',
    no_trade_signal: str = 'no_trade',
    lookback_period: int = 5,
    long_risk_reward_ratio: float = 2,
    short_risk_reward_ratio: float = 2,
    buffer: float = 0) -> pd.DataFrame:
    """
    Calculate stop loss, entry price, and take profit levels based on trade signals (long, short, or no trade).

    In order to make this function work, you have to do the following:
    - adjust the signal_column name to match the column that contains the trade signal
    - change the long_trade_signal to your own preferred way of naming a long trade signal
    - change the short_trade_signal to your own preferred way of naming a short trade signal
    - change the default way of naming the period where no trade is allowed in no_trade_signal

    TRADE SIGNAL GENERATION:

    The trade signal can be created by a function that is similar of that below:

    def determine_trade_signal(row):
        # Long trade condition
        if (row['close'] > row['sma']) and (row['rsi'] > row['rsi_level']):
            return 'long_trade'

        # Short trade condition
        elif (row['close'] < row['sma']) and (row['rsi'] < row['rsi_level']):
            return 'short_trade'

        # No trade condition
        else:
            return 'no_trade'

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing trading data.
    - signal_column (str): Column name with trade signals. Default is 'trade_signal'.
    - long_trade_signal (str): Signal for long trades. Default is 'long_trade'.
    - short_trade_signal (str): Signal for short trades. Default is 'short_trade'.
    - no_trade_signal (str): Signal for no trade. Default is 'no_trade'.
    - lookback_period (int): Lookback period for calculating stop loss. Default is 5.
    - long_risk_reward_ratio (float): Risk-reward ratio for long trades. Default is 2.
    - short_risk_reward_ratio (float): Risk-reward ratio for short trades. Default is 2.
    - buffer (float): Buffer added to the stop loss. Default is 0.

    Call with:
        trade_cols = bta.CalculateFixedStopLossTakeProfitWithSignal(
            df, 
            signal_column='trade_signal',
            long_trade_signal='long_trade', 
            short_trade_signal='short_trade', 
            no_trade_signal='no_trade', 
            lookback_period=3, 
            long_risk_reward_ratio=2, 
            short_risk_reward_ratio=2, 
            buffer=0
        )

        # Add the result to the DataFrame (or inspect it separately)
        df[['stop_loss', 'entry_price', 'take_profit', 'trade_active', 'exit_reason']] = trade_cols

        or:
        
        trade_cols = CalculateFixedStopLossTakeProfitWithSignal(df, signal_column='trade_signal')

    Returns:
    - pd.DataFrame: DataFrame with new columns: 'stop_loss', 'entry_price', 'take_profit', 'trade_active', and 'exit_reason'.
    """
    # Initialize new columns if not already present
    if 'stop_loss' not in df.columns:
        df['stop_loss'] = np.nan
    if 'entry_price' not in df.columns:
        df['entry_price'] = np.nan
    if 'take_profit' not in df.columns:
        df['take_profit'] = np.nan
    if 'trade_active' not in df.columns:
        df['trade_active'] = False
    if 'exit_reason' not in df.columns:
        df['exit_reason'] = pd.NA
        df['exit_reason'] = df['exit_reason'].astype('object')

    trade_active = False
    stop_loss = entry_price = take_profit = None
    current_trade_type = None
    clear_next_row = False

    for i in range(lookback_period, len(df)):
        if clear_next_row:
            df.loc[i, 'stop_loss'] = np.nan
            df.loc[i, 'entry_price'] = np.nan
            df.loc[i, 'take_profit'] = np.nan
            clear_next_row = False
            continue

        if trade_active:
            if current_trade_type == long_trade_signal:
                if df.loc[i, 'close'] >= take_profit:
                    df.loc[i, 'exit_reason'] = 'take_profit_hit'
                    df.loc[i, 'trade_active'] = False
                    trade_active = False
                    clear_next_row = True
                    continue
                elif df.loc[i, 'close'] <= stop_loss:
                    df.loc[i, 'exit_reason'] = 'stop_loss_hit'
                    df.loc[i, 'trade_active'] = False
                    trade_active = False
                    clear_next_row = True
                    continue

            elif current_trade_type == short_trade_signal:
                if df.loc[i, 'close'] <= take_profit:
                    df.loc[i, 'exit_reason'] = 'take_profit_hit'
                    df.loc[i, 'trade_active'] = False
                    trade_active = False
                    clear_next_row = True
                    continue
                elif df.loc[i, 'close'] >= stop_loss:
                    df.loc[i, 'exit_reason'] = 'stop_loss_hit'
                    df.loc[i, 'trade_active'] = False
                    trade_active = False
                    clear_next_row = True
                    continue

        advice_changed = df.loc[i, signal_column] != df.loc[i - 1, signal_column]

        if advice_changed and df.loc[i, signal_column] in [long_trade_signal, short_trade_signal]:
            entry_price = df.loc[i, 'close']
            current_trade_type = df.loc[i, signal_column]

            if current_trade_type == long_trade_signal:
                stop_loss = df.loc[i - lookback_period:i, 'low'].min() - buffer
                risk = entry_price - stop_loss
                take_profit = entry_price + (risk * long_risk_reward_ratio)
            elif current_trade_type == short_trade_signal:
                stop_loss = df.loc[i - lookback_period:i, 'high'].max() + buffer
                risk = stop_loss - entry_price
                take_profit = entry_price - (risk * short_risk_reward_ratio)

            df.loc[i, 'stop_loss'] = stop_loss
            df.loc[i, 'entry_price'] = entry_price
            df.loc[i, 'take_profit'] = take_profit
            df.loc[i, 'trade_active'] = True
            df.loc[i, 'exit_reason'] = pd.NA

            trade_active = True

        elif advice_changed and df.loc[i, signal_column] == no_trade_signal:
            df.loc[i, 'stop_loss'] = np.nan
            df.loc[i, 'entry_price'] = np.nan
            df.loc[i, 'take_profit'] = np.nan
            df.loc[i, 'trade_active'] = False
            df.loc[i, 'exit_reason'] = 'trade_signal_lost'
            trade_active = False

        elif trade_active:
            df.loc[i, 'stop_loss'] = df.loc[i - 1, 'stop_loss']
            df.loc[i, 'entry_price'] = df.loc[i - 1, 'entry_price']
            df.loc[i, 'take_profit'] = df.loc[i - 1, 'take_profit']
            df.loc[i, 'trade_active'] = True

    # Return only the new columns
    return df[['stop_loss', 'entry_price', 'take_profit', 'trade_active', 'exit_reason']]


def ConsecutiveCount(consecutive_diff):
    """
    Calculate the average consecutive count of non-zero differences
    
    Parameters:
    - consecutive_diff (np.ndarray): Array of consecutive differences.

    Returns:
    - float: Average consecutive count.
    """
    non_zero_diff = np.where(consecutive_diff != 0)[0]
    if len(non_zero_diff) < 2:
        return 0
    return np.mean(np.abs(np.diff(non_zero_diff)))


def CrossedAbove(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Check if series1 crosses above series2 in a vectorized manner.

    Parameters:
    - series1 (pd.Series): First input series to check for crossover.
    - series2 (pd.Series): Second input series to compare against.

    Call with:
        crossover = CrossedAbove(series1, series2)
        df['crossed_above'] = crossover

    Returns:
    - pd.Series: Boolean series where True indicates a crossover above.
    """
    return (series1 > series2) & (series1.shift(1) <= series2.shift(1))


def CrossedBelow(series1: pd.Series, series2: pd.Series) -> pd.Series:
    """
    Check if series1 crosses below series2 in a vectorized manner.

    Parameters:
    - series1 (pd.Series): First input series to check for crossover.
    - series2 (pd.Series): Second input series to compare against.

    Call with:
        crossover = CrossedBelow(series1, series2)
        df['crossed_below'] = crossover

    Returns:
    - pd.Series: Boolean series where True indicates a crossover below.
    """
    return (series1 < series2) & (series1.shift(1) >= series2.shift(1))



def CumulativeReturn(df, column="close", fillna=False):
    """
    Cumulative Return (CR)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the cumulative return is to be calculated. Default is "close".
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        cr = CumulativeReturn(df)
        df['cumulative_return'] = cr

    Returns:
    - pd.Series: Series of cumulative return values.
    """
    df_copy = df.copy()
    df_copy['cum_ret'] = (df_copy[column] / df_copy[column].iloc[0]) - 1
    df_copy['cum_ret'] *= 100
    if fillna:
        df_copy['cum_ret'] = df_copy['cum_ret'].fillna(-1)
    return df_copy['cum_ret'].rename("cum_ret")


def DailyLogReturn(df, column="close", fillna=False):
    """
    Daily Log Return (DLR)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily log return is to be calculated. Default is "close".
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        dlr = DailyLogReturn(df)
        df['daily_log_return'] = dlr

    Returns:
    - pd.Series: Series of daily log return values.
    """
    df_copy = df.copy()
    df_copy['d_logret'] = pd.Series(np.log(df_copy[column])).diff()
    df_copy['d_logret'] *= 100
    if fillna:
        df_copy['d_logret'] = df_copy['d_logret'].fillna(0)
    return df_copy['d_logret'].rename("d_logret")


def DailyReturn(df, column="close", fillna=False):
    """
    Daily Return (DR)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily return is to be calculated. Default is "close".
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        dr = DailyReturn(df)
        df['daily_return'] = dr

    Returns:
    - pd.Series: Series of daily return values.
    """
    df_copy = df.copy()
    df_copy['d_ret'] = (df_copy[column] / df_copy[column].shift(1)) - 1
    df_copy['d_ret'] *= 100
    if fillna:
        df_copy['d_ret'] = df_copy['d_ret'].fillna(0)
    return df_copy['d_ret'].rename("d_ret")


def ExhaustionCandles(df, window=1, multiplier=1):
    """
    Calculate the average consecutive length of ups and downs to adjust the exhaustion bands dynamically
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - window (int): Lookback window for calculation.
    - multiplier (int or np.ndarray): Scalar or array of multipliers.

    Call with:
        maj_qual, min_qual = ExhaustionCandles(df, window, multiplier)
        df['maj_qual'] = maj_qual
        df['min_qual'] = min_qual

    Returns:
    - np.ndarray, np.ndarray: Arrays of major and minor quality values.
    """
    consecutive_diff = np.sign(df['close'].diff())
    maj_qual = np.zeros(len(df))
    min_qual = np.zeros(len(df))

    # Ensure multiplier is an array
    if isinstance(multiplier, (int, float)):
        multiplier = np.full(len(df), multiplier)
    elif isinstance(multiplier, np.ndarray) and multiplier.shape[0] != len(df):
        raise ValueError("Length of multiplier array must match the length of the DataFrame")

    for i in range(len(df)):
        idx_range = consecutive_diff[i - window + 1:i + 1] if i >= window else consecutive_diff[:i + 1]
        avg_consecutive = ConsecutiveCount(idx_range)
        if isinstance(avg_consecutive, np.ndarray):
            avg_consecutive = avg_consecutive.item()
        maj_qual[i] = int(avg_consecutive * (3 * multiplier[i])) if not np.isnan(avg_consecutive) else 0
        min_qual[i] = int(avg_consecutive * (3 * multiplier[i])) if not np.isnan(avg_consecutive) else 0

    return maj_qual, min_qual


def ExhaustionLengths(df):
    """
    Calculate the average length of peaks and valleys to adjust the exhaustion bands dynamically
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame.

    Call with:
        maj_len, min_len = ExhaustionLengths(df)
        df['maj_len'] = maj_len
        df['min_len'] = min_len

    Returns:
    - int, int: Average peak distance and average valley distance.
    """
    high_indices = argrelextrema(df['high'].to_numpy(), np.greater)[0]
    low_indices = argrelextrema(df['low'].to_numpy(), np.less)[0]

    if len(high_indices) < 2 or len(low_indices) < 2:
        return 0, 0

    avg_peak_distance = np.mean(np.diff(high_indices))
    std_peak_distance = np.std(np.diff(high_indices))
    avg_valley_distance = np.mean(np.diff(low_indices))
    std_valley_distance = np.std(np.diff(low_indices))

    maj_len = int(avg_peak_distance + std_peak_distance)
    min_len = int(avg_valley_distance + std_valley_distance)

    return maj_len, min_len


def GetMinMax(series1: pd.Series, series2: pd.Series, function: str = "min"):
    """
    Find min or max value between two lists for each index

    Parameters:
    - series1 (pd.Series): First input series.
    - series2 (pd.Series): Second input series.
    - function (str): Function to apply ("min" or "max"). Default is "min".

    Call with:
        min_max_series = GetMinMax(series1, series2, function)
        df['min_max'] = min_max_series

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
        raise ValueError('"function" variable value should be "min" or "max"')

    return pd.Series(output)


def LinearDecay(start: float, end: float, start_time: int, end_time: int, trade_time: int) -> float:
    """
    Simple linear decay function. Decays from start to end after end_time minutes (starts after start_time minutes)

    Parameters:
    - start (float): Starting value.
    - end (float): Ending value.
    - start_time (int): Start time in minutes.
    - end_time (int): End time in minutes.
    - trade_time (int): Current trade time in minutes.

    Call with:
        decayed_value = LinearDecay(start, end, start_time, end_time, trade_time)

    Returns:
    - float: Decayed value.
    """
    time = max(0, trade_time - start_time)
    rate = (start - end) / (end_time - start_time)
    return max(end, start - (rate * time))


def LinearGrowth(start: float, end: float, start_time: int, end_time: int, trade_time: int) -> float:
    """
    Simple linear growth function. Grows from start to end after end_time minutes (starts after start_time minutes)

    Parameters:
    - start (float): Starting value.
    - end (float): Ending value.
    - start_time (int): Start time in minutes.
    - end_time (int): End time in minutes.
    - trade_time (int): Current trade time in minutes.

    Call with:
        grown_value = LinearGrowth(start, end, start_time, end_time, trade_time)

    Returns:
    - float: Grown value.
    """
    time = max(0, trade_time - start_time)
    rate = (end - start) / (end_time - start_time)
    return min(end, start + (rate * time))


def PopulateLeledcMajorMinor(df, maj_qual, min_qual, maj_len, min_len):
    """
    Populate Leledc Major and Minor columns

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - maj_qual (np.ndarray): Array of major quality values.
    - min_qual (np.ndarray): Array of minor quality values.
    - maj_len (int): Major length value.
    - min_len (int): Minor length value.

    Call with:
        leledc_major_minor = PopulateLeledcMajorMinor(df, maj_qual, min_qual, maj_len, min_len)

    Returns:
    - pd.DataFrame: DataFrame with populated columns.
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
        if bindex_maj > maj_qual[i] and close < df_copy['open'][i] and df_copy['high'][i] >= df_copy['high'][i - maj_len:i].max():
            bindex_maj, trend_maj, update_major = 0, 1, True
        elif sindex_maj > maj_qual[i] and close > df_copy['open'][i] and df_copy['low'][i] <= df_copy['low'][i - maj_len:i].min():
            sindex_maj, trend_maj, update_major = 0, -1, True

        df_copy.at[i, 'leledc_major'] = trend_maj if update_major else np.nan if trend_maj == 0 else trend_maj
        if bindex_min > min_qual[i] and close < df_copy['open'][i] and df_copy['high'][i] >= df_copy['high'][i - min_len:i].max():
            bindex_min = 0
            df_copy.at[i, 'leledc_minor'] = -1
        elif sindex_min > min_qual[i] and close > df_copy['open'][i] and df_copy['low'][i] <= df_copy['low'][i - min_len:i].min():
            sindex_min = 0
            df_copy.at[i, 'leledc_minor'] = 1
        else:
            df_copy.at[i, 'leledc_minor'] = 0

    return df_copy


def RegressionSlope(df, lookback_period=20):
    """
    Calculate the slope of the linear regression for a given lookback period.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the 'close' prices.
    - lookback_period (int): The lookback period for calculating the regression slope. Default is 20.

    Call with:
        slope = RegressionSlope(df, lookback_period)
        df['slope'] = slope

    Returns:
    - pd.Series: Series containing the regression slopes.
    """
    # Initialize the 'slope' column with NaN values
    slope_series = pd.Series(np.nan, index=df.index)

    # Loop over each row starting from the lookback period
    for i in range(lookback_period, len(df)):
        # Define the x-values (time steps) for the lookback window
        x_values = np.arange(lookback_period)
        # Extract the corresponding 'close' prices for the lookback window
        y_values = df.loc[i - lookback_period:i - 1, 'close'].values

        # Calculate the slope using linear regression
        slope, _, _, _, _ = linregress(x_values, y_values)

        # Store the calculated slope in the series
        slope_series[i] = slope

    return slope_series


def SameLength(bigger, shorter):
    """
    Ensures the shorter array has the same length as the bigger array by padding with NaN values.

    Parameters:
    - bigger (np.ndarray): The array with the larger size.
    - shorter (np.ndarray): The array with the smaller size.

    Call with:
        padded_array = SameLength(bigger, shorter)

    Returns:
    - np.ndarray: The shorter array padded with NaN values to match the size of the bigger array.
    """
    return np.concatenate((np.full((bigger.shape[0] - shorter.shape[0]), np.nan), shorter))


def StDev(series, period):
    """
    Calculate the standard deviation over a specified period.

    Parameters:
    - series (pd.Series): The data series to calculate the standard deviation for.
    - period (int): The period over which to calculate the standard deviation.

    Returns:
    - pd.Series: The standard deviation of the series.
    """
    return series.rolling(window=period).std()


def ZScore(series, window=500):
    """
    Calculate the z-score of a series.

    Parameters:
    - series (pd.Series): Input series.
    - window (int): Lookback window for mean and standard deviation calculation.

    Call with:
        zscore = ZScore(series)
        df['zscore'] = zscore

    Returns:
    - pd.Series: Z-score series.
    """
    mean = series.rolling(window=window, min_periods=1).mean()
    std = series.rolling(window=window, min_periods=1).std(ddof=0)
    zscore = (series - mean) / std
    zscore = zscore.fillna(0)  # Fill NaN values with 0 to avoid issues with calculations

    return zscore


class IndicatorMixin:
    """Util mixin indicator class"""

    _fillna = False

    def _check_fillna(self, series: pd.Series, value: int = 0) -> pd.Series:
        """Check if fillna flag is True.

        Parameters:
        - series (pandas.Series): Calculated indicator series.
        - value (int): Value to fill gaps; if -1 fill values using 'backfill' mode.

        Returns:
        - pd.Series: New feature generated.
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
        tr1 = high - low
        tr2 = (high - prev_close).abs()
        tr3 = (low - prev_close).abs()
        true_range = pd.DataFrame(data={"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
        return true_range


def DropNa(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows with 'NaN' values

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.

    Call with:
        dropna = dropna(df)

    Returns:
    - pd.DataFrame: DataFrame without NaN values.
    """
    df = df.copy()
    number_cols = df.select_dtypes(include=np.number).columns.tolist()
    df[number_cols] = df[number_cols][df[number_cols] < math.exp(709)]  # big number
    df[number_cols] = df[number_cols][df[number_cols] != 0.0]
    df = df.dropna()
    return df


# def _sma(series, periods: int, fillna: bool = False):
#     """
#     Simple Moving Average (SMA)

#     Parameters:
#     - series (pd.Series): Input series.
#     - periods (int): Period for SMA calculation.
#     - fillna (bool): If True, fill NaN values. Default is False.

#     Call with:
#         sma = _sma(series, periods)
#         df['sma'] = sma

#     Returns:
#     - pd.Series: Series of SMA values.
#     """
#     min_periods = 0 if fillna else periods
#     return series.rolling(window=periods, min_periods=min_periods).mean()


# def _ema(series, periods: int, fillna: bool = False):
#     """
#     Exponential Moving Average (EMA)

#     Parameters:
#     - series (pd.Series): Input series.
#     - periods (int): Period for EMA calculation.
#     - fillna (bool): If True, fill NaN values. Default is False.

#     Call with:
#         ema = _ema(series, periods)
#         df['ema'] = ema

#     Returns:
#     - pd.Series: Series of EMA values.
#     """
#     min_periods = 0 if fillna else periods
#     return series.ewm(span=periods, min_periods=min_periods, adjust=False).mean()




