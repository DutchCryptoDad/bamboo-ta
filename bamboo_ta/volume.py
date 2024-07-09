# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import EMA


def OBV_Oscillator(df, channel=10, average=21):
    """
    On Balance Volume (OBV) Oscillator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - channel (int): OBV Channel Length. Default is 10.
    - average (int): OBV Average Length. Default is 21.

    Call with:
        obv_osc = OBV_Oscillator(df)
        df['OBV_Oscillator'] = obv_osc['OBV_Oscillator']

    Returns:
    - pd.DataFrame: DataFrame with 'OBV_Oscillator' column.
    """
    df_copy = df.copy()

    # Calculate OBV
    df_copy['change'] = df_copy['close'].diff()
    df_copy['OBV'] = np.where(df_copy['change'] > 0, df_copy['volume'] * df_copy['change'], 
                              np.where(df_copy['change'] < 0, df_copy['volume'] * df_copy['change'], 0))
    df_copy['OBV'] = df_copy['OBV'].cumsum()

    # Calculate OBV Oscillator
    ema_obv_channel = df_copy['OBV'].ewm(span=channel, adjust=False).mean()
    ema_abs_obv_channel = (df_copy['OBV'] - ema_obv_channel).abs().ewm(span=channel, adjust=False).mean()
    df_copy['OBV_Oscillator'] = ((df_copy['OBV'] - ema_obv_channel) / (0.015 * ema_abs_obv_channel)).ewm(span=average, adjust=False).mean()

    return df_copy[['OBV_Oscillator']]

