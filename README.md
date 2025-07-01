# Bamboo-TA: Technical Analysis Indicators Library

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

---

## About Bamboo-TA

**Bamboo-TA** is a personal library that consolidates various Technical Analysis (TA) indicators into one simple and modular package for analyzing financial market data. It is designed to help traders develop trading strategies based on candlestick data.

While this library includes popular TA indicators like **MACD**, **RSI**, **SMA**, **EMA**, it also provides lesser-known indicators like **Waddah Attar Explosion** and **Bollinger Bands Trend Indicator**. Bamboo-TA is complementary to other libraries like **TA-lib**, **Pandas-ta**, and **qtpylib**, and it is not intended to replace them.

If you're looking for a library to use for data analysis, backtesting, or integrating indicators into trading bots, Bamboo-TA is designed for simplicity and ease of use.

---

## Features

- **Modular Indicators**: Includes a wide range of trend, volatility, momentum, performance, volume, and other types of indicators.
- **Complementary to Other Libraries**: Works alongside popular TA libraries such as **TA-lib** and **Pandas-ta**.
- **Focus on Algorithmic Trading**: Useful for developing custom algorithmic trading strategies with backtesting capabilities.
- **Personal Project**: Built and maintained for personal use but shared with the community.

---

## Installation

### Stable Version

Install the latest stable version directly from PyPi:

```bash
pip install bamboo-ta
```

### Development Version

To install the bleeding-edge version from the GitHub repository:

```bash
pip install -U git+https://github.com/DutchCryptoDad/bamboo-ta.git@development
```

## Usage

### Importing the Library

To start using Bamboo-TA, import the library in your Python scripts or notebooks:

```python
import bamboo_ta as bta
import pandas as pd
import numpy as np
```

### Preparing Data

Make sure to format your `DataFrame` correctly, like this:

Bamboo-TA expects a pandas DataFrame with specific column names. Here's how to prepare your data:
  
```python
df = pd.read_json("./BTC_USDT-1d.json")
df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
df['date'] = pd.to_datetime(df['date'], unit='ms')
```
  
### Applying Indicators
  
You can apply indicators in various ways. Here's how to use **Alligator Bands**:

Most indicators in Bamboo-TA return a DataFrame with one or more columns. You can then add these columns to your original DataFrame. Here's an example using **Alligator Bands**:
  
```python
alligator_result = bta.alligator_bands(df, 'close', 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
df['jaw'] = alligator_result['jaw']
df['teeth'] = alligator_result['teeth']
df['lips'] = alligator_result['lips']
```

For indicators that return a single value, you can simplify this:
  
```python
df['rsi'] = bta.relative_strength_index(df, column='close', period=14)['rsi']
```
  
### Importing Individual Indicators
  
You can also import and apply individual indicators. Here's how to the **Exponential Moving Average**::

You can also import individual indicators directly from their respective modules. When doing this, make sure to use the imported function name directly (not with the `bta.` prefix):
  
```python
from bamboo_ta.trend import exponential_moving_average
  
df['ema'] = bta.exponential_moving_average(df, "close", 21)
# Use the imported function directly
ema_result = exponential_moving_average(df, "close", 21)
df['ema'] = ema_result['ema']
```

### Chaining Multiple Indicators

You can easily apply multiple indicators to your DataFrame:

```python
# Add RSI
df['rsi'] = bta.relative_strength_index(df, column='close', period=14)['rsi']

# Add MACD
macd_result = bta.macd(df, 'close', 12, 26, 9)
df['macd'] = macd_result['macd']
df['macd_signal'] = macd_result['macd_signal']
df['macd_histogram'] = macd_result['macd_histogram']

# Add Bollinger Bands
bb_result = bta.bollinger_bands(df, 'close', 20, 2)
df['bb_upper'] = bb_result['upper']
df['bb_middle'] = bb_result['middle']
df['bb_lower'] = bb_result['lower']
```

### Accessing Indicator Documentation

Each indicator in Bamboo-TA comes with comprehensive documentation that includes a description, parameters, usage examples, and more. You can access this documentation in several ways:

#### Using the help() Function

The simplest way to access indicator documentation is to use Python's built-in `help()` function:

```python
# Get help for a specific indicator
help(bta.macd_v)
help(bta.relative_strength_index)
help(bta.awesome_oscillator)
```

This will display the indicator's docstring, which includes all the information you need to use it effectively.

#### Accessing Docstrings Directly

You can also access the docstring directly:

```python
# Print the docstring for a specific indicator
print(bta.macd_v.__doc__)
```

#### Using the test_indicators.py Script

When you run the `test_indicators.py` script, it automatically displays the indicator's documentation:

```bash
python test_indicators.py macd_v
```

This will show the indicator description along with the test results.

## Testing Indicators

Bamboo-TA includes a built-in testing system that allows you to quickly test any indicator in the library. This is useful for verifying that indicators are working correctly and producing the expected results, which you can compare with what you see on TradingView.

### Test all indicators in one go

Use the ``test_all_indicators.py`` script to test all the indicators in the module. Be warned, this test only works after all the requirements have been installed on the (virtual) system.

### Using the test_indicators.py Script

The easiest way to test an indicator is to use the `test_indicators.py` script:

```bash
python test_indicators.py [indicator_name] [timeframe]
```

For example:

```bash
python test_indicators.py relative_strength_index 1d
python test_indicators.py awesome_oscillator 4h
python test_indicators.py momentum_divergence 1h
```

This will:

1. Load the appropriate data file (e.g., BTC_USDT-1d.json or BTC_USDT-4h.json)
2. Apply the indicator to the data
3. Display the indicator description and the last 32 rows of data with the indicator values

### Testing Individual Indicator Files

Each indicator file also includes a `test()` function that can be run directly:

```bash
python -m bamboo_ta.momentum.relative_strength_index
```

This will run the test function in the indicator file, which uses the generic `test_indicator` function.

### Using the test_indicator Function Directly

You can also use the `test_indicator` function directly in your code:

```python
import bamboo_ta.bamboo_ta as bta
from bamboo_ta.momentum import relative_strength_index

bta.test_indicator(relative_strength_index)
```

This gives you more flexibility to test indicators with custom parameters.

## Indicator Categories

Bamboo-TA includes a wide range of technical analysis indicators organized into the following categories:

### Candles

Indicators for candlestick pattern analysis and transformations:

- Candlestick Patterns
- Dynamic Exhaustion Bars
- Exhaustion Bars
- Hansen Heiken Ashi
- Heiken Ashi
- Linear Regression Candles
- Smoothed Heiken Ashi

### Cycles

Indicators for analyzing market cycles:

- Even Better Sinewave

### Momentum

Indicators that measure the rate of change in price movements:

- Absolute Price Oscillator
- Awesome Oscillator
- Balance Of Power
- Bias
- Brar
- Calculate Intraday Momentum Index
- Center Of Gravity
- Chande Forecast Oscillator
- Chande Momentum Oscillator
- Commodity Channel Index
- Coppock Curve
- Correlation Trend Indicator
- Directional Movement
- Efficiency Ratio
- Ehlers Fisher Stochastic Center Of Gravity
- Ehlers Ray Index
- Elliott Wave Oscillator
- Fisher Transform
- Inertia
- Kaufmans Adaptive Moving Average
- Kdj
- Know Sure Thing
- Ma Streak
- Momentum
- Momentum Divergence
- Moving Average Convergence Divergence
- Moving Average Convergence Divergence Leader
- Moving Average Convergence Divergence V
- Percentage Price Oscillator
- Percentage Volume Oscillator
- Pretty Good Oscillator
- Psychological Line
- Qualitative Quantitative Estimation
- Rate Of Change
- Relative Momentum Index
- Relative Strength Index
- Relative Strength Index Exponential
- Relative Vigor Index
- Schaff Trend Cycle
- Smi Ergodic Indicator
- Smoothed Rate Of Change
- Stochastic Momentum Index
- Stochastic Rsi
- Stochastics Oscillator
- Td Sequential
- Triple Exponential Average
- True Strength Index
- Ttm Squeeze
- Ultimate Oscillator
- Waddah Attar Explosion
- Waddah Attar Explosion Atr
- Wave Trend
- Wave Trend Oscillator
- Williams R

### Performance

*Note: This category is currently under development.*


### Statistics

*Note: This category is currently under development.*


### Trend

Indicators that help identify the direction of market trends:

- Alligator Bands
- Archer Moving Averages Trends
- Arnaud Legoux Moving Average
- Aroon
- Average Directional Index
- Bollinger Trend
- Bollinger Trend Fast With Ma
- Breakouts
- Chande Kroll Stop
- Choppiness Index
- Cross Signals
- Decay
- Decreasing
- Detrended Price Oscillator
- Double Exponential Moving Average
- Exponential Moving Average
- Fractal Weighted Moving Average
- Gaussian Channel
- Holt Winters Moving Average
- Hull Moving Average
- Increasing
- Jurik Moving Average
- Least Squares Moving Average
- Long Run
- Mcginley Dynamic
- Parabolic Sar
- Pascals Weighted Moving Average
- Percent Price Channel
- Pmax
- Price Channel
- Q Stick
- Range Filter
- Rolling Moving Average
- Sequential Weighted Moving Average
- Short Run
- Simple Moving Average
- Sine Weighted Moving Average
- Ssl Channels
- Ssl Channels Atr
- Supertrend
- T3 Average
- Trend Signals
- Triangular Moving Average
- Triple Exponential Moving Average
- Ttm Trend
- Ut Bot
- Variable Index Dynamic Average
- Vertical Horizontal Filter
- Volumatic Variable Index Dynamic Average
- Volume Weighted Moving Average
- Vortex Indicator
- Weighted Moving Average
- Zero Exponential Moving Average
- Zero Lag Exponential Moving Average

### Utility

Utility functions and indicators for various calculations:

- Calculate Atr Stop Loss Take Profit
- Calculate Stop Loss Take Profit
- Compounded Annual Growth Rate
- Consecutive Count
- Consecutive Higher Highs
- Consecutive Lower Lows
- Cross
- Cross Value
- Cumulative Return
- Daily Log Return
- Daily Return
- Drawdown
- Drop Na
- Entropy
- Error Function
- Exhaustion Candles
- Exhaustion Lengths
- Filter By Dates
- First Crossed Above Second
- First Crossed Below Second
- Geometric Mean
- Get Min Max
- Indicator Mixin
- Is Above
- Is Above Value
- Is Below
- Is Below Value
- Kurtosis
- Linear Decay
- Linear Growth
- Linear Regression Slope
- Log Geometric Mean
- Log Return
- Mean Absolute Deviation
- Median
- Month To Date
- Overbought Oversold
- Pascals Triangle
- Percent Return
- Populate Leledc Major Minor
- Pump Dump Protection
- Quantile
- Quarter To Date
- Regression Slope
- Same Length
- Sharpe Ratio
- Skew
- St Dev
- Symmetric Triangle
- Top Percent Change
- Tos Standard Deviation All
- Variance
- Year To Date
- Z Score

### Volatility

Indicators that measure the rate and magnitude of price changes:

- Aberration Bands
- Acceleration Bands
- Average True Range
- Bbw Expansion
- Bollinger Bands
- Donchian Channel
- Hurst Winter Channel
- Keltner Channel
- Mass Index
- Normalized Average True Range
- Percentage Distance
- Relative Volatility Index
- Thermometer
- True Range
- Ulcer Index
- Williams Vix Fix

### Volume

Indicators that incorporate trading volume to confirm price movements:

- Accumulation Distribution Index
- Accumulation Distribution Oscillator
- Accumulation On Balance Volume
- Chaikin Money Flow
- Ease Of Movement
- Force Index
- Klinger Volume Oscillator
- Money Flow Index
- Negative Volume Index
- On Balance Volume
- On Balance Volume Oscillator
- Positive Volume Index
- Price Volume
- Price Volume Rank
- Price Volume Trend
- Relative Volume
- Time Relative Volume Oscillator
- Volume Profile
- Volume Weighted Average Price
- Volume Weighted Average Price Bands

To access detailed documentation for any indicator, use the `help()` function or access the docstring directly as described in the [Accessing Indicator Documentation](#accessing-indicator-documentation) section.

Or read [the indicator documentation page](documentation/indicators.md) for all the indicators on one page.

## Social & Community

- **YouTube**: Check out my [YouTube channel](https://www.youtube.com/@dutchalgotrading) for tutorials on [Freqtrade](https://www.youtube.com/watch?v=VHvikJmQrVM), [Tradingview](https://www.youtube.com/watch?v=aQSC-W8oYdw), and tested [trading strategies](https://www.youtube.com/watch?v=Jj9MSzHwa44).
- **Patreon**: For exclusive trading algorithms, backtests, and strategy codes, support me on [Patreon](https://www.patreon.com/dutchalgotrading).
- **Strategy League**: View the results of my tested strategies at [DutchAlgoTrading.com](https://www.dutchalgotrading.com).

## Support & Donations

If you find Bamboo-TA useful, consider supporting the project:

- **Patreon**: Support via [Patreon](https://www.patreon.com/dutchalgotrading).
- **Ko-fi**: Make a one-time donation on [Ko-fi](https://ko-fi.com/dutchcryptodad).

### Affiliates

- [Bybit Rewards](https://partner.bybit.com/b/dutchalgo)
- [Linode $100 Credit](https://bit.ly/Linode_Advantages)
- [TradingView Discount](https://www.tradingview.com/?aff_id=139223)
- [Saxo Bank (Dutch Only)](https://refer.saxo/fKnth)

## Disclaimer

Bamboo-TA is a personal project, and while I make every effort to ensure accuracy, I cannot guarantee the functionality of the indicators. They are tested against Binance (BTC/USDT) data and compared with similar indicators on [TradingView](https://www.tradingview.com/?aff_id=139223).

I personally use these indicators to build my own trading strategies, for backtesting and manual & bot trading using the [Freqtrade trading bot](https://www.youtube.com/watch?v=VHvikJmQrVM&list=PL8gq8aFDPpbNEx4lUvpmRjxtCkjvX-Jpg). So it is in my own personal best interest to make these indicators work as accurately as possible.

Suggestions and bug reports are welcome, but fixes will be handled on a best-effort basis. Please be patient!

## Indicator sources

- [ThinkOrSwim Tech indicators](https://tlc.thinkorswim.com/center/reference/Tech-Indicators)
- [Legendary TA](https://github.com/just-nilux/legendary_ta)
- [CryptoFrog Custom Indicators](https://github.com/froggleston/cryptofrog-strategies/blob/main/custom_indicators.py)
- [Linnsoft](https://www.linnsoft.com/techind/accumulation-distribution)
- [Profitspi](https://www.profitspi.com/stock/view.aspx?v=stock-chart-library)
- [Cybernetic Analysis](https://www.neuroshell.com/manuals/cyber/index.html)
- [TRradeStation](https://help.tradestation.com/10_00/eng/tradestationhelp/elanalysis/indicator/price_channel__percent_pc_indicator_.htm)
- [Sierra Chart](https://www.sierrachart.com/index.php?page=doc/TechnicalStudiesReference.php)
- [qtpylib](https://github.com/ranaroussi/qtpylib/blob/main/qtpylib/indicators.py)

## Creating the Python pip package (personal notes)

After creating and testing the code, make a Python pip package as follows:

Update the file ``setup.py`` and update version number.

In the library folder, create the package

``python3 setup.py sdist bdist_wheel``

Before uploading the package to Pypi it is wise to test the package on your system.

Load the package to the system with:

``pip install .``

After you've checked that everything is working correctly, then use the following command to upload to Pypi.
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

First create an API token (at <https://test.pypi.org/manage/account/token/>).

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
