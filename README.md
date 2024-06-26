# bamboo-ta

<p align="center">
  <a href="https://github.com/DutchCryptoDad/bamboo-ta">
    <img src="images/bamboo.png" alt="Bamboo TA" width="250">
  </a>
</p>


The Bamboo TA Indicators module provides a comprehensive suite of technical analysis tools for trading. This module imports various submodules, each dedicated to a specific category of technical indicators.

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


## Installation

### Stable version

Install bamboo-ta from Pypi with:

``pip install bamboo-ta``

Or you can install this directly from the Github repository with the following command:

``$ pip install -U git+https://github.com/DutchCryptoDad/bamboo-ta``

### Development version

The bleeding edge development version can be installed with:

``$ pip install -U git+https://github.com/DutchCryptoDad/bamboo-ta.git@development``

### How to Use This Module

Using the complete module all at once.

1. **Importing the complete library**: Import the library into your Python scripts or Notebook.
   ```python
   import bamboo_ta as bta
   ```

2. **Applying Indicators**: Use the imported indicators on your data.
   ```python
   df['lsma'] = bta.calculate_lsma(df, 14)
   ```

Or individual indicators.

1. **Importing Indicators**: Import the necessary submodules or individual indicators directly from `bamboo_ta`.
   ```python
   from bamboo_ta.trend import AlligatorBands, BollingerTrend, EMA, HMA, LSMA, SMA, WMA, ZLEMA
   ```

2. **Applying Indicators**: Use the imported indicators on your data.
   ```python
   result = AlligatorBands(df, "high", 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
   ```

3. **Combining Indicators**: Combine multiple indicators for comprehensive analysis.
   ```python
   df['ema'] = EMA(df, "close", 21)
   df['sma'] = SMA(df, "close", 50)
   ```

## Bamboo TA Indicators Module

### Submodules

1. **candles**
   - **Description**: Contains indicators related to candlestick patterns.
   - **Indicators**:
     - **HeikinAshi**: Heikin Ashi candlesticks with optional pre and post smoothing.
       - **Usage**: 
         ```python
         ha_df = HeikinAshi(df, pre_smoothing_period=14, post_smoothing_period=14)
         df['HA_Close'] = ha_df['HA_Close']
         df['HA_Open'] = ha_df['HA_Open']
         df['HA_High'] = ha_df['HA_High']
         df['HA_Low'] = ha_df['HA_Low']
         ```
     - **LinRegCandles**: Linear Regression Candles with optional signal line.
       - **Usage**: 
         ```python
         lr_df = LinRegCandles(df, linreg_length=11, sma_signal=True, signal_length=11)
         df['LRC_Open'] = lr_df['bopen']
         df['LRC_High'] = lr_df['bhigh']
         df['LRC_Low'] = lr_df['blow']
         df['LRC_Close'] = lr_df['bclose']
         df['LRC_Signal'] = lr_df['signal']
         ```

2. **cycles**
   - **Description**: Includes indicators for cycle analysis.

3. **momentum**
   - **Description**: Provides momentum-based indicators.
   - **Indicators**:
     - **EWO**: Elliott Wave Oscillator.
       - **Usage**: 
         ```python
         df['ewo'] = EWO(df, "close", 5, 35)
         ```
     - **MACD**: Moving Average Convergence Divergence.
       - **Usage**: 
         ```python
         macd_result = MACD(df, "close", 12, 26, 9)
         df['macd'] = macd_result['MACD']
         df['macd_signal'] = macd_result['MACD_signal']
         df['macd_histogram'] = macd_result['MACD_histogram']
         ```
     - **RSI**: Relative Strength Index.
       - **Usage**: 
         ```python
         df['rsi'] = RSI(df, "close", 14)
         ```

4. **performance**
   - **Description**: Contains performance-related indicators.

5. **statistics**
   - **Description**: Statistical indicators for trading analysis.

6. **trend**
   - **Description**: Includes trend-based indicators.
   - **Indicators**:
     - **AlligatorBands**: Bill Williams Alligator Indicator.
       - **Usage**: 
         ```python
         alligator_result = AlligatorBands(df, "high", 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
         df['jaw'] = alligator_result['jaw']
         df['teeth'] = alligator_result['teeth']
         df['lips'] = alligator_result['lips']
         ```
     - **BollingerTrend**: Bollinger Trend Indicator.
       - **Usage**: 
         ```python
         df['BBTrend'] = BollingerTrend(df, "close", 20, 50, 2.0)
         ```
     - **BollingerTrendFastWithMA**: Bollinger Trend Indicator with selectable Moving Average.
       - **Usage**: 
         ```python
         result = BollingerTrendFastWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14)
         df['BBTrend'] = result['BBTrend']
         df['BBTrendMA'] = result['BBTrendMA']
         ```
     - **EMA**: Exponential Moving Average.
       - **Usage**: 
         ```python
         df['ema'] = EMA(df, "close", 21)
         ```
     - **HMA**: Hull Moving Average.
       - **Usage**: 
         ```python
         df['hma'] = HMA(df, "close", 9)
         ```
     - **LSMA**: Least Squares Moving Average.
       - **Usage**: 
         ```python
         df['lsma'] = LSMA(df, "close", 50)
         ```
     - **SMA**: Simple Moving Average.
       - **Usage**: 
         ```python
         df['sma'] = SMA(df, "close", 50)
         ```
     - **WMA**: Weighted Moving Average.
       - **Usage**: 
         ```python
         df['wma'] = WMA(df, "close", 9)
         ```
     - **ZLEMA**: Zero Lag Exponential Moving Average.
       - **Usage**: 
         ```python
         df['zlema'] = ZLEMA(df, "close", 21)
         ```

7. **utility**
   - **Description**: Utility functions and helper methods for technical analysis.

8. **volatility**
   - **Description**: Volatility indicators.
   - **Indicators**:
     - **BollingerBands**: Calculates Bollinger Bands (upper, middle, lower bands).
       - **Usage**: 
         ```python
         bb_result = BollingerBands(df, "close", 21, 2, 0)
         df['bb_upper'] = bb_result['BB_upper']
         df['bb_middle'] = bb_result['BB_middle']
         df['bb_lower'] = bb_result['BB_lower']
         ```

9. **volume**
   - **Description**: Indicators related to trading volume.

#### Practical example

Example script:

```
# -*- coding: utf-8 -*-
# Import necessary libraries
import pandas_ta as pta
import bamboo_ta as bta
import pandas as pd
from pandas import DataFrame
import numpy as np

# create dataframe and read the json data in the datasets directory
df = pd.read_json("./testdata/BTC_USDT-1d.json")
# name the columns that are loaded into the dataframe
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
# the date column consists of unix time in milliseconds, so this command changes this data into human readable form.
df['date'] = (pd.to_datetime(df['date'], unit='ms'))

print(df)  # This command outputs the dataframe

# Using the pandas_ta library
df['imi_ema'] = pta.ema(close=df['close'], length=7)

df['lsma'] = bta.calculate_lsma(df, 14)  # Using the bamboo_ta library

print(df)
```

Output:

```
➜  python test.py 
           date      open      high       low     close         volume
0    2017-08-17   4261.48   4485.39   4200.74   4285.08     795.150377
1    2017-08-18   4285.08   4371.52   3938.77   4108.37    1199.888264
2    2017-08-19   4108.37   4184.69   3850.00   4139.98     381.309763
3    2017-08-20   4120.98   4211.08   4032.62   4086.29     467.083022
4    2017-08-21   4069.13   4119.62   3911.79   4016.00     691.743060
...         ...       ...       ...       ...       ...            ...
1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.566410
1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.284150
1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.568800
1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.896950
1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.527230

[1972 rows x 6 columns]
           date      open      high       low     close         volume       imi_ema          lsma
0    2017-08-17   4261.48   4485.39   4200.74   4285.08     795.150377           NaN           NaN
1    2017-08-18   4285.08   4371.52   3938.77   4108.37    1199.888264           NaN           NaN
2    2017-08-19   4108.37   4184.69   3850.00   4139.98     381.309763           NaN           NaN
3    2017-08-20   4120.98   4211.08   4032.62   4086.29     467.083022           NaN           NaN
4    2017-08-21   4069.13   4119.62   3911.79   4016.00     691.743060           NaN           NaN
...         ...       ...       ...       ...       ...            ...           ...           ...
1967 2023-01-05  16850.36  16879.82  16753.00  16831.85  163473.566410  16737.537534  16633.800286
1968 2023-01-06  16831.85  17041.00  16679.00  16950.65  207401.284150  16790.815651  16678.202286
1969 2023-01-07  16950.31  16981.91  16908.00  16943.57  104526.568800  16829.004238  16746.722286
1970 2023-01-08  16943.83  17176.99  16911.00  17127.83  135155.896950  16903.710678  16816.734571
1971 2023-01-09  17127.83  17398.80  17104.66  17178.26  266211.527230  16972.348009  16930.485143

[1972 rows x 8 columns]
```


## Creating the Python pip package (personal notes)

After creating and testing the code, make a Python pip package as follows:

Update the file ``setup.py`` and update version number.

In the library folder, create the package

``python3 setup.py sdist bdist_wheel``

Before uploading the package to Pypi it is wise to test the package on your system.

Load the package to the system with:

``pip install .``

After you've checked that everything is worknig correctly, then use the following command to upload to Pypi.
You'll have to install twine for this (``pip install twine`` or ``sudo apt install twine``)

When you get the error:

```
ImportError: cannot import name 'appengine' from 'requests.packages.urllib3.contrib' (/home/user/.local/lib/python3.10/site-packages/urllib3/contrib/__init__.py)
```

You should do a ``pip install --upgrade twine requests-toolbelt``.

### Before uploading

```
# Check first

twine check dist/*

# Test upload first

twine upload -r testpypi dist/*

# Upload to Pypi

twine upload dist/*
```

Note: uploading new versions requires to delete the older versions from the /dist folder.

Another option is to use the ``--skip-existing`` option like this:

```
# Testpypi
twine upload -r testpypi dist/* --skip-existing 

# ProductionPypi
twine upload -r pypi dist/* --skip-existing
```

### Uploading with 2FA enabled

First create an API token (at https://test.pypi.org/manage/account/token/).

Create a file .pypirc in your home folder (e.g. ``nano $HOME/.pypirc``)

Add the given token to the file like this:

```
[testpypi]
  username = __token__
  password =
pypi-AgENdGVzdC5weXtMjBjOS00ZjgxLWIyZDMtYWViMDAwOTk3MWZmAAIqWzMsImU3YjkzMGVmLWQzMGItNGFhYi1iNB6NZ-rSrzc8UXHRmWp5fzZwP


[pypi]
  username = __token__
  password =
pypi-AgEIcHlwaS5vcmcCJDgxYWFiYjYwLTMxYmUtNDczZC1hNjBhLTU0MDJhNmQ2NmZhMgAQ3NTAtOGVkNy0xN2U0NmU0MjEzMQFAYWNj0FcsP-Slnj9-wkEWWwQXkaw
```

Save the file and reload environment if necessary.

Now you an upload libraries without having to use the password.

## Other sources

* [ThinkOrSwim Tech indicators](https://tlc.thinkorswim.com/center/reference/Tech-Indicators)
