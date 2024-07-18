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

# exhaustion = bta.ExhaustionBars(df)
# df['leledc_major'] = exhaustion['leledc_major']
# df['leledc_minor'] = exhaustion['leledc_minor']

# dynamic_exhaustion = bta.DynamicExhaustionBars(df)
# df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
# df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']

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

# df['ao'] = bta.AwesomeOscillator(df, 'high', 'low', 5, 34)['ao']

# df['cmo'] = bta.ChandeMomentumOscillator(df)

# df['ewo'] = bta.ElliottWaveOscillator(df, "close", 5, 35)

# fisher = bta.FisherCenterOfGravity(df)
# df['fisher_cg'] = fisher['fisher_cg']
# df['fisher_sig'] = fisher['fisher_sig']

# df['ift'] = bta.InverseFisherTransform(df)['ift']

# df['kama'] = bta.KaufmansAdaptiveMovingAverage(df)['kama']

# macd_result = bta.MACD(df, "close", 12, 26, 9)
# df['macd'] = macd_result['macd']
# df['macd_signal'] = macd_result['macd_signal']
# df['macd_histogram'] = macd_result['macd_histogram']

# df['macd_leader'] = bta.MACDLeader(df, 'close')['macd_leader']

# df['mastreak'] = bta.MAStreak(df, period=4, column='close')['mastreak']

# df['mastreak'] = bta.MAStreak(df, period=4, column='close')['mastreak']

# ppo = bta.PercentagePriceOscillator(df)
# df['ppo'] = ppo['ppo']
# df['ppo_signal'] = ppo['ppo_signal']
# df['ppo_hist'] = ppo['ppo_hist']

# df['rmi'] = bta.RelativeMomentumIndex(df, length=20, mom=5)['rmi']

# df['roc'] = bta.RateOfChange(df, column='close', period=21)['roc']

# df['sroc'] = bta.SmoothedRateOfChange(df, roclen=21, emalen=13, smooth=21)['sroc']

# wt = bta.WaveTrend(df, chlen=10, avg=21, smalen=4)
# df['wt1'] = wt['wt1']
# df['wt2'] = wt['wt2']

# df['rsi'] = bta.RelativeStrengthIndex(df, column='close', period=14)['rsi']

# df['smi'] = bta.StochasticMomentumIndex(df, k_length=9, d_length=3)['smi']

# stoch_rsi = bta.StochasticRSI(df, 'close', 14, 3, 3)
# df['stoch_rsi'] = stoch_rsi['stoch_rsi']
# df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
# df['stoch_rsi_d'] = stoch_rsi['stoch_rsi_d']

# df['tsi'] = bta.TrueStrengthIndex(df, 'close', 25, 13)['tsi']

# df['uo'] = bta.UltimateOscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']

# df['williams_r'] = bta.WilliamsR(df, 'high', 'low', 'close', 14)['williams_r']

# df['ema'] = bta.EMA(df, 'close', 50)['ema']
# df['hma'] = bta.HMA(df, 'close', 9)['hma']
# df['wma'] = bta.WMA(df, 'close', 10)['wma']
# df['lsma'] = bta.LSMA(df, 'close', 50)['lsma']

# pcc_result = bta.PercentPriceChannel(df, period=20, mult=2)
# df['pcc_upper'] = pcc_result['pcc_upper']
# df['pcc_rangema'] = pcc_result['pcc_rangema']
# df['pcc_lower'] = pcc_result['pcc_lower']
# df['zema'] = bta.ZEMA(df, 'close', 21)['zema']

# df['rma'] = bta.RMA(df, 'close', 14)['rma']
# df['sma'] = bta.SMA(df, 'close', 50)['sma']

# ssl_result = bta.SSLChannels(df, length=10, mode='sma')
# df['ssl_down'] = ssl_result['ssl_down']
# df['ssl_up'] = ssl_result['ssl_up']

# ssl_result = bta.SSLChannelsATR(df, length=7)
# df['ssl_atr_down'] = ssl_result['ssl_atr_down']
# df['ssl_atr_up'] = ssl_result['ssl_atr_up']

# df['t3_average'] = bta.T3(df, length=5)['t3_average']

# df['zlema'] = bta.ZLEMA(df, 'close', 21)['zlema']

# breakout = bta.Breakouts(df, length=20)
# df['support_level'] = breakout['support_level']
# df['resistance_level'] = breakout['resistance_level']
# df['support_breakout'] = breakout['support_breakout']
# df['resistance_breakout'] = breakout['resistance_breakout']
# df['support_retest'] = breakout['support_retest']
# df['potential_support_retest'] = breakout['potential_support_retest']
# df['resistance_retest'] = breakout['resistance_retest']
# df['potential_resistance_retest'] = breakout['potential_resistance_retest']

# stoch = bta.StochasticsOscillator(df, 'high', 'low', 'close', 14, 3)
# df['stoch'] = stoch['stoch']
# df['stoch_signal'] = stoch['stoch_signal']
# df['stoch_hist'] = stoch['stoch_hist']

# df['wto'] = bta.WaveTrendOscillator(df, 'close')['wavetrend']

# df['atr'] = bta.AverageTrueRange(df, 14)['atr']

# bb_result = bta.BollingerBands(df, 'close', 21, 2, 0)
# df['bb_upper'] = bb_result['bb_upper']
# df['bb_middle'] = bb_result['bb_middle']
# df['bb_lower'] = bb_result['bb_lower']

# df['true_range'] = bta.TrueRange(df)['true_range']

# df['bbtrend'] = bta.BollingerTrend(df, 'close', 20, 50, 2.0)['bbtrend']

# result = bta.bollinger_trend_fast_with_ma(df, 'close', 10, 50, 1.0, 2.0, 'SMA', 14)
# df['bollinger_trend_fast'] = result['bbtrend']
# df['bollinger_trend_fast_ma'] = result['bbtrend_ma']

# wae = bta.WaddahAttarExplosion(df)
# df['trend_up'] = wae['trend_up']
# df['trend_down'] = wae['trend_down']
# df['explosion_line'] = wae['explosion_line']
# df['dead_zone_line'] = wae['dead_zone_line']

# qqe_mod = bta.QQEMod(df)
# df['qqe_line'] = qqe_mod['qqe_line']
# df['histo2'] = qqe_mod['histo2']
# df['qqe_up'] = qqe_mod['qqe_up']
# df['qqe_down'] = qqe_mod['qqe_down']

# pin = bta.Pinbar(df)
# df['pinbar_sell'] = pin['pinbar_sell']
# df['pinbar_buy'] = pin['pinbar_buy']


# ### VOLUME INDICATORS TEST
# df['adi'] = bta.AccumulationDistributionIndex(df, fillna=True)['adi']
# df['cmf'] = bta.ChaikinMoneyFlow(df, window=20, fillna=True)['cmf']
# df['eom'] = bta.EaseOfMovement(df, window=14, fillna=True)['eom']
# df['seom'] = bta.EaseOfMovementSMA(df, window=14, fillna=True)['seom']
# df['fi'] = bta.ForceIndex(df, window=13, fillna=True)['fi']
# df['mfi']  = bta.MoneyFlowIndex(df, window=14, fillna=True)['mfi']
# df['nvi'] = bta.NegativeVolumeIndex(df, fillna=True)['nvi']
# df['obv'] = bta.OnBalanceVolume(df, fillna=True)['obv']
# df['obv_osc'] = bta.OnBalanceVolumeOscillator(df, channel=10, average=21, fillna=True)['obv_oscillator']
# df['vpt'] = bta.VolumePriceTrend(df, fillna=True, smoothing_factor=10, dropnans=True)['volume_price_trend']
# df['vwap'] = bta.VolumeWeightedAveragePrice(df, window=14, fillna=True)['volume_weighted_average_price']
# ###

#  TOT HIER GOED ++++++++++


print(df.tail(25))

