# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *
from .volatility import *
from .utility import *


def AwesomeOscillator(df: pd.DataFrame, high_col: str = 'high', low_col: str = 'low', window1: int = 5, window2: int = 34, fillna: bool = False) -> pd.DataFrame:
    """
    Awesome Oscillator (AO)

    The Awesome Oscillator is a momentum indicator used to measure market momentum.
    It is calculated by subtracting a 34-period simple moving average (SMA) of the
    median price from a 5-period SMA of the median price.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing 'high' and 'low' columns.
    - high_col (str): The name of the 'high' column. Default is 'high'.
    - low_col (str): The name of the 'low' column. Default is 'low'.
    - window1 (int, optional): Short period. Default is 5.
    - window2 (int, optional): Long period. Default is 34.
    - fillna (bool, optional): If True, fill nan values with 0. Default is False.

    Call with:
        df['ao'] = bta.AwesomeOscillator(df, 'high', 'low', 5, 34)['ao']

    Returns:
    - pd.DataFrame: DataFrame with the 'ao' column.
    """
    df_copy = df.copy()

    median_price = 0.5 * (df_copy[high_col] + df_copy[low_col])
    min_periods_s = 0 if fillna else window1
    min_periods_l = 0 if fillna else window2

    df_copy['ao'] = (
        median_price.rolling(window1, min_periods=min_periods_s).mean()
        - median_price.rolling(window2, min_periods=min_periods_l).mean()
    )
    if fillna:
        df_copy['ao'] = df_copy['ao'].fillna(0)

    df_copy['ao'] = df_copy['ao'].round(2)
    
    return df_copy[['ao']]


def ChandeMomentumOscillator(df, length: int = 14) -> pd.DataFrame:
    """
    Chande Momentum Oscillator (CMO)

    The Chande Momentum Oscillator (CMO) is a technical momentum indicator developed by Tushar Chande. 
    It measures the amount that an asset's price has changed over a specified period of time.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Length for the CMO calculation. Default is 14.

    Call with:
        df['cmo'] = bta.ChandeMomentumOscillator(df)

    For Signal line:
        df['cmo_signal'] = df['cmo'].rolling(window=10).mean().round(2)  # Using SMA for signal

    Returns:
    - pd.DataFrame: DataFrame with 'cmo' column.
    """
    df_copy = df.copy()

    mom = df['close'].diff()
    pos_mom = mom.where(mom > 0, 0)
    neg_mom = -mom.where(mom < 0, 0)
    sm1 = pos_mom.rolling(window=length).sum()
    sm2 = neg_mom.rolling(window=length).sum()
    df_copy['cmo'] = 100 * (sm1 - sm2) / (sm1 + sm2)

    df_copy['cmo'] = df_copy['cmo'].round(2)
    return df_copy[['cmo']]


def ElliottWaveOscillator(df, column: str = 'close', sma1_period: int = 5, sma2_period: int = 35) -> pd.DataFrame:
    """
    Elliott Wave Oscillator (EWO)

    The Elliott Wave Oscillator (EWO) is a specific tool to help you identify the trend and the overall market pattern to assist in finding future trading opportunities.
    It is derived by calculating the difference between a short and long period simple moving average, then normalizing the result with the close price.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EWO is to be calculated. Default is "close".
    - sma1_period (int): The period for the shorter SMA used in EWO calculation. Default is 5.
    - sma2_period (int): The period for the longer SMA used in EWO calculation. Default is 35.

    Call with:
        df['ewo'] = bta.ElliottWaveOscillator(df, "close", 5, 35)

    Returns:
    - pd.DataFrame: DataFrame with 'ewo' column.
    """
    df_copy = df.copy()

    sma1 = df[column].rolling(window=sma1_period).mean()
    sma2 = df[column].rolling(window=sma2_period).mean()
    df_copy['ewo'] = ((sma1 - sma2) / df[column] * 100).round(2)

    return df_copy[['ewo']]


def FisherCenterOfGravity(df, length: str = 20, min_period: str = 10) -> pd.DataFrame:
    """
    Fisher Stochastic Center of Gravity

    Original Pinescript by dasanc
    https://tradingview.com/script/5BT3a9mJ-Fisher-Stochastic-Center-of-Gravity/

    The Fisher Stochastic Center of Gravity is an indicator that aims to identify the center of gravity of the market.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): Lookback period. Default is 20.
    - min_period (int): Minimum lookback period. Default is 10.

    Call with:
        fisher = bta.FisherCenterOfGravity(df)
        df['fisher_cg'] = fisher['fisher_cg']
        df['fisher_sig'] = fisher['fisher_sig']

    Returns:
    - pd.DataFrame: DataFrame with 'fisher_cg' and 'fisher_sig' columns populated.
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

    cg = -num / denom + (length + 1) / 2
    max_cg = cg.rolling(window=length).max()
    min_cg = cg.rolling(window=length).min()

    value1 = np.where(max_cg != min_cg, (cg - min_cg) / (max_cg - min_cg), 0)
    value2 = (4 * value1 + 3 * np.roll(value1, 1) + 2 * np.roll(value1, 2) + np.roll(value1, 3)) / 10
    value3 = 0.5 * np.log((1 + 1.98 * (value2 - 0.5)) / (1 - 1.98 * (value2 - 0.5)))

    df_copy['fisher_cg'] = pd.Series(value3, index=df_copy.index).round(2)  # Center of Gravity
    df_copy['fisher_sig'] = df_copy['fisher_cg'].shift(1).round(2)  # Signal / Trigger

    return df_copy[['fisher_cg', 'fisher_sig']]


def InverseFisherTransform(df, column: str = 'close', rsi_length: int = 14, rsi_smoothing: int = 9) -> pd.DataFrame:
    """
    Inverse Fisher Transform

    The Inverse Fisher Transform is a technical indicator used to amplify price movements and identify potential buy and sell signals.
    It applies an inverse Fisher transform to a smoothed RSI to highlight changes in price momentum.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - column (str): Source column to calculate the indicator. Default is 'close'.
    - rsi_length (int): Length for the RSI calculation. Default is 10.
    - rsi_smoothing (int): Length for the RSI smoothing (EMA). Default is 5.
    - e_value (float): E value for the inverse fisher transform. Default is 2.71.

    Call with:
        df['ift'] = bta.InverseFisherTransform(df)['ift']

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
    rsi_values = RelativeStrengthIndex(df, column=column, period=rsi_length)
    
    # Smooth RSI values with EMA
    rsi_ema_values = EMA(df.assign(rsi_values=rsi_values), 'rsi_values', rsi_smoothing)
    
    # Apply Inverse Fisher Transform
    inv_fisher = (np.exp(2.0 * (rsi_ema_values - 50) * 0.1) - 1) / (np.exp(2.0 * (rsi_ema_values - 50) * 0.1) + 1)

    df_copy['ift'] = inv_fisher.round(2)
    
    return df_copy[['ift']]


def KaufmansAdaptiveMovingAverage(
    df: pd.DataFrame,
    close_col: str = 'close',
    window: int = 14,
    pow1: int = 2,
    pow2: int = 30,
    fillna: bool = False,
) -> pd.DataFrame:
    """
    Kaufman's Adaptive Moving Average (KAMA)

    Moving average designed to account for market noise or volatility. KAMA
    will closely follow prices when the price swings are relatively small and
    the noise is low. KAMA will adjust when the price swings widen and follow
    prices from a greater distance. This trend-following indicator can be
    used to identify the overall trend, time turning points and filter price
    movements.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - close_col (str): Column name for the close prices. Default is 'close'.
    - window (int): Number of periods for the efficiency ratio. Default is 10.
    - pow1 (int): Number of periods for the fastest EMA constant. Default is 2.
    - pow2 (int): Number of periods for the slowest EMA constant. Default is 30.
    - fillna (bool): If True, fill nan values with the close prices. Default is False.

    Call with:
        df['kama'] = bta.KaufmansAdaptiveMovingAverage(df)['kama']

    Returns:
    - pd.DataFrame: DataFrame with 'kama' column.
    """
    close = df[close_col]
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
    
    kama_series = pd.Series(kama, index=close.index).round(2)
    if fillna:
        kama_series = kama_series.fillna(close)

    df_copy = df.copy()
    df_copy['kama'] = kama_series

    return df_copy[['kama']]


def MACD(df, column: str = 'close', short_window: int = 12, long_window: int = 26, signal_window: str = 9) -> pd.DataFrame:
    """
    Moving Average Convergence Divergence (MACD)

    MACD is a trend-following momentum indicator that shows the relationship between two moving averages of a security’s price.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which MACD is to be calculated. Default is "close".
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - signal_window (int): The signal line period for EMA. Default is 9.

    Call with:
        macd_result = bta.MACD(df, "close", 12, 26, 9)
        df['macd'] = macd_result['macd']
        df['macd_signal'] = macd_result['macd_signal']
        df['macd_histogram'] = macd_result['macd_histogram']

    Returns:
    - pd.DataFrame: DataFrame with 'macd', 'macd_signal', and 'macd_histogram' columns.
    """
    short_ema = EMA(df, column=column, period=short_window)
    long_ema = EMA(df, column=column, period=long_window)
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_window, adjust=False).mean()
    histogram = macd - signal

    df_copy = df.copy()
    df_copy['macd'] = macd.round(2)
    df_copy['macd_signal'] = signal.round(2)
    df_copy['macd_histogram'] = histogram.round(2)

    return df_copy[['macd', 'macd_signal', 'macd_histogram']]


def MACDLeader(df: pd.DataFrame, src: str = 'close', fast_length: int = 12, slow_length: int = 26, signal_length: int = 9) -> pd.DataFrame:
    """
    MACD Leader

    The MACD Leader is a variation of the standard MACD that aims to provide an earlier signal by using a different calculation method.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - fast_length (int): Length for the fast EMA. Default is 12.
    - slow_length (int): Length for the slow EMA. Default is 26.
    - signal_length (int): Length for the signal EMA. Default is 9.

    Call with:
        df['macd_leader'] = bta.MACDLeader(df, 'close')['macd_leader']

    Returns:
    - pd.DataFrame: DataFrame with 'macd_leader' column.
    """
    df_copy = df.copy()
    src_series = df[src]

    sema = EMA(df, column=src, period=fast_length)['ema']
    lema = EMA(df, column=src, period=slow_length)['ema']
    diff_sema = src_series - sema
    diff_lema = src_series - lema
    i1 = sema + EMA(df.assign(diff=diff_sema), column='diff', period=fast_length)['ema']
    i2 = lema + EMA(df.assign(diff=diff_lema), column='diff', period=slow_length)['ema']
    macd_leader = ((i1 - i2) / 10) * 10

    df_copy['macd_leader'] = macd_leader.round(2)
    
    return df_copy[['macd_leader']]


def MAStreak(df: pd.DataFrame, period: int = 10, column: str = 'close') -> pd.DataFrame:
    """
    MA Streak

    Port of: https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/

    The MA Streak indicator shows the length of consecutive periods where the moving average is increasing or decreasing.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - period (int): Period for the ZEMA calculation. Default is 10.
    - column (str): The column name on which the ZEMA is to be applied. Default is "close".

    Call with:
        df['mastreak'] = bta.MAStreak(df, period=4, column='close')['mastreak']

    Returns:
    - pd.DataFrame: DataFrame with 'mastreak' column.
    """
    df_copy = df.copy()

    avgval = ZEMA(df_copy, column=column, period=period)['zema']
    arr = np.diff(avgval)
    pos = np.clip(arr, 0, 1).astype(bool).cumsum()
    neg = np.clip(arr, -1, 0).astype(bool).cumsum()
    streak = np.where(arr >= 0, pos - np.maximum.accumulate(np.where(arr <= 0, pos, 0)),
                      -neg + np.maximum.accumulate(np.where(arr >= 0, neg, 0)))

    streak_series = SameLength(df_copy['close'], streak)
    df_copy['mastreak'] = streak_series.round(2)
    
    return df_copy[['mastreak']]


def PercentagePriceOscillator(
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
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window_slow (int): n period long-term. Default is 26.
    - window_fast (int): n period short-term. Default is 12.
    - window_sign (int): n period to signal. Default is 9.
    - fillna (bool): if True, fill nan values. Default is False.

    Call with:
        ppo = bta.PercentagePriceOscillator(df)
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

    df_copy['ppo'] = ppo.round(2)
    df_copy['ppo_signal'] = ppo_signal.round(2)
    df_copy['ppo_hist'] = ppo_hist.round(2)

    return df_copy[['ppo', 'ppo_signal', 'ppo_hist']]


def PercentageVolumeOscillator(
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

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the volume column.
    - volume_col (str): Name of the column containing volume data. Default is 'volume'.
    - window_slow (int): n period long-term. Default is 26.
    - window_fast (int): n period short-term. Default is 12.
    - window_sign (int): n period to signal. Default is 9.
    - fillna (bool): if True, fill nan values. Default is False.

    Call with:
        pvo = bta.PercentageVolumeOscillator(df)
        df['pvo'] = pvo['pvo']
        df['pvo_signal'] = pvo['pvo_signal']
        df['pvo_hist'] = pvo['pvo_hist']

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

    df_copy['pvo'] = pvo.round(2)
    df_copy['pvo_signal'] = pvo_signal.round(2)
    df_copy['pvo_hist'] = pvo_hist.round(2)

    return df_copy[['pvo', 'pvo_signal', 'pvo_hist']]


def RelativeMomentumIndex(df, length: int = 20, mom: int = 5) -> pd.DataFrame:
    """
    Relative Momentum Index (RMI)

    The Relative Momentum Index (RMI) is an oscillator that applies the RSI formula to momentum rather than price.

    Source: https://www.tradingview.com/script/DdT7MmPa/ and https://github.com/freqtrade/technical/blob/master/technical/indicators/indicators.py#L912  

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - length (int): Period for the EMA calculation. Default is 20.
    - mom (int): Momentum period. Default is 5.

    Call with:
        df['rmi'] = bta.RelativeMomentumIndex(df, length=20, mom=5)['rmi']

    Returns:
    - pd.DataFrame: DataFrame with 'rmi' column.
    """
    df_copy = df.copy()

    df_copy['maxup'] = (df_copy['close'] - df_copy['close'].shift(mom)).clip(lower=0)
    df_copy['maxdown'] = (df_copy['close'].shift(mom) - df_copy['close']).clip(lower=0)
    df_copy.fillna(0, inplace=True)
    df_copy["ema_inc"] = EMA(df_copy, column='maxup', period=length)
    df_copy["ema_dec"] = EMA(df_copy, column='maxdown', period=length)
    df_copy['rmi'] = np.where(df_copy['ema_dec'] == 0, 0, 100 - 100 / (1 + df_copy["ema_inc"] / df_copy["ema_dec"]))

    df_copy['rmi'] = df_copy['rmi'].round(2)
    
    return df_copy[['rmi']]


def RateOfChange(df, column: str = 'close', period: int = 21) -> pd.DataFrame:
    """
    Rate of Change (ROC)

    The Rate of Change (ROC) is a momentum oscillator that measures the percentage change in price between the current price and the price n periods ago.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the ROC is to be applied. Default is 'close'.
    - period (int): Period for the ROC calculation. Default is 21.

    Call with:
        df['roc'] = bta.RateOfChange(df, column='close', period=21)['roc']

    Returns:
    - pd.DataFrame: DataFrame with 'roc' column.
    """
    df_copy = df.copy()

    df_copy['roc'] = df_copy[column].diff(period) / df_copy[column].shift(period) * 100
    df_copy['roc'] = df_copy['roc'].round(2)
    
    return df_copy[['roc']]


def SmoothedRateOfChange(df, roclen: int = 21, emalen: int = 13, smooth: int = 21) -> pd.DataFrame:
    """
    Smoothed Rate of Change (SROC)

    The Smoothed Rate of Change (SROC) is a momentum oscillator that applies an exponential moving average (EMA) to the Rate of Change (ROC) to smooth out short-term fluctuations.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - roclen (int): Period for the ROC calculation. Default is 21.
    - emalen (int): Period for the EMA calculation. Default is 13.
    - smooth (int): Smoothing period for the ROC calculation. Default is 21.

    Call with:
        df['sroc'] = bta.SmoothedRateOfChange(df, roclen=21, emalen=13, smooth=21)['sroc']

    Returns:
    - pd.DataFrame: DataFrame with 'sroc' column.
    """
    df_copy = df.copy()

    # Calculate ROC
    roc = df_copy['close'].diff(roclen) / df_copy['close'].shift(roclen) * 100

    # Calculate EMA of the close price
    ema = df_copy['close'].ewm(span=emalen, adjust=False).mean()

    # Calculate SROC
    sroc = ema.diff(smooth) / ema.shift(smooth) * 100

    df_copy['sroc'] = sroc.round(2)
    
    return df_copy[['sroc']]


def WaddahAttarExplosion(df, sensitivity: int = 150, fast_length: int = 20, slow_length: int = 40, channel_length: int = 20, mult: float = 2.0) -> pd.DataFrame:
    """
    Waddah Attar Explosion Indicator

    The Waddah Attar Explosion indicator is used to identify potential breakout opportunities by combining the MACD and Bollinger Bands.

    Inspired by: https://www.tradingview.com/script/d9IjcYyS-Waddah-Attar-Explosion-V2-SHK/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        wae = bta.WaddahAttarExplosion(df)
        df['trend_up'] = wae['trend_up']
        df['trend_down'] = wae['trend_down']
        df['explosion_line'] = wae['explosion_line']
        df['dead_zone_line'] = wae['dead_zone_line']

    Returns:
    - pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate EMA
    def calculate_ema(series, period):
        return series.ewm(span=period, adjust=False).mean()
    
    # Calculate RMA
    def calculate_rma(series, period):
        return series.ewm(alpha=1/period, adjust=False).mean()

    # Calculate DEAD_ZONE
    true_range = pd.DataFrame({
        'high_low': df['high'] - df['low'],
        'high_close': (df['high'] - df['close'].shift()).abs(),
        'low_close': (df['low'] - df['close'].shift()).abs()
    })
    true_range['true_range'] = true_range[['high_low', 'high_close', 'low_close']].max(axis=1)
    # dead_zone = RMA(pd.DataFrame(true_range), 'true_range', 100)['rma'] * 3.7
    dead_zone = calculate_rma(true_range['true_range'], 100) * 3.7

    # Calculate MACD
    macd_fast = calculate_ema(df['close'], fast_length)
    macd_slow = calculate_ema(df['close'], slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity

    # Calculate Bollinger Bands
    bb = BollingerBands(df, column='close', period=channel_length, std_dev=mult)
    e1 = bb['bb_upper'] - bb['bb_lower']

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy['trend_up'] = trend_up.round(2)
    df_copy['trend_down'] = trend_down.round(2)
    df_copy['explosion_line'] = e1.round(2)
    df_copy['dead_zone_line'] = dead_zone.values.round(2)

    return df_copy[['trend_up', 'trend_down', 'explosion_line', 'dead_zone_line']]


def WaveTrend(df, chlen: int = 10, avg: int = 21, smalen: int = 4) -> pd.DataFrame:
    """
    WaveTrend Oscillator

    The WaveTrend Oscillator is used to identify overbought and oversold conditions in the market.

    Inspired by:  https://www.tradingview.com/script/2KE8wTuF-Indicator-WaveTrend-Oscillator-WT/ 
    and: https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - chlen (int): Channel length for the EMA calculation. Default is 10.
    - avg (int): Average period for the EMA calculation. Default is 21.
    - smalen (int): Period for the SMA calculation. Default is 4.

    Call with:
        wt = bta.WaveTrend(df, chlen=10, avg=21, smalen=4)
        df['wt1'] = wt['wt1']
        df['wt2'] = wt['wt2']

    Returns:
    - pd.DataFrame: DataFrame with 'wt1' and 'wt2' columns.
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

    df_copy['wt1'] = df_copy['wt1'].round(2)
    df_copy['wt2'] = df_copy['wt2'].round(2)

    return df_copy[['wt1', 'wt2']]


def WaveTrendOscillator(df: pd.DataFrame, src: str = 'close', n1: int = 8, n2: int = 12) -> pd.DataFrame:
    """
    WaveTrend Oscillator

    The WaveTrend Oscillator is used to identify overbought and oversold conditions in the market.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - n1 (int): Length for the first EMA. Default is 8.
    - n2 (int): Length for the second EMA. Default is 12.

    Call with:
        df['wto'] = bta.WaveTrendOscillator(df, 'close')['wavetrend']

    Returns:
    - pd.DataFrame: DataFrame with 'wavetrend' column.
    """
    df_copy = df.copy()

    src_series = df[src]
    ema_src = EMA(df, column=src, period=n1)['ema']
    diff_series = np.abs(src_series - ema_src)
    d = EMA(pd.DataFrame({'diff': diff_series}), column='diff', period=n1)['ema']
    ci = (src_series - ema_src) / (0.015 * d)
    tci = EMA(pd.DataFrame({'ci': ci}), column='ci', period=n2)['ema']
    wavetrend = tci - SMA(pd.DataFrame({'tci': tci}), column='tci', period=4)['sma']

    df_copy['wavetrend'] = wavetrend.round(2)
    
    return df_copy[['wavetrend']]


def QQEMod(df, rsi_period: int = 6, rsi_smoothing: int = 5, qqe_factor: int = 3, threshold: int = 3, bollinger_length: int = 50, bb_multiplier: float = 0.35, rsi_period2: int = 6, rsi_smoothing2: int = 5, qqe_factor2: float = 1.61, threshold2: int = 3) -> pd.DataFrame:
    """
    QQE Mod Indicator

    The QQE (Quantitative Qualitative Estimation) is a technical analysis indicator that combines the Relative Strength Index (RSI) with a smoothing technique to generate buy and sell signals. The QQE indicator helps traders to identify trends, potential breakouts, and changes in market momentum by providing an enhanced visualization of the underlying price dynamics.

    Inspired by: https://www.tradingview.com/script/TpUW4muw-QQE-MOD/

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
        qqe_mod = bta.QQEMod(df, 6, 5, 3, 3, 50, 0.35, 6, 5, 1.61, 3)
        df['qqe_line'] = qqe_mod['qqe_line']
        df['histo2'] = qqe_mod['histo2']
        df['qqe_up'] = qqe_mod['qqe_up']
        df['qqe_down'] = qqe_mod['qqe_down']

    Returns:
    - pd.DataFrame: DataFrame with 'qqe_line', 'histo2', 'qqe_up', and 'qqe_down' columns.
    """
    def wilders_ema(series, period):
        return series.ewm(alpha=1/period, adjust=False).mean()

    df_copy = df.copy()

    # First QQE Calculation
    src = df_copy['close']
    wilders_period = rsi_period * 2 - 1

    rsi = RelativeStrengthIndex(df_copy, column='close', period=rsi_period)
    rsi_ma = EMA(df_copy.assign(rsi=rsi), column='rsi', period=rsi_smoothing)['ema']
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
        if rsindex.iloc[i] > shortband[i - 1]:
            trend[i] = 1
        elif cross_1:
            trend[i] = -1
        else:
            trend[i] = trend[i - 1]

    fast_atr_rsi_tl = np.where(trend == 1, longband, shortband)

    # Bollinger Bands on FastATRRSI TL
    basis = SMA(pd.DataFrame(fast_atr_rsi_tl - 50), column=0, period=bollinger_length)['sma']
    dev = bb_multiplier * (pd.Series(fast_atr_rsi_tl - 50).rolling(window=bollinger_length).std())
    upper = basis + dev
    lower = basis - dev

    # Second QQE Calculation
    wilders_period2 = rsi_period2 * 2 - 1

    rsi2 = RelativeStrengthIndex(df_copy, column='close', period=rsi_period2)
    rsi_ma2 = EMA(df_copy.assign(rsi2=rsi2), column='rsi2', period=rsi_smoothing2)['ema']
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
        if rsindex2.iloc[i] > shortband2[i - 1]:
            trend2[i] = 1
        elif cross_2:
            trend2[i] = -1
        else:
            trend2[i] = trend2[i - 1]

    fast_atr_rsi2_tl = np.where(trend2 == 1, longband2, shortband2)

    df_copy['qqe_line'] = (fast_atr_rsi2_tl - 50).round(2)
    df_copy['histo2'] = (rsi_ma2 - 50).round(2)

    greenbar1 = rsi_ma2 - 50 > threshold2
    greenbar2 = rsi_ma - 50 > upper

    redbar1 = rsi_ma2 - 50 < -threshold2
    redbar2 = rsi_ma - 50 < lower

    df_copy['qqe_up'] = np.where(greenbar1 & greenbar2, rsi_ma2 - 50, np.nan).round(2)
    df_copy['qqe_down'] = np.where(redbar1 & redbar2, rsi_ma2 - 50, np.nan).round(2)

    return df_copy[['qqe_line', 'histo2', 'qqe_up', 'qqe_down']]


def RelativeStrengthIndex(df, column: str = 'close', period: int = 14) -> pd.DataFrame:
    """
    Relative Strength Index (RSI)

    RSI measures the magnitude of recent price changes to evaluate overbought or oversold conditions in the price of a stock or other asset.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which RSI is to be calculated. Default is "close".
    - period (int): The period over which RSI is to be calculated. Default is 14.

    Call with:
        df['rsi'] = bta.RelativeStrengthIndex(df, column='close', period=14)['rsi']

    Returns:
    - pd.DataFrame: DataFrame with 'rsi' column.
    """
    df_copy = df.copy()

    delta = df_copy[column].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    for i in range(period, len(df_copy)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df_copy['rsi'] = rsi.round(2)

    return df_copy[['rsi']]


def StochasticMomentumIndex(df, k_length=9, d_length=3):
    """
    The Stochastic Momentum Index (SMI) Indicator

    The Stochastic Momentum Index (SMI) Indicator was developed by 
    William Blau in 1993 and is considered to be a momentum indicator 
    that can help identify trend reversal points.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - k_length (int): Period for %K. Default is 9.
    - d_length (int): Period for %D. Default is 3.

    Call with:
        df['smi'] = bta.StochasticMomentumIndex(df, k_length=9, d_length=3)['smi']

    Returns:
    - pd.DataFrame: DataFrame with 'smi' column populated.
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

    df_copy['smi'] = np.where(avgdiff != 0, (avgrel / (avgdiff / 2) * 100), 0).round(2)
    
    return df_copy[['smi']]


def StochasticRSI(
    df: pd.DataFrame,
    close_col: str = 'close',
    window: int = 14,
    smooth1: int = 3,
    smooth2: int = 3,
    fillna: bool = False
) -> pd.DataFrame:
    """
    Stochastic RSI

    The Stochastic RSI is an indicator used in technical analysis that ranges between 0 and 1 and is created by applying the Stochastic oscillator formula to a set of Relative Strength Index (RSI) values.

    Parameters:
    - df (pd.DataFrame): Input DataFrame which should contain the close column.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window (int): Lookback period for RSI. Default is 14.
    - smooth1 (int): Smoothing period for %K line. Default is 3.
    - smooth2 (int): Smoothing period for %D line. Default is 3.
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        stoch_rsi = bta.StochasticRSI(df, 'close', 14, 3, 3)
        df['stoch_rsi'] = stoch_rsi['stoch_rsi']
        df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
        df['stoch_rsi_d'] = stoch_rsi['stoch_rsi_d']

    Returns:
    - pd.DataFrame: DataFrame with columns ['stoch_rsi', 'stoch_rsi_k', 'stoch_rsi_d'].
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required column
    if close_col not in df.columns:
        raise KeyError(f"DataFrame must contain '{close_col}' column")

    rsi = RelativeStrengthIndex(df, column=close_col, period=window)
    lowest_low_rsi = rsi.rolling(window).min()
    highest_high_rsi = rsi.rolling(window).max()
    stoch_rsi = (rsi - lowest_low_rsi) / (highest_high_rsi - lowest_low_rsi)
    stoch_rsi_k = stoch_rsi.rolling(smooth1).mean()
    stoch_rsi_d = stoch_rsi_k.rolling(smooth2).mean()

    if fillna:
        stoch_rsi = stoch_rsi.fillna(0)
        stoch_rsi_k = stoch_rsi_k.fillna(0)
        stoch_rsi_d = stoch_rsi_d.fillna(0)

    df_copy['stoch_rsi'] = stoch_rsi.round(3)
    df_copy['stoch_rsi_k'] = stoch_rsi_k.round(3)
    df_copy['stoch_rsi_d'] = stoch_rsi_d.round(3)

    return df_copy[['stoch_rsi', 'stoch_rsi_k', 'stoch_rsi_d']]


def TrueStrengthIndex(df, close_col: str ='close', window_slow: int = 25, window_fast: int = 13, fillna: bool = False) -> pd.DataFrame:
    """
    True Strength Index (TSI)

    The True Strength Index (TSI) shows both trend direction and overbought/oversold conditions.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the close column.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window_slow (int): High period. Default is 25.
    - window_fast (int): Low period. Default is 13.
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        df['tsi'] = bta.TrueStrengthIndex(df, 'close', 25, 13)['tsi']

    Returns:
    - pd.DataFrame: DataFrame with 'tsi' column.
    """
    df_copy = df.copy()

    diff_close = df_copy[close_col] - df_copy[close_col].shift(1)
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
    tsi = smoothed / smoothed_abs * 100
    if fillna:
        tsi = tsi.fillna(0)

    df_copy['tsi'] = tsi.round(2)

    return df_copy[['tsi']]


def UltimateOscillator(
    df: pd.DataFrame,
    high_col: str = 'high',
    low_col: str = 'low',
    close_col: str = 'close',
    window1: int = 7,
    window2: int = 14,
    window3: int = 28,
    weight1: float = 4.0,
    weight2: float = 2.0,
    weight3: float = 1.0,
    fillna: bool = False,
) -> pd.DataFrame:
    """
    Ultimate Oscillator

    The Ultimate Oscillator combines short-term, intermediate-term, and long-term price action into one oscillator.

    Parameters:
    - df (pandas.DataFrame): DataFrame containing the data.
    - high_col (str): Name of the column containing high price data. Default is 'high'.
    - low_col (str): Name of the column containing low price data. Default is 'low'.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window1 (int): Short period. Default is 7.
    - window2 (int): Medium period. Default is 14.
    - window3 (int): Long period. Default is 28.
    - weight1 (float): Weight of short BP average for UO. Default is 4.0.
    - weight2 (float): Weight of medium BP average for UO. Default is 2.0.
    - weight3 (float): Weight of long BP average for UO. Default is 1.0.
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        df['uo'] = bta.UltimateOscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']

    Returns:
    - pd.DataFrame: DataFrame with 'uo' column.
    """
    df_copy = df.copy()

    close_shift = df_copy[close_col].shift(1)
    true_range = np.maximum(df_copy[high_col], close_shift) - np.minimum(df_copy[low_col], close_shift)
    buying_pressure = df_copy[close_col] - np.minimum(df_copy[low_col], close_shift)

    min_periods_s = 0 if fillna else window1
    min_periods_m = 0 if fillna else window2
    min_periods_l = 0 if fillna else window3

    avg_s = (buying_pressure.rolling(window1, min_periods=min_periods_s).sum() /
             true_range.rolling(window1, min_periods=min_periods_s).sum())
    avg_m = (buying_pressure.rolling(window2, min_periods=min_periods_m).sum() /
             true_range.rolling(window2, min_periods=min_periods_m).sum())
    avg_l = (buying_pressure.rolling(window3, min_periods=min_periods_l).sum() /
             true_range.rolling(window3, min_periods=min_periods_l).sum())

    uo = 100.0 * ((weight1 * avg_s) + (weight2 * avg_m) + (weight3 * avg_l)) / (weight1 + weight2 + weight3)
    if fillna:
        uo = uo.fillna(50)
    
    df_copy['uo'] = uo.round(2)

    return df_copy[['uo']]


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

    The Stochastic Oscillator is a momentum indicator comparing a particular closing price of a security to a range of its prices over a certain period of time.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - high_col (str): Column name for 'High' prices. Default is 'high'.
    - low_col (str): Column name for 'Low' prices. Default is 'low'.
    - close_col (str): Column name for 'Close' prices. Default is 'close'.
    - window (int): Lookback period for stochastic calculation. Default is 14.
    - smooth_window (int): Lookback period for signal calculation. Default is 3.
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        stoch = bta.StochasticsOscillator(df, 'high', 'low', 'close', 14, 3)
        df['stoch'] = stoch['stoch']
        df['stoch_signal'] = stoch['stoch_signal']
        df['stoch_hist'] = stoch['stoch_hist']

    Returns:
    - pd.DataFrame: DataFrame with 'stoch', 'stoch_signal', and 'stoch_hist' columns.
    """
    df_copy = df.copy()

    high = df_copy[high_col]
    low = df_copy[low_col]
    close = df_copy[close_col]

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

    df_copy['stoch'] = stoch_k.round(2)
    df_copy['stoch_signal'] = stoch_d.round(2)
    df_copy['stoch_hist'] = stoch_hist.round(2)

    return df_copy[['stoch', 'stoch_signal', 'stoch_hist']]


def WilliamsR(
    df: pd.DataFrame,
    high_col: str = 'high',
    low_col: str = 'low',
    close_col: str = 'close',
    lbp: int = 14,
    fillna: bool = False,
) -> pd.DataFrame:
    """
    Williams %R

    The Williams %R is a momentum indicator that measures overbought and oversold levels.

    Inspired by: https://www.tradingview.com/script/REGZq58T-Williams-R/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the high, low, and close columns.
    - high_col (str): Name of the column containing high price data. Default is 'high'.
    - low_col (str): Name of the column containing low price data. Default is 'low'.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - lbp (int): Lookback period. Default is 14.
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        df['williams_r'] = bta.WilliamsR(df, 'high', 'low', 'close', 14)['williams_r']

    Returns:
    - pd.DataFrame: DataFrame with 'williams_r' column.
    """
    df_copy = df.copy()

    min_periods = 0 if fillna else lbp
    highest_high = df_copy[high_col].rolling(lbp, min_periods=min_periods).max()
    lowest_low = df_copy[low_col].rolling(lbp, min_periods=min_periods).min()
    wr = -100 * (highest_high - df_copy[close_col]) / (highest_high - lowest_low)
    if fillna:
        wr = wr.fillna(-50)

    df_copy['williams_r'] = wr.round(2)
    
    return df_copy[['williams_r']]
