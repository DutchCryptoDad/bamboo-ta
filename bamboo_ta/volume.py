# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import EMA


# def OBV_Oscillator(df, channel=10, average=21):
#     """
#     On Balance Volume (OBV) Oscillator

#     Parameters:
#     - df (pandas.DataFrame): Input DataFrame which should contain columns: 'close' and 'volume'.
#     - channel (int): Length for the OBV EMA. Default is 10.
#     - average (int): Length for the oscillator EMA. Default is 21.

#     Call with:
#         obv = OBV_Oscillator(df)
#         df['obv_oscillator'] = obv['obv_oscillator']

#     Returns:
#     - pd.DataFrame: DataFrame with 'obv_oscillator' column.
#     """
#     df_copy = df.copy()

#     # Ensure the DataFrame contains the required columns
#     required_columns = ['close', 'volume']
#     for col in required_columns:
#         if col not in df.columns:
#             raise KeyError(f"DataFrame must contain '{col}' column")

#     # Calculate OBV
#     obv = np.where(df['close'].diff() > 0, df['volume'], 
#                    np.where(df['close'].diff() < 0, -df['volume'], 0))
#     obv = np.cumsum(obv)
#     df_copy['obv'] = obv
    
#     # Calculate EMA of OBV
#     obv_ema_channel = EMA(df_copy.assign(obv=obv), 'obv', channel)
    
#     # Calculate the difference between OBV and its EMA
#     obv_diff = obv - obv_ema_channel
    
#     # Calculate the absolute value of the difference and its EMA
#     abs_obv_diff = np.abs(obv_diff)
#     abs_obv_diff_ema_channel = EMA(df_copy.assign(abs_obv_diff=abs_obv_diff), 'abs_obv_diff', channel)
    
#     # Calculate the oscillator
#     oscillator = EMA(df_copy.assign(obv_diff=obv_diff / (0.015 * abs_obv_diff_ema_channel)), 'obv_diff', average)

#     df_copy['obv_oscillator'] = oscillator.round(2)
    
#     return df_copy[['obv_oscillator']]



# def OBV_Oscillator(df, n1=10, n2=21):
#     """
#     On Balance Volume (OBV) Oscillator

#     Parameters:
#     - df (pandas.DataFrame): Input DataFrame which should contain columns: 'close' and 'volume'.
#     - n1 (int): Length for the OBV EMA. Default is 10.
#     - n2 (int): Length for the oscillator EMA. Default is 21.

#     Call with:
#         obv = OBV_Oscillator(df)
#         df['obv_oscillator'] = obv['obv_oscillator']

#     Returns:
#     - pd.DataFrame: DataFrame with 'obv_oscillator' column.
#     """
#     df_copy = df.copy()

#     # Ensure the DataFrame contains the required columns
#     required_columns = ['close', 'volume']
#     for col in required_columns:
#         if col not in df.columns:
#             raise KeyError(f"DataFrame must contain '{col}' column")

#     obv = np.where(df['close'].diff() > 0, df['volume'], 
#                    np.where(df['close'].diff() < 0, -df['volume'], 0))
#     obv = np.cumsum(obv)
#     obv_series = pd.Series(obv, index=df.index)
#     obv_ema_n1 = EMA(df.assign(obv=obv_series), 'obv', n1)
#     obv_diff = obv_series - obv_ema_n1
#     abs_obv_diff = np.abs(obv_diff)
#     oscillator = EMA(df.assign(obv_diff=obv_diff), 'obv_diff', n2) / (0.015 * EMA(df.assign(abs_obv_diff=abs_obv_diff), 'abs_obv_diff', n1))

#     df_copy['obv_oscillator'] = oscillator.round(2)
    
#     return df_copy[['obv_oscillator']]