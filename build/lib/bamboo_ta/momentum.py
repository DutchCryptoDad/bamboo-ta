# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *
from .volatility import *
# from .utility import *


def CMO(df, length=14):
    """
    Chande Momentum Oscillator (CMO)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Length for the CMO calculation. Default is 14.

    Call with:
        cmo = CMO(df)
        df['cmo'] = cmo['cmo']

    For Signal line:
        df['CMO_Signal'] = df['CMO'].rolling(window=10).mean().round(2)  # Using SMA for signal

    Returns:
    - pd.DataFrame: DataFrame with 'cmo' column.
    """
    df_copy = df.copy()

    mom = df['close'].diff()
    pos_mom = mom.where(mom > 0, 0)
    neg_mom = -mom.where(mom < 0, 0)
    sm1 = pos_mom.rolling(window=length).sum()
    sm2 = neg_mom.rolling(window=length).sum()
    cmo = 100 * (sm1 - sm2) / (sm1 + sm2)

    df_copy['cmo'] = cmo.round(2)
    
    return df_copy[['cmo']]


def EWO(df, column="close", sma1_period=5, sma2_period=35):
    """
    Elliott Wave Oscillator (EWO)

    Call with:
        df['ewo'] = bta.EWO(df, "close", 5, 35)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EWO is to be calculated. Default is "close".
    - sma1_period (int): The period for the shorter SMA used in EWO calculation. Default is 5.
    - sma2_period (int): The period for the longer SMA used in EWO calculation. Default is 35.

    Returns:
    - pandas.Series: A series of EWO values.

    Description:
    The Elliott Wave Oscillator (EWO) is a specific tool to help you identify the trend and the overall market pattern to assist in finding future trading opportunities. It is derived by calculating the difference between a short and long period simple moving average, then normalizing the result with the close price.
    """
    sma1 = df[column].rolling(window=sma1_period).mean()
    sma2 = df[column].rolling(window=sma2_period).mean()
    ewo = (sma1 - sma2) / df[column] * 100

    return ewo


def MACD(df, column="close", short_window=12, long_window=26, signal_window=9):
    """
    Moving Average Convergence Divergence (MACD)

    Call with:
        macd_result = bta.MACD(df, "close", 12, 26, 9)
        df['macd'] = macd_result['MACD']
        df['macd_signal'] = macd_result['MACD_signal']
        df['macd_histogram'] = macd_result['MACD_histogram']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - signal_window (int): The signal line period for EMA. Default is 9.

    Returns:
    - pd.DataFrame: DataFrame with 'MACD', 'Signal', and 'Histogram' columns.

    Description:
    MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.
    """
    short_ema = EMA(df, column=column, period=short_window)
    long_ema = EMA(df, column=column, period=long_window)
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    histogram = macd - signal

    # Returning as DataFrame
    return pd.DataFrame({
        'MACD': macd,
        'MACD_signal': signal,
        'MACD_histogram': histogram
    })


def MACD_Leader(df, src, fast_length=12, slow_length=26, signal_length=9):
    """
    MACD Leader

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations.
    - fast_length (int): Length for the fast EMA. Default is 12.
    - slow_length (int): Length for the slow EMA. Default is 26.
    - signal_length (int): Length for the signal EMA. Default is 9.

    Call with:
        macd_leader = MACD_Leader(df, 'close')
        df['macd_leader'] = macd_leader['macd_leader']

    Returns:
    - pd.DataFrame: DataFrame with 'macd_leader' column.
    """
    df_copy = df.copy()

    src_series = df[src]
    sema = EMA(df.assign(src_series=src_series), 'src_series', fast_length)
    lema = EMA(df.assign(src_series=src_series), 'src_series', slow_length)
    i1 = sema + EMA(df.assign(diff=src_series - sema), 'diff', fast_length)
    i2 = lema + EMA(df.assign(diff=src_series - lema), 'diff', slow_length)
    macd_leader = ((i1 - i2) / 10) * 100

    df_copy['macd_leader'] = macd_leader.round(2)
    
    return df_copy[['macd_leader']]

def Inverse_Fisher_Transform(df, src='close', rsi_length=10, rsi_smoothing=5, e_value=2.71):
    """
    Inverse Fisher Transform

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - src (str): Source column to calculate the indicator.
    - rsi_length (int): Length for the RSI calculation. Default is 10.
    - rsi_smoothing (int): Length for the RSI smoothing (EMA). Default is 5.
    - e_value (float): E value for the inverse fisher transform. Default is 2.71.

    Call with:
        ift = Inverse_Fisher_Transform(df)
        df['ift'] = ift['ift']

    Use additional levels in your dataframe for 
        # Add horizontal levels
        df['level_1_35'] = 1.35
        df['level_0_5'] = 0.5
        df['level_0'] = 0
        df['level_minus_0_5'] = -0.5
        df['level_minus_1'] = -1

    Returns:
    - pd.DataFrame: DataFrame with 'ift' column.
    """
    df_copy = df.copy()

    # Calculate RSI values
    rsi_values = RSI(df, column=src, period=rsi_length)
    
    # Smooth RSI values with EMA
    rsi_ema_values = EMA(df.assign(rsi_values=rsi_values), 'rsi_values', rsi_smoothing)
    
    # Apply Inverse Fisher Transform
    inv_fisher = (np.exp(2.0 * (rsi_ema_values - 50) * 0.1) - 1) / (np.exp(2.0 * (rsi_ema_values - 50) * 0.1) + 1)

    df_copy['ift'] = inv_fisher.round(2)
    
    return df_copy[['ift']]

def Waddah_Attar_Explosion(df, sensitivity=150, fast_length=20, slow_length=40, channel_length=20, mult=2.0):
    """
    Waddah Attar Explosion Indicator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        WAE = bta.Waddah_Attar_Explosion(df)
        df['trend_up'] = WAE['trend_up']
        df['trend_down'] = WAE['trend_down']
        df['explosion_line'] = WAE['explosion_line']
        df['dead_zone_line'] = WAE['dead_zone_line']

    Returns:
    - pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    print("DataFrame columns:", df.columns)  # Debug print
    print("First few rows of the DataFrame:\n", df.head())  # Debug print

    # Calculate DEAD_ZONE
    dead_zone = RMA(TR(df), 100) * 3.7
    print("DEAD_ZONE calculated")  # Debug print

    # Calculate MACD
    macd_fast = EMA(df, 'close', fast_length)
    macd_slow = EMA(df, 'close', slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity
    print("MACD and t1 calculated")  # Debug print

    # Calculate Bollinger Bands
    bb = BollingerBands(df, column='close', period=channel_length, std_dev=mult)
    e1 = bb['BB_upper'] - bb['BB_lower']
    print("Bollinger Bands calculated")  # Debug print

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy['trend_up'] = trend_up.round(2)
    df_copy['trend_down'] = trend_down.round(2)
    df_copy['explosion_line'] = e1.round(2)
    df_copy['dead_zone_line'] = dead_zone.round(2)

    return df_copy[['trend_up', 'trend_down', 'explosion_line', 'dead_zone_line']]


def WaveTrend_Oscillator(df, src, n1=8, n2=12):
    """
    WaveTrend Oscillator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations.
    - n1 (int): Length for the first EMA. Default is 8.
    - n2 (int): Length for the second EMA. Default is 12.

    Call with:
        wt = WaveTrend_Oscillator(df, 'close')
        df['wavetrend'] = wt['wavetrend']

    Returns:
    - pd.DataFrame: DataFrame with 'wavetrend' column.
    """
    df_copy = df.copy()

    src_series = df[src]
    ema_src = EMA(df.assign(src_series=src_series), 'src_series', n1)
    d = EMA(df.assign(diff=np.abs(src_series - ema_src)), 'diff', n1)
    ci = (src_series - ema_src) / (0.015 * d)
    tci = EMA(df.assign(ci=ci), 'ci', n2)
    wavetrend = tci - SMA(df.assign(tci=tci), 'tci', 4)

    df_copy['wavetrend'] = wavetrend.round(2)
    
    return df_copy[['wavetrend']]


def RSI(df, column="close", period=14):
    """
    Relative Strength Index (RSI)

    Call with:
        df['rsi'] = bta.RSI(df, "close", 14)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which RSI is to be calculated. Default is "close".
    - period (int): The period over which RSI is to be calculated. Default is 14.

    Returns:
    - pandas.Series: A series of RSI values.

    Description:
    RSI measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset.
    """
    delta = df[column].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    for i in range(period, len(df)):
        avg_gain[i] = (avg_gain[i-1] * (period - 1) + gain[i]) / period
        avg_loss[i] = (avg_loss[i-1] * (period - 1) + loss[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


# def QQE_Mod(df, rsi_period=6, rsi_smoothing=5, qqe_factor=3, threshold=3, bollinger_length=50, bb_multiplier=0.35):
#     """
#     QQE Mod Indicator

#     Parameters:
#     - df (pandas.DataFrame): Input DataFrame which should contain a 'close' column.
#     - rsi_period (int): Period for RSI calculation. Default is 6.
#     - rsi_smoothing (int): Smoothing period for RSI. Default is 5.
#     - qqe_factor (int): Fast QQE Factor. Default is 3.
#     - threshold (int): Thresh-hold value. Default is 3.
#     - bollinger_length (int): Length for Bollinger Bands calculation. Default is 50.
#     - bb_multiplier (float): Multiplier for Bollinger Bands. Default is 0.35.

#     Call with:
#         qqe_mod = QQE_Mod(df)
#         df['QQE_Line'] = qqe_mod['QQE_Line']
#         df['Histo2'] = qqe_mod['Histo2']
#         df['QQE_Up'] = qqe_mod['QQE_Up']
#         df['QQE_Down'] = qqe_mod['QQE_Down']

#     Returns:
#     - pd.DataFrame: DataFrame with 'QQE_Line', 'Histo2', 'QQE_Up', and 'QQE_Down' columns.
#     """
#     def wilders_ema(series, period):
#         return series.ewm(alpha=1/period, adjust=False).mean()

#     df_copy = df.copy()

#     # First QQE Calculation
#     src = df_copy['close']
#     wilders_period = rsi_period * 2 - 1

#     rsi = RSI(df_copy, column='close', period=rsi_period)
#     rsi_ma = EMA(df_copy.assign(rsi=rsi), column='rsi', period=rsi_smoothing)
#     atr_rsi = abs(rsi_ma.shift(1) - rsi_ma)
#     ma_atr_rsi = wilders_ema(atr_rsi, wilders_period)
#     dar = wilders_ema(ma_atr_rsi, wilders_period) * qqe_factor

#     longband = np.zeros(len(df_copy))
#     shortband = np.zeros(len(df_copy))
#     trend = np.zeros(len(df_copy))

#     delta_fast_atr_rsi = dar
#     rsindex = rsi_ma
#     newshortband = rsindex + delta_fast_atr_rsi
#     newlongband = rsindex - delta_fast_atr_rsi

#     for i in range(1, len(df_copy)):
#         if rsindex.iloc[i - 1] > longband[i - 1] and rsindex.iloc[i] > longband[i - 1]:
#             longband[i] = max(longband[i - 1], newlongband.iloc[i])
#         else:
#             longband[i] = newlongband.iloc[i]

#         if rsindex.iloc[i - 1] < shortband[i - 1] and rsindex.iloc[i] < shortband[i - 1]:
#             shortband[i] = min(shortband[i - 1], newshortband.iloc[i])
#         else:
#             shortband[i] = newshortband.iloc[i]

#         cross_1 = (longband[i - 1] > rsindex.iloc[i]) and (longband[i - 1] <= rsindex.iloc[i - 1])
#         if (rsindex.iloc[i] > shortband[i - 1]):
#             trend[i] = 1
#         elif cross_1:
#             trend[i] = -1
#         else:
#             trend[i] = trend[i - 1]

#     fast_atr_rsi_tl = np.where(trend == 1, longband, shortband)

#     # Bollinger Bands on FastATRRSI TL
#     basis = SMA(pd.DataFrame(fast_atr_rsi_tl - 50), column=0, period=bollinger_length)
#     dev = bb_multiplier * stdev(pd.Series(fast_atr_rsi_tl - 50), bollinger_length)
#     upper = basis + dev
#     lower = basis - dev

#     # Second QQE Calculation
#     rsi_period2 = 6
#     rsi_smoothing2 = 5
#     qqe_factor2 = 1.61
#     threshold2 = 3
#     wilders_period2 = rsi_period2 * 2 - 1

#     rsi2 = RSI(df_copy, column='close', period=rsi_period2)
#     rsi_ma2 = EMA(df_copy.assign(rsi2=rsi2), column='rsi2', period=rsi_smoothing2)
#     atr_rsi2 = abs(rsi_ma2.shift(1) - rsi_ma2)
#     ma_atr_rsi2 = wilders_ema(atr_rsi2, wilders_period2)
#     dar2 = wilders_ema(ma_atr_rsi2, wilders_period2) * qqe_factor2

#     longband2 = np.zeros(len(df_copy))
#     shortband2 = np.zeros(len(df_copy))
#     trend2 = np.zeros(len(df_copy))

#     delta_fast_atr_rsi2 = dar2
#     rsindex2 = rsi_ma2
#     newshortband2 = rsindex2 + delta_fast_atr_rsi2
#     newlongband2 = rsindex2 - delta_fast_atr_rsi2

#     for i in range(1, len(df_copy)):
#         if rsindex2.iloc[i - 1] > longband2[i - 1] and rsindex2.iloc[i] > longband2[i - 1]:
#             longband2[i] = max(longband2[i - 1], newlongband2.iloc[i])
#         else:
#             longband2[i] = newlongband2.iloc[i]

#         if rsindex2.iloc[i - 1] < shortband2[i - 1] and rsindex2.iloc[i] < shortband2[i - 1]:
#             shortband2[i] = min(shortband2[i - 1], newshortband2.iloc[i])
#         else:
#             shortband2[i] = newshortband2.iloc[i]

#         cross_2 = (longband2[i - 1] > rsindex2.iloc[i]) and (longband2[i - 1] <= rsindex2.iloc[i - 1])
#         if (rsindex2.iloc[i] > shortband2[i - 1]):
#             trend2[i] = 1
#         elif cross_2:
#             trend2[i] = -1
#         else:
#             trend2[i] = trend2[i - 1]

#     fast_atr_rsi2_tl = np.where(trend2 == 1, longband2, shortband2)

#     hcolor2 = np.where(rsi_ma2 - 50 > threshold2, 'silver', np.where(rsi_ma2 - 50 < -threshold2, 'silver', np.nan))

#     df_copy['QQE_Line'] = (fast_atr_rsi2_tl - 50).round(2)
#     df_copy['Histo2'] = (rsi_ma2 - 50).round(2)

#     greenbar1 = rsi_ma2 - 50 > threshold2
#     greenbar2 = rsi_ma - 50 > upper

#     redbar1 = rsi_ma2 - 50 < -threshold2
#     redbar2 = rsi_ma - 50 < lower

#     df_copy['QQE_Up'] = np.where(greenbar1 & greenbar2, rsi_ma2 - 50, np.nan).round(2)
#     df_copy['QQE_Down'] = np.where(redbar1 & redbar2, rsi_ma2 - 50, np.nan).round(2)

#     return df_copy[['QQE_Line', 'Histo2', 'QQE_Up', 'QQE_Down']]


def QQE_Mod(df, rsi_period=6, rsi_smoothing=5, qqe_factor=3, threshold=3, bollinger_length=50, bb_multiplier=0.35,
            rsi_period2=6, rsi_smoothing2=5, qqe_factor2=1.61, threshold2=3):
    """
    QQE Mod Indicator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain a 'close' column.
    - rsi_period (int): Period for RSI calculation. Default is 6.
    - rsi_smoothing (int): Smoothing period for RSI. Default is 5.
    - qqe_factor (int): Fast QQE Factor. Default is 3.
    - threshold (int): Threshold value. Default is 3.
    - bollinger_length (int): Length for Bollinger Bands calculation. Default is 50.
    - bb_multiplier (float): Multiplier for Bollinger Bands. Default is 0.35.
    - rsi_period2 (int): Period for the second RSI calculation. Default is 6.
    - rsi_smoothing2 (int): Smoothing period for the second RSI. Default is 5.
    - qqe_factor2 (float): Fast QQE Factor for the second QQE. Default is 1.61.
    - threshold2 (int): Threshold value for the second QQE. Default is 3.

    Call with:
        qqe_mod = QQE_Mod(df)
        df['QQE_Line'] = qqe_mod['QQE_Line']
        df['Histo2'] = qqe_mod['Histo2']
        df['QQE_Up'] = qqe_mod['QQE_Up']
        df['QQE_Down'] = qqe_mod['QQE_Down']

    Returns:
    - pd.DataFrame: DataFrame with 'QQE_Line', 'Histo2', 'QQE_Up', and 'QQE_Down' columns.
    """
    def wilders_ema(series, period):
        return series.ewm(alpha=1/period, adjust=False).mean()

    df_copy = df.copy()

    # First QQE Calculation
    src = df_copy['close']
    wilders_period = rsi_period * 2 - 1

    rsi = RSI(df_copy, column='close', period=rsi_period)
    rsi_ma = EMA(df_copy.assign(rsi=rsi), column='rsi', period=rsi_smoothing)
    atr_rsi = abs(rsi_ma.shift(1) - rsi_ma)
    ma_atr_rsi = wilders_ema(atr_rsi, wilders_period)
    dar = wilders_ema(ma_atr_rsi, wilders_period) * qqe_factor

    longband = np.zeros(len(df_copy))
    shortband = np.zeros(len(df_copy))
    trend = np.zeros(len(df_copy))

    delta_fast_atr_rsi = dar
    rsindex = rsi_ma
    newshortband = rsindex + delta_fast_atr_rsi
    newlongband = rsindex - delta_fast_atr_rsi

    for i in range(1, len(df_copy)):
        if rsindex.iloc[i - 1] > longband[i - 1] and rsindex.iloc[i] > longband[i - 1]:
            longband[i] = max(longband[i - 1], newlongband.iloc[i])
        else:
            longband[i] = newlongband.iloc[i]

        if rsindex.iloc[i - 1] < shortband[i - 1] and rsindex.iloc[i] < shortband[i - 1]:
            shortband[i] = min(shortband[i - 1], newshortband.iloc[i])
        else:
            shortband[i] = newshortband.iloc[i]

        cross_1 = (longband[i - 1] > rsindex.iloc[i]) and (longband[i - 1] <= rsindex.iloc[i - 1])
        if (rsindex.iloc[i] > shortband[i - 1]):
            trend[i] = 1
        elif cross_1:
            trend[i] = -1
        else:
            trend[i] = trend[i - 1]

    fast_atr_rsi_tl = np.where(trend == 1, longband, shortband)

    # Bollinger Bands on FastATRRSI TL
    basis = SMA(pd.DataFrame(fast_atr_rsi_tl - 50), column=0, period=bollinger_length)
    dev = bb_multiplier * stdev(pd.Series(fast_atr_rsi_tl - 50), bollinger_length)
    upper = basis + dev
    lower = basis - dev

    # Second QQE Calculation
    wilders_period2 = rsi_period2 * 2 - 1

    rsi2 = RSI(df_copy, column='close', period=rsi_period2)
    rsi_ma2 = EMA(df_copy.assign(rsi2=rsi2), column='rsi2', period=rsi_smoothing2)
    atr_rsi2 = abs(rsi_ma2.shift(1) - rsi_ma2)
    ma_atr_rsi2 = wilders_ema(atr_rsi2, wilders_period2)
    dar2 = wilders_ema(ma_atr_rsi2, wilders_period2) * qqe_factor2

    longband2 = np.zeros(len(df_copy))
    shortband2 = np.zeros(len(df_copy))
    trend2 = np.zeros(len(df_copy))

    delta_fast_atr_rsi2 = dar2
    rsindex2 = rsi_ma2
    newshortband2 = rsindex2 + delta_fast_atr_rsi2
    newlongband2 = rsindex2 - delta_fast_atr_rsi2

    for i in range(1, len(df_copy)):
        if rsindex2.iloc[i - 1] > longband2[i - 1] and rsindex2.iloc[i] > longband2[i - 1]:
            longband2[i] = max(longband2[i - 1], newlongband2.iloc[i])
        else:
            longband2[i] = newlongband2.iloc[i]

        if rsindex2.iloc[i - 1] < shortband2[i - 1] and rsindex2.iloc[i] < shortband2[i - 1]:
            shortband2[i] = min(shortband2[i - 1], newshortband2.iloc[i])
        else:
            shortband2[i] = newshortband2.iloc[i]

        cross_2 = (longband2[i - 1] > rsindex2.iloc[i]) and (longband2[i - 1] <= rsindex2.iloc[i - 1])
        if (rsindex2.iloc[i] > shortband2[i - 1]):
            trend2[i] = 1
        elif cross_2:
            trend2[i] = -1
        else:
            trend2[i] = trend2[i - 1]

    fast_atr_rsi2_tl = np.where(trend2 == 1, longband2, shortband2)

    hcolor2 = np.where(rsi_ma2 - 50 > threshold2, 'silver', np.where(rsi_ma2 - 50 < -threshold2, 'silver', np.nan))

    df_copy['QQE_Line'] = (fast_atr_rsi2_tl - 50).round(2)
    df_copy['Histo2'] = (rsi_ma2 - 50).round(2)

    greenbar1 = rsi_ma2 - 50 > threshold2
    greenbar2 = rsi_ma - 50 > upper

    redbar1 = rsi_ma2 - 50 < -threshold2
    redbar2 = rsi_ma - 50 < lower

    df_copy['QQE_Up'] = np.where(greenbar1 & greenbar2, rsi_ma2 - 50, np.nan).round(2)
    df_copy['QQE_Down'] = np.where(redbar1 & redbar2, rsi_ma2 - 50, np.nan).round(2)

    return df_copy[['QQE_Line', 'Histo2', 'QQE_Up', 'QQE_Down']]
