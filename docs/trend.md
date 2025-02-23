# `trend` - Trend Indicators

## Alligator Bands

### Description

The **Alligator Indicator**, developed by Bill Williams, is used to identify trends and their direction in the market. It consists of three smoothed moving averages known as the **Jaw**, **Teeth**, and **Lips**.

### Interpretation

- **Jaw**: Represents the slowest moving average and is shifted by 8 periods to indicate long-term trends.
- **Teeth**: Represents the medium-term trend and is shifted by 5 periods.
- **Lips**: Represents the fastest moving average and is shifted by 3 periods.

### Usage Example

```python
alligator_result = bta.alligator_bands(df, 'close', 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
df['jaw'] = alligator_result['jaw']
df['teeth'] = alligator_result['teeth']
df['lips'] = alligator_result['lips']
```

### Parameters

- `df` (pandas.DataFrame): DataFrame containing the data.
- `column` (str): The column on which the Alligator is applied. Default is `'close'`.
- `jaw_period` (int): Period for the Alligator's Jaw. Default is `13`.
- `teeth_period` (int): Period for the Alligator's Teeth. Default is `8`.
- `lips_period` (int): Period for the Alligator's Lips. Default is `5`.
- `jaw_shift` (int): Number of periods to shift the Jaw line. Default is `8`.
- `teeth_shift` (int): Number of periods to shift the Teeth line. Default is `5`.
- `lips_shift` (int): Number of periods to shift the Lips line. Default is `3`.

### Returns

- **DataFrame**: A DataFrame with `'jaw'`, `'teeth'`, and `'lips'` columns.

---

## Bollinger Trend Indicator

### Description

The **Bollinger Trend Indicator** measures the trend based on the difference between short and long Bollinger Bands, indicating the strength of the trend.

### Interpretation

- Positive values of **BBTrend** suggest a strong uptrend, while negative values indicate a downtrend.

### Usage Example

```python
df['bbtrend'] = bta.bollinger_trend(df, 'close', 20, 50, 2.0)['bbtrend']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which BBTrend is calculated. Default is `'close'`.
- `short_length` (int): Period for the short Bollinger Bands. Default is `20`.
- `long_length` (int): Period for the long Bollinger Bands. Default is `50`.
- `std_dev` (float): Standard deviation multiplier for the Bollinger Bands. Default is `2.0`.

### Returns

- **DataFrame**: A DataFrame with a single `'bbtrend'` column.

---

## Bollinger Trend Fast with Moving Average

### Description

This variation of the **Bollinger Trend Indicator** calculates a more responsive Bollinger Trend and applies a selectable moving average to the BBTrend result.

### Interpretation

- **BBTrend** indicates the direction of the trend, while the selected moving average can smooth the BBTrend values.

### Usage Example

```python
result = bta.bollinger_trend_fast_with_ma(df, 'close', 10, 50, 1.0, 2.0, 'SMA', 14)
df['bollinger_trend_fast'] = result['bbtrend']
df['bollinger_trend_fast_ma'] = result['bbtrend_ma']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame.
- `column` (str): The column on which BBTrend is calculated. Default is `'close'`.
- `short_length` (int): Period for the short Bollinger Bands. Default is `10`.
- `long_length` (int): Period for the long Bollinger Bands. Default is `50`.
- `short_stddev` (float): Standard deviation multiplier for short Bollinger Bands. Default is `1.0`.
- `long_stddev` (float): Standard deviation multiplier for long Bollinger Bands. Default is `2.0`.
- `ma_type` (str): Type of moving average to apply. Default is `'SMA'`.
- `ma_length` (int): Period for the moving average. Default is `14`.

### Returns

- **DataFrame**: A DataFrame with `'bbtrend'` and `'bbtrend_ma'` columns.

---

## Breakouts

### Description

The **Breakouts** function identifies **Support and Resistance (S/R)** levels and their breakouts or retests. It highlights potential trend reversals and continuation points.

### Interpretation

- **Support/Resistance Breakout**: Indicates if the price breaks through a support or resistance level.
- **Retests**: Signals whether the price retests a previously broken support or resistance level.

### Usage Example

```python
breakout = bta.breakouts(df, length=20)
df['support_level'] = breakout['support_level']
df['resistance_level'] = breakout['resistance_level']
df['support_breakout'] = breakout['support_breakout']
df['resistance_breakout'] = breakout['resistance_breakout']
df['support_retest'] = breakout['support_retest']
df['potential_support_retest'] = breakout['potential_support_retest']
df['resistance_retest'] = breakout['resistance_retest']
df['potential_resistance_retest'] = breakout['potential_resistance_retest']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the columns `'high'`, `'low'`, and `'close'`.
- `length` (int): Lookback period. Default is `20`.

### Returns

- **DataFrame**: A DataFrame with columns for support and resistance levels, breakouts, and retests.

---

## Exponential Moving Average (EMA)

### Description

The **Exponential Moving Average (EMA)** gives more weight to recent prices, making it more responsive to recent price changes compared to the Simple Moving Average (SMA).

### Interpretation

- **EMA** is used to identify trends and smooth out price action, with more emphasis on recent data points.

### Usage Example

```python
df['ema'] = bta.exponential_moving_average(df, 'close', 21)['ema']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which EMA is to be calculated. Default is `'close'`.
- `period` (int): The period for the EMA calculation. Default is `21`.

### Returns

- **DataFrame**: A DataFrame with the `'ema'` column.

---

## Hull Moving Average (HMA)

### Description

The **Hull Moving Average (HMA)** is a smoothed moving average designed to minimize lag while retaining responsiveness to price changes. It achieves this by using the **Weighted Moving Average (WMA)**.

### Interpretation

- **HMA** provides a faster signal than traditional moving averages and can be used to detect trends more effectively.

### Usage Example

```python
df['hma'] = bta.hull_moving_average(df, 'close', 9)['hma']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which HMA is to be calculated. Default is `'close'`.
- `period` (int): The period for the HMA calculation. Default is `9`.

### Returns

- **DataFrame**: A DataFrame with the `'hma'` column.

---

## Least Squares Moving Average (LSMA)

### Description

The **Least Squares Moving Average (LSMA)** fits a straight line to the price data over a specified period using the **least squares** method. This line is used to depict the direction of movement.

### Interpretation

- **LSMA** is used to identify the current trend and smooth price data by removing noise.

### Usage Example

```python
df['lsma'] = bta.least_squares_moving_average(df, 'close', 50)['lsma']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which LSMA is to be calculated. Default is `'close'`.
- `period` (int): The period for LSMA calculation. Default is `21`.

### Returns

- **DataFrame**: A DataFrame with the `'lsma'` column.

---

## Pmax Indicator

### Description

The **Pmax Indicator** is a technical analysis tool designed to identify trend direction and potential reversals. It calculates upper and lower bands based on a moving average and the Average True Range (ATR). The Pmax values and the associated trend direction (`up` or `down`) help traders make informed decisions about market trends.

### Interpretation

- **Pmax Values**: The calculated values represent dynamic support and resistance levels.  
  - When the trend is `up`, prices are expected to stay above the Pmax line.
  - When the trend is `down`, prices are expected to stay below the Pmax line.
- **Trend Direction**:
  - `up`: Indicates an uptrend where prices are above the Pmax line.
  - `down`: Indicates a downtrend where prices are below the Pmax line.

### Usage Example

```python
# Example usage
result = pmax(df, period=14, multiplier=2.0, length=20, ma_type='EMA', src='close')
df['pmax'] = result['pmax']
df['pmax_trend'] = result['pmax_trend']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the following OHLC columns:
  - `open`
  - `high`
  - `low`
  - `close`
- `period` (int): Lookback period for calculating the ATR.
- `multiplier` (float): The multiplier applied to the ATR for calculating the bands.
- `length` (int): Lookback period for the moving average.
- `ma_type` (str, default=`'EMA'`): The type of moving average to use. Options include:
  - `'EMA'` (Exponential Moving Average)
  - `'SMA'` (Simple Moving Average)
- `src` (str, default=`'close'`): The source price for calculations. Options include:
  - `'close'`: Closing price (default).
  - `'hl2'`: Average of high and low prices.
  - `'ohlc4'`: Average of open, high, low, and close prices.

### Returns

- **DataFrame**: A DataFrame with two additional columns:
  - `'pmax'`: Final Pmax values, which serve as dynamic support/resistance levels.
  - `'pmax_trend'`: The trend direction (`'up'` or `'down'`).

### Notes

- The Pmax indicator is versatile and can be adapted to different markets and timeframes by adjusting the `period`, `length`, and `multiplier` parameters.
- For shorter-term analysis, use a smaller `period` and `length`. For longer-term trends, increase these values.

---

## Percent Price Channel (PPC)

### Description

The **Percent Price Channel (PPC)** calculates the percentage change of a price channel, based on the highest high and lowest low of a trailing period.

### Interpretation

- A **breakout** above the upper band indicates market strength, while a **breakout** below the lower band signals weakness. The **percent_p** value shows the current price’s position within the price channel.

### Usage Example

```python
ppc_result = bta.price_channel(df, period=20)
df['ppc_upper'] = ppc_result['ppc_upper']
df['ppc_mid'] = ppc_result['ppc_mid']
df['ppc_lower'] = ppc_result['ppc_lower']
df['percent_p'] = ppc_result['percent_p']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `period` (int): The period for calculating the highest high and lowest low. Default is `20`.

### Returns

- **DataFrame**: A DataFrame with `'ppc_upper'`, `'ppc_mid'`, `'ppc_lower'`, and `'percent_p'` columns.

---

## Range Filter Buy and Sell Indicator  

### Description

The **Range Filter Buy and Sell Indicator** is a technical indicator that identifies trend direction and potential entry points. It uses two moving averages to create a range and determine the trend.

### Interpretation

- **Range Filter**: The indicator creates a range based on two moving averages.
- **Long Signal**: Indicates a bullish trend when the price is above the upper band.
- **Short Signal**: Indicates a bearish trend when the price is below the lower band.

### Usage Example

```python
range_filter_result = bta.range_filter(df, "close", 100, 3.0)
df["range_filter"] = range_filter_result["range_filter"]
df["high_band"] = range_filter_result["high_band"]
df["low_band"] = range_filter_result["low_band"]
df["long_signal"] = range_filter_result["long_signal"]
df["short_signal"] = range_filter_result["short_signal"]
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which the Range Filter is applied. Default is `'close'`.
- `short_length` (int): The period for the short moving average. Default is `100`.
- `long_length` (int): The period for the long moving average. Default is `3.0`.

### Returns

- **DataFrame**: A DataFrame with the `'range_filter'`, `'high_band'`, `'low_band'`, `'long_signal'`, and `'short_signal'` columns.

---

## Rolling Moving Average (RMA)

### Description

The **Rolling Moving Average (RMA)** is a type of **Exponential Moving Average (EMA)** that smooths data over a specified period, providing a trend-following measure.

### Interpretation

- **RMA** is used similarly to EMA, giving more weight to recent price data, and is helpful in trend identification.

### Usage Example

```python
df['rma'] = bta.rolling_moving_average(df, 'close', 14)['rma']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which RMA is calculated. Default is `'close'`.
- `period` (int): The period for the RMA calculation. Default is `14`.

### Returns

- **DataFrame**: A DataFrame with the `'rma'` column.

---

## Simple Moving Average (SMA)

### Description

The **Simple Moving Average (SMA)** is the unweighted mean of the previous n data points. It is used to smooth price data to identify trends.

### Interpretation

- **SMA** is used to identify the overall direction of a trend. Longer periods smooth out more short-term fluctuations.

### Usage Example

```python
df['sma'] = bta.simple_moving_average(df, 'close', 50)['sma']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which SMA is to be calculated. Default is `'close'`.
- `period` (int): The period for SMA calculation. Default is `21`.

### Returns

- **DataFrame**: A DataFrame with the `'sma'` column.

---

## SSL Channels

### Description

**SSL Channels** use moving averages to identify trends by calculating SSL Down and SSL Up series based on price action.

### Interpretation

- **SSL Down** and **SSL Up** signals indicate potential buy or sell conditions depending on the relationship between price and these levels.

### Usage Example

```python
ssl_result = bta.ssl_channels(df, length=10, mode='sma')
df['ssl_down'] = ssl_result['ssl_down']
df['ssl_up'] = ssl_result['ssl_up']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `length` (int): Period for the SMA calculation. Default is `10`.
- `mode` (str): The type of moving average. Currently, only `'sma'` is supported.

### Returns

- **DataFrame**: A DataFrame with `'ssl_down'` and `'ssl_up'` columns.

---

## SSL Channels with ATR

### Description

The **SSL Channels with ATR** use the **Average True Range (ATR)** to dynamically adjust support and resistance levels, helping identify trend reversals and continuations.

### Interpretation

- The **ATR-adjusted SSL Down** and **SSL Up** provide dynamic support and resistance levels based on volatility.

### Usage Example

```python
ssl_result = bta.ssl_channels_atr(df, column='close', length=14, atr_period=7)
df['ssl_atr_down'] = ssl_result['ssl_atr_down']
df['ssl_atr_up'] = ssl_result['ssl_atr_up']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `length` (int): Period for the SMA calculation. Default is `14`.
- `atr_period` (int): Period for the ATR calculation. Default is `7`.
- `column` (str): The column to use for moving average calculations. Default is `'close'`.

### Returns

- **DataFrame**: A DataFrame with `'ssl_atr_down'` and `'ssl_atr_up'` columns.

---

## T3 Average

### Description

The **T3 Average** is a smoothed moving average designed to reduce lag while maintaining responsiveness to price changes. It is calculated using multiple stages of **Exponential Moving Averages (EMAs)**.

### Interpretation

- The **T3 Average** offers a smooth trend-following signal that is more responsive than traditional moving averages while reducing lag.

### Usage Example

```python
df['t3_average'] = bta.t3_average(df, length=5)['t3_average']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `length` (int): Period for the EMA calculation. Default is `5`.

### Returns

- **DataFrame**: A DataFrame with the `'t3_average'` column.

---

## UT Bot Indicator

### Description

The **UT Bot Indicator** is a trend-following indicator that uses ATR (Average True Range) to create a dynamic trailing stop. Originally created by HPotter, it helps identify trend changes and potential entry/exit points by generating a trailing stop line that adapts to market volatility.

### Interpretation

- When price crosses above the trailing stop, it generates a buy signal and indicates an uptrend
- When price crosses below the trailing stop, it generates a sell signal and indicates a downtrend
- The trailing stop acts as dynamic support in uptrends and resistance in downtrends
- Position value of 1 indicates a long position, -1 indicates a short position

### Usage Example

```python
result = bta.ut_bot(df, 'close', 10, 3.0)
df['ut_bot_stop'] = result['ut_bot_stop']
df['ut_bot_position'] = result['ut_bot_position']
df['ut_bot_buy'] = result['ut_bot_buy']
df['ut_bot_sell'] = result['ut_bot_sell']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing OHLC data
- `close_col` (str): Column name for close prices. Default is `'close'`
- `atr_period` (int): Period for ATR calculation. Default is `10`
- `key_value` (float): Sensitivity multiplier for ATR. Default is `3.0`

### Returns

- **DataFrame**: A DataFrame with the following columns:
  - `ut_bot_stop`: The trailing stop level
  - `ut_bot_position`: Position indicator (1 for long, -1 for short, 0 for neutral)
  - `ut_bot_buy`: Buy signals (1 when triggered, 0 otherwise)
  - `ut_bot_sell`: Sell signals (1 when triggered, 0 otherwise)

---

## Weighted Moving Average (WMA)

### Description

The **Weighted Moving Average (WMA)** gives more weight to recent data points and less weight to older data points. It is useful for tracking trends while placing emphasis on recent prices.

### Interpretation

- **WMA** can be used to identify trends similarly to other moving averages, but it reacts faster to price changes due to its weighting system.

### Usage Example

```python
df['wma'] = bta.weighted_moving_average(df, 'close', 10)['wma']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column to calculate the WMA on. Default is `'close'`.
- `period` (int): The period for the WMA calculation. Default is `10`.

### Returns

- **DataFrame**: A DataFrame with the `'wma'` column.

---

## Zero Exponential Moving Average (ZEMA)

### Description

The **Zero Exponential Moving Average (ZEMA)** is an improved version of the **Exponential Moving Average (EMA)** that reduces lag by incorporating a zero-lag component.

### Interpretation

- **ZEMA** is faster to respond to price changes compared to the regular EMA and can be used to detect trends more effectively.

### Usage Example

```python
df['zema'] = bta.zero_exponential_moving_average(df, 'close', 21)['zema']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which ZEMA is to be calculated. Default is `'close'`.
- `period` (int): The period for ZEMA calculation. Default is `21`.

### Returns

- **DataFrame**: A DataFrame with the `'zema'` column.

---

## Zero Lag Exponential Moving Average (ZLEMA)

### Description

The **Zero Lag Exponential Moving Average (ZLEMA)** is an **Exponential Moving Average (EMA)** that adjusts for lag, making it more responsive to recent price changes by using lagged data differences to adjust the EMA calculation.

### Interpretation

- **ZLEMA** provides a faster and more responsive trend signal by reducing the inherent lag of the EMA.

### Usage Example

```python
df['zlema'] = bta.zero_lag_exponential_moving_average(df, 'close', 21)['zlema']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which ZLEMA is to be calculated. Default is `'close'`.
- `period` (int): The period for ZLEMA calculation. Default is `21`.

### Returns

- **DataFrame**: A DataFrame with the `'zlema'` column.

---
