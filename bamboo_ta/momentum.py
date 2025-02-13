# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *
from .volatility import *
from .utility import *


def awesome_oscillator(
    df: pd.DataFrame, 
    high_col: str = 'high', 
    low_col: str = 'low', 
    window1: int = 5, 
    window2: int = 34, 
    fillna: bool = False
) -> pd.DataFrame:
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
        df['ao'] = bta.awesome_oscillator(df, 'high', 'low', 5, 34)['ao']

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

    return df_copy[['ao']]


def chande_momentum_oscillator(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:
    """
    Chande Momentum Oscillator (CMO)

    The Chande Momentum Oscillator (CMO) is a technical momentum indicator developed 
    by Tushar Chande. It measures the amount that an asset's price has changed over 
    a specified period of time.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Length for the CMO calculation. Default is 14.

    Call with:
        df['cmo'] = bta.chande_momentum_oscillator(df)

    For Signal line:
        df['cmo_signal'] = df['cmo'].rolling(window=10).mean()  # Using SMA for signal

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

    return df_copy[['cmo']]


def elliott_wave_oscillator(
    df: pd.DataFrame, 
    column: str = 'close', 
    sma1_period: int = 5, 
    sma2_period: int = 35
) -> pd.DataFrame:
    """
    Elliott Wave Oscillator (EWO)

    The Elliott Wave Oscillator (EWO) is a tool to help identify the trend and 
    overall market pattern, assisting in finding future trading opportunities.
    It is derived by calculating the difference between a short and long period 
    simple moving average, then normalizing the result with the close price.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the 
      column specified.
    - column (str): The column on which EWO is to be calculated. Default is 'close'.
    - sma1_period (int): The period for the shorter SMA used in EWO calculation. 
      Default is 5.
    - sma2_period (int): The period for the longer SMA used in EWO calculation. 
      Default is 35.

    Call with:
        df['ewo'] = bta.elliott_wave_oscillator(df, 'close', 5, 35)

    Returns:
    - pd.DataFrame: DataFrame with 'ewo' column.
    """
    df_copy = df.copy()

    sma1 = df[column].rolling(window=sma1_period).mean()
    sma2 = df[column].rolling(window=sma2_period).mean()
    
    df_copy['ewo'] = ((sma1 - sma2) / df[column] * 100)

    return df_copy[['ewo']]


def ehlers_fisher_stochastic_center_of_gravity(df: pd.DataFrame, length: int = 8) -> pd.DataFrame:
    """
    Ehlers Fisher Stochastic Center of Gravity Indicator

    The Fisher Stochastic Center of Gravity indicator, developed by John Ehlers, 
    is used to identify potential turning points in the market by calculating 
    the center of gravity of price movements.

    Inspired by: 
    https://ninjatraderecosystem.com/user-app-share-download/john-ehlers-the-fisher-stochastic-center-of-gravity/
    and: https://fxstill.com/indikators/the-fisher-stochastic-center-of-gravity
    and: https://viewer.mathworks.com/?viewer=plain_code&url=https%3A%2F%2Fes.mathworks.com%2Fmatlabcentral%2Fmlc-downloads%2Fdownloads%2F5a9e5f01-906c-4152-98c6-87484eed86bf%2F853ab8ad-8751-4bcd-ae00-60a9444e9182%2Ffiles%2Fmatlab%2FChapter4-Ehlers%2FEhlerStochCG.m&embed=web
    and: https://www.tradingview.com/script/TLjl71aL-Ehlers-Fisher-Stochastic-Center-Of-Gravity-CC/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high', 'low'.
    - length (int): Period for the indicator. Default is 8.

    Call with:
        fscg = bta.ehlers_fisher_stochastic_center_of_gravity(df)
        df['cg'] = fscg['cg']
        df['trigger'] = fscg['trigger']

    Returns:
    - pd.DataFrame: DataFrame with 'CG' and 'Trigger' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    price = (df['high'] + df['low']) / 2

    # Initialize series
    num = pd.Series([0.0] * len(df), index=df.index)
    denom = pd.Series([0.0] * len(df), index=df.index)
    sg = pd.Series([0.0] * len(df), index=df.index)

    min_bar = length + 1
    l = (length + 1) / 2

    # Calculate CG
    for i in range(min_bar, len(df)):
        num_val = 0.0
        denom_val = 0.0
        for count in range(length):
            num_val += (1 + count) * price.iloc[i - count]
            denom_val += price.iloc[i - count]

        if denom_val != 0:
            sg.iloc[i] = l - num_val / denom_val
        else:
            sg.iloc[i] = 0.0

        max_cg = sg.iloc[i - length + 1:i + 1].max()
        min_cg = sg.iloc[i - length + 1:i + 1].min()

        if max_cg != min_cg:
            num.iloc[i] = (sg.iloc[i] - min_cg) / (max_cg - min_cg)
        else:
            num.iloc[i] = 0.0

        denom.iloc[i] = (4 * num.iloc[i] + 3 * num.iloc[i - 1] + 
                         2 * num.iloc[i - 2] + num.iloc[i - 3]) / 10

    # Calculate Value3 (V3) and Trigger
    v3 = 0.5 * np.log((1 + 1.98 * (denom - 0.5)) / (1 - 1.98 * (denom - 0.5)))
    trigger = v3.shift(1)

    df_copy['cg'] = v3
    df_copy['trigger'] = trigger

    return df_copy[['cg', 'trigger']]


def calculate_intraday_momentum_index(df: pd.DataFrame, length: int = 14) -> pd.Series:
    """
    Intraday Momentum Index (IMI)

    The Intraday Momentum Index combines candlestick analysis with relative strength index (RSI)
    principles to measure intraday momentum based on the relationship between the open and close prices.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the following columns:
        - 'open': Opening price.
        - 'close': Closing price.
    - length (int, default=14): Lookback period for calculating the IMI.

    Call with:
        df['imi'] = bta.calculate_intraday_momentum_index(df, length=14)

    Returns:
    - pd.Series: A Series representing the Intraday Momentum Index (IMI) values.
    """
    # Ensure the DataFrame contains the required columns
    if not {'open', 'close'}.issubset(df.columns):
        raise ValueError("DataFrame must contain 'open' and 'close' columns.")

    # Calculate gains and losses
    gain = np.where(df['close'] > df['open'], df['close'] - df['open'], 0)
    loss = np.where(df['close'] < df['open'], df['open'] - df['close'], 0)

    # Calculate rolling sums of gains and losses
    up_sum = pd.Series(gain).rolling(window=length).sum()
    down_sum = pd.Series(loss).rolling(window=length).sum()

    # Calculate IMI
    imi = 100 * up_sum / (up_sum + down_sum)

    # Return the IMI as a Pandas Series
    return imi


def kaufmans_adaptive_moving_average(
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
    used to identify the overall trend, time turning points, and filter price
    movements.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - close_col (str): Column name for the close prices. Default is 'close'.
    - window (int): Number of periods for the efficiency ratio. Default is 10.
    - pow1 (int): Number of periods for the fastest EMA constant. Default is 2.
    - pow2 (int): Number of periods for the slowest EMA constant. Default is 30.
    - fillna (bool): If True, fill nan values with the close prices. Default is False.

    Call with:
        df['kama'] = bta.kaufmans_adaptive_moving_average(df)['kama']

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
    
    kama_series = pd.Series(kama, index=close.index)

    if fillna:
        kama_series = kama_series.fillna(close)

    df_copy = df.copy()
    df_copy['kama'] = kama_series

    return df_copy[['kama']]


def macd(
    df: pd.DataFrame, 
    column: str = 'close', 
    short_window: int = 12, 
    long_window: int = 26, 
    signal_window: int = 9
) -> pd.DataFrame:
    """
    Moving Average Convergence Divergence (MACD)

    MACD is a trend-following momentum indicator that shows the relationship 
    between two moving averages of a security's price.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which MACD is to be calculated. Default is "close".
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - signal_window (int): The signal line period for EMA. Default is 9.

    Call with:
        macd_result = bta.macd(df, 'close', 12, 26, 9)
        df['macd'] = macd_result['macd']
        df['macd_signal'] = macd_result['macd_signal']
        df['macd_histogram'] = macd_result['macd_histogram']

    Returns:
    - pd.DataFrame: DataFrame with 'macd', 'macd_signal', and 'macd_histogram' columns.
    """
    def ema_calculation(series, span):
        return series.ewm(span=span, adjust=False).mean()

    short_ema = ema_calculation(df[column], span=short_window)
    long_ema = ema_calculation(df[column], span=long_window)
    macd = short_ema - long_ema
    signal = ema_calculation(macd, span=signal_window)
    histogram = macd - signal

    df_copy = df.copy()
    df_copy['macd'] = macd
    df_copy['macd_signal'] = signal
    df_copy['macd_histogram'] = histogram
    
    return df_copy[['macd', 'macd_signal', 'macd_histogram']]


def macd_leader(
    df: pd.DataFrame, 
    src: str = 'close', 
    fast_length: int = 12, 
    slow_length: int = 26, 
    signal_length: int = 9
) -> pd.DataFrame:
    """
    MACD Leader

    The MACD Leader is a variation of the standard MACD that aims to provide an 
    earlier signal by using a different calculation method.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - fast_length (int): Length for the fast EMA. Default is 12.
    - slow_length (int): Length for the slow EMA. Default is 26.
    - signal_length (int): Length for the signal EMA. Default is 9.

    Call with:
        df['macd_leader'] = bta.macd_leader(df, 'close')['macd_leader']

    Returns:
    - pd.DataFrame: DataFrame with 'macd_leader' column.
    """
    def ema_calculation(series, span):
        return series.ewm(span=span, adjust=False).mean()

    df_copy = df.copy()
    src_series = df[src]

    sema = ema_calculation(src_series, span=fast_length)
    lema = ema_calculation(src_series, span=slow_length)
    diff_sema = src_series - sema
    diff_lema = src_series - lema
    i1 = sema + ema_calculation(diff_sema, span=fast_length)
    i2 = lema + ema_calculation(diff_lema, span=slow_length)
    macd_leader = ((i1 - i2) / 10) * 10

    df_copy['macd_leader'] = macd_leader
    
    return df_copy[['macd_leader']]

def ma_streak(
    df: pd.DataFrame, 
    length: int = 10, 
    src: str = 'close', 
    matype: int = 1
) -> pd.DataFrame:
    """
    MA Streak Indicator

    This indicator tracks how many bars a given moving average is rising or falling. 
    It's color-coded green (positive) or red (negative).

    Inspired by: 
    https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/
    
    Call with:
        df['ma_streak'] = bta.ma_streak(df, length=10, src='close', matype=1)['ma_streak']

    MA types:
    1 - Simple Moving Average (SMA)
    2 - Exponential Moving Average (EMA)
    3 - Hull Moving Average (HMA)
    4 - Weighted Moving Average (WMA)
    5 - Volume Weighted Moving Average (VWMA)

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the moving average calculation. Default is 10.
    - src (str): The column name to use for the moving average calculation. Default is 'close'.
    - matype (int): Type of moving average to use. Default is 1 (SMA).

    Returns:
    - pd.DataFrame: DataFrame with 'ma_streak' column.
    """
    df_copy = df.copy()

    # Calculate different types of moving averages
    df_copy['sma'] = df_copy[src].rolling(window=length).mean()
    df_copy['ema'] = df_copy[src].ewm(span=length, adjust=False).mean()
    df_copy['wma'] = df_copy[src].rolling(window=length).apply(
        lambda prices: np.dot(prices, np.arange(1, length + 1)) / np.arange(1, length + 1).sum(), 
        raw=True
    )
    df_copy['vwma'] = (
        (df_copy[src] * df_copy['volume']).rolling(window=length).sum() 
        / df_copy['volume'].rolling(window=length).sum()
    )

    # Calculate Hull Moving Average (HMA)
    half_length = int(length / 2)
    sqrt_length = int(np.sqrt(length))
    df_copy['hma'] = df_copy[src].rolling(window=half_length).mean()
    df_copy['hma'] = 2 * df_copy['hma'] - df_copy[src].rolling(window=length).mean()
    df_copy['hma'] = df_copy['hma'].rolling(window=sqrt_length).mean()

    # Select the appropriate moving average
    if matype == 1:
        df_copy['avgval'] = df_copy['sma']
    elif matype == 2:
        df_copy['avgval'] = df_copy['ema']
    elif matype == 3:
        df_copy['avgval'] = df_copy['hma']
    elif matype == 4:
        df_copy['avgval'] = df_copy['wma']
    elif matype == 5:
        df_copy['avgval'] = df_copy['vwma']
    else:
        raise ValueError("Invalid moving average type. Choose a value between 1 and 5.")

    # Initialize the streak columns
    df_copy['upcount'] = 0
    df_copy['dncount'] = 0
    df_copy['ma_streak'] = 0

    # Calculate the streak
    for i in range(1, len(df_copy)):
        if df_copy['avgval'].iloc[i] > df_copy['avgval'].iloc[i - 1]:
            df_copy.at[i, 'upcount'] = df_copy.at[i - 1, 'upcount'] + 1
            df_copy.at[i, 'dncount'] = 0
        elif df_copy['avgval'].iloc[i] < df_copy['avgval'].iloc[i - 1]:
            df_copy.at[i, 'dncount'] = df_copy.at[i - 1, 'dncount'] - 1
            df_copy.at[i, 'upcount'] = 0
        df_copy.at[i, 'ma_streak'] = df_copy.at[i, 'upcount'] + df_copy.at[i, 'dncount']

    return df_copy[['ma_streak']]


def momentum_divergence(df: pd.DataFrame, mom_length: int = 10, bb_length: int = 20, bb_dev: float = 2.0, lookback: int = 30) -> pd.DataFrame:
    """
    Momentum Divergence (momdiv)

    A self-contained implementation of the Momentum Divergence indicator. It calculates
    momentum and applies Bollinger Bands to identify potential buy and sell signals
    based on momentum divergence. Additionally, it detects if the current high or low
    breaks the highest high or lowest low over a specified lookback period.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data.
    - mom_length (int, default=10): Lookback period for momentum calculation.
    - bb_length (int, default=20): Lookback period for Bollinger Bands calculation.
    - bb_dev (float, default=2.0): Number of standard deviations for Bollinger Bands.
    - lookback (int, default=30): Lookback period for detecting highest high and lowest low.

    Call with:
        momdiv_result = bta.momentum_divergence(df, mom_length=5, bb_length=5, bb_dev=1.0, lookback=5)
        df['momentum_divergence_mom'] = momdiv_result['momentum_divergence_mom']
        df['momentum_divergence_upperb'] = momdiv_result['momentum_divergence_upperb']
        df['momentum_divergence_lowerb'] = momdiv_result['momentum_divergence_lowerb']
        df['momentum_divergence_buy'] = momdiv_result['momentum_divergence_buy']
        df['momentum_divergence_sell'] = momdiv_result['momentum_divergence_sell']
        df['momentum_divergence_coh'] = momdiv_result['momentum_divergence_coh']
        df['momentum_divergence_col'] = momdiv_result['momentum_divergence_col']

    Returns:
    - pd.DataFrame: DataFrame with the following columns:
        - 'momentum_divergence_mom': Calculated momentum.
        - 'momentum_divergence_upperb': Upper Bollinger Band for momentum.
        - 'momentum_divergence_lowerb': Lower Bollinger Band for momentum.
        - 'momentum_divergence_buy': Boolean indicating a buy signal (momentum crossed below lower band).
        - 'momentum_divergence_sell': Boolean indicating a sell signal (momentum crossed above upper band).
        - 'momentum_divergence_coh': Boolean indicating the current high is the highest high over the lookback period.
        - 'momentum_divergence_col': Boolean indicating the current low is the lowest low over the lookback period.
    """
    df_copy = df.copy()

    # Calculate momentum
    df_copy['mom'] = df_copy['close'].diff(mom_length)

    # Calculate Bollinger Bands for momentum
    df_copy['mom_mean'] = df_copy['mom'].rolling(window=bb_length).mean()
    df_copy['mom_std'] = df_copy['mom'].rolling(window=bb_length).std()
    df_copy['upperb'] = df_copy['mom_mean'] + (bb_dev * df_copy['mom_std'])
    df_copy['lowerb'] = df_copy['mom_mean'] - (bb_dev * df_copy['mom_std'])

    # Buy and sell signals
    df_copy['buy'] = (df_copy['mom'] < df_copy['lowerb']).astype(int)
    df_copy['sell'] = (df_copy['mom'] > df_copy['upperb']).astype(int)

    # Highest high and lowest low over lookback period
    df_copy['hh'] = df_copy['high'].rolling(window=lookback).max()
    df_copy['ll'] = df_copy['low'].rolling(window=lookback).min()
    df_copy['coh'] = (df_copy['high'] >= df_copy['hh']).astype(int)
    df_copy['col'] = (df_copy['low'] <= df_copy['ll']).astype(int)

    # Return relevant columns
    result = pd.DataFrame({
        'momentum_divergence_mom': df_copy['mom'],
        'momentum_divergence_upperb': df_copy['upperb'],
        'momentum_divergence_lowerb': df_copy['lowerb'],
        'momentum_divergence_buy': df_copy['buy'],
        'momentum_divergence_sell': df_copy['sell'],
        'momentum_divergence_coh': df_copy['coh'],
        'momentum_divergence_col': df_copy['col']
    })

    return result


def percentage_price_oscillator(
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
        ppo = bta.percentage_price_oscillator(df)
        df['ppo'] = ppo['ppo']
        df['ppo_signal'] = ppo['ppo_signal']
        df['ppo_hist'] = ppo['ppo_hist']

    Returns:
    - pd.DataFrame: DataFrame with columns ['ppo', 'ppo_signal', 'ppo_hist'].
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required column
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


def percentage_volume_oscillator(
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
        pvo = bta.percentage_volume_oscillator(df)
        df['pvo'] = pvo['pvo']
        df['pvo_signal'] = pvo['pvo_signal']
        df['pvo_hist'] = pvo['pvo_hist']

    Returns:
    - pd.DataFrame: DataFrame with columns ['pvo', 'pvo_signal', 'pvo_hist'].
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required column
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


def relative_momentum_index(df: pd.DataFrame, length: int = 20, mom: int = 5) -> pd.DataFrame:
    """
    Relative Momentum Index (RMI)

    The Relative Momentum Index (RMI) is an oscillator that applies the RSI formula 
    to momentum rather than price.

    Source: 
    https://www.tradingview.com/script/DdT7MmPa/ 
    https://github.com/freqtrade/technical/blob/master/technical/indicators/indicators.py#L912  

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - length (int): Period for the EMA calculation. Default is 20.
    - mom (int): Momentum period. Default is 5.

    Call with:
        df['rmi'] = bta.relative_momentum_index(df, length=20, mom=5)['rmi']

    Returns:
    - pd.DataFrame: DataFrame with 'rmi' column.
    """
    df_copy = df.copy()

    # Calculate the momentum up and down changes
    df_copy['maxup'] = (df_copy['close'] - df_copy['close'].shift(mom)).clip(lower=0)
    df_copy['maxdown'] = (df_copy['close'].shift(mom) - df_copy['close']).clip(lower=0)
    
    df_copy.fillna(0, inplace=True)
    
    # Calculate the EMA of increases and decreases
    df_copy["ema_inc"] = exponential_moving_average(df_copy, column='maxup', period=length)
    df_copy["ema_dec"] = exponential_moving_average(df_copy, column='maxdown', period=length)
    
    # Calculate the Relative Momentum Index (RMI)
    df_copy['rmi'] = np.where(
        df_copy['ema_dec'] == 0, 
        0, 
        100 - 100 / (1 + df_copy["ema_inc"] / df_copy["ema_dec"])
    )

    return df_copy[['rmi']]


def rate_of_change(df: pd.DataFrame, column: str = 'close', period: int = 21) -> pd.DataFrame:
    """
    Rate of Change (ROC)

    The Rate of Change (ROC) is a momentum oscillator that measures the percentage 
    change in price between the current price and the price n periods ago.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the ROC is to be applied. Default is 'close'.
    - period (int): Period for the ROC calculation. Default is 21.

    Call with:
        df['roc'] = bta.rate_of_change(df, column='close', period=21)['roc']

    Returns:
    - pd.DataFrame: DataFrame with 'roc' column.
    """
    df_copy = df.copy()

    df_copy['roc'] = df_copy[column].diff(period) / df_copy[column].shift(period) * 100
    
    return df_copy[['roc']]


def smoothed_rate_of_change(
    df: pd.DataFrame, 
    roclen: int = 21, 
    emalen: int = 13, 
    smooth: int = 21
) -> pd.DataFrame:
    """
    Smoothed Rate of Change (SROC)

    The Smoothed Rate of Change (SROC) is a momentum oscillator that applies 
    an exponential moving average (EMA) to the Rate of Change (ROC) to smooth 
    out short-term fluctuations.

    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - roclen (int): Period for the ROC calculation. Default is 21.
    - emalen (int): Period for the EMA calculation. Default is 13.
    - smooth (int): Smoothing period for the ROC calculation. Default is 21.

    Call with:
        df['sroc'] = bta.smoothed_rate_of_change(df, roclen=21, emalen=13, smooth=21)['sroc']

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

    df_copy['sroc'] = sroc
    
    return df_copy[['sroc']]


def waddah_attar_explosion_atr(
    df: pd.DataFrame,
    sensitivity: int = 150,
    fast_length: int = 20,
    slow_length: int = 40,
    channel_length: int = 20,
    mult: float = 2.0
) -> pd.DataFrame:
    """
    Waddah Attar Explosion Indicator

    The Waddah Attar Explosion indicator is used to identify potential breakout 
    opportunities by combining the MACD and Bollinger Bands. The dead zone line 
    is based on ATR in this indicator.

    Inspired by: https://www.tradingview.com/script/d9IjcYyS-Waddah-Attar-Explosion-V2-SHK/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        wae = bta.waddah_attar_explosion_atr(df)
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
        return series.ewm(alpha=1 / period, adjust=False).mean()

    # Calculate DEAD_ZONE
    true_range = pd.DataFrame({
        'high_low': df['high'] - df['low'],
        'high_close': (df['high'] - df['close'].shift()).abs(),
        'low_close': (df['low'] - df['close'].shift()).abs()
    })
    true_range['true_range'] = true_range[['high_low', 'high_close', 'low_close']].max(axis=1)
    dead_zone = calculate_rma(true_range['true_range'], 100) * 3.7

    # Calculate MACD
    macd_fast = calculate_ema(df['close'], fast_length)
    macd_slow = calculate_ema(df['close'], slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity

    # Calculate Bollinger Bands
    bb = bollinger_bands(df, column='close', period=channel_length, std_dev=mult)
    e1 = bb['bb_upper'] - bb['bb_lower']

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy['trend_up'] = trend_up
    df_copy['trend_down'] = trend_down
    df_copy['explosion_line'] = e1
    df_copy['dead_zone_line'] = dead_zone.values

    return df_copy[['trend_up', 'trend_down', 'explosion_line', 'dead_zone_line']]


def waddah_attar_explosion(
    df: pd.DataFrame,
    sensitivity: int = 150,
    fast_length: int = 20,
    slow_length: int = 40,
    channel_length: int = 20,
    dead_zone: int = 20,
    mult: float = 2.0
) -> pd.DataFrame:
    """
    Waddah Attar Explosion Indicator

    The Waddah Attar Explosion indicator is used to identify potential breakout 
    opportunities by combining the MACD and Bollinger Bands.

    Inspired by: https://www.tradingview.com/script/iu3kKWDI-Waddah-Attar-Explosion-LazyBear/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - dead_zone (int): Dead zone factor for the indicator. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        wae = bta.waddah_attar_explosion(df)
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
    
    # Calculate MACD
    macd_fast = calculate_ema(df['close'], fast_length)
    macd_slow = calculate_ema(df['close'], slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity

    # Calculate Bollinger Bands
    bb = bollinger_bands(df, column='close', period=channel_length, std_dev=mult)
    e1 = bb['bb_upper'] - bb['bb_lower']

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy['trend_up'] = trend_up
    df_copy['trend_down'] = trend_down
    df_copy['explosion_line'] = e1
    df_copy['dead_zone_line'] = dead_zone

    return df_copy[['trend_up', 'trend_down', 'explosion_line', 'dead_zone_line']]


def wave_trend(df: pd.DataFrame, chlen: int = 10, avg: int = 21, smalen: int = 4) -> pd.DataFrame:
    """
    WaveTrend

    The WaveTrend is used to identify overbought and oversold conditions in the market.

    Inspired by:  
    https://www.tradingview.com/script/2KE8wTuF-Indicator-WaveTrend-Oscillator-WT/ 
    and: https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - chlen (int): Channel length for the EMA calculation. Default is 10.
    - avg (int): Average period for the EMA calculation. Default is 21.
    - smalen (int): Period for the SMA calculation. Default is 4.

    Call with:
        wt = bta.wave_trend(df, chlen=10, avg=21, smalen=4)
        df['wt1'] = wt['wt1']
        df['wt2'] = wt['wt2']

    Returns:
    - pd.DataFrame: DataFrame with 'wt1' and 'wt2' columns.
    """
    df_copy = df.copy()

    df_copy['hlc3'] = (df_copy['high'] + df_copy['low'] + df_copy['close']) / 3
    df_copy['esa'] = exponential_moving_average(df_copy, column='hlc3', period=chlen)
    df_copy['abs_diff'] = (df_copy['hlc3'] - df_copy['esa']).abs()
    df_copy['d'] = exponential_moving_average(df_copy, column='abs_diff', period=chlen)
    df_copy['ci'] = (df_copy['hlc3'] - df_copy['esa']) / (0.015 * df_copy['d'])
    df_copy['tci'] = exponential_moving_average(df_copy, column='ci', period=avg)
    df_copy['wt1'] = df_copy['tci']
    df_copy['wt2'] = simple_moving_average(df_copy, column='wt1', period=smalen)

    return df_copy[['wt1', 'wt2']]


def wave_trend_oscillator(
    df: pd.DataFrame, 
    src: str = 'close', 
    n1: int = 8, 
    n2: int = 12
) -> pd.DataFrame:
    """
    WaveTrend Oscillator

    The WaveTrend Oscillator is used to identify overbought and oversold conditions 
    in the market.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - n1 (int): Length for the first EMA. Default is 8.
    - n2 (int): Length for the second EMA. Default is 12.

    Call with:
        df['wto'] = bta.wave_trend_oscillator(df, 'close')['wavetrend']

    Returns:
    - pd.DataFrame: DataFrame with 'wavetrend' column.
    """
    df_copy = df.copy()

    src_series = df[src]
    ema_src = exponential_moving_average(df, column=src, period=n1)['ema']
    diff_series = np.abs(src_series - ema_src)
    d = exponential_moving_average(pd.DataFrame({'diff': diff_series}), column='diff', period=n1)['ema']
    ci = (src_series - ema_src) / (0.015 * d)
    tci = exponential_moving_average(pd.DataFrame({'ci': ci}), column='ci', period=n2)['ema']
    wavetrend = tci - simple_moving_average(pd.DataFrame({'tci': tci}), column='tci', period=4)['sma']

    df_copy['wavetrend'] = wavetrend
    
    return df_copy[['wavetrend']]


def qqe_mod(
    df: pd.DataFrame, 
    rsi_period: int = 6, 
    rsi_smoothing: int = 5, 
    qqe_factor: int = 3, 
    threshold: int = 3, 
    bollinger_length: int = 50, 
    bb_multiplier: float = 0.35, 
    rsi_period2: int = 6, 
    rsi_smoothing2: int = 5, 
    qqe_factor2: float = 1.61, 
    threshold2: int = 3
) -> pd.DataFrame:
    """
    QQE Mod Indicator

    The QQE (Quantitative Qualitative Estimation) is a technical analysis indicator 
    that combines the Relative Strength Index (RSI) with a smoothing technique to 
    generate buy and sell signals. The QQE indicator helps traders identify trends, 
    potential breakouts, and changes in market momentum by providing an enhanced 
    visualization of the underlying price dynamics.

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
        qqe_mod = bta.qqe_mod(df, 6, 5, 3, 3, 50, 0.35, 6, 5, 1.61, 3)
        df['qqe_line'] = qqe_mod['qqe_line']
        df['histo2'] = qqe_mod['histo2']
        df['qqe_up'] = qqe_mod['qqe_up']
        df['qqe_down'] = qqe_mod['qqe_down']

    Returns:
    - pd.DataFrame: DataFrame with 'qqe_line', 'histo2', 'qqe_up', and 'qqe_down' columns.
    """
    
    def wilders_ema(series, period):
        return series.ewm(alpha=1 / period, adjust=False).mean()

    df_copy = df.copy()

    # First QQE Calculation
    src = df_copy['close']
    wilders_period = rsi_period * 2 - 1

    rsi = relative_strength_index(df_copy, column='close', period=rsi_period)
    rsi_ma = exponential_moving_average(df_copy.assign(rsi=rsi), column='rsi', period=rsi_smoothing)['ema']
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
    basis = simple_moving_average(pd.DataFrame(fast_atr_rsi_tl - 50), column=0, period=bollinger_length)['sma']
    dev = bb_multiplier * (pd.Series(fast_atr_rsi_tl - 50).rolling(window=bollinger_length).std())
    upper = basis + dev
    lower = basis - dev

    # Second QQE Calculation
    wilders_period2 = rsi_period2 * 2 - 1

    rsi2 = relative_strength_index(df_copy, column='close', period=rsi_period2)
    rsi_ma2 = exponential_moving_average(df_copy.assign(rsi2=rsi2), column='rsi2', period=rsi_smoothing2)['ema']
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

    df_copy['qqe_line'] = (fast_atr_rsi2_tl - 50)
    df_copy['histo2'] = (rsi_ma2 - 50)

    greenbar1 = rsi_ma2 - 50 > threshold2
    greenbar2 = rsi_ma - 50 > upper

    redbar1 = rsi_ma2 - 50 < -threshold2
    redbar2 = rsi_ma - 50 < lower

    df_copy['qqe_up'] = np.where(greenbar1 & greenbar2, rsi_ma2 - 50, np.nan)
    df_copy['qqe_down'] = np.where(redbar1 & redbar2, rsi_ma2 - 50, np.nan)

    return df_copy[['qqe_line', 'histo2', 'qqe_up', 'qqe_down']]


def relative_strength_index(df: pd.DataFrame, column: str = 'close', period: int = 14) -> pd.DataFrame:
    """
    Relative Strength Index (RSI)

    RSI measures the magnitude of recent price changes to evaluate overbought or oversold 
    conditions in the price of a stock or other asset.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which RSI is to be calculated. Default is "close".
    - period (int): The period over which RSI is to be calculated. Default is 14.

    Call with:
        df['rsi'] = bta.relative_strength_index(df, column='close', period=14)['rsi']

    Returns:
    - pd.DataFrame: DataFrame with 'rsi' column.
    """
    df_copy = df.copy()

    delta = df_copy[column].diff(1)
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    # Apply the Wilder's smoothing technique for gain and loss averages
    for i in range(period, len(df_copy)):
        avg_gain.iloc[i] = (avg_gain.iloc[i - 1] * (period - 1) + gain.iloc[i]) / period
        avg_loss.iloc[i] = (avg_loss.iloc[i - 1] * (period - 1) + loss.iloc[i]) / period

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    df_copy['rsi'] = rsi

    return df_copy[['rsi']]


def stochastic_momentum_index(df: pd.DataFrame, k_length: int = 9, d_length: int = 3) -> pd.DataFrame:
    """
    The Stochastic Momentum Index (SMI) Indicator

    The Stochastic Momentum Index (SMI) Indicator was developed by William Blau 
    in 1993 and is considered to be a momentum indicator that can help identify 
    trend reversal points.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - k_length (int): Period for %K. Default is 9.
    - d_length (int): Period for %D. Default is 3.

    Call with:
        df['smi'] = bta.stochastic_momentum_index(df, k_length=9, d_length=3)['smi']

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

    df_copy['smi'] = np.where(avgdiff != 0, (avgrel / (avgdiff / 2) * 100), 0)

    return df_copy[['smi']]


def stochastics_oscillator(
    df: pd.DataFrame,
    high_col: str = 'high',
    low_col: str = 'low',
    close_col: str = 'close',
    window: int = 14,
    smooth_window: int = 3,
    fillna: bool = False
) -> pd.DataFrame:
    """
    Stochastic Oscillator, Stochastic Signal, and Histogram Combined.

    The Stochastic Oscillator is a momentum indicator comparing a particular 
    closing price of a security to a range of its prices over a certain period of time.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - high_col (str): Column name for 'High' prices. Default is 'high'.
    - low_col (str): Column name for 'Low' prices. Default is 'low'.
    - close_col (str): Column name for 'Close' prices. Default is 'close'.
    - window (int): Lookback period for stochastic calculation. Default is 14.
    - smooth_window (int): Lookback period for signal calculation. Default is 3.
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        stoch = bta.stochastics_oscillator(df, 'high', 'low', 'close', 14, 3)
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

    df_copy['stoch'] = stoch_k
    df_copy['stoch_signal'] = stoch_d
    df_copy['stoch_hist'] = stoch_hist

    return df_copy[['stoch', 'stoch_signal', 'stoch_hist']]


def stochastic_rsi(
    df: pd.DataFrame, 
    length_rsi: int = 14, 
    length_stoch: int = 14, 
    smooth_k: int = 3, 
    smooth_d: int = 3
) -> pd.DataFrame:
    """
    Stochastic RSI (StochasticRSI)
    
    The Stochastic RSI is used to identify overbought and oversold conditions in the market.
    
    Parameters:
    - df (pd.DataFrame): DataFrame containing the data with a 'close' column.
    - length_rsi (int): Period for the RSI calculation. Default is 14.
    - length_stoch (int): Period for the Stochastic calculation. Default is 14.
    - smooth_k (int): Smoothing period for %K line. Default is 3.
    - smooth_d (int): Smoothing period for %D line. Default is 3.
    
    Call with:
        stoch_rsi = bta.stochastic_rsi(df, length_rsi=14, length_stoch=14, smooth_k=3, smooth_d=3)
        df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
        df['stoch_rsi_d'] = stoch_rsi['stoch_rsi_d']
    
    Returns:
    - pd.DataFrame: DataFrame with 'stoch_rsi_k' and 'stoch_rsi_d' columns.
    """
    df_copy = df.copy()
    
    # Step 1: Calculate RSI
    delta = df_copy['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(window=length_rsi).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length_rsi).mean()
    rs = gain / loss
    df_copy['rsi'] = 100 - (100 / (1 + rs))
    
    # Step 2: Calculate the Stochastic Oscillator on RSI
    df_copy['min_rsi'] = df_copy['rsi'].rolling(window=length_stoch).min()
    df_copy['max_rsi'] = df_copy['rsi'].rolling(window=length_stoch).max()
    df_copy['stoch_rsi'] = (df_copy['rsi'] - df_copy['min_rsi']) / (df_copy['max_rsi'] - df_copy['min_rsi']) * 100
    
    # Step 3: Smooth the Stochastic RSI values
    df_copy['stoch_rsi_k'] = df_copy['stoch_rsi'].rolling(window=smooth_k).mean()
    df_copy['stoch_rsi_d'] = df_copy['stoch_rsi_k'].rolling(window=smooth_d).mean()
    
    return df_copy[['stoch_rsi_k', 'stoch_rsi_d']]


def true_strength_index(
    df: pd.DataFrame, 
    close_col: str = 'close', 
    window_slow: int = 25, 
    window_fast: int = 13, 
    fillna: bool = False
) -> pd.DataFrame:
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
        df['tsi'] = bta.true_strength_index(df, 'close', 25, 13)['tsi']

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

    df_copy['tsi'] = tsi

    return df_copy[['tsi']]


def ultimate_oscillator(
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

    The Ultimate Oscillator combines short-term, intermediate-term, and long-term 
    price action into one oscillator.

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
        df['uo'] = bta.ultimate_oscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']

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
    
    df_copy['uo'] = uo

    return df_copy[['uo']]


def williams_r(
    df: pd.DataFrame,
    high_col: str = 'high',
    low_col: str = 'low',
    close_col: str = 'close',
    lbp: int = 14,
    fillna: bool = False
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
        df['williams_r'] = bta.williams_r(df, 'high', 'low', 'close', 14)['williams_r']

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

    df_copy['williams_r'] = wr
    
    return df_copy[['williams_r']]


def macd_v(
    df: pd.DataFrame,
    column: str = 'close',
    short_window: int = 12,
    long_window: int = 26,
    atr_window: int = 26,
    signal_window: int = 9,
    fillna: bool = False
) -> pd.DataFrame:
    """
    MACD-V (Volatility Normalized Momentum)

    The MACD-V is a refined version of the traditional MACD indicator, adjusted for volatility
    using the Average True Range (ATR). This normalization allows for more stable and comparable
    momentum readings across different markets and timeframes.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which MACD-V is to be calculated. Default is "close".
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - atr_window (int): The period for ATR calculation. Default is 26.
    - signal_window (int): The period for the signal line EMA. Default is 9.
    - fillna (bool): If True, fill nan values. Default is False.

    Call with:
        macd_v_result = bta.macd_v(df, 'close', 12, 26, 26, 9)
        df['macd_v'] = macd_v_result['macd_v']
        df['macd_v_signal'] = macd_v_result['macd_v_signal']

    Returns:
    - pd.DataFrame: DataFrame with 'macd_v' and 'macd_v_signal' columns.
    """
    def ema_calculation(series, span):
        return series.ewm(span=span, adjust=False).mean()

    def wilder_ema(series, period):
        return series.ewm(alpha=1/period, adjust=False).mean()

    # Calculate MACD
    short_ema = ema_calculation(df[column], span=short_window)
    long_ema = ema_calculation(df[column], span=long_window)
    macd = short_ema - long_ema

    # Calculate ATR using Wilder's method
    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()
    true_range = high_low.combine(high_close, max).combine(low_close, max)
    atr = wilder_ema(true_range, period=atr_window)

    # Calculate MACD-V
    macd_v = (macd / atr) * 100

    # Calculate Signal Line
    macd_v_signal = ema_calculation(macd_v, span=signal_window)

    if fillna:
        macd_v = macd_v.fillna(0)
        macd_v_signal = macd_v_signal.fillna(0)

    df_copy = df.copy()
    df_copy['macd_v'] = macd_v
    df_copy['macd_v_signal'] = macd_v_signal

    return df_copy[['macd_v', 'macd_v_signal']]
