# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import EMA


def Accumulation_Distribution_Index(df, src_cols=('high', 'low', 'close', 'volume'), fillna=False):
    """
    Accumulation/Distribution Index (ADI)
    Acts as a leading indicator of price movements.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'high', 'low', 'close', and 'volume'. Default is ('high', 'low', 'close', 'volume').
    - fillna (bool): if True, fill nan values.

    Call with:
        adi_df = Accumulation_Distribution_Index(df, src_cols=('high', 'low', 'close', 'volume'), fillna=True)
        df['adi'] = adi_df['adi']

    Returns:
    - pd.DataFrame: DataFrame with 'adi' column.
    """
    high_col, low_col, close_col, volume_col = src_cols
    df_copy = df.copy()

    # Calculate the ADI values
    clv = ((df_copy[close_col] - df_copy[low_col]) - (df_copy[high_col] - df_copy[close_col])) / (df_copy[high_col] - df_copy[low_col])
    clv = clv.fillna(0.0)  # float division by zero
    adi = clv * df_copy[volume_col]
    adi = adi.cumsum()
    if fillna:
        adi = adi.fillna(0)

    df_copy['adi'] = adi

    return df_copy[['adi']]


def Chaikin_Money_Flow(df, src_cols=('high', 'low', 'close', 'volume'), window=20, fillna=False):
    """
    Chaikin Money Flow (CMF)
    Measures the amount of Money Flow Volume over a specific period.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'high', 'low', 'close', and 'volume'. Default is ('high', 'low', 'close', 'volume').
    - window (int): n period.
    - fillna (bool): if True, fill nan values.

    Call with:
        cmf_df = Chaikin_Money_Flow(df, src_cols=('high', 'low', 'close', 'volume'), window=20, fillna=True)
        df['cmf'] = cmf_df['cmf']

    Returns:
    - pd.DataFrame: DataFrame with 'cmf' column.
    """
    high_col, low_col, close_col, volume_col = src_cols
    df_copy = df.copy()

    # Calculate the CMF values
    mfv = ((df_copy[close_col] - df_copy[low_col]) - (df_copy[high_col] - df_copy[close_col])) / (df_copy[high_col] - df_copy[low_col])
    mfv = mfv.fillna(0.0)  # float division by zero
    mfv *= df_copy[volume_col]
    min_periods = 0 if fillna else window
    cmf = mfv.rolling(window, min_periods=min_periods).sum() / df_copy[volume_col].rolling(window, min_periods=min_periods).sum()
    if fillna:
        cmf = cmf.fillna(0)

    df_copy['cmf'] = cmf

    return df_copy[['cmf']]


def Ease_Of_Movement(df, src_cols=('high', 'low', 'volume'), window=14, fillna=False):
    """
    Ease of movement (EoM, EMV)
    Relates an asset's price change to its volume and is useful for assessing trend strength.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'high', 'low', and 'volume'. Default is ('high', 'low', 'volume').
    - window (int): n period.
    - fillna (bool): if True, fill nan values.

    Call with:
        eom_df = Ease_Of_Movement(df, src_cols=('high', 'low', 'volume'), window=14, fillna=True)
        df['eom'] = eom_df['eom']

    Returns:
    - pd.DataFrame: DataFrame with 'eom' column.
    """
    high_col, low_col, volume_col = src_cols
    df_copy = df.copy()

    # Calculate the Ease of Movement values
    emv = ((df_copy[high_col].diff(1) + df_copy[low_col].diff(1)) * (df_copy[high_col] - df_copy[low_col])) / (2 * df_copy[volume_col])
    emv *= 100000000
    if fillna:
        emv = emv.fillna(0)

    df_copy['eom'] = emv

    return df_copy[['eom']]


def Sma_Ease_Of_Movement(df, src_cols=('high', 'low', 'volume'), window=14, fillna=False):
    """
    Signal Ease of movement (EoM, EMV)
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'high', 'low', and 'volume'. Default is ('high', 'low', 'volume').
    - window (int): n period.
    - fillna (bool): if True, fill nan values.

    Call with:
        seom_df = Sma_Ease_Of_Movement(df, src_cols=('high', 'low', 'volume'), window=14, fillna=True)
        df['seom'] = seom_df['seom']

    Returns:
    - pd.DataFrame: DataFrame with 'seom' column.
    """
    emv_df = Ease_Of_Movement(df, src_cols=src_cols, window=window, fillna=fillna)
    min_periods = 0 if fillna else window
    sma_emv = emv_df['eom'].rolling(window, min_periods=min_periods).mean()
    if fillna:
        sma_emv = sma_emv.fillna(0)

    df_copy = df.copy()
    df_copy['seom'] = sma_emv

    return df_copy[['seom']]


def Force_Index(df, src_cols=('close', 'volume'), window=13, fillna=False):
    """
    Force Index (FI)
    Illustrates how strong the actual buying or selling pressure is.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'close' and 'volume'. Default is ('close', 'volume').
    - window (int): n period.
    - fillna (bool): if True, fill nan values.

    Call with:
        fi_df = Force_Index(df, src_cols=('close', 'volume'), window=13, fillna=True)
        df['fi'] = fi_df['fi']

    Returns:
    - pd.DataFrame: DataFrame with 'fi' column.
    """
    close_col, volume_col = src_cols
    df_copy = df.copy()

    # Calculate the Force Index values
    fi = (df_copy[close_col] - df_copy[close_col].shift(1)) * df_copy[volume_col]
    fi_ema = fi.ewm(span=window, adjust=False).mean()
    if fillna:
        fi_ema = fi_ema.fillna(0)

    df_copy['fi'] = fi_ema

    return df_copy[['fi']]


def Money_Flow_Index(df, src_cols=('high', 'low', 'close', 'volume'), window=14, fillna=False):
    """
    Money Flow Index (MFI)
    Uses both price and volume to measure buying and selling pressure.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'high', 'low', 'close', and 'volume'. Default is ('high', 'low', 'close', 'volume').
    - window (int): n period.
    - fillna (bool): if True, fill nan values.

    Call with:
        mfi_df = Money_Flow_Index(df, src_cols=('high', 'low', 'close', 'volume'), window=14, fillna=True)
        df['mfi'] = mfi_df['mfi']

    Returns:
    - pd.DataFrame: DataFrame with 'mfi' column.
    """
    high_col, low_col, close_col, volume_col = src_cols
    df_copy = df.copy()

    # Calculate typical price
    typical_price = (df_copy[high_col] + df_copy[low_col] + df_copy[close_col]) / 3.0
    up_down = np.where(
        typical_price > typical_price.shift(1),
        1,
        np.where(typical_price < typical_price.shift(1), -1, 0)
    )
    mfr = typical_price * df_copy[volume_col] * up_down

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

    df_copy['mfi'] = mfi

    return df_copy[['mfi']]


def Negative_Volume_Index(df, src_cols=('close', 'volume'), fillna=False):
    """
    Negative Volume Index (NVI)
    Uses volume changes to decide when the smart money is active.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'close' and 'volume'. Default is ('close', 'volume').
    - fillna (bool): if True, fill nan values.

    Call with:
        nvi_df = Negative_Volume_Index(df, src_cols=('close', 'volume'), fillna=True)
        df['nvi'] = nvi_df['nvi']

    Returns:
    - pd.DataFrame: DataFrame with 'nvi' column.
    """
    close_col, volume_col = src_cols
    df_copy = df.copy()

    # Calculate price change and volume decrease
    price_change = df_copy[close_col].pct_change()
    vol_decrease = df_copy[volume_col].shift(1) > df_copy[volume_col]

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

    df_copy['nvi'] = nvi

    return df_copy[['nvi']]


def On_Balance_Volume(df, src_cols=('close', 'volume'), fillna=False):
    """
    On-balance volume (OBV)
    Relates price and volume in the stock market. OBV is based on a cumulative total volume.
    
    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'close' and 'volume'. Default is ('close', 'volume').
    - fillna (bool): if True, fill nan values.

    Call with:
        obv_df = On_Balance_Volume(df, src_cols=('close', 'volume'), fillna=True)
        df['obv'] = obv_df['obv']

    Returns:
    - pd.DataFrame: DataFrame with 'obv' column.
    """
    close_col, volume_col = src_cols
    df_copy = df.copy()

    # Calculate OBV
    obv = np.where(df_copy[close_col] < df_copy[close_col].shift(1), -df_copy[volume_col], df_copy[volume_col])
    obv = pd.Series(obv, index=df_copy.index).cumsum()

    if fillna:
        obv = obv.fillna(0)

    df_copy['obv'] = obv

    return df_copy[['obv']]


def OBV_Oscillator(df, src_cols=('close', 'volume'), channel=10, average=21, fillna=False):
    """
    On Balance Volume (OBV) Oscillator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - src_cols (tuple): Tuple containing column names for 'close' and 'volume'. Default is ('close', 'volume').
    - channel (int): OBV Channel Length. Default is 10.
    - average (int): OBV Average Length. Default is 21.
    - fillna (bool): If True, fill nan values.

    Call with:
        obv_osc_df = OBV_Oscillator(df, src_cols=('close', 'volume'), channel=10, average=21, fillna=True)
        df['OBV_Oscillator'] = obv_osc_df['OBV_Oscillator']

    Returns:
    - pd.DataFrame: DataFrame with 'OBV_Oscillator' column.
    """
    close_col, volume_col = src_cols
    df_copy = df.copy()

    # Calculate OBV
    df_copy['change'] = df_copy[close_col].diff()
    df_copy['OBV'] = np.where(df_copy['change'] > 0, df_copy[volume_col] * df_copy['change'], 
                              np.where(df_copy['change'] < 0, df_copy[volume_col] * df_copy['change'], 0))
    df_copy['OBV'] = df_copy['OBV'].cumsum()

    # Calculate OBV Oscillator
    ema_obv_channel = df_copy['OBV'].ewm(span=channel, adjust=False).mean()
    ema_abs_obv_channel = (df_copy['OBV'] - ema_obv_channel).abs().ewm(span=channel, adjust=False).mean()
    df_copy['OBV_Oscillator'] = ((df_copy['OBV'] - ema_obv_channel) / (0.015 * ema_abs_obv_channel)).ewm(span=average, adjust=False).mean()

    if fillna:
        df_copy['OBV_Oscillator'] = df_copy['OBV_Oscillator'].fillna(0)

    return df_copy[['OBV_Oscillator']]


def Volume_Price_Trend(df, src_cols=('close', 'volume'), fillna=False, smoothing_factor=None, dropnans=False):
    """
    Volume-price trend (VPT)
    Based on cumulative volume that adds or subtracts a multiple of the percentage change in share price trend.

    Call with:
        vpt_df = Volume_Price_Trend(df, src_cols=('close', 'volume'), fillna=True, smoothing_factor=10, dropnans=True)
        df['Volume_Price_Trend'] = vpt_df['Volume_Price_Trend']

    Args:
        df (pd.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
        src_cols (tuple): Tuple containing column names for 'close' and 'volume'. Default is ('close', 'volume').
        fillna (bool): If True, fill nan values.
        smoothing_factor (int, optional): Will smooth VPT implementation with SMA.
        dropnans (bool): Drop nans after indicator calculated.

    Returns:
        pd.DataFrame: DataFrame with 'Volume_Price_Trend' column.
    """
    close_col, volume_col = src_cols
    df_copy = df.copy()

    vpt = (df_copy[close_col].pct_change() * df_copy[volume_col]).cumsum()
    if smoothing_factor:
        min_periods = 0 if fillna else smoothing_factor
        vpt = vpt.rolling(smoothing_factor, min_periods=min_periods).mean()
    if dropnans:
        vpt = vpt.dropna()
    if fillna:
        vpt = vpt.fillna(0)

    df_copy['Volume_Price_Trend'] = vpt
    return df_copy[['Volume_Price_Trend']]


def Volume_Weighted_Average_Price(df, src_cols=('high', 'low', 'close', 'volume'), window=14, fillna=False):
    """
    Volume Weighted Average Price (VWAP)
    Equals the dollar value of all trading periods divided by the total trading volume for the current day.

    Call with:
        vwap_df = Volume_Weighted_Average_Price(df, src_cols=('high', 'low', 'close', 'volume'), window=14, fillna=True)
        df['Volume_Weighted_Average_Price'] = vwap_df['Volume_Weighted_Average_Price']

    Args:
        df (pd.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
        src_cols (tuple): Tuple containing column names for 'high', 'low', 'close', and 'volume'. Default is ('high', 'low', 'close', 'volume').
        window (int): n period.
        fillna (bool): If True, fill nan values.

    Returns:
        pd.DataFrame: DataFrame with 'Volume_Weighted_Average_Price' column.
    """
    high_col, low_col, close_col, volume_col = src_cols
    df_copy = df.copy()

    typical_price = (df_copy[high_col] + df_copy[low_col] + df_copy[close_col]) / 3.0
    typical_price_volume = typical_price * df_copy[volume_col]

    min_periods = 0 if fillna else window
    total_pv = typical_price_volume.rolling(window, min_periods=min_periods).sum()
    total_volume = df_copy[volume_col].rolling(window, min_periods=min_periods).sum()

    vwap = total_pv / total_volume
    if fillna:
        vwap = vwap.fillna(0)

    df_copy['Volume_Weighted_Average_Price'] = vwap
    return df_copy[['Volume_Weighted_Average_Price']]
