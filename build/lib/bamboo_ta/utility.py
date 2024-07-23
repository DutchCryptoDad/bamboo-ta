# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd
from .bamboo_ta import *
from scipy.signal import argrelextrema


def Calculate_Exhaustion_Lengths(df):
    """
    Calculate the average length of peaks and valleys to adjust the exhaustion bands dynamically
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame.

    Call with:
        maj_len, min_len = Calculate_Exhaustion_Lengths(df)
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


def Calculate_Exhaustion_Candles(df, window=1, multiplier=1):
    """
    Calculate the average consecutive length of ups and downs to adjust the exhaustion bands dynamically
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - window (int): Lookback window for calculation.
    - multiplier (int or np.ndarray): Scalar or array of multipliers.

    Call with:
        maj_qual, min_qual = Calculate_Exhaustion_Candles(df, window, multiplier)
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
        avg_consecutive = Consecutive_Count(idx_range)
        if isinstance(avg_consecutive, np.ndarray):
            avg_consecutive = avg_consecutive.item()
        maj_qual[i] = int(avg_consecutive * (3 * multiplier[i])) if not np.isnan(avg_consecutive) else 0
        min_qual[i] = int(avg_consecutive * (3 * multiplier[i])) if not np.isnan(avg_consecutive) else 0

    return maj_qual, min_qual

def Consecutive_Count(consecutive_diff):
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


def Linear_Decay(start: float, end: float, start_time: int, end_time: int, trade_time: int) -> float:
    """
    Simple linear decay function. Decays from start to end after end_time minutes (starts after start_time minutes)

    Parameters:
    - start (float): Starting value.
    - end (float): Ending value.
    - start_time (int): Start time in minutes.
    - end_time (int): End time in minutes.
    - trade_time (int): Current trade time in minutes.

    Call with:
        decayed_value = Linear_Decay(start, end, start_time, end_time, trade_time)

    Returns:
    - float: Decayed value.
    """
    time = max(0, trade_time - start_time)
    rate = (start - end) / (end_time - start_time)
    return max(end, start - (rate * time))


def Linear_Growth(start: float, end: float, start_time: int, end_time: int, trade_time: int) -> float:
    """
    Simple linear growth function. Grows from start to end after end_time minutes (starts after start_time minutes)

    Parameters:
    - start (float): Starting value.
    - end (float): Ending value.
    - start_time (int): Start time in minutes.
    - end_time (int): End time in minutes.
    - trade_time (int): Current trade time in minutes.

    Call with:
        grown_value = Linear_Growth(start, end, start_time, end_time, trade_time)

    Returns:
    - float: Grown value.
    """
    time = max(0, trade_time - start_time)
    rate = (end - start) / (end_time - start_time)
    return min(end, start + (rate * time))


def populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len):
    """
    Populate Leledc Major and Minor columns

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - maj_qual (np.ndarray): Array of major quality values.
    - min_qual (np.ndarray): Array of minor quality values.
    - maj_len (int): Major length value.
    - min_len (int): Minor length value.

    Call with:
        leledc_major_minor = populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len)

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


def dropna(df: pd.DataFrame) -> pd.DataFrame:
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


def _sma(series, periods: int, fillna: bool = False):
    """
    Simple Moving Average (SMA)

    Parameters:
    - series (pd.Series): Input series.
    - periods (int): Period for SMA calculation.
    - fillna (bool): If True, fill NaN values. Default is False.

    Call with:
        sma = _sma(series, periods)
        df['sma'] = sma

    Returns:
    - pd.Series: Series of SMA values.
    """
    min_periods = 0 if fillna else periods
    return series.rolling(window=periods, min_periods=min_periods).mean()


def _ema(series, periods: int, fillna: bool = False):
    """
    Exponential Moving Average (EMA)

    Parameters:
    - series (pd.Series): Input series.
    - periods (int): Period for EMA calculation.
    - fillna (bool): If True, fill NaN values. Default is False.

    Call with:
        ema = _ema(series, periods)
        df['ema'] = ema

    Returns:
    - pd.Series: Series of EMA values.
    """
    min_periods = 0 if fillna else periods
    return series.ewm(span=periods, min_periods=min_periods, adjust=False).mean()

def STDEV(series, period):
    """
    Calculate the standard deviation over a specified period.

    Parameters:
    - series (pd.Series): The data series to calculate the standard deviation for.
    - period (int): The period over which to calculate the standard deviation.

    Returns:
    - pd.Series: The standard deviation of the series.
    """
    return series.rolling(window=period).std()

def get_min_max(series1: pd.Series, series2: pd.Series, function: str = "min"):
    """
    Find min or max value between two lists for each index

    Parameters:
    - series1 (pd.Series): First input series.
    - series2 (pd.Series): Second input series.
    - function (str): Function to apply ("min" or "max"). Default is "min".

    Call with:
        min_max_series = get_min_max(series1, series2, function)
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


def Daily_Return(df, column="close", fillna=False):
    """
    Daily Return (DR)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily return is to be calculated. Default is "close".
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        dr = Daily_Return(df)
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


def Daily_Log_Return(df, column="close", fillna=False):
    """
    Daily Log Return (DLR)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily log return is to be calculated. Default is "close".
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        dlr = Daily_Log_Return(df)
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


def Cumulative_Return(df, column="close", fillna=False):
    """
    Cumulative Return (CR)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the cumulative return is to be calculated. Default is "close".
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        cr = Cumulative_Return(df)
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
