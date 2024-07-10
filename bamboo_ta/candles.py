# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *
from .utility import *
from.momentum import *


def Exhaustion_Bars(df, maj_qual=6, maj_len=12, min_qual=6, min_len=12, core_length=4):
    """
    Leledc Exhaustion Bars - Extended
    
    Leledc Exhaustion Bars - Extended
    Infamous S/R Reversal Indicator

    leledc_major (Trend): 
     1 Up
    -1 Down
    
    leledc_minor: 
    1 Sellers exhausted
    0 Neutral / Hold
    -1 Buyers exhausted 

    Original (MT4) https://www.abundancetradinggroup.com/leledc-exhaustion-bar-mt4-indicator/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low', and 'close' columns.
    - maj_qual (int): Major quality parameter.
    - maj_len (int): Major length parameter.
    - min_qual (int): Minor quality parameter.
    - min_len (int): Minor length parameter.
    - core_length (int): Core length parameter.

    Call with:
        exhaustion = bta.Exhaustion_Bars(df)
        df['leledc_major'] = exhaustion['leledc_major']
        df['leledc_minor'] = exhaustion['leledc_minor']

    Returns:
    - pd.DataFrame: DataFrame with columns populated.
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


def Dynamic_Exhaustion_Bars(df, window=500):
    """
    Dynamic Leledc Exhaustion Bars -  By nilux
    The lookback length and exhaustion bars adjust dynamically to the market.
    
    leledc_major (Trend): 
     1 Up
    -1 Down
    
    leledc_minor: 
    1 Sellers exhausted
    0 Neutral / Hold
    -1 Buyers exhausted 
        
    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - window (int): Lookback window for z-score calculation.

    Call with:
        dynamic_exhaustion = bta.Dynamic_Exhaustion_Bars(df)
        df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
        df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']

    Returns:
    - pd.DataFrame: DataFrame with columns populated.
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


def Pinbar(df, smi=None):
    """ 
    Pinbar - Price Action Indicator

    Pinbars are an easy but sure indication
    of incoming price reversal. 
    Signal confirmation with SMI.
    
    Pinescript Source by PeterO - Thx!
    https://tradingview.com/script/aSJnbGnI-PivotPoints-with-Momentum-confirmation-by-PeterO/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close' columns.
    - smi: Optional Series for SMI.

    Call with:
        pin = bta.Pinbar(df)
        df['pinbar_sell'] = pin['pinbar_sell']
        df['pinbar_buy'] = pin['pinbar_buy']

    Returns:
    - pd.DataFrame: DataFrame with buy / sell signals columns populated.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    low = df_copy['low']
    high = df_copy['high']
    close = df_copy['close']
    
    tr = True_Range(df_copy)
    
    if smi is None:
        df_copy = SMI_Momentum(df_copy)
        smi = df_copy['smi']
    
    df_copy['pinbar_sell'] = (
        (high < high.shift(1)) &
        (close < high - (tr * 2 / 3)) &
        (smi < smi.shift(1)) &
        (smi.shift(1) > 40) &
        (smi.shift(1) < smi.shift(2))
    )

    df_copy['pinbar_buy'] = (
        (low > low.shift(1)) &
        (close > low + (tr * 2 / 3)) &
        (smi.shift(1) < -40) &
        (smi > smi.shift(1)) &
        (smi.shift(1) > smi.shift(2))
    )
    
    return df_copy[['pinbar_sell', 'pinbar_buy']]


def HeikinAshi(df, pre_smoothing_period=None, post_smoothing_period=None):
    """
    Heikin Ashi (HA) with Optional Pre and Post Smoothing

    Call with:
    - Regular Heiken Ashi:
        ha_df = bta.HeikinAshi(df)

    - With pre-smoothing of the original data:
        ha_df = bta.HeikinAshi(df, pre_smoothing_period=14)

    - With both pre and post smoothing:
        ha_df = bta.HeikinAshi(df, pre_smoothing_period=14, post_smoothing_period=14)

    After calling, the following columns can be extracted:
        df['HA_Close'] = ha_df['HA_Close']
        df['HA_Open'] = ha_df['HA_Open']
        df['HA_High'] = ha_df['HA_High']
        df['HA_Low'] = ha_df['HA_Low']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - pre_smoothing_period (int, optional): Period for EMA pre-smoothing of the original data. If provided, original price bars are smoothed before Heikin Ashi calculations.
    - post_smoothing_period (int, optional): Period for EMA post-smoothing of Heikin Ashi values. If provided, Heikin Ashi values are smoothed post calculations.

    Returns:
    - pd.DataFrame: DataFrame with 'HA_Close', 'HA_Open', 'HA_High', 'HA_Low' columns.

    Description:
    Heikin Ashi is a type of price chart that shares some characteristics with candlestick charts but differs due to the values used to plot them. This modified version allows for optional smoothing of the original data before the Heikin Ashi calculation and/or smoothing of the Heikin Ashi values themselves, aiming to provide a more refined and smoother representation of price action, making it easier to identify the trend.
    """
    df_copy = df.copy()

    # If pre-smoothing is required
    if pre_smoothing_period:
        df_copy['open'] = EMA(df_copy, 'open', pre_smoothing_period)
        df_copy['close'] = EMA(df_copy, 'close', pre_smoothing_period)
        df_copy['high'] = EMA(df_copy, 'high', pre_smoothing_period)
        df_copy['low'] = EMA(df_copy, 'low', pre_smoothing_period)

    # Regular Heikin Ashi calculations
    df_copy['HA_Close'] = (df_copy['open'] + df_copy['high'] +
                           df_copy['low'] + df_copy['close']) / 4
    df_copy.reset_index(inplace=True)
    ha_open = [(df_copy['open'][0] + df_copy['close'][0]) / 2]
    [ha_open.append((ha_open[i] + df_copy['HA_Close'].values[i]) / 2)
     for i in range(0, len(df_copy) - 1)]
    df_copy['HA_Open'] = ha_open
    df_copy.set_index('index', inplace=True)
    df_copy['HA_High'] = df_copy[['HA_Open', 'HA_Close', 'high']].max(axis=1)
    df_copy['HA_Low'] = df_copy[['HA_Open', 'HA_Close', 'low']].min(axis=1)

    # If post-smoothing is required
    if post_smoothing_period:
        df_copy['HA_Open'] = EMA(df_copy, 'HA_Open', post_smoothing_period)
        df_copy['HA_High'] = EMA(df_copy, 'HA_High', post_smoothing_period)
        df_copy['HA_Low'] = EMA(df_copy, 'HA_Low', post_smoothing_period)
        df_copy['HA_Close'] = EMA(df_copy, 'HA_Close', post_smoothing_period)

    return df_copy[['HA_Open', 'HA_High', 'HA_Low', 'HA_Close']]


def LinRegCandles(df, linreg_length=11, sma_signal=True, signal_length=11):
    """
    Linear Regression Candles with Optional Signal Line

    Call with:
    - Regular Linear Regression Candles with SMA signal line:
        lr_df = bta.LinRegCandles(df)

    - With EMA signal line:
        lr_df = bta.LinRegCandles(df, sma_signal=False)

    - With SMA signal line:
        lr_df = bta.LinRegCandles(df, sma_signal=True)

    After calling, the following columns can be extracted:
        df['LRC_Open'] = lr_df['bopen']
        df['LRC_High'] = lr_df['bhigh']
        df['LRC_Low'] = lr_df['blow']
        df['LRC_Close'] = lr_df['bclose']
        df['LRC_Signal'] = lr_df['signal']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - linreg_length (int, optional): Period for linear regression calculation. Default is 11.
    - sma_signal (bool, optional): If True, uses SMA for the signal line. If False, uses EMA. Default is True.
    - signal_length (int, optional): Period for the moving average signal line. Default is 11.

    Returns:
    - pd.DataFrame: DataFrame with 'bopen', 'bhigh', 'blow', 'bclose' as the Linear Regression Candles, and 'signal' as the signal line.

    Description:
    The Linear Regression Candles transform the traditional OHLC bars using a linear regression algorithm, providing a smoothed representation of price action. The function also provides an optional signal line, which can be either an SMA or an EMA of the Linear Regression Candle close. This signal line can help to identify trends and potential trading signals.
    """
    df_copy = df.copy()

    # Calculate linear regression coefficients for open, high, low, and close
    df_copy['bopen'] = df_copy['open'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[
            1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['bhigh'] = df_copy['high'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[
            1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['blow'] = df_copy['low'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[
            1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    df_copy['bclose'] = df_copy['close'].rolling(window=linreg_length).apply(
        lambda x: np.polyfit(np.arange(len(x)), x, 1)[
            1] + np.polyfit(np.arange(len(x)), x, 1)[0] * (len(x) - 1),
        raw=True
    )

    # Calculate the signal line using SMA or EMA
    if sma_signal:
        df_copy['signal'] = df_copy['bclose'].rolling(
            window=signal_length).mean()
    else:
        df_copy['signal'] = df_copy['bclose'].ewm(
            span=signal_length, adjust=False).mean()

    return df_copy
