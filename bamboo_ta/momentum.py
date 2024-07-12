# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *
from .volatility import *
from .utility import *


def AwesomeOscillator(
    high: pd.Series,
    low: pd.Series,
    window1: int = 5,
    window2: int = 34,
    fillna: bool = False,
) -> pd.Series:
    """Awesome Oscillator

    Call with:
        df['ao'] = bta.AwesomeOscillator(df['high'], df['low'], 5, 34)

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        window1(int): short period.
        window2(int): long period.
        fillna(bool): if True, fill nan values with -50.

    Returns:
        pandas.Series: New feature generated.
    """
    median_price = 0.5 * (high + low)
    min_periods_s = 0 if fillna else window1
    min_periods_l = 0 if fillna else window2
    ao = (
        median_price.rolling(window1, min_periods=min_periods_s).mean()
        - median_price.rolling(window2, min_periods=min_periods_l).mean()
    )
    if fillna:
        ao = ao.fillna(0)
    return ao


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


def Fisher_cg(df, length=20, min_period=10):
    """ 
    Fisher Stochastic Center of Gravity
    
    Original Pinescript by dasanc
    https://tradingview.com/script/5BT3a9mJ-Fisher-Stochastic-Center-of-Gravity/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): Lookback period.
    - min_period (int): Minimum lookback period.

    Call with:
        fisher = bta.Fisher_cg(df)
        df['fisher_cg'] = fisher['fisher_cg']
        df['fisher_sig'] = fisher['fisher_sig']

    Returns:
    - pd.DataFrame: DataFrame with fisher_cg and fisher_sig columns populated.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    df_copy['hl2'] = (df_copy['high'] + df_copy['low']) / 2

    if length < min_period:
        length = min_period

    num = sum((1 + i) * df_copy['hl2'].shift(i) for i in range(length))
    denom = sum(df_copy['hl2'].shift(i) for i in range(length))

    CG = -num / denom + (length + 1) / 2
    MaxCG = CG.rolling(window=length).max()
    MinCG = CG.rolling(window=length).min()

    Value1 = np.where(MaxCG != MinCG, (CG - MinCG) / (MaxCG - MinCG), 0)
    Value2 = (4 * Value1 + 3 * np.roll(Value1, 1) + 2 * np.roll(Value1, 2) + np.roll(Value1, 3)) / 10
    Value3 = 0.5 * np.log((1 + 1.98 * (Value2 - 0.5)) / (1 - 1.98 * (Value2 - 0.5)))

    df_copy['fisher_cg'] = pd.Series(Value3, index=df_copy.index)  # Center of Gravity
    df_copy['fisher_sig'] = df_copy['fisher_cg'].shift(1)  # Signal / Trigger

    return df_copy[['fisher_cg', 'fisher_sig']]


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


def KAMA(
    close: pd.Series,
    window: int = 10,
    pow1: int = 2,
    pow2: int = 30,
    fillna: bool = False,
) -> pd.Series:
    """Kaufman's Adaptive Moving Average (KAMA)

    Moving average designed to account for market noise or volatility. KAMA
    will closely follow prices when the price swings are relatively small and
    the noise is low. KAMA will adjust when the price swings widen and follow
    prices from a greater distance. This trend-following indicator can be
    used to identify the overall trend, time turning points and filter price
    movements.

    Call with:
        df['kama'] = bta.KAMA(df['close'], 10, 2, 30)

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n number of periods for the efficiency ratio.
        pow1(int): number of periods for the fastest EMA constant.
        pow2(int): number of periods for the slowest EMA constant.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    close_values = close.values
    vol = pd.Series(abs(close - np.roll(close, 1)))

    min_periods = 0 if fillna else window
    er_num = abs(close_values - np.roll(close_values, window))
    er_den = vol.rolling(window, min_periods=min_periods).sum()
    efficiency_ratio = np.divide(
        er_num, er_den, out=np.zeros_like(er_num), where=er_den != 0
    )

    smoothing_constant = (
        (
            efficiency_ratio * (2.0 / (pow1 + 1) - 2.0 / (pow2 + 1.0))
            + 2 / (pow2 + 1.0)
        )
        ** 2.0
    ).values

    kama = np.zeros(smoothing_constant.size)
    len_kama = len(kama)
    first_value = True

    for i in range(len_kama):
        if np.isnan(smoothing_constant[i]):
            kama[i] = np.nan
        elif first_value:
            kama[i] = close_values[i]
            first_value = False
        else:
            kama[i] = kama[i - 1] + smoothing_constant[i] * (
                close_values[i] - kama[i - 1]
            )
    
    kama_series = pd.Series(kama, index=close.index)
    if fillna:
        kama_series = kama_series.fillna(close)
    return kama_series


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


def MAStreak(df, period=4, column='close'):
    """
    MA Streak
    Port of: https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/
    
    Call with:
        df['mastreak'] = bta.MAStreak(df, period=4, column='close')

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    period (int): Period for the ZEMA calculation. Default is 4.
    column (str): The column name on which the ZEMA is to be applied. Default is "close".

    Returns:
    pd.Series: Series of MA Streak values.
    """
    df_copy = df.copy()

    avgval = ZEMA(df_copy, period, column)
    arr = np.diff(avgval)
    pos = np.clip(arr, 0, 1).astype(bool).cumsum()
    neg = np.clip(arr, -1, 0).astype(bool).cumsum()
    streak = np.where(arr >= 0, pos - np.maximum.accumulate(np.where(arr <= 0, pos, 0)),
                      -neg + np.maximum.accumulate(np.where(arr >= 0, neg, 0)))
    
    return SameLength(df_copy['close'], streak)


def PPO(
    df: pd.DataFrame,
    close_col: str = 'close',
    window_slow: int = 26,
    window_fast: int = 12,
    window_sign: int = 9,
    fillna: bool = False
) -> pd.DataFrame:
    """
    Percentage Price Oscillator (PPO) Combined Function

    This function calculates and returns the PPO, PPO Signal, and PPO Histogram values.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the close column.
    - close_col (str): Name of the column containing close price data.
    - window_slow (int): n period long-term.
    - window_fast (int): n period short-term.
    - window_sign (int): n period to signal.
    - fillna (bool): if True, fill nan values.

    Call with:
        ppo = bta.PPO(df)
        df['ppo'] = ppo['ppo']
        df['ppo_signal'] = ppo['ppo_signal']
        df['ppo_hist'] = ppo['ppo_hist']

    Returns:
    - pd.DataFrame: DataFrame with columns ['ppo', 'ppo_signal', 'ppo_hist'].
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    if close_col not in df.columns:
        raise KeyError(f"DataFrame must contain '{close_col}' column")

    close = df_copy[close_col]

    # Calculate EMA
    emafast = close.ewm(span=window_fast, adjust=False).mean()
    emaslow = close.ewm(span=window_slow, adjust=False).mean()
    ppo = ((emafast - emaslow) / emaslow) * 100

    ppo_signal = ppo.ewm(span=window_sign, adjust=False).mean()
    ppo_hist = ppo - ppo_signal

    if fillna:
        ppo = ppo.fillna(0)
        ppo_signal = ppo_signal.fillna(0)
        ppo_hist = ppo_hist.fillna(0)

    df_copy['ppo'] = ppo
    df_copy['ppo_signal'] = ppo_signal
    df_copy['ppo_hist'] = ppo_hist

    return df_copy[['ppo', 'ppo_signal', 'ppo_hist']]


def PVO(
    df: pd.DataFrame,
    volume_col: str = 'volume',
    window_slow: int = 26,
    window_fast: int = 12,
    window_sign: int = 9,
    fillna: bool = False
) -> pd.DataFrame:
    """
    Percentage Volume Oscillator (PVO) Combined Function
    
    This function calculates and returns the PVO, PVO Signal, and PVO Histogram values.

    Call with:
        pvo = bta.PVO(df)
        df['pvo'] = pvo['pvo']
        df['pvo_signal'] = pvo['pvo_signal']
        df['pvo_hist'] = pvo['pvo_hist']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the volume column.
    - volume_col (str): Name of the column containing volume data.
    - window_slow (int): n period long-term.
    - window_fast (int): n period short-term.
    - window_sign (int): n period to signal.
    - fillna (bool): if True, fill nan values.

    Returns:
    - pd.DataFrame: DataFrame with columns ['pvo', 'pvo_signal', 'pvo_hist'].
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    if volume_col not in df.columns:
        raise KeyError(f"DataFrame must contain '{volume_col}' column")

    volume = df_copy[volume_col]

    # Calculate EMA
    emafast = volume.ewm(span=window_fast, adjust=False).mean()
    emaslow = volume.ewm(span=window_slow, adjust=False).mean()
    pvo = ((emafast - emaslow) / emaslow) * 100

    pvo_signal = pvo.ewm(span=window_sign, adjust=False).mean()
    pvo_hist = pvo - pvo_signal

    if fillna:
        pvo = pvo.fillna(0)
        pvo_signal = pvo_signal.fillna(0)
        pvo_hist = pvo_hist.fillna(0)

    df_copy['pvo'] = pvo
    df_copy['pvo_signal'] = pvo_signal
    df_copy['pvo_hist'] = pvo_hist

    return df_copy[['pvo', 'pvo_signal', 'pvo_hist']]


def RMI(df, length=20, mom=5):
    """
    Relative Momentum Index (RMI)
    Source: https://github.com/freqtrade/technical/blob/master/technical/indicators/indicators.py#L912

    Call with:
        df['rmi'] = bta.RMI(df, length=20, mom=5)

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    length (int): Period for the EMA calculation. Default is 20.
    mom (int): Momentum period. Default is 5.

    Returns:
    pd.Series: Series of RMI values.
    """
    df_copy = df.copy()

    df_copy['maxup'] = (df_copy['close'] - df_copy['close'].shift(mom)).clip(lower=0)
    df_copy['maxdown'] = (df_copy['close'].shift(mom) - df_copy['close']).clip(lower=0)
    df_copy.fillna(0, inplace=True)
    df_copy["emaInc"] = EMA(df_copy, column='maxup', period=length)
    df_copy["emaDec"] = EMA(df_copy, column='maxdown', period=length)
    df_copy['RMI'] = np.where(df_copy['emaDec'] == 0, 0, 100 - 100 / (1 + df_copy["emaInc"] / df_copy["emaDec"]))
    
    return df_copy['RMI']


def ROC(df, column='close', period=21):
    """
    Rate of Change (ROC)

    Call with:
        df['roc'] = bta.ROC(df, column='close', period=21)

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    column (str): The column name on which the ROC is to be applied. Default is "close".
    period (int): Period for the ROC calculation. Default is 21.

    Returns:
    pd.Series: Series of ROC values.
    """
    df_copy = df.copy()

    df_copy['roc'] = df_copy[column].diff(period) / df_copy[column].shift(period) * 100
    
    return df_copy['roc']


def SROC(df, roclen=21, emalen=13, smooth=21):
    """
    Smoothed Rate of Change (SROC)

    Call with:
        df['sroc'] = bta.SROC(df, roclen=21, emalen=13, smooth=21)

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    roclen (int): Period for the ROC calculation. Default is 21.
    emalen (int): Period for the EMA calculation. Default is 13.
    smooth (int): Smoothing period for the ROC calculation. Default is 21.

    Returns:
    pd.Series: Series of SROC values.
    """
    df_copy = df.copy()

    roc = ROC(df_copy, column='close', period=roclen)
    ema = EMA(df_copy, column='close', period=emalen)
    sroc = ROC(pd.DataFrame(ema), column='close', period=smooth)
    
    return sroc


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

    # print("DataFrame columns:", df.columns)  # Debug print
    # print("First few rows of the DataFrame:\n", df.head())  # Debug print

    # Calculate DEAD_ZONE
    dead_zone = RMA(TR(df), 100) * 3.7
    # print("DEAD_ZONE calculated")  # Debug print

    # Calculate MACD
    macd_fast = EMA(df, 'close', fast_length)
    macd_slow = EMA(df, 'close', slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity
    # print("MACD and t1 calculated")  # Debug print

    # Calculate Bollinger Bands
    bb = BollingerBands(df, column='close', period=channel_length, std_dev=mult)
    e1 = bb['BB_upper'] - bb['BB_lower']
    # print("Bollinger Bands calculated")  # Debug print

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy['trend_up'] = trend_up.round(2)
    df_copy['trend_down'] = trend_down.round(2)
    df_copy['explosion_line'] = e1.round(2)
    df_copy['dead_zone_line'] = dead_zone.round(2)

    return df_copy[['trend_up', 'trend_down', 'explosion_line', 'dead_zone_line']]


def WaveTrend(df, chlen=10, avg=21, smalen=4):
    """
    WaveTrend Oscillator by LazyBear
    https://www.tradingview.com/script/2KE8wTuF-Indicator-WaveTrend-Oscillator-WT/

    Call with:
        wt1, wt2 = bta.WaveTrend(df, chlen=10, avg=21, smalen=4)
        df['wt1'] = wt1
        df['wt2'] = wt2

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    chlen (int): Channel length for the EMA calculation. Default is 10.
    avg (int): Average period for the EMA calculation. Default is 21.
    smalen (int): Period for the SMA calculation. Default is 4.

    Returns:
    tuple: WaveTrend 1 and WaveTrend 2 series.
    """
    df_copy = df.copy()

    df_copy['hlc3'] = (df_copy['high'] + df_copy['low'] + df_copy['close']) / 3
    df_copy['esa'] = EMA(df_copy, column='hlc3', period=chlen)
    df_copy['abs_diff'] = (df_copy['hlc3'] - df_copy['esa']).abs()
    df_copy['d'] = EMA(df_copy, column='abs_diff', period=chlen)
    df_copy['ci'] = (df_copy['hlc3'] - df_copy['esa']) / (0.015 * df_copy['d'])
    df_copy['tci'] = EMA(df_copy, column='ci', period=avg)
    df_copy['wt1'] = df_copy['tci']
    df_copy['wt2'] = SMA(df_copy, column='wt1', period=smalen)

    # Return only the calculated columns
    return df_copy['wt1'], df_copy['wt2']


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
    dev = bb_multiplier * STDEV(pd.Series(fast_atr_rsi_tl - 50), bollinger_length)
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


def ROC(close: pd.Series, window: int = 12, fillna: bool = False) -> pd.Series:
    """Rate of Change (ROC)

    The Rate-of-Change (ROC) indicator, which is also referred to as simply
    Momentum, is a pure momentum oscillator that measures the percent change in
    price from one period to the next. The ROC calculation compares the current
    price with the price “n” periods ago. The plot forms an oscillator that
    fluctuates above and below the zero line as the Rate-of-Change moves from
    positive to negative. As a momentum oscillator, ROC signals include
    centerline crossovers, divergences and overbought-oversold readings.
    Divergences fail to foreshadow reversals more often than not, so this
    article will forgo a detailed discussion on them. Even though centerline
    crossovers are prone to whipsaw, especially short-term, these crossovers
    can be used to identify the overall trend. Identifying overbought or
    oversold extremes comes naturally to the Rate-of-Change oscillator.

    Call with:
        df['roc'] = bta.ROC(df['close'], 12)
    
    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n periods.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    roc = ((close - close.shift(window)) / close.shift(window)) * 100
    if fillna:
        roc = roc.fillna(0)
    return roc


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


def SMI_Momentum(df, k_length=9, d_length=3):
    """ 
    The Stochastic Momentum Index (SMI) Indicator
    
    The Stochastic Momentum Index (SMI) Indicator was developed by 
    William Blau in 1993 and is considered to be a momentum indicator 
    that can help identify trend reversal points

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - k_length (int): Period for %K.
    - d_length (int): Period for %D.

    Call with:
        smi = bta.SMI_Momentum(df)
        df['smi'] = smi['smi']

    Returns:
    - pd.DataFrame: DataFrame with smi column populated.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    ll = df_copy['low'].rolling(window=k_length).min()
    hh = df_copy['high'].rolling(window=k_length).max()

    diff = hh - ll
    rdiff = df_copy['close'] - (hh + ll) / 2

    avgrel = rdiff.ewm(span=d_length).mean().ewm(span=d_length).mean()
    avgdiff = diff.ewm(span=d_length).mean().ewm(span=d_length).mean()

    df_copy['smi'] = np.where(avgdiff != 0, (avgrel / (avgdiff / 2) * 100), 0)
    
    return df_copy[['smi']]


def StochRSI(
    df: pd.DataFrame,
    close_col: str = 'close',
    window: int = 14,
    smooth1: int = 3,
    smooth2: int = 3,
    fillna: bool = False
) -> pd.DataFrame:
    """
    Stochastic RSI

    Call with:
        stoch_rsi = bta.StochRSI(df, 'close', 14, 3, 3)
        df['stoch_rsi'] = stoch_rsi['stoch_rsi']
        df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
        df['stoch_rsi_d'] = stoch_rsi['stoch_rsi_d']

    Args:
        df (pd.DataFrame): Input DataFrame which should contain the close column.
        close_col (str): Name of the column containing close price data.
        window (int): Lookback period for RSI (default is 14).
        smooth1 (int): Smoothing period for %K line (default is 3).
        smooth2 (int): Smoothing period for %D line (default is 3).
        fillna (bool): If True, fill nan values (default is False).

    Returns:
        pd.DataFrame: DataFrame with columns ['stoch_rsi', 'stoch_rsi_k', 'stoch_rsi_d'].
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required column
    if close_col not in df.columns:
        raise KeyError(f"DataFrame must contain '{close_col}' column")

    rsi = RSI(df, close_col, window)
    lowest_low_rsi = rsi.rolling(window).min()
    highest_high_rsi = rsi.rolling(window).max()
    stoch_rsi = (rsi - lowest_low_rsi) / (highest_high_rsi - lowest_low_rsi)
    stoch_rsi_k = stoch_rsi.rolling(smooth1).mean()
    stoch_rsi_d = stoch_rsi_k.rolling(smooth2).mean()

    if fillna:
        stoch_rsi = stoch_rsi.fillna(0)
        stoch_rsi_k = stoch_rsi_k.fillna(0)
        stoch_rsi_d = stoch_rsi_d.fillna(0)

    df_copy['stoch_rsi'] = stoch_rsi
    df_copy['stoch_rsi_k'] = stoch_rsi_k
    df_copy['stoch_rsi_d'] = stoch_rsi_d

    return df_copy[['stoch_rsi', 'stoch_rsi_k', 'stoch_rsi_d']]


def TSI(close: pd.Series, window_slow: int = 25, window_fast: int = 13, fillna: bool = False) -> pd.Series:
    """True Strength Index (TSI)

    Shows both trend direction and overbought/oversold conditions.

    Call with:
        df['tsi'] = bta.TSI(df['close'], 25, 13)

    Args:
        close(pandas.Series): dataset 'Close' column.
        window_slow(int): high period.
        window_fast(int): low period.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    diff_close = close - close.shift(1)
    min_periods_r = 0 if fillna else window_slow
    min_periods_s = 0 if fillna else window_fast
    smoothed = (
        diff_close.ewm(span=window_slow, min_periods=min_periods_r, adjust=False)
        .mean()
        .ewm(span=window_fast, min_periods=min_periods_s, adjust=False)
        .mean()
    )
    smoothed_abs = (
        abs(diff_close)
        .ewm(span=window_slow, min_periods=min_periods_r, adjust=False)
        .mean()
        .ewm(span=window_fast, min_periods=min_periods_s, adjust=False)
        .mean()
    )
    tsi = smoothed / smoothed_abs
    tsi *= 100
    if fillna:
        tsi = tsi.fillna(0)
    return tsi


def UltimateOscillator(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    window1: int = 7,
    window2: int = 14,
    window3: int = 28,
    weight1: float = 4.0,
    weight2: float = 2.0,
    weight3: float = 1.0,
    fillna: bool = False,
) -> pd.Series:
    """Ultimate Oscillator

    Call with:
        df['uo'] = bta.UltimateOscillator(df['high'], df['low'], df['close'], 7, 14, 28)

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window1(int): short period.
        window2(int): medium period.
        window3(int): long period.
        weight1(float): weight of short BP average for UO.
        weight2(float): weight of medium BP average for UO.
        weight3(float): weight of long BP average for UO.
        fillna(bool): if True, fill nan values with 50.

    Returns:
        pandas.Series: New feature generated.
    """
    close_shift = close.shift(1)
    true_range = IndicatorMixin._true_range(high, low, close_shift)
    buying_pressure = close - pd.DataFrame({"low": low, "close": close_shift}).min(axis=1, skipna=False)
    min_periods_s = 0 if fillna else window1
    min_periods_m = 0 if fillna else window2
    min_periods_l = 0 if fillna else window3
    avg_s = (buying_pressure.rolling(window1, min_periods=min_periods_s).sum()
             / true_range.rolling(window1, min_periods=min_periods_s).sum())
    avg_m = (buying_pressure.rolling(window2, min_periods=min_periods_m).sum()
             / true_range.rolling(window2, min_periods=min_periods_m).sum())
    avg_l = (buying_pressure.rolling(window3, min_periods=min_periods_l).sum()
             / true_range.rolling(window3, min_periods=min_periods_l).sum())
    uo = 100.0 * ((weight1 * avg_s) + (weight2 * avg_m) + (weight3 * avg_l)) / (weight1 + weight2 + weight3)
    if fillna:
        uo = uo.fillna(50)
    return uo

def StochasticsOscillator(
    df: pd.DataFrame,
    high_col: str = 'high',
    low_col: str = 'low',
    close_col: str = 'close',
    window: int = 14,
    smooth_window: int = 3,
    fillna: bool = False,
) -> pd.DataFrame:
    """
    Stochastic Oscillator, Stochastic Signal, and Histogram Combined.

    Call with:
        stoch = bta.StochasticsOscillator(df, 'high', 'low', 'close', 14, 3)
        df['stoch'] = stoch['stoch']
        df['stoch_signal'] = stoch['stoch_signal']
        df['stoch_hist'] = stoch['stoch_hist']

    Args:
        df(pandas.DataFrame): Input DataFrame.
        high_col(str): Column name for 'High' prices.
        low_col(str): Column name for 'Low' prices.
        close_col(str): Column name for 'Close' prices.
        window(int): Lookback period for stochastic calculation.
        smooth_window(int): Lookback period for signal calculation.
        fillna(bool): If True, fill nan values.

    Returns:
        pandas.DataFrame: DataFrame with stoch, stoch_signal, and stoch_hist columns.
    """
    high = df[high_col]
    low = df[low_col]
    close = df[close_col]

    min_periods = 0 if fillna else window
    smin = low.rolling(window, min_periods=min_periods).min()
    smax = high.rolling(window, min_periods=min_periods).max()
    stoch_k = 100 * (close - smin) / (smax - smin)
    if fillna:
        stoch_k = stoch_k.fillna(50)

    min_periods = 0 if fillna else smooth_window
    stoch_d = stoch_k.rolling(smooth_window, min_periods=min_periods).mean()
    if fillna:
        stoch_d = stoch_d.fillna(50)

    stoch_hist = stoch_k - stoch_d
    if fillna:
        stoch_hist = stoch_hist.fillna(0)

    return pd.DataFrame({
        'stoch': stoch_k,
        'stoch_signal': stoch_d,
        'stoch_hist': stoch_hist
    })


def WilliamsR(
    high: pd.Series,
    low: pd.Series,
    close: pd.Series,
    lbp: int = 14,
    fillna: bool = False,
) -> pd.Series:
    """Williams %R

    Call with:
        df['williams_r'] = bta.WilliamsR(df['high'], df['low'], df['close'], 14)
    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        lbp(int): lookback period.
        fillna(bool): if True, fill nan values with -50.

    Returns:
        pandas.Series: New feature generated.
    """
    min_periods = 0 if fillna else lbp
    highest_high = high.rolling(lbp, min_periods=min_periods).max()
    lowest_low = low.rolling(lbp, min_periods=min_periods).min()
    wr = -100 * (highest_high - close) / (highest_high - lowest_low)
    if fillna:
        wr = wr.fillna(-50)
    return wr

