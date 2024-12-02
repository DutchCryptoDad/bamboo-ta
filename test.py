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

# # GOOD
# exhaustion = bta.exhaustion_bars(df)
# df['leledc_major'] = exhaustion['leledc_major']
# df['leledc_minor'] = exhaustion['leledc_minor']

# # # GOOD
# dynamic_exhaustion = bta.dynamic_exhaustion_bars(df)
# df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
# df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']

# # # GOOD
# ha_df = bta.heiken_ashi(df)
# df['ha_open'] = ha_df['ha_open']
# df['ha_high'] = ha_df['ha_high']
# df['ha_low'] = ha_df['ha_low']
# df['ha_close'] = ha_df['ha_close']

# # # GOOD
# hha_result = bta.hansen_heiken_ashi(df, period=6)
# df['hha_emac'] = hha_result['emac']
# df['hha_emao'] = hha_result['emao']

# # GOOD
# lr_df = bta.linear_regression_candles(df)
# df['lrc_open'] = lr_df['bopen']
# df['lrc_high'] = lr_df['bhigh']
# df['lrc_low'] = lr_df['blow']
# df['lrc_close'] = lr_df['bclose']
# df['lrc_signal'] = lr_df['signal']

# ## MOMENTUM.PY FUNCTIES ###

# # # WERKT GOED!!!
# df['ao'] = bta.awesome_oscillator(df, 'high', 'low', 5, 34)['ao']

# # # # WERKT GOED!!!
# df['cmo'] = bta.chande_momentum_oscillator(df)

# # # # WERKT GOED!!!
# df['ewo'] = bta.elliott_wave_oscillator(df, 'close', 5, 35)

# # # WERKT GOED!!!
# fscg = bta.ehlers_fisher_stochastic_center_of_gravity(df)
# df['cg'] = fscg['cg']
# df['trigger'] = fscg['trigger']

# # # WERKT GOED!!!
# df['kama'] = bta.kaufmans_adaptive_moving_average(df)['kama']

# # WERKT GOED!!!
# macd_result = bta.macd(df, 'close', 12, 26, 9)
# df['macd'] = macd_result['macd']
# df['macd_signal'] = macd_result['macd_signal']
# df['macd_histogram'] = macd_result['macd_histogram']

# # # # WERKT GOED!!!
# df['macd_leader'] = bta.macd_leader(df, 'close')['macd_leader']

# # # WERKT GOED!!! https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/
# df['ma_streak'] = bta.ma_streak(df, length=10, src='close', matype=1)['ma_streak']

# # # WERKT GOED!!!
# ppo = bta.percentage_price_oscillator(df)
# df['ppo'] = ppo['ppo']
# df['ppo_signal'] = ppo['ppo_signal']
# df['ppo_hist'] = ppo['ppo_hist']

# pvo = bta.percentage_volume_oscillator(df)
# df['pvo'] = pvo['pvo']
# df['pvo_signal'] = pvo['pvo_signal']
# df['pvo_hist'] = pvo['pvo_hist']

# # GOED VOLGENS https://www.tradingview.com/script/DdT7MmPa/
# # Maar liever ombouwen naar: https://www.tradingview.com/script/kwIt9OgQ-Relative-Momentum-Index/
# df['rmi'] = bta.relative_momentum_index(df, length=20, mom=5)['rmi']

# # # WERKT GOED!!!
# df['roc'] = bta.rate_of_change(df, column='close', period=21)['roc']

# # # WERKT GOED!!!
# df['sroc'] = bta.smoothed_rate_of_change(df, roclen=21, emalen=13, smooth=21)['sroc']

# # # WERKT GOED!!!
# wae = bta.waddah_attar_explosion_atr(df)
# df['trend_up'] = wae['trend_up']
# df['trend_down'] = wae['trend_down']
# df['explosion_line'] = wae['explosion_line']
# df['dead_zone_line'] = wae['dead_zone_line']

# # # WERKT GOED!!!
# wae = bta.waddah_attar_explosion(df)
# df['trend_up'] = wae['trend_up']
# df['trend_down'] = wae['trend_down']
# df['explosion_line'] = wae['explosion_line']
# df['dead_zone_line'] = wae['dead_zone_line']

# # # # WERKT GOED!!!
# # https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/
# wt = bta.wave_trend(df, chlen=10, avg=21, smalen=4)
# df['wt1'] = wt['wt1']
# df['wt2'] = wt['wt2']

# # # WERKT GOED!!!
# df['wto'] = bta.wave_trend_oscillator(df, 'close')['wavetrend']

# qqe_mod = bta.qqe_mod(df, 6, 5, 3, 3, 50, 0.35, 6, 5, 1.61, 3)
# df['qqe_line'] = qqe_mod['qqe_line']
# df['histo2'] = qqe_mod['histo2']
# df['qqe_up'] = qqe_mod['qqe_up']
# df['qqe_down'] = qqe_mod['qqe_down']

# # WERKT GOED!!!
# df['rsi'] = bta.relative_strength_index(df, column='close', period=14)['rsi']

# # # WERKT GOED!!!
# df['smi'] = bta.stochastic_momentum_index(df, k_length=9, d_length=3)['smi']

# stoch = bta.stochastics_oscillator(df, 'high', 'low', 'close', 14, 3)
# df['stoch'] = stoch['stoch']
# df['stoch_signal'] = stoch['stoch_signal']
# df['stoch_hist'] = stoch['stoch_hist']

# # # WERKT GOED!!!
# stoch_rsi = bta.stochastic_rsi(df, length_rsi=14, length_stoch=14, smooth_k=3, smooth_d=3)
# df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
# df['stoch_rsi_d'] = stoch_rsi['stoch_rsi_d']

# # # # WERKT GOED!!!
# df['tsi'] = bta.true_strength_index(df, 'close', 25, 13)['tsi']
# # # # WERKT GOED!!!
# df['uo'] = bta.ultimate_oscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']

# # # WERKT CONFORM https://www.tradingview.com/script/REGZq58T-Williams-R/
# df['williams_r'] = bta.williams_r(df, 'high', 'low', 'close', 14)['williams_r']


# ### TREND.PY ####

# alligator_result = bta.alligator_bands(df, 'close', 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
# df['jaw'] = alligator_result['jaw']
# df['teeth'] = alligator_result['teeth']
# df['lips'] = alligator_result['lips']

# df['bbtrend'] = bta.bollinger_trend(df, 'close', 20, 50, 2.0)['bbtrend']

# result = bta.bollinger_trend_fast_with_ma(df, 'close', 10, 50, 1.0, 2.0, 'SMA', 14)
# df['bollinger_trend_fast'] = result['bbtrend']
# df['bollinger_trend_fast_ma'] = result['bbtrend_ma']

# # # # WERKT GOED!!!
# breakout = bta.breakouts(df, length=20)
# df['support_level'] = breakout['support_level']
# df['resistance_level'] = breakout['resistance_level']
# df['support_breakout'] = breakout['support_breakout']
# df['resistance_breakout'] = breakout['resistance_breakout']
# df['support_retest'] = breakout['support_retest']
# df['potential_support_retest'] = breakout['potential_support_retest']
# df['resistance_retest'] = breakout['resistance_retest']
# df['potential_resistance_retest'] = breakout['potential_resistance_retest']


# # # WERKT GOED!!!
# df['ema'] = bta.exponential_moving_average(df, "close", 21)
# # # # WERKT GOED!!!
# df['hma'] = bta.hull_moving_average(df, 'close', 9)['hma']
# # # # WERKT GOED!!!
# df['wma'] = bta.weighted_moving_average(df, 'close', 10)['wma']
# # # # WERKT GOED!!!
# df['lsma'] = bta.least_squares_moving_average(df, 'close', 50)['lsma']

# # # # # WERKT GOED!!! # https://help.tradestation.com/10_00/eng/tradestationhelp/elanalysis/indicator/price_channel__percent_pc_indicator_.htm
# pcc_result = bta.percent_price_channel(df, period=20, mult=2)
# df['pcc_upper'] = pcc_result['pcc_upper']
# df['pcc_rangema'] = pcc_result['pcc_rangema']
# df['pcc_lower'] = pcc_result['pcc_lower']

# ppc_result = bta.price_channel(df, period=20)
# df['ppc_upper'] = ppc_result['ppc_upper']
# df['ppc_mid'] = ppc_result['ppc_mid']
# df['ppc_lower'] = ppc_result['ppc_lower']
# df['percent_p'] = ppc_result['percent_p']


# ## # # WERKT GOED!!!
# df['rma'] = bta.rolling_moving_average(df, 'close', 14)['rma']

# # # # WERKT GOED!!!
# df['sma'] = bta.simple_moving_average(df, 'close', 50)['sma']

# # # # # # WERKT GOED!!!
# ssl_result = bta.ssl_channels(df, length=10, mode='sma')
# df['ssl_down'] = ssl_result['ssl_down']
# df['ssl_up'] = ssl_result['ssl_up']

# # ## KLOPT NIET HELEMAAL< MAAR WEL BIJNA MET DE OPGEGEVEN INDICATOR: https://www.tradingview.com/script/SKHqWzql-SSL-ATR-channel/ GEACCEPTEERD RISICO HIER
# ssl_result = bta.ssl_channels_atr(df, column='close', length=14, atr_period=7)
# df['ssl_atr_down'] = ssl_result['ssl_atr_down']
# df['ssl_atr_up'] = ssl_result['ssl_atr_up']

# # # WERKT GOED!!!
# df['t3_average'] = bta.t3_average(df, length=5)['t3_average']

# # # WERKT GOED!!!
# df['zema'] = bta.zero_exponential_moving_average(df, 'close', 21)['zema']

# # # # WERKT GOED!!!
# df['zlema'] = bta.zero_lag_exponential_moving_average(df, 'close', 21)['zlema']

pmax_result = bta.pmax(df, period=10, multiplier=3.0, length=10, ma_type='EMA', src='close')
df['pmax'] = pmax_result['pmax']
df['pmax_trend'] = pmax_result['pmax_trend']


###### UTILITY.PY FILE ###############



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

###### UTILITY.PY FILE ###############

### NOG TE TESTEN
# atr_sl_tp_df = bta.calculate_atr_stop_loss_take_profit(df, signal_column='signal')
# df['takeprofit'] = atr_sl_tp_df['takeprofit']
# df['stoploss'] = atr_sl_tp_df['stoploss']
# df['buyprice'] = atr_sl_tp_df['buyprice']

### NOG TE TESTEN
# stop_loss_take_profit = bta.calculate_stop_loss_take_profit(df, 
#                                                             signal_column='trade_signal',
#                                                             long_trade_signal='long_trade', 
#                                                             short_trade_signal='short_trade', 
#                                                             no_trade_signal='no_trade', 
#                                                             lookback_period=5, 
#                                                             long_reward_ratio=2, 
#                                                             short_reward_ratio=1.5, 
#                                                             buffer=0.5)
# df['stop_loss'] = stop_loss_take_profit['stop_loss']
# df['entry_price'] = stop_loss_take_profit['entry_price']
# df['take_profit'] = stop_loss_take_profit['take_profit']
# df['exit_reason'] = stop_loss_take_profit['exit_reason']

### NOG TE TESTEN
# df['first_crossed_below_second'] = bta.first_crossed_below_second(series1, series2)

### NOG TE TESTEN
# df['first_crossed_above_second'] = bta.first_crossed_above_second(series1, series2)

# ## LIJKT GOED TE WERKEN
# df['min_max'] = bta.get_min_max(df['open'], df['open'], 'max')

# ## LIJKT GOED TE WERKEN
# df['daily_return'] = bta.daily_return(df)

# ## LIJKT GOED TE WERKEN
# df['cumulative_return'] = bta.cumulative_return(df)

# ## LIJKT GOED TE WERKEN
# df['daily_log_return'] = bta.daily_log_return(df)


# # LIJKT GOED TE WERKEN
# maj_qual, min_qual = bta.exhaustion_candles(df, 2, 1)
# df['maj_qual'] = maj_qual
# df['min_qual'] = min_qual


# # LIJKT GOED TE WERKEN
# df['zscore']  = bta.z_score(df['close'])

# # LIJKT GOED TE WERKEN
# df['std_dev'] = bta.st_dev(df['close'], period=14)

# df['df_cleaned'] = bta.drop_na(df)

# # ## WERKT GOED!!!
# df['slope'] = bta.regression_slope(df, 20)

# # NIET TE TESTEN
# leledc_major_minor = bta.populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len)
# df['leledc_major'] = leledc_major_minor['leledc_major']
# df['leledc_minor'] = leledc_major_minor['leledc_minor']

###### VOLATILITY.PY FILE ###############

# # ## WERKT GOED!!!
# df['atr'] = bta.average_true_range(df, 14)['atr']

# # ## WERKT GOED!!!
# bb_result = bta.bollinger_bands(df, 'close', 20, 2, 0)
# df['bb_upper'] = bb_result['bb_upper']
# df['bb_middle'] = bb_result['bb_middle']
# df['bb_lower'] = bb_result['bb_lower']

# # ## WERKT GOED!!!
# df['bbw_expansion'] = bta.bbw_expansion(df, upper_band='bb_upper', lower_band='bb_lower', 
#                                                 middle_band='bb_middle', mult=0.5, rolling_window=20)['bbw_expansion']

# # ## WERKT GOED!!!
# df['true_range'] = bta.true_range(df)['true_range']

# ##### VOLUME.PY FILE ###############

# ## WERKT GOED!!!
# df['adi'] = bta.accumulation_distribution_index(df, fillna=True)['adi']

# ## WERKT GOED!!!
# df['cmf'] = bta.chaikin_money_flow(df, window=20, fillna=True)['cmf']

# ## WERKT GOED!!!
# eom_df = bta.ease_of_movement(df, eom_length=14, seom_length=14, fillna=True)
# df['eom'] = eom_df['eom']
# df['seom'] = eom_df['seom']

# # ## WERKT GOED!!!
# df['fi'] = bta.force_index(df, window=13, fillna=True)['fi']

# # ## WERKT GOED!!!
# df['mfi'] = bta.money_flow_index(df, window=14, fillna=True)['mfi']

# # ## WERKT GOED!!!
# nvi_df = bta.negative_volume_index(df, signal_type='EMA', signal_length=255, fillna=True)
# df['nvi'] = nvi_df['nvi']
# df['nvi_signal'] = nvi_df['nvi_signal']

# # ## WERKT GOED!!
# obv_df = bta.on_balance_volume(df, signal_type='SMA', signal_length=21, show_signal=True, fillna=True)
# df['obv'] = obv_df['obv']
# df['signal'] = obv_df['signal']

# # ## WERKT GOED!!
# df['obv_oscillator'] = bta.on_balance_volume_oscillator(df, length=20, fillna=True)['obv_oscillator']

# # ## WERKT GOED!!!
# pvi_df = bta.positive_volume_index(df, signal_type='EMA', signal_length=255, fillna=True)
# df['pvi'] = pvi_df['pvi']
# df['pvi_signal'] = pvi_df['pvi_signal']

# # ## WERKT GOED!!
# pvt_df = bta.price_volume_trend(df, fillna=True, signal_type='EMA', signal_length=21, dropnans=True)
# df['pvt'] = pvt_df['price_volume_trend']
# df['pvt_signal'] = pvt_df['signal']

# # ## WERKT GOED!!
# df['vwap'] = bta.volume_weighted_average_price(df, window=14, fillna=True)['volume_weighted_average_price']

## WERKT GOED!!
# df['rvol'] = bta.relative_volume(df, volume_col='volume', window=24)['rvol']



# Print the updated DataFrame with the new columns
# print(df)


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



print(df.tail(50))
# dir(bta)