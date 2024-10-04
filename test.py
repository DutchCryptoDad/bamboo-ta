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

# # WERKT GOED!!!
# df['kama'] = bta.KaufmansAdaptiveMovingAverage(df)['kama']

# # # WERKT GOED!!!
# fscg = bta.EhlersFisherStochasticCenterOfGravity(df)
# df['CG'] = fscg['CG']
# df['Trigger'] = fscg['Trigger']

# # WERKT GOED!!!
# macd_result = bta.MACD(df, 'close', 12, 30, 9)
# df['macd'] = macd_result['macd']
# df['macd_signal'] = macd_result['macd_signal']
# df['macd_histogram'] = macd_result['macd_histogram']

# # # WERKT GOED!!!
# df['macd_leader'] = bta.MACDLeader(df, 'close', 12, 30, 9)['macd_leader']

# # WERKT GOED!!! https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/
# df['ma_streak'] = bta.MAStreak(df, length=10, src='close', matype=1)['ma_streak']

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
# https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/
# wt = bta.WaveTrend(df, chlen=10, avg=21, smalen=4)
# df['wt1'] = wt['wt1']
# df['wt2'] = wt['wt2']

# # WERKT GOED!!!
# df['rsi'] = bta.RelativeStrengthIndex(df, column='close', period=14)['rsi']

# # WERKT GOED!!!
# df['smi'] = bta.StochasticMomentumIndex(df, k_length=9, d_length=3)['smi']

# # WERKT GOED!!!
# stoch_rsi = bta.StochasticRSI(df, lengthRSI=14, lengthStoch=14, smoothK=3, smoothD=3)
# df['StochRSI_K'] = stoch_rsi['stoch_rsi_k']
# df['StochRSI_D'] = stoch_rsi['stoch_rsi_d']

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

# # # # WERKT GOED!!! # https://help.tradestation.com/10_00/eng/tradestationhelp/elanalysis/indicator/price_channel__percent_pc_indicator_.htm
# ppc_result = bta.PriceChannel(df, period=20)
# df['ppc_upper'] = ppc_result['ppc_upper']
# df['ppc_mid'] = ppc_result['ppc_mid']
# df['ppc_lower'] = ppc_result['ppc_lower']
# df['percent_p'] = ppc_result['percent_p']

# # # # WERKT GOED!!!
# df['zema'] = bta.ZEMA(df, 'close', 21)['zema']

## # # WERKT GOED!!!
# df['rma'] = bta.RMA(df, 'close', 14)['rma']

# # # WERKT GOED!!!
# df['sma'] = bta.SMA(df, 'close', 50)['sma']

# # # # # WERKT GOED!!!
# ssl_result = bta.SSLChannels(df, length=10, mode='sma')
# df['ssl_down'] = ssl_result['ssl_down']
# df['ssl_up'] = ssl_result['ssl_up']

# ## KLOPT NIET HELEMAAL< MAAR WEL BIJNA MET DE OPGEGEVEN INDICATOR: https://www.tradingview.com/script/SKHqWzql-SSL-ATR-channel/ GEACCEPTEERD RISICO HIER
# ssl_result = bta.SSLChannelsATR(df, column='open', length=14, atr_period=7)
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

# ## ONDUIDELIJK WELKE OSCILLATOR HIER NU WORDT GEBRUIKT NIET TE CONTROLEREN
# df['wto'] = bta.WaveTrendOscillator(df, 'close', 10, 21)['wavetrend']

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
# result = bta.BollingerTrendFastWithMA(df, 'close', 10, 50, 1.0, 2.0, 'SMA', 14)
# df['bollinger_trend_fast'] = result['bbtrend']
# df['bollinger_trend_fast_ma'] = result['bbtrend_ma']

# WERKT GOED!!! 
# wae = bta.WaddahAttarExplosion(df)
# df['trend_up'] = wae['trend_up']
# df['trend_down'] = wae['trend_down']
# df['explosion_line'] = wae['explosion_line']
# df['dead_zone_line'] = wae['dead_zone_line']

# # WERKT GOED!!! 
# wae_atr = bta.WaddahAttarExplosionAtr(df)
# df['trend_up'] = wae_atr['trend_up']
# df['trend_down'] = wae_atr['trend_down']
# df['explosion_line'] = wae_atr['explosion_line']
# df['dead_zone_line'] = wae_atr['dead_zone_line']

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


# # ## TEST FOR RegressionSlope
# slope_series = bta.RegressionSlope(df, lookback_period=20)
# df['slope'] = slope_series

# # ## TEST FOR DailyReturn
# daily_return_series = bta.DailyReturn(df, column='close', fillna=True)
# df['daily_return'] = daily_return_series

# # ## TEST FOR DailyLogReturn
# daily_log_return_series = bta.DailyLogReturn(df, column='close', fillna=True)
# df['daily_log_return'] = daily_log_return_series

# # ## TEST FOR CumulativeReturn
# cumulative_return_series = bta.CumulativeReturn(df, column='close', fillna=True)
# df['cumulative_return'] = cumulative_return_series

# # ## TEST FOR ExhaustionCandles
# maj_qual, min_qual = bta.ExhaustionCandles(df, window=1, multiplier=1)
# df['maj_qual'] = maj_qual
# df['min_qual'] = min_qual

# # ## TEST FOR ExhaustionLengths
# maj_len, min_len = bta.ExhaustionLengths(df)
# df['maj_len'] = maj_len
# df['min_len'] = min_len

# # ## TEST FOR GetMinMax
# min_max_series = bta.GetMinMax(df['high'], df['low'], function="min")
# df['min_max'] = min_max_series


# ## TEST FOR StDev
# stdev_series = bta.StDev(df['close'], period=20)
# df['stdev'] = stdev_series

# # ## TEST FOR ZScore
# zscore_series = bta.ZScore(df['close'], window=500)
# df['zscore'] = zscore_series

# # ## TEST FOR SameLength
# padded_series = bta.SameLength(df['high'].values, df['low'].values)
# df['padded_series'] = padded_series

# ## TEST FOR DropNa
# df_clean = bta.DropNa(df)

# # ## TEST FOR CrossedAbove
# crossed_above_series = bta.CrossedAbove(df['series1'], df['series2'])
# df['crossed_above'] = crossed_above_series


# # ## TEST FOR CrossedBelow
# crossed_below_series = bta.CrossedBelow(df['series1'], df['series2'])
# df['crossed_below'] = crossed_below_series

# # Import the function (assuming it's in a module named 'bta')
# trade_cols = bta.CalculateFixedStopLossTakeProfitWithSignal(
#     df, 
#     signal_column='trade_signal',
#     long_trade_signal='long_trade', 
#     short_trade_signal='short_trade', 
#     no_trade_signal='no_trade', 
#     lookback_period=3, 
#     long_risk_reward_ratio=2, 
#     short_risk_reward_ratio=2, 
#     buffer=0
# )

# # Add the result to the DataFrame (or inspect it separately)
# df[['stop_loss', 'entry_price', 'take_profit', 'trade_active', 'exit_reason']] = trade_cols


# df = bta.CalculateATRStopLossTakeProfit(df, signal_column='signal', atr_column='atr')



# Print the updated DataFrame with the new columns
print(df)


# ###
#  TOT HIER GOED ++++++++++


# print(df.tail(40))



# TODO: 





# 

# BUGGY INDICATORS..?
# # ## TEST FOR LinearDecay
# df['linear_decay'] =  bta.LinearDecay(start, end, start_time, end_time, trade_time)

# # ## TEST FOR LinearGrowth
# df['linear_growth'] = df.apply(lambda row: bta.LinearGrowth(50, 100, 0, 100, row['time']), axis=1)

# # ## TEST FOR PopulateLeledcMajorMinor
# leledc_df = bta.PopulateLeledcMajorMinor(df, maj_qual, min_qual, maj_len, min_len)
# df['leledc_major'] = leledc_df['leledc_major']
# df['leledc_minor'] = leledc_df['leledc_minor']

# 



print(df.tail(30))
