# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from scipy.signal import argrelextrema


def Calculate_Exhaustion_Candles(df, window, multiplier):
    """
    Calculate the average consecutive length of ups and downs to adjust the exhaustion bands dynamically
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - window (int): Lookback window for calculation.
    - multiplier (np.ndarray): Array of multipliers.

    Returns:
    - np.ndarray, np.ndarray: Arrays of major and minor quality values.
    """
    consecutive_diff = np.sign(df['close'].diff())
    maj_qual = np.zeros(len(df))
    min_qual = np.zeros(len(df))

    for i in range(len(df)):
        idx_range = consecutive_diff[i - window + 1:i + 1] if i >= window else consecutive_diff[:i + 1]
        avg_consecutive = Consecutive_Count(idx_range)
        if isinstance(avg_consecutive, np.ndarray):
            avg_consecutive = avg_consecutive.item()
        maj_qual[i] = int(avg_consecutive * (3 * multiplier[i])) if not np.isnan(avg_consecutive) else 0
        min_qual[i] = int(avg_consecutive * (3 * multiplier[i])) if not np.isnan(avg_consecutive) else 0

    return maj_qual, min_qual

def Calculate_Exhaustion_Lengths(df):
    """
    Calculate the average length of peaks and valleys to adjust the exhaustion bands dynamically
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame.

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

    Returns:
    - pd.DataFrame: DataFrame with populated columns.
    """
    bindex_maj, sindex_maj, trend_maj = 0, 0, 0
    bindex_min, sindex_min = 0, 0

    df['leledc_major'] = np.nan
    df['leledc_minor'] = 0

    for i in range(1, len(df)):
        close = df['close'][i]
        short_length = i if i < 4 else 4

        if close > df['close'][i - short_length]:
            bindex_maj += 1
            bindex_min += 1
        elif close < df['close'][i - short_length]:
            sindex_maj += 1
            sindex_min += 1

        update_major = False
        if bindex_maj > maj_qual[i] and close < df['open'][i] and df['high'][i] >= df['high'][i - maj_len:i].max():
            bindex_maj, trend_maj, update_major = 0, 1, True
        elif sindex_maj > maj_qual[i] and close > df['open'][i] and df['low'][i] <= df['low'][i - maj_len:i].min():
            sindex_maj, trend_maj, update_major = 0, -1, True

        df.at[i, 'leledc_major'] = trend_maj if update_major else np.nan if trend_maj == 0 else trend_maj
        if bindex_min > min_qual[i] and close < df['open'][i] and df['high'][i] >= df['high'][i - min_len:i].max():
            bindex_min = 0
            df.at[i, 'leledc_minor'] = -1
        elif sindex_min > min_qual[i] and close > df['open'][i] and df['low'][i] <= df['low'][i - min_len:i].min():
            sindex_min = 0
            df.at[i, 'leledc_minor'] = 1
        else:
            df.at[i, 'leledc_minor'] = 0

    return df


def True_Range(df):
    """
    Calculate True Range (TR)
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.

    Returns:
    - pd.Series: Series of True Range values.
    """
    prev_close = df['close'].shift()
    tr = pd.concat([df['high'] - df['low'], abs(df['high'] - prev_close), abs(df['low'] - prev_close)], axis=1).max(axis=1)
    return tr


def ZScore(series, window=500):
    """
    Calculate the z-score of a series.

    Parameters:
    - series (pd.Series): Input series.
    - window (int): Lookback window for mean and standard deviation calculation.

    Returns:
    - pd.Series: Z-score series.
    """
    mean = series.rolling(window=window, min_periods=1).mean()
    std = series.rolling(window=window, min_periods=1).std(ddof=0)
    zscore = (series - mean) / std
    zscore = zscore.fillna(0)  # Fill NaN values with 0 to avoid issues with calculations
    return zscore
