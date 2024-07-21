# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *


def AccumulationDistributionIndex(df: pd.DataFrame, fillna: bool = False) -> pd.DataFrame:
    """
    Accumulation/Distribution Index (ADI)

    Acts as a leading indicator of price movements.

    Inspired by: https://www.tradingview.com/script/uRMAN1ho-ADL-Accumulation-Distribution-Line-UTS/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - fillna (bool): if True, fill nan values.

    Call with:
        df['adi'] = bta.accumulation_distribution_index(df, fillna=True)['adi']

    Returns:
    - pd.DataFrame: DataFrame with 'adi' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the ADI values
    clv = ((df_copy['close'] - df_copy['low']) - (df_copy['high'] - df_copy['close'])) / (df_copy['high'] - df_copy['low'])
    clv = clv.fillna(0.0)  # float division by zero
    adi = clv * df_copy['volume']
    adi = adi.cumsum()
    if fillna:
        adi = adi.fillna(0)

    df_copy['adi'] = adi.round(2)

    return df_copy[['adi']]


def ChaikinMoneyFlow(df: pd.DataFrame, window: int = 20, fillna: bool = False) -> pd.DataFrame:
    """
    Chaikin Money Flow (CMF)

    Measures the amount of Money Flow Volume over a specific period.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): n period. Default is 20.
    - fillna (bool): if True, fill nan values.

    Call with:
        df['cmf'] = bta.ChaikinMoneyFlow(df, window=20, fillna=True)['cmf']

    Returns:
    - pd.DataFrame: DataFrame with 'cmf' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the CMF values
    mfv = ((df_copy['close'] - df_copy['low']) - (df_copy['high'] - df_copy['close'])) / (df_copy['high'] - df_copy['low'])
    mfv = mfv.fillna(0.0)  # float division by zero
    mfv *= df_copy['volume']
    min_periods = 0 if fillna else window
    cmf = mfv.rolling(window, min_periods=min_periods).sum() / df_copy['volume'].rolling(window, min_periods=min_periods).sum()
    if fillna:
        cmf = cmf.fillna(0)

    df_copy['cmf'] = cmf.round(2)

    return df_copy[['cmf']]


def EaseOfMovement(df: pd.DataFrame, eom_length: int = 14, seom_length: int = 14, fillna: bool = False) -> pd.DataFrame:
    """
    Ease of Movement (EoM, EMV) and Signal Ease of Movement (SMA of EoM)

    Relates an asset's price change to its volume and is useful for assessing trend strength.
    The SMA of the EoM serves as a signal line for the indicator.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'volume' columns.
    - eom_length (int): n period for the EoM calculation. Default is 14.
    - seom_length (int): n period for the SMA of EoM calculation. Default is 14.
    - fillna (bool): if True, fill nan values.

    Call with:
        eom_df = bta.EaseOfMovement(df, eom_length=14, seom_length=14, fillna=True)
        df['eom'] = eom_df['eom']
        df['eom_ma'] = eom_df['eom_ma']

    Returns:
    - pd.DataFrame: DataFrame with 'eom' and 'seom' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the Ease of Movement (EoM) values
    emv = ((df_copy['high'].diff(1) + df_copy['low'].diff(1)) * (df_copy['high'] - df_copy['low'])) / (2 * df_copy['volume'])
    emv *= 100000000
    if fillna:
        emv = emv.fillna(0)

    df_copy['eom'] = emv.round(2) / 100000

    # Calculate the Signal Ease of Movement (SMA of EoM)
    min_periods = 0 if fillna else seom_length
    sma_emv = df_copy['eom'].rolling(seom_length, min_periods=min_periods).mean()
    if fillna:
        sma_emv = sma_emv.fillna(0)

    df_copy['seom'] = sma_emv.round(2) * 10

    return df_copy[['eom', 'seom']]


def ForceIndex(df: pd.DataFrame, window: int = 13, fillna: bool = False) -> pd.DataFrame:
    """
    Force Index (FI)

    Illustrates how strong the actual buying or selling pressure is.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - window (int): n period. Default is 13.
    - fillna (bool): if True, fill nan values.

    Call with:
        df['fi'] = bta.ForceIndex(df, window=13, fillna=True)['fi']

    Returns:
    - pd.DataFrame: DataFrame with 'fi' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the Force Index values
    fi = (df_copy['close'] - df_copy['close'].shift(1)) * df_copy['volume']
    fi_ema = fi.ewm(span=window, adjust=False).mean()
    if fillna:
        fi_ema = fi_ema.fillna(0)

    df_copy['fi'] = fi_ema.round(2)

    return df_copy[['fi']]


def MoneyFlowIndex(df: pd.DataFrame, window: int = 14, fillna: bool = False) -> pd.DataFrame:
    """
    Money Flow Index (MFI)

    Uses both price and volume to measure buying and selling pressure.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): n period. Default is 14.
    - fillna (bool): if True, fill nan values.

    Call with:
        df['mfi']  = bta.MoneyFlowIndex(df, window=14, fillna=True)['mfi']

    Returns:
    - pd.DataFrame: DataFrame with 'mfi' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate typical price
    typical_price = (df_copy['high'] + df_copy['low'] + df_copy['close']) / 3.0
    up_down = np.where(
        typical_price > typical_price.shift(1),
        1,
        np.where(typical_price < typical_price.shift(1), -1, 0)
    )
    mfr = typical_price * df_copy['volume'] * up_down

    # Calculate positive and negative money flow
    min_periods = 0 if fillna else window
    n_positive_mf = mfr.rolling(window, min_periods=min_periods).apply(
        lambda x: np.sum(np.where(x >= 0.0, x, 0.0)), raw=True
    )
    n_negative_mf = abs(mfr.rolling(window, min_periods=min_periods).apply(
        lambda x: np.sum(np.where(x < 0.0, x, 0.0)), raw=True
    ))

    # Calculate Money Flow Index
    mfi = n_positive_mf / n_negative_mf
    mfi = 100 - (100 / (1 + mfi))
    if fillna:
        mfi = mfi.fillna(50)

    df_copy['mfi'] = mfi.round(2)

    return df_copy[['mfi']]


def NegativeVolumeIndex(df: pd.DataFrame, fillna: bool = False) -> pd.DataFrame:
    """
    Negative Volume Index (NVI)

    Uses volume changes to decide when the smart money is active.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - fillna (bool): if True, fill nan values.

    Call with:
        df['nvi'] = bta.NegativeVolumeIndex(df, fillna=True)['nvi']

    Returns:
    - pd.DataFrame: DataFrame with 'nvi' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate price change and volume decrease
    price_change = df_copy['close'].pct_change()
    vol_decrease = df_copy['volume'].shift(1) > df_copy['volume']

    # Initialize NVI series
    nvi = pd.Series(data=np.nan, index=df_copy.index, dtype="float64", name="nvi")
    nvi.iloc[0] = 1000

    # Calculate NVI
    for i in range(1, len(nvi)):
        if vol_decrease.iloc[i]:
            nvi.iloc[i] = nvi.iloc[i - 1] * (1.0 + price_change.iloc[i])
        else:
            nvi.iloc[i] = nvi.iloc[i - 1]

    if fillna:
        nvi = nvi.fillna(1000)

    df_copy['nvi'] = nvi.round(2)

    return df_copy[['nvi']]


def OnBalanceVolume(df: pd.DataFrame, fillna: bool = False) -> pd.DataFrame:
    """
    On-balance volume (OBV)

    Relates price and volume in the stock market. OBV is based on a cumulative total volume.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - fillna (bool): if True, fill nan values.

    Call with:
        df['obv'] = bta.OnBalanceVolume(df, fillna=True)['obv']

    Returns:
    - pd.DataFrame: DataFrame with 'obv' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate OBV
    obv = np.where(df_copy['close'] < df_copy['close'].shift(1), -df_copy['volume'], df_copy['volume'])
    obv = pd.Series(obv, index=df_copy.index).cumsum()

    if fillna:
        obv = obv.fillna(0)

    df_copy['obv'] = obv.round(2)

    return df_copy[['obv']]


def OnBalanceVolumeOscillator(df: pd.DataFrame, channel: int = 10, average: int = 21, fillna: bool = False) -> pd.DataFrame:
    """
    On Balance Volume (OBV) Oscillator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - channel (int): OBV Channel Length. Default is 10.
    - average (int): OBV Average Length. Default is 21.
    - fillna (bool): If True, fill nan values.

    Call with:
        df['obv_osc'] = bta.OnBalanceVolumeOscillator(df, channel=10, average=21, fillna=True)['obv_oscillator']

    Returns:
    - pd.DataFrame: DataFrame with 'obv_oscillator' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate OBV
    df_copy['change'] = df_copy['close'].diff()
    df_copy['obv'] = np.where(df_copy['change'] > 0, df_copy['volume'] * df_copy['change'], 
                              np.where(df_copy['change'] < 0, df_copy['volume'] * df_copy['change'], 0))
    df_copy['obv'] = df_copy['obv'].cumsum()

    # Calculate OBV Oscillator
    ema_obv_channel = df_copy['obv'].ewm(span=channel, adjust=False).mean()
    ema_abs_obv_channel = (df_copy['obv'] - ema_obv_channel).abs().ewm(span=channel, adjust=False).mean()
    df_copy['obv_oscillator'] = ((df_copy['obv'] - ema_obv_channel) / (0.015 * ema_abs_obv_channel)).ewm(span=average, adjust=False).mean()

    if fillna:
        df_copy['obv_oscillator'] = df_copy['obv_oscillator'].fillna(0)

    return df_copy[['obv_oscillator']]


def PriceVolumeTrend(df: pd.DataFrame, fillna: bool = False, smoothing_factor: int = None, signal_type: str = 'SMA', signal_length: int = 21, dropnans: bool = False) -> pd.DataFrame:
    """
    Price Volume trend (PVT)

    Based on cumulative volume that adds or subtracts a multiple of the percentage change in share price trend. 
    PVT = [((CurrentClose - PreviousClose) / PreviousClose) x Volume] + PreviousPVT
    Inspired by: https://www.tradingview.com/script/3Ah2ALck-Price-Volume-Trend/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - fillna (bool): If True, fill nan values.
    - smoothing_factor (int, optional): Will smooth PVT implementation with SMA.
    - signal_type (str): Type of signal smoothing ('SMA' or 'EMA').
    - signal_length (int): Length of the signal smoothing.
    - dropnans (bool): Drop nans after indicator calculated.

    Call with:
        pvt_df = bta.PriceVolumeTrend(df, fillna=True, signal_type='EMA', signal_length=21, dropnans=True)
        df['pvt'] = pvt_df['price_volume_trend']
        df['pvt_signal'] = pvt_df['signal']

    Returns:
    - pd.DataFrame: DataFrame with 'price_volume_trend' and 'signal' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Initialize PVT column
    df_copy['price_volume_trend'] = 0.0

    # Calculate PVT iteratively
    for i in range(1, len(df_copy)):
        prev_pvt = df_copy.at[i-1, 'price_volume_trend']
        price_change = (df_copy.at[i, 'close'] - df_copy.at[i-1, 'close']) / df_copy.at[i-1, 'close']
        df_copy.at[i, 'price_volume_trend'] = price_change * df_copy.at[i, 'volume'] + prev_pvt

    if smoothing_factor:
        min_periods = 0 if fillna else smoothing_factor
        df_copy['price_volume_trend'] = df_copy['price_volume_trend'].rolling(smoothing_factor, min_periods=min_periods).mean()
    if dropnans:
        df_copy['price_volume_trend'] = df_copy['price_volume_trend'].dropna()
    if fillna:
        df_copy['price_volume_trend'] = df_copy['price_volume_trend'].fillna(0)

    # Calculate signal
    if signal_type == 'SMA':
        df_copy['signal'] = df_copy['price_volume_trend'].rolling(window=signal_length, min_periods=1 if fillna else signal_length).mean()
    elif signal_type == 'EMA':
        df_copy['signal'] = df_copy['price_volume_trend'].ewm(span=signal_length, adjust=False, min_periods=1 if fillna else signal_length).mean()
    else:
        raise ValueError("signal_type must be either 'SMA' or 'EMA'")

    if dropnans:
        df_copy['signal'] = df_copy['signal'].dropna()
    if fillna:
        df_copy['signal'] = df_copy['signal'].fillna(0)

    df_copy['price_volume_trend'] = df_copy['price_volume_trend'].round(2)
    df_copy['signal'] = df_copy['signal'].round(2)

    return df_copy[['price_volume_trend', 'signal']]


def VolumeWeightedAveragePrice(df: pd.DataFrame, window: int = 14, fillna: bool = False) -> pd.DataFrame:
    """
    Volume Weighted Average Price (VWAP)
    Equals the dollar value of all trading periods divided by the total trading volume for the current day.

    Inspired by: https://www.tradingview.com/script/rSTNnV6B-VWAP-with-period/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): n period.
    - fillna (bool): If True, fill nan values.

    Call with:
        df['vwap'] = bta.VolumeWeightedAveragePrice(df, window=14, fillna=True)['volume_weighted_average_price']

    Returns:
    - pd.DataFrame: DataFrame with 'volume_weighted_average_price' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'close', 'volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate typical price
    typical_price = (df_copy['high'] + df_copy['low'] + df_copy['close']) / 3.0
    typical_price_volume = typical_price * df_copy['volume']

    min_periods = 0 if fillna else window
    total_pv = typical_price_volume.rolling(window, min_periods=min_periods).sum()
    total_volume = df_copy['volume'].rolling(window, min_periods=min_periods).sum()

    vwap = total_pv / total_volume
    if fillna:
        vwap = vwap.fillna(0)

    df_copy['volume_weighted_average_price'] = vwap.round(2)
    return df_copy[['volume_weighted_average_price']]

