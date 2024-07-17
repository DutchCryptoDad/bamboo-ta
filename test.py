# -*- coding: utf-8 -*-
# Import necessary libraries
# Importeer necessary libraries
import bamboo_ta.bamboo_ta as bta
#import pandas_ta as pta
import pandas as pd
from pandas import DataFrame
import numpy as np

# Create dataframe
# create dataframe and read the json data in the datasets directory
df = pd.read_json("./BTC_USDT-1d.json")
# name the columns that are loaded into the dataframe
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
# the date column consists of unix time in milliseconds, so this command changes this data into human readable form.
df['date'] = (pd.to_datetime(df['date'], unit='ms'))

# ========================================
### After refactoring:

# exhaustion = bta.Exhaustion_Bars(df)
# df['leledc_major'] = exhaustion['leledc_major']
# df['leledc_minor'] = exhaustion['leledc_minor']

# dynamic_exhaustion = bta.Dynamic_Exhaustion_Bars(df)
# df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
# df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']

# pin = bta.Pinbar(df)
# df['pinbar_sell'] = pin['pinbar_sell']
# df['pinbar_buy'] = pin['pinbar_buy']

# ha_df = bta.HeikinAshi(df)
# df['ha_close'] = ha_df['ha_close']
# df['ha_open'] = ha_df['ha_open']
# df['ha_high'] = ha_df['ha_high']
# df['ha_low'] = ha_df['ha_low']

# lr_df = bta.LinRegCandles(df)
# df['lrc_open'] = lr_df['bopen']
# df['lrc_high'] = lr_df['bhigh']
# df['lrc_low'] = lr_df['blow']
# df['lrc_close'] = lr_df['bclose']
# df['lrc_signal'] = lr_df['signal']

# df['ao'] = bta.Awesome_Oscillator(df['high'], df['low'], 5, 34)
# df['ao'] = bta.Awesome_Oscillator(df)

# df['cmo'] = bta.Chande_Momentum_Oscillator(df)

# df['ewo'] = bta.Elliott_Wave_Oscillator(df, "close", 5, 35)

# fisher = bta.Fisher_Center_Of_Gravity(df)
# df['fisher_cg'] = fisher['fisher_cg']
# df['fisher_sig'] = fisher['fisher_sig']

# ift = bta.Inverse_Fisher_Transform(df)
# df['ift'] = ift['ift']

# df['ift'] = bta.Inverse_Fisher_Transform(df)['ift']

# df['kama'] = bta.Kaufmans_Adaptive_Moving_Average(df)['kama']

# macd_result = bta.macd(df, "close", 12, 26, 9)
# df['macd'] = macd_result['macd']
# df['macd_signal'] = macd_result['macd_signal']
# df['macd_histogram'] = macd_result['macd_histogram']

# df['macd_leader'] = bta.MACD_Leader(df, 'close')

# df['mastreak'] = bta.ma_streak(df, period=4, column='close')['mastreak']

# ppo = bta.Percentage_Price_Oscillator(df)
# df['ppo'] = ppo['ppo']
# df['ppo_signal'] = ppo['ppo_signal']
# df['ppo_hist'] = ppo['ppo_hist']

# df['rmi'] = bta.Relative_Momentum_Index(df, length=20, mom=5)['rmi']

# df['roc'] = bta.Rate_Of_Change(df, column='close', period=21)['roc']

# df['sroc'] = bta.Smoothed_Rate_Of_Change(df, roclen=21, emalen=13, smooth=21)['sroc']

# wae = bta.Waddah_Attar_Explosion(df)
# df['trend_up'] = wae['trend_up']
# df['trend_down'] = wae['trend_down']
# df['explosion_line'] = wae['explosion_line']
# df['dead_zone_line'] = wae['dead_zone_line']

# wt = bta.Wave_Trend(df, chlen=10, avg=21, smalen=4)
# df['wt1'] = wt['wt1']
# df['wt2'] = wt['wt2']

# df['wto'] = bta.Wave_Trend_Oscillator(df, 'close')['wavetrend']

# qqe_mod = bta.QQE_Mod(df)
# df['qqe_line'] = qqe_mod['qqe_line']
# df['histo2'] = qqe_mod['histo2']
# df['qqe_up'] = qqe_mod['qqe_up']
# df['qqe_down'] = qqe_mod['qqe_down']

# df['rsi'] = bta.Relative_Strength_Index(df, column='close', period=14)['rsi']

# df['smi'] = bta.Stochastic_Momentum_Index(df, k_length=9, d_length=3)['smi']

# stoch_rsi = bta.Stochastic_RSI(df, 'close', 14, 3, 3)
# df['stoch_rsi'] = stoch_rsi['stoch_rsi']
# df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
# df['stoch_rsi_d'] = stoch_rsi['stoch_rsi_d']

# df['tsi'] = bta.True_Strength_Index(df, 'close', 25, 13)['tsi']

# df['uo'] = bta.Ultimate_Oscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']

# stoch = bta.Stochastics_Oscillator(df, 'high', 'low', 'close', 14, 3)
# df['stoch'] = stoch['stoch']
# df['stoch_signal'] = stoch['stoch_signal']
# df['stoch_hist'] = stoch['stoch_hist']

# df['williams_r'] = bta.Williams_R(df, 'high', 'low', 'close', 14)['williams_r']

# breakout = bta.Breakouts(df, length=20)
# df['support_level'] = breakout['support_level']
# df['resistance_level'] = breakout['resistance_level']
# df['support_breakout'] = breakout['support_breakout']
# df['resistance_breakout'] = breakout['resistance_breakout']
# df['support_retest'] = breakout['support_retest']
# df['potential_support_retest'] = breakout['potential_support_retest']
# df['resistance_retest'] = breakout['resistance_retest']
# df['potential_resistance_retest'] = breakout['potential_resistance_retest']

# df['bbtrend'] = bta.BollingerTrend(df, 'close', 20, 50, 2.0)['bbtrend']

df['ema'] = bta.EMA(df, "close", 50)

print(df.tail(25))

