# -*- coding: utf-8 -*-
# Import necessary libraries
# Importeer necessary libraries
import bamboo_ta.bamboo_ta as bta
import pandas_ta as pta
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
# df['BB_upper'] = bb_result['BB_upper']
# df['BB_middle'] = bb_result['BB_middle']
# df['BB_lower'] = bb_result['BB_lower']


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
# macd_result = bta.MACD(df, 12, 26, 9)
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

# Print stuff
print(df.tail(5))
