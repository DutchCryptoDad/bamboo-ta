# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *
from .utility import *
from.momentum import *


def ExhaustionBars(df, maj_qual=6, maj_len=30, min_qual=5, min_len=5, core_length=4):
    """
    Leledc Exhaustion Bars

    Infamous S/R Reversal Indicator

    Leledc exhaustion bars are a specific type of price action pattern used in technical analysis to identify potential reversals in the market trend. These bars are characterized by a sharp move in price with an increase in volume, often indicating that the current trend is losing momentum and may reverse direction soon. Traders use them to pinpoint the end of a trend and the beginning of a new one, thereby making more informed trading decisions.

    For more information, see: https://www.abundancetradinggroup.com/leledc-exhaustion-bar-mt4-indicator/
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low', and 'close' columns.
    - maj_qual (int): Major quality parameter. Default is 6.
    - maj_len (int): Major length parameter. Default is 30.
    - min_qual (int): Minor quality parameter. Default is 5.
    - min_len (int): Minor length parameter. Default is 5.
    - core_length (int): Core length parameter. Default is 4.

    Call with:
        exhaustion = bta.ExhaustionBars(df)
        df['leledc_major'] = exhaustion['leledc_major']
        df['leledc_minor'] = exhaustion['leledc_minor']

    Returns:
    - pd.DataFrame: DataFrame with 'leledc_major' and 'leledc_minor' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    bindex_maj, sindex_maj, trend_maj = 0, 0, 0
    bindex_min, sindex_min = 0, 0

    for i in range(len(df_copy)):
        close = df_copy['close'][i]

        if i < 1 or i - core_length < 0:
            df_copy.loc[i, 'leledc_major'] = np.nan
            df_copy.loc[i, 'leledc_minor'] = 0
            continue

        bindex_maj, sindex_maj = np.nan_to_num(bindex_maj), np.nan_to_num(sindex_maj)
        bindex_min, sindex_min = np.nan_to_num(bindex_min), np.nan_to_num(sindex_min)

        if close > df_copy['close'][i - core_length]:
            bindex_maj += 1
            bindex_min += 1
        elif close < df_copy['close'][i - core_length]:
            sindex_maj += 1
            sindex_min += 1

        update_major = False
        if bindex_maj > maj_qual and close < df_copy['open'][i] and df_copy['high'][i] >= df_copy['high'][i - maj_len:i].max():
            bindex_maj, trend_maj, update_major = 0, 1, True
        elif sindex_maj > maj_qual and close > df_copy['open'][i] and df_copy['low'][i] <= df_copy['low'][i - maj_len:i].min():
            sindex_maj, trend_maj, update_major = 0, -1, True

        df_copy.loc[i, 'leledc_major'] = trend_maj if update_major else np.nan if trend_maj == 0 else trend_maj

        if bindex_min > min_qual and close < df_copy['open'][i] and df_copy['high'][i] >= df_copy['high'][i - min_len:i].max():
            bindex_min = 0
            df_copy.loc[i, 'leledc_minor'] = -1
        elif sindex_min > min_qual and close > df_copy['open'][i] and df_copy['low'][i] <= df_copy['low'][i - min_len:i].min():
            sindex_min = 0
            df_copy.loc[i, 'leledc_minor'] = 1
        else:
            df_copy.loc[i, 'leledc_minor'] = 0

    return df_copy[['leledc_major', 'leledc_minor']]


def DynamicExhaustionBars(df, window=500):
    """
    Dynamic Leledc Exhaustion Bars
    The lookback length and exhaustion bars adjust dynamically to the market conditions.

    This indicator dynamically adjusts the lookback length and the exhaustion bars based on the market's behavior, helping to identify potential reversals and trend strength.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - window (int): Lookback window for z-score calculation. Default is 500.

    Call with:
        dynamic_exhaustion = bta.DynamicExhaustionBars(df)
        df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
        df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']

    Returns:
    - pd.DataFrame: DataFrame with 'leledc_major' and 'leledc_minor' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    df_copy['close_pct_change'] = df_copy['close'].pct_change()
    df_copy['pct_change_zscore'] = ZScore(df_copy['close_pct_change'], window)
    df_copy['pct_change_zscore_smoothed'] = df_copy['pct_change_zscore'].rolling(window=3).mean()
    df_copy['pct_change_zscore_smoothed'] = df_copy['pct_change_zscore_smoothed'].fillna(1.0)

    zscore = df_copy['pct_change_zscore_smoothed'].to_numpy()
    zscore_multi = np.maximum(np.minimum(5.0 - zscore * 2, 5.0), 1.5)

    maj_qual, min_qual = Calculate_Exhaustion_Candles(df_copy, window, zscore_multi)
    
    df_copy['maj_qual'] = maj_qual
    df_copy['min_qual'] = min_qual

    maj_len, min_len = Calculate_Exhaustion_Lengths(df_copy)
    
    df_copy['maj_len'] = maj_len
    df_copy['min_len'] = min_len

    df_copy = populate_leledc_major_minor(df_copy, maj_qual, min_qual, maj_len, min_len)

    return df_copy[['leledc_major', 'leledc_minor']]


# def Pinbar(df: pd.DataFrame, smi: pd.Series = None) -> pd.DataFrame:
#     """
#     Pinbar - Price Action Indicator

#     Pinbars are an easy but sure indication of incoming price reversal.
#     Signal confirmation with SMI (Stochastic Momentum Index) can enhance the accuracy of the signals.

#     Parameters:
#     - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
#     - smi (pandas.Series, optional): Optional Series for SMI. If not provided, it will be calculated internally.

#     Call with:
#         pin = bta.Pinbar(df)
#         df['pinbar_sell'] = pin['pinbar_sell']
#         df['pinbar_buy'] = pin['pinbar_buy']

#     Returns:
#     - pd.DataFrame: DataFrame with 'pinbar_sell' and 'pinbar_buy' columns populated.
#     """
#     df_copy = df.copy()

#     # Ensure the DataFrame contains the required columns
#     required_columns = ['high', 'low', 'close']
#     for col in required_columns:
#         if col not in df.columns:
#             raise KeyError(f"DataFrame must contain '{col}' column")

#     low = df_copy['low']
#     high = df_copy['high']
#     close = df_copy['close']
    
#     tr = TrueRange(df_copy)['true_range']
    
#     if smi is None:
#         df_copy = StochasticMomentumIndex(df_copy)
#         smi = df_copy['smi']
    
#     df_copy['pinbar_sell'] = (
#         (high < high.shift(1)) &
#         (close < high - (tr * 2 / 3).iloc[:]) &
#         (smi < smi.shift(1)) &
#         (smi.shift(1) > 40) &
#         (smi.shift(1) < smi.shift(2))
#     )

#     df_copy['pinbar_buy'] = (
#         (low > low.shift(1)) &
#         (close > low + (tr * 2 / 3).iloc[:]) &
#         (smi.shift(1) < -40) &
#         (smi > smi.shift(1)) &
#         (smi.shift(1) > smi.shift(2))
#     )
    
#     return df_copy[['pinbar_sell', 'pinbar_buy']]


def HeikinAshi(df, pre_smoothing_period=None, post_smoothing_period=None):
    """
    Heikin Ashi (HA) with Optional Pre and Post Smoothing

    Heikin Ashi is a type of price chart that shares some characteristics with candlestick charts but differs due to the values used to plot them. 
    This modified version allows for optional smoothing of the original data before the Heikin Ashi calculation and/or smoothing of the Heikin Ashi values themselves, 
    aiming to provide a more refined and smoother representation of price action, making it easier to identify the trend.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - pre_smoothing_period (int, optional): Period for EMA pre-smoothing of the original data. If provided, original price bars are smoothed before Heikin Ashi calculations.
    - post_smoothing_period (int, optional): Period for EMA post-smoothing of Heikin Ashi values. If provided, Heikin Ashi values are smoothed post calculations.

    Call with:
        ha_df = bta.HeikinAshi(df)
        df['ha_open'] = ha_df['ha_open']
        df['ha_high'] = ha_df['ha_high']
        df['ha_low'] = ha_df['ha_low']
        df['ha_close'] = ha_df['ha_close']

    Returns:
    - pd.DataFrame: DataFrame with 'ha_open', 'ha_high', 'ha_low', and 'ha_close' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # If pre-smoothing is required
    if pre_smoothing_period:
        df_copy['open'] = EMA(df_copy, 'open', pre_smoothing_period)
        df_copy['close'] = EMA(df_copy, 'close', pre_smoothing_period)
        df_copy['high'] = EMA(df_copy, 'high', pre_smoothing_period)
        df_copy['low'] = EMA(df_copy, 'low', pre_smoothing_period)

    # Regular Heikin Ashi calculations
    df_copy['ha_close'] = (df_copy['open'] + df_copy['high'] +
                           df_copy['low'] + df_copy['close']) / 4
    df_copy.reset_index(inplace=True)
    ha_open = [(df_copy['open'][0] + df_copy['close'][0]) / 2]
    [ha_open.append((ha_open[i] + df_copy['ha_close'].values[i]) / 2)
     for i in range(0, len(df_copy) - 1)]
    df_copy['ha_open'] = ha_open
    df_copy.set_index('index', inplace=True)
    df_copy['ha_high'] = df_copy[['ha_open', 'ha_close', 'high']].max(axis=1)
    df_copy['ha_low'] = df_copy[['ha_open', 'ha_close', 'low']].min(axis=1)

    # If post-smoothing is required
    if post_smoothing_period:
        df_copy['ha_open'] = EMA(df_copy, 'ha_open', post_smoothing_period)
        df_copy['ha_high'] = EMA(df_copy, 'ha_high', post_smoothing_period)
        df_copy['ha_low'] = EMA(df_copy, 'ha_low', post_smoothing_period)
        df_copy['ha_close'] = EMA(df_copy, 'ha_close', post_smoothing_period)

    # Limit to two decimal places
    df_copy['ha_open'] = df_copy['ha_open'].round(2)
    df_copy['ha_high'] = df_copy['ha_high'].round(2)
    df_copy['ha_low'] = df_copy['ha_low'].round(2)
    df_copy['ha_close'] = df_copy['ha_close'].round(2)

    return df_copy[['ha_open', 'ha_high', 'ha_low', 'ha_close']]


def LinRegCandles(df, linreg_length=11, sma_signal=True, signal_length=11):
    """
    Linear Regression Candles with Optional Signal Line

    The Linear Regression Candles transform the traditional OHLC bars using a linear regression algorithm, providing a smoothed representation of price action. The function also provides an optional signal line, which can be either an SMA or an EMA of the Linear Regression Candle close. This signal line can help to identify trends and potential trading signals.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - linreg_length (int, optional): Period for linear regression calculation. Default is 11.
    - sma_signal (bool, optional): If True, uses SMA for the signal line. If False, uses EMA. Default is True.
    - signal_length (int, optional): Period for the moving average signal line. Default is 11.

    Call with:
        lr_df = bta.LinRegCandles(df)
        df['lrc_open'] = lr_df['bopen']
        df['lrc_high'] = lr_df['bhigh']
        df['lrc_low'] = lr_df['blow']
        df['lrc_close'] = lr_df['bclose']
        df['lrc_signal'] = lr_df['signal']

    Returns:
    - pd.DataFrame: DataFrame with 'bopen', 'bhigh', 'blow', 'bclose' as the Linear Regression Candles, and 'signal' as the signal line.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate linear regression coefficients for open, high, low, and close
    df_copy['bopen'] = df_copy['open'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['bhigh'] = df_copy['high'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['blow'] = df_copy['low'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['bclose'] = df_copy['close'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    # Calculate the signal line using SMA or EMA
    if sma_signal:
        df_copy['signal'] = df_copy['bclose'].rolling(window=signal_length).mean()
    else:
        df_copy['signal'] = df_copy['bclose'].ewm(span=signal_length, adjust=False).mean()

    # Limit to two decimal places
    df_copy['bopen'] = df_copy['bopen'].round(2)
    df_copy['bhigh'] = df_copy['bhigh'].round(2)
    df_copy['blow'] = df_copy['blow'].round(2)
    df_copy['bclose'] = df_copy['bclose'].round(2)
    df_copy['signal'] = df_copy['signal'].round(2)

    return df_copy[['bopen', 'bhigh', 'blow', 'bclose', 'signal']]
