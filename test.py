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

# TREND CALCULATIONS

# # Simple Moving Average
# df['sma'] = bta.SMA(df, "close", 50)  # correct
# # Exponential Moving Average
# df['ema'] = bta.EMA(df, "close", 50)  # correct
# # Least squares moving average
# df['lsma'] = bta.LSMA(df, "close", 50)  # correct

# RESULTS:
#            date      open      high       low     close        volume         sma           ema          lsma
# 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641  16793.0500  17123.708932  16908.227482
# 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415  16798.2118  17116.922308  16916.445059
# 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880  16803.0742  17110.124178  16923.821224
# 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  16811.6172  17110.818524  16944.941788
# 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  16829.5778  17113.463288  16952.155035

# # VOLATILITY CALCULATIONS
# bb_result = bta.BollingerBands(df, "close", 21, 2, 0)
# df['bb_upper'] = bb_result['BB_upper']
# df['bb_middle'] = bb_result['BB_middle']
# df['bb_lower'] = bb_result['BB_lower']


# # Based on Pandas TA
# lng = 21
# dev = 2

# df['bb_upper'] = pta.bbands(close=df['close'], length=lng,
#                             std=dev, mamode=None, offset=None)[f'BBU_{lng}_{dev}.0']
# df['bb_middle'] = pta.bbands(close=df['close'], length=lng,
#                              std=dev, mamode=None, offset=None)[f'BBM_{lng}_{dev}.0']
# df['bb_lower'] = pta.bbands(close=df['close'], length=lng,
#                             std=dev, mamode=None, offset=None)[f'BBL_{lng}_{dev}.0']

# RESULT OF BOLLINGER CHECKS:
# python test.py
#            date      open      high       low     close        volume      BB_upper     BB_middle      BB_lower      bb_upper     bb_middle      bb_lower
# 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641  16976.289552  16722.740000  16469.190448  16976.289552  16722.740000  16469.190448
# 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415  17005.670681  16737.908095  16470.145510  17005.670681  16737.908095  16470.145510
# 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880  17027.316671  16745.862857  16464.409044  17027.316671  16745.862857  16464.409044
# 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  17089.406121  16764.416190  16439.426259  17089.406121  16764.416190  16439.426259
# 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  17135.923174  16799.624762  16463.326350  17135.923174  16799.624762  16463.326350


# MOMENTUM INDICATORS

# # RSI
# df['rsi'] = bta.RSI(df, "close", 14)
# df['p_rsi'] = pta.rsi(close=df['close'], length=14)

#  /bamboo-ta on  main ≡  ~5
# ➜  python test.py
#            date      open      high       low     close        volume        rsi      p_rsi
# 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641  50.071524  50.071524
# 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415  53.243658  53.243658
# 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880  53.027433  53.027433
# 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  57.827520  57.827520
# 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  59.060593  59.060593

# MACD
# macd_result = bta.MACD(df, "close", 12, 26, 9)
# df['macd'] = macd_result['MACD']
# df['macd_signal'] = macd_result['MACD_signal']
# df['macd_histogram'] = macd_result['MACD_histogram']

# # Pandas MACD
# pta.macd(close=df['close'], fast=None, slow=None,
#          signal=None, offset=None).tail(5)
# df['P_macd'] = pta.macd(close=df['close'], fast=None,
#                         slow=None, signal=None, offset=None)['MACD_12_26_9']
# df['P_macs'] = pta.macd(close=df['close'], fast=None,
#                         slow=None, signal=None, offset=None)['MACDs_12_26_9']
# df['P_macdh'] = pta.macd(close=df['close'], fast=None,
#                          slow=None, signal=None, offset=None)['MACDh_12_26_9']

#  /bamboo-ta on  main ≡  ~13
# ➜  python test.py
#            date      open      high       low     close        volume       macd  macd_signal  macd_histogram     P_macd      P_macs    P_macdh
# 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641 -83.250482  -111.409248       28.158766 -83.250482 -111.409248  28.158766
# 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415 -60.071674  -101.141734       41.070059 -60.071674 -101.141734  41.070059
# 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880 -41.791848   -89.271757       47.479908 -41.791848  -89.271757  47.479908
# 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695 -12.294984   -73.876402       61.581418 -12.294984  -73.876402  61.581418
# 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  14.978115   -56.105499       71.083614  14.978115  -56.105499  71.083614

# supertrend_result = bta.SuperTrend(df, "close", 7, 3.0, 0)
# df['supertrend'] = supertrend_result['ST_trend']
# df['supertrend_d'] = supertrend_result['ST_direction']
# df['supertrend_l'] = supertrend_result['ST_long']
# df['supertrend_s'] = supertrend_result['ST_short']

# # Using Pandas TA
# # Supertrend is 1 where close is above supertrend (bullish), and -1 if close is below supertrend (bearish).

# st_length = 7
# st_mult = 3.0

# df['st'] = pta.supertrend(high=df['high'], low=df['low'], close=df['close'],
#                           length=st_length, multiplier=st_mult)[f'SUPERT_{st_length}_{st_mult}']
# df['std'] = pta.supertrend(high=df['high'], low=df['low'], close=df['close'],
#                            length=st_length, multiplier=st_mult)[f'SUPERTd_{st_length}_{st_mult}']
# df['stl'] = pta.supertrend(high=df['high'], low=df['low'], close=df['close'],
#                            length=st_length, multiplier=st_mult)[f'SUPERTl_{st_length}_{st_mult}']
# df['sts'] = pta.supertrend(high=df['high'], low=df['low'], close=df['close'],
#                            length=st_length, multiplier=st_mult)[f'SUPERTs_{st_length}_{st_mult}']

# df['wma'] = bta.WMA(df, "close", 50)
# df['hma'] = bta.HMA(df, "close", 50)
# df['zlema'] = bta.ZLEMA(df, "close", 50)

# ➜  python test.py
#            date      open      high       low     close        volume         sma           wma           hma         zlema
# 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641  16793.0500  16831.442494  16689.219892  16590.685184
# 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415  16798.2118  16837.622886  16676.593601  16572.485765
# 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880  16803.0742  16843.323208  16672.061953  16553.329069
# 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  16811.6172  16856.058729  16680.025132  16566.897341
# 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  16829.5778  16870.436878  16700.310344  16612.289602

# df['ewo'] = bta.EWO(df, "close", 5, 35)

# ➜  python test.py
#            date      open      high       low     close        volume       ewo
# 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641 -1.075050
# 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415 -0.649598
# 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880 -0.340181
# 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  0.188342
# 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  0.534305


# ha_result = bta.HeikinAshi(
#     df, pre_smoothing_period=14, post_smoothing_period=14)
# df['HA_Open'] = ha_result['HA_Open']
# df['HA_High'] = ha_result['HA_High']
# df['HA_Low'] = ha_result['HA_Low']
# df['HA_Close'] = ha_result['HA_Close']

# #  /bamboo-ta on  main ≡  ~2
# # ➜  python test.py
# #            date      open      high       low     close        volume    HA_Close       HA_Open   HA_High        HA_Low
# # 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641  16828.7575  16721.877756  16879.82  16721.877756
# # 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415  16875.6250  16775.317628  17041.00  16679.000000
# # 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880  16945.9475  16825.471314  16981.91  16825.471314
# # 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  17039.9125  16885.709407  17176.99  16885.709407
# # 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  17202.3875  16962.810954  17398.80  16962.810954

# ➜  python test.py
#            date      open      high       low     close        volume       HA_Open       HA_High        HA_Low      HA_Close
# 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641  16828.347559  16955.448586  16642.252201  16801.965683
# 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415  16815.156621  16945.774718  16639.259120  16795.707645
# 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880  16805.432133  16939.150974  16641.788599  16793.678094
# 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  16799.555114  16938.404055  16648.474500  16796.531177
# 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  16798.043145  16946.027853  16661.606318  16805.889382

# lr_df = bta.LinRegCandles(df, sma_signal=True)

# # After calling, the following columns can be extracted:
# df['LRC_Open'] = lr_df['bopen']
# df['LRC_High'] = lr_df['bhigh']
# df['LRC_Low'] = lr_df['blow']
# df['LRC_Close'] = lr_df['bclose']
# df['LRC_Signal'] = lr_df['signal']

#  /bamboo-ta on  main ≡  ~2
# ➜  python test.py
#            date      open      high       low     close        volume      LRC_Open      LRC_High       LRC_Low     LRC_Close    LRC_Signal
# 1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641  16648.707727  16794.727273  16597.960000  16718.946364  16680.307975
# 1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415  16719.063636  16899.244091  16676.039091  16842.977727  16676.179628
# 1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880  16842.992273  16985.721364  16795.958182  16924.602727  16683.688719
# 1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  16924.666364  17099.740455  16879.386818  17025.155455  16707.076570
# 1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  17025.216364  17244.566364  17008.464091  17131.032273  16744.021033

# alligator_result = bta.AlligatorBands(df, "close", 13, 8, 5)
# df['jaw'] = alligator_result['jaw']
# df['teeth'] = alligator_result['teeth']
# df['lips'] = alligator_result['lips']
# alligator_result = bta.AlligatorBands(
#     df, "close", 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
# df['jaw'] = alligator_result['jaw']
# df['teeth'] = alligator_result['teeth']
# df['lips'] = alligator_result['lips']
# # Print stuff
# print(df.tail(7))


df['BBTrend'] = bta.BollingerTrend(df, "close", 20, 50, 2.0)

BollingerTrendFast = bta.BollingerTrendFastWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14)
df['BollingerTrendFast'] = BollingerTrendFast['BBTrend']
df['BollingerTrendFastMA'] = BollingerTrendFast['BBTrendMA']

print(df.tail(20))