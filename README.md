# bamboo-ta

<p align="center">
  <a href="https://github.com/DutchCryptoDad/bamboo-ta">
    <img src="images/bamboo.png" alt="Bamboo TA" width="250">
  </a>
</p>


[![license](https://img.shields.io/github/license/DutchCryptoDad/bamboo-ta)](#license)
[![Python Version](https://img.shields.io/pypi/pyversions/bamboo-ta?style=flat)](https://pypi.org/project/bamboo-ta/)
[![PyPi Version](https://img.shields.io/pypi/v/bamboo-ta?style=flat)](https://pypi.org/project/bamboo-ta/)
[![Package Status](https://img.shields.io/pypi/status/bamboo-ta?style=flat)](https://pypi.org/project/bamboo-ta/)
[![Downloads](https://img.shields.io/pypi/dm/bamboo_ta?style=flat)](https://pypistats.org/packages/bamboo_ta)
[![Stars](https://img.shields.io/github/stars/DutchCryptoDad/bamboo-ta?style=flat)](#stars)
[![Forks](https://img.shields.io/github/forks/DutchCryptoDad/bamboo-ta?style=flat)](#forks)
[![Used By](https://img.shields.io/badge/used_by-0-orange.svg?style=flat)](#usedby)
[![Contributors](https://img.shields.io/github/contributors/DutchCryptoDad/bamboo-ta?style=flat)](#contributors)
[![Issues](https://img.shields.io/github/issues-raw/DutchCryptoDad/bamboo-ta?style=flat)](#issues)
[![Closed Issues](https://img.shields.io/github/issues-closed-raw/DutchCryptoDad/bamboo-ta?style=flat)](#closed-issues)
[![Support me on Patreon](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.vercel.app%2Fapi%3Fusername%3Ddutchalgotrading%26type%3Dpatrons&style=flat)](https://patreon.com/dutchalgotrading)
[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC-AOcefy1x7lTc17JiqaxqA)
](https://www.youtube.com/@dutchalgotrading)
[![YouTube Channel Views](https://img.shields.io/youtube/channel/views/UC-AOcefy1x7lTc17JiqaxqA)](https://www.youtube.com/@dutchalgotrading)

## Why this library

Bamboo-ta is a personal project that consolidates various Technical Analysis Indicators for trading into a single library. It’s primarily built for personal use, with a focus on data analysis of candlestick data to develop new (algorithmic) trading strategies. It can also serve as an auxiliary library for indicators in trading bots.

This library includes not only some of the most popular indicators (like MACD, RSI, SMA, EMA, and more), but also more obscure (and possibly brand new) indicators such as ‘Waddah Attar Explosion’ and ‘Bollinger Bands Trend Indicator’. For more information on the available indicators, please refer to the indicator category pages.

While Bamboo-ta complements other popular TA libraries like TA-lib, Pandas-ta, qtpylib, and others, it is not intended to replace them. There will likely be many indicators that are better served by these other libraries. 

Bamboo-ta is designed with a focus on simplicity and modularity. It aims to be easy to use and maintain. If you’re seeking a library for complex indicator applications, you might want to consider other options.

## Social

See my [Youtube channel](youtube.com/channel/UC-AOcefy1x7lTc17JiqaxqA?sub_confirmation=1) for [Freqtrade tutorials](https://www.youtube.com/watch?v=VHvikJmQrVM&list=PL8gq8aFDPpbNEx4lUvpmRjxtCkjvX-Jpg), [Tradingview knowledge](https://www.youtube.com/watch?v=aQSC-W8oYdw&list=PL8gq8aFDPpbNyIFWaQMovp9dSjDhAQcsd) and [video's about trading strategies and algorithms I tested](https://www.youtube.com/watch?v=Jj9MSzHwa44&list=PL8gq8aFDPpbNthwcFtdTjt6i9zoLmq6zO).

See my [Patreon page](https://www.patreon.com/dutchalgotrading) for all the algorithmic strategies code (trading algorithms and automated backtests). These are all based on the [Freqtrade](https://github.com/freqtrade) trading bot btw.

For the Strategy League (an overview of all the trading strategies/algorithms I tested) go to [dutchalgotrading.com](https://www.dutchalgotrading.com/). Ths league contains a ranked list with all the tested strategies I present on my [Youtube channel](youtube.com/channel/UC-AOcefy1x7lTc17JiqaxqA?sub_confirmation=1) and [Patreon page](https://www.patreon.com/dutchalgotrading)

## Support and donations

Sometimes, the best motivation a person can receive is a small contribution that shows appreciation for their work.

You can support my work by becoming a Patron on [Patreon](https://www.patreon.com/dutchalgotrading). 

For one-time donations you can visit [Ko-fi.com](https://ko-fi.com/dutchcryptodad)

Or send some crypto to the following addresses:
* BTC : bc1qrtmdycvzc2vntx5jmg86qysnsm6h3xa9valu0e
* ETH : 0xa27966A67F8B1225116509f6503EDf0534DE2927
* DOGE: DEPuQLhViQDtZcyXtaqqLSPQWmMs5cckht
* SOL : FDiyWgFRsLAMCuzAiuDe9yZ8BYsVnn244zYfqEz7bWom
* ADA : addr1qxyr5xxvp52vf9zmpt8gtxfnkfjs5gzxh0sm2j504wgsr2vg8gvvcrg5cj29kzkwskvn8vn9pgsydwlpk49gl2u3qx5spl8gf4
* PEPE: 0xa27966A67F8B1225116509f6503EDf0534DE2927
* SHIB: 0xa27966A67F8B1225116509f6503EDf0534DE2927

## Installation

### Stable version

Install bamboo-ta from Pypi with:

``pip install bamboo-ta``

Or you can install this directly from the Github repository with the following command:

``$ pip install -U git+https://github.com/DutchCryptoDad/bamboo-ta``

### Development version

The bleeding edge development version can be installed with:

``$ pip install -U git+https://github.com/DutchCryptoDad/bamboo-ta.git@development``

## How to Use This Module

Using the complete module all at once.

1. **Importing the complete library**: Import the library into your Python scripts or Notebook.
   ```python
   import bamboo_ta as bta
   ```

   Additionally import Pandas and Numpy too:

   ```python
   import pandas as pd
   from pandas import DataFrame
   import numpy as np
   ```

2. **Build the dataframe**: The dataframe should be build as follows for the fastest results. 

    ```python
    df = pd.read_json("./BTC_USDT-1d.json")
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['date'] = (pd.to_datetime(df['date'], unit='ms'))
   ```

3. **Applying Indicators**: Use the imported indicators on your data.

   ```python
   df['ao'] = bta.AwesomeOscillator(df, 'high', 'low', 5, 34)['ao']
   ```

   Or

   ```python
   lr_df = bta.LinRegCandles(df)
   df['lrc_open'] = lr_df['bopen']
   df['lrc_high'] = lr_df['bhigh']
   df['lrc_low'] = lr_df['blow']
   df['lrc_close'] = lr_df['bclose']
   df['lrc_signal'] = lr_df['signal']
   ```

Or individual indicators.

1. **Importing Indicators**: Import the necessary submodules or individual indicators directly from `bamboo_ta`.
   ```python
   from bamboo_ta.trend import AlligatorBands
   ```

2. **Applying Indicators**: Use the imported indicators on your data.
   ```python
    alligator_result = bta.AlligatorBands(df, 'close', 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
    df['jaw'] = alligator_result['jaw']
    df['teeth'] = alligator_result['teeth']
    df['lips'] = alligator_result['lips']
   ```

### Practical example

Example script:

```
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

fscg = bta.EhlersFisherStochasticCenterOfGravity(df)
df['CG'] = fscg['CG']
df['Trigger'] = fscg['Trigger']

print(df.tail(40))
```

Output:

```
 python test.py
1962 2022-12-31  16607.48  16644.09  16470.00  16542.40  114490.42864 -0.75    -0.21
1963 2023-01-01  16541.77  16628.00  16499.01  16616.75   96925.41374 -1.28    -0.75
1964 2023-01-02  16617.17  16799.23  16548.70  16672.87  121888.57191 -1.07    -1.28
1965 2023-01-03  16672.78  16778.40  16605.28  16675.18  159541.53733 -0.23    -1.07
1966 2023-01-04  16675.65  16991.87  16652.66  16850.36  220362.18862  0.37    -0.23
1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.56641  0.96     0.37
1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.28415  1.78     0.96
1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.56880  2.65     1.78
1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.89695  2.65     2.65
1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.52723  2.65     2.65
```

## Indicator categories

* [Candles](./docs/candles.md)
* [Cycles](./docs/cycles.md)
* [Momentum](./docs/momentum.md)
* [Performance](./docs/performance.md)
* [Statistics](./docs/statistics.md)
* [Trend](./docs/trend.md)
* [Utility](./docs/utility.md)
* [Volatility](./docs/volatility.md)
* [Volume](./docs/volume.md)

## Sources on which some indicators are based on

* [ThinkOrSwim Tech indicators](https://tlc.thinkorswim.com/center/reference/Tech-Indicators)
* [Legendary TA](https://github.com/just-nilux/legendary_ta)
* [CryptoFrog Custom Indicators](https://github.com/froggleston/cryptofrog-strategies/blob/main/custom_indicators.py)
* [Linnsoft](https://www.linnsoft.com/techind/accumulation-distribution)
* [Profitspi](https://www.profitspi.com/stock/view.aspx?v=stock-chart-library)
* [Cybernetic Analysis](https://www.neuroshell.com/manuals/cyber/index.html)
* [TRradeStation](https://help.tradestation.com/10_00/eng/tradestationhelp/elanalysis/indicator/price_channel__percent_pc_indicator_.htm)
* [Sierra Chart](https://www.sierrachart.com/index.php?page=doc/TechnicalStudiesReference.php)

## Disclaimer !!!

Most of the indicators I configured are tested agains a dataset from Binance (BTC/USDT) and verified with the same indicators on [Tradingview](tradingview.com/?aff_id=139223). However I will and cannot guarantee the workings and accuracy. 

I personally use these indicators to build my own trading strategies, for backtesting and manual & bot trading using the [Freqtrade trading bot](https://www.youtube.com/watch?v=VHvikJmQrVM&list=PL8gq8aFDPpbNEx4lUvpmRjxtCkjvX-Jpg). So it is in my own personal best interest to make these indicators work as accurately as possible.

You are welcome to do suggestions and report bugs if you find these. But I will handle these on a 'best effort' base. I believe that the pressure of maintaining larger and popular libraries will lead to abandonment of the project by the original developer(s) at some point in time. And I do not want this to happen with this project (although no guarantees here too...).  
So be patient and the proposed suggestions might be handled all in good time.