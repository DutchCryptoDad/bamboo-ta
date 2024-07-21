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

### CANDLES.PY FUNCTIES ###

# VERDER UIT TE VINDEN WAT DEZE INDICATOR DOET...
# exhaustion = bta.ExhaustionBars(df)
# df['leledc_major'] = exhaustion['leledc_major']
# df['leledc_minor'] = exhaustion['leledc_minor']

# VERDER UIT TE VINDEN WAT DEZE INDICATOR DOET...
# dynamic_exhaustion = bta.DynamicExhaustionBars(df)
# df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
# df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']

## TWIJFELACHTIG, KOMT NIET OVEREEN MET https://www.tradingview.com/script/RF6to9Nk-PINBAR-By-Bhajanpreet/ of https://www.tradingview.com/script/JO3S0SLV/
# FUNCTIE LIJKT ANDERS TE WERKEN MET STOCHASTICS< VERDER TE ANALYSEREN
# pin = bta.Pinbar(df)
# df['pinbar_sell'] = pin['pinbar_sell']
# df['pinbar_buy'] = pin['pinbar_buy']

# # WERKT GOED!!!
# ha_df = bta.HeikinAshi(df)
# df['ha_open'] = ha_df['ha_open']
# df['ha_high'] = ha_df['ha_high']
# df['ha_low'] = ha_df['ha_low']
# df['ha_close'] = ha_df['ha_close']

# # # WERKT GOED!!!
# lr_df = bta.LinRegCandles(df)
# df['lrc_open'] = lr_df['bopen']
# df['lrc_high'] = lr_df['bhigh']
# df['lrc_low'] = lr_df['blow']
# df['lrc_close'] = lr_df['bclose']
# df['lrc_signal'] = lr_df['signal']

### MOMENTUM.PY FUNCTIES ###

# # # WERKT GOED!!!
# df['ao'] = bta.AwesomeOscillator(df, 'high', 'low', 5, 34)['ao']
# # # WERKT GOED!!!
# df['cmo'] = bta.ChandeMomentumOscillator(df)
# # # WERKT GOED!!!
# df['ewo'] = bta.ElliottWaveOscillator(df, "close", 5, 35)

## DOES NOT HAVE SAME VALUES AS https://tradingview.com/script/5BT3a9mJ-Fisher-Stochastic-Center-of-Gravity/
# fisher = bta.FisherCenterOfGravity(df)
# df['fisher_cg'] = fisher['fisher_cg']
# df['fisher_sig'] = fisher['fisher_sig']

## DOES NOT HAVE SAME VALUES AS https://www.tradingview.com/script/8OxW1SF4-3-more-indicators-Inverse-Fisher-on-RSI-MFI-and-CyberCycle/
# df['ift'] = bta.InverseFisherTransform(df)['ift']

# # WERKT GOED!!!
# df['kama'] = bta.KaufmansAdaptiveMovingAverage(df)['kama']

# # WERKT GOED!!!
# macd_result = bta.MACD(df, "close", 12, 26, 9)
# df['macd'] = macd_result['macd']
# df['macd_signal'] = macd_result['macd_signal']
# df['macd_histogram'] = macd_result['macd_histogram']

# # WERKT GOED!!!
# df['macd_leader'] = bta.MACDLeader(df, 'close')['macd_leader']

## WERKT NIET GOED CONFORM https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/
# df['mastreak'] = bta.MAStreak(df, period=10, column='close')['mastreak']

# # WERKT GOED!!!
# ppo = bta.PercentagePriceOscillator(df)
# df['ppo'] = ppo['ppo']
# df['ppo_signal'] = ppo['ppo_signal']
# df['ppo_hist'] = ppo['ppo_hist']

# GOED VOLGENS https://www.tradingview.com/script/DdT7MmPa/
# Maar liever ombouwen naar: https://www.tradingview.com/script/kwIt9OgQ-Relative-Momentum-Index/
# df['rmi'] = bta.RelativeMomentumIndex(df, length=20, mom=5)['rmi']

# # WERKT GOED!!!
# df['roc'] = bta.RateOfChange(df, column='close', period=21)['roc']

# # WERKT GOED!!!
# df['sroc'] = bta.SmoothedRateOfChange(df, roclen=21, emalen=13, smooth=21)['sroc']

# # # WERKT GOED!!!
# # https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/
# wt = bta.WaveTrend(df, chlen=10, avg=21, smalen=4)
# df['wt1'] = wt['wt1']
# df['wt2'] = wt['wt2']

# # WERKT GOED!!!
# df['rsi'] = bta.RelativeStrengthIndex(df, column='close', period=14)['rsi']

# # WERKT GOED!!!
# df['smi'] = bta.StochasticMomentumIndex(df, k_length=9, d_length=3)['smi']

# FOUTIEF EN MOET UITGEZOCHT WORDEN!!!!
# stoch_rsi = bta.StochasticRSI(df, 'close', 14, 3, 3)
# df['stoch_rsi'] = stoch_rsi['stoch_rsi']
# df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
# df['stoch_rsi_d'] = stoch_rsi['stoch_rsi_d']

# # # WERKT GOED!!!
# df['tsi'] = bta.TrueStrengthIndex(df, 'close', 25, 13)['tsi']
# # # WERKT GOED!!!
# df['uo'] = bta.UltimateOscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']

# # WERKT CONFORM https://www.tradingview.com/script/REGZq58T-Williams-R/
# df['williams_r'] = bta.WilliamsR(df, 'high', 'low', 'close', 14)['williams_r']

#### TREND.PY ####

# # # WERKT GOED!!!
# df['ema'] = bta.EMA(df, 'close', 9)['ema']
# # # WERKT GOED!!!
# df['hma'] = bta.HMA(df, 'close', 9)['hma']
# # # WERKT GOED!!!
# df['wma'] = bta.WMA(df, 'close', 30)['wma']
# # # WERKT GOED!!!
# df['lsma'] = bta.LSMA(df, 'close', 25)['lsma']

## KLOPT NIET MET DE OPGEGEVEN INDICATOR: https://www.tradingview.com/script/6wwAWXA1-MA-Streak-Change-Channel/
# pcc_result = bta.PercentPriceChannel(df, period=20, mult=2)
# df['pcc_upper'] = pcc_result['pcc_upper']
# df['pcc_rangema'] = pcc_result['pcc_rangema']
# df['pcc_lower'] = pcc_result['pcc_lower']

# # # # WERKT GOED!!!
# df['zema'] = bta.ZEMA(df, 'close', 21)['zema']

## UITZOEKEN OF DEZE GOED WERKT, GEEN INDICATOR HIERVAN TE VINDEN VREEMD GENOEG
# df['rma'] = bta.RMA(df, 'close', 14)['rma']

# # # WERKT GOED!!!
# df['sma'] = bta.SMA(df, 'close', 50)['sma']

# # # # # WERKT GOED!!!
# ssl_result = bta.SSLChannels(df, length=10, mode='sma')
# df['ssl_down'] = ssl_result['ssl_down']
# df['ssl_up'] = ssl_result['ssl_up']


# ## KLOPT NIET MET DE OPGEGEVEN INDICATOR: https://www.tradingview.com/script/SKHqWzql-SSL-ATR-channel/
# ssl_result = bta.SSLChannelsATR(df, length=21)
# df['ssl_atr_down'] = ssl_result['ssl_atr_down']
# df['ssl_atr_up'] = ssl_result['ssl_atr_up']

# # WERKT GOED!!!
# df['t3_average'] = bta.T3(df, length=5)['t3_average']

# # WERKT GOED!!!
# df['zlema'] = bta.ZLEMA(df, 'close', 21)['zlema']

## CANNOT VERIFY THIS - HAVE TO TRUST THE BUILDER
# breakout = bta.Breakouts(df, length=20)
# df['support_level'] = breakout['support_level']
# df['resistance_level'] = breakout['resistance_level']
# df['support_breakout'] = breakout['support_breakout']
# df['resistance_breakout'] = breakout['resistance_breakout']
# df['support_retest'] = breakout['support_retest']
# df['potential_support_retest'] = breakout['potential_support_retest']
# df['resistance_retest'] = breakout['resistance_retest']
# df['potential_resistance_retest'] = breakout['potential_resistance_retest']

## WERKT GOED!!! TESTED AGAINST THE DEFAULTBUILDIN TV Stochastic (STOCH) https://www.tradingview.com/chart/?symbol=BINANCE%3ABTCUSDT&solution=43000502332
# stoch = bta.StochasticsOscillator(df, 'high', 'low', 'close', 14, 3)
# df['stoch'] = stoch['stoch']
# df['stoch_signal'] = stoch['stoch_signal']
# df['stoch_hist'] = stoch['stoch_hist']

# ## KLOPT NIET ONDUIDELIJK WELKE OSCILLATOR HIER NU WORDT GEBRUIKT
df['wto'] = bta.WaveTrendOscillator(df, 'close', 10, 21)['wavetrend']

# ## WERKT GOED!!! 
# df['atr'] = bta.AverageTrueRange(df, 14)['atr']

# ## WERKT GOED!!! 
# bb_result = bta.BollingerBands(df, 'close', 20, 2, 0)
# df['bb_upper'] = bb_result['bb_upper']
# df['bb_middle'] = bb_result['bb_middle']
# df['bb_lower'] = bb_result['bb_lower']

# ## WERKT GOED!!! 
# df['true_range'] = bta.TrueRange(df)['true_range']

# # ## WERKT GOED!!! 
# df['bbtrend'] = bta.BollingerTrend(df, 'close', 20, 50, 2.0)['bbtrend']

# # ## WERKT GOED!!! 
# result = bta.bollinger_trend_fast_with_ma(df, 'close', 10, 50, 1.0, 2.0, 'SMA', 14)
# df['bollinger_trend_fast'] = result['bbtrend']
# df['bollinger_trend_fast_ma'] = result['bbtrend_ma']

## WERKT GOED!!! 
# wae = bta.WaddahAttarExplosion(df)
# df['trend_up'] = wae['trend_up']
# df['trend_down'] = wae['trend_down']
# df['explosion_line'] = wae['explosion_line']
# df['dead_zone_line'] = wae['dead_zone_line']

## WERKT BIJNA GOED, ALLEEN DE QQE LIJN VERTOONT AFWIJKINGEN TOV https://www.tradingview.com/script/TpUW4muw-QQE-MOD/
# qqe_mod = bta.QQEMod(df)
# qqe_mod = bta.QQEMod(df, 6, 5, 3, 3, 50, 0.35, 6, 5, 1.61, 3)
# df['qqe_line'] = qqe_mod['qqe_line']
# df['histo2'] = qqe_mod['histo2']
# df['qqe_up'] = qqe_mod['qqe_up']
# df['qqe_down'] = qqe_mod['qqe_down']


# qqe_df = bta.QQE(df, rsi_period=6, sf=5, qqe_factor=4.238, threshold=10, fillna=True)
# df['rsi_ma'] = qqe_df['rsi_ma']
# df['fast_atr_rsi_tl'] = qqe_df['fast_atr_rsi_tl']
# df['histogram'] = qqe_df['histogram']


# ### VOLUME INDICATORS TEST

## WERKT GOED!!!
# df['adi'] = bta.AccumulationDistributionIndex(df, fillna=True)['adi']

## WERKT GOED!!!
# df['cmf'] = bta.ChaikinMoneyFlow(df, window=20, fillna=True)['cmf']

## WERKT GOED!!!
# eom_df = bta.EaseOfMovement(df, eom_length=14, seom_length=14, fillna=True)
# df['eom'] = eom_df['eom']
# df['eom_ma'] = eom_df['eom_ma']

# ## WERKT GOED!!!
# df['fi'] = bta.ForceIndex(df, window=13, fillna=True)['fi']

# ## WERKT GOED!!!
# df['mfi']  = bta.MoneyFlowIndex(df, window=14, fillna=True)['mfi']

# ## WERKT GOED!!!
# nvi_df = bta.NegativeVolumeIndex(df, signal_type='EMA', signal_length=255, fillna=True)
# df['nvi'] = nvi_df['nvi']
# df['nvi_signal'] = nvi_df['nvi_signal']

# ## WERKT GOED!!!
# pvi_df = bta.PositiveVolumeIndex(df, signal_type='EMA', signal_length=255, fillna=True)
# df['pvi'] = pvi_df['pvi']
# df['pvi_signal'] = pvi_df['pvi_signal']


# ## WERKT GOED!!
# obv_df = bta.OnBalanceVolume(df, signal_type='SMA', signal_length=21, show_signal=True, fillna=True)
# df['obv'] = obv_df['obv']
# df['signal'] = obv_df['signal']

# ## WERKT GOED!!!
# df['obv_osc'] = bta.OnBalanceVolumeOscillator(df, length=20, fillna=True)['obv_oscillator']

# # # WERKT BIJNA HETZELFDE ALS https://www.tradingview.com/script/3Ah2ALck-Price-Volume-Trend/
# pvt_df = bta.PriceVolumeTrend(df, fillna=True, signal_type='SMA', signal_length=21, dropnans=True)
# df['pvt'] = pvt_df['price_volume_trend']
# df['pvt_signal'] = pvt_df['signal']

# ## WERKT GOED conform https://www.tradingview.com/script/rSTNnV6B-VWAP-with-period/!!!
# df['vwap'] = bta.VolumeWeightedAveragePrice(df, window=14, fillna=True)['volume_weighted_average_price']


# ###
#  TOT HIER GOED ++++++++++


print(df.tail(40))

