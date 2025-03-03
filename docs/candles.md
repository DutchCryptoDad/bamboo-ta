# `candles` - Technical Analysis Indicators

## Leledc Exhaustion Bars

### Description

The **Leledc Exhaustion Bars** are a reversal indicator that identifies potential trend reversals by looking for price exhaustion. This occurs when there is a sharp price move combined with increased volume, indicating that the current trend may be losing momentum.

### Interpretation

- **Leledc Major** (`leledc_major`): Signals major reversals in price. A value of `1` indicates a potential bullish reversal, while `-1` suggests a bearish reversal.
- **Leledc Minor** (`leledc_minor`): Signals smaller or minor reversals. A value of `1` indicates a minor bullish reversal, and `-1` indicates a minor bearish reversal.

### Usage Example

```python
exhaustion = bta.exhaustion_bars(df)
df['leledc_major'] = exhaustion['leledc_major']
df['leledc_minor'] = exhaustion['leledc_minor']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame with columns `open`, `high`, `low`, and `close`.
- `maj_qual` (int): Major quality threshold. Default is `6`.
- `maj_len` (int): Major length. Default is `30`.
- `min_qual` (int): Minor quality threshold. Default is `5`.
- `min_len` (int): Minor length. Default is `5`.
- `core_length` (int): Core length for pattern recognition. Default is `4`.

### Returns

- **DataFrame**: A DataFrame with two columns:
  - `'leledc_major'`: Major reversal signal.
  - `'leledc_minor'`: Minor reversal signal.

---

## Dynamic Leledc Exhaustion Bars

### Description

The **Dynamic Leledc Exhaustion Bars** dynamically adjust their lookback window based on market conditions. They are useful for identifying reversals in volatile markets where price behavior changes rapidly.

### Interpretation

- **Dynamic Leledc Major** (`dynamic_leledc_major`): A dynamic version of the Leledc Major that adapts to market conditions.
- **Dynamic Leledc Minor** (`dynamic_leledc_minor`): A dynamic version of the Leledc Minor that adapts to market conditions.

### Usage Example

```python
dynamic_exhaustion = bta.dynamic_exhaustion_bars(df)
df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame with a `close` column.
- `window` (int): Lookback window for z-score calculation. Default is `500`.

### Returns

- **DataFrame**: A DataFrame with two columns:
  - `'leledc_major'`: Dynamic major reversal signal.
  - `'leledc_minor'`: Dynamic minor reversal signal.

---

## Hansen Heiken Ashi (HHA)

### Description

**Hansen Heiken Ashi (HHA)** is a modified version of the Heiken Ashi candlestick calculation. It incorporates a custom formula for the open value (`hhopen`) and uses a Simple Moving Average (SMA) to smooth the calculated values, reducing noise for better trend visualization.

### Interpretation

- **Smoothed Hansen Heiken Ashi Values**:
  - The `emac` (smoothed close) represents the overall trend direction with reduced noise.
  - The `emao` (smoothed open) serves as a secondary confirmation of trend continuation or reversal.

### Usage Example

```python
hha_result = bta.hansen_heiken_ashi(df, period=6)
df['hha_emac'] = hha_result['emac']
df['hha_emao'] = hha_result['emao']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame containing the following OHLC columns:
  - `'open'`
  - `'high'`
  - `'low'`
  - `'close'`
- `period` (int, default=6): The period for the Simple Moving Average (SMA) to smooth the calculated values.

### Returns

- **DataFrame**: A DataFrame with two columns:
  - `'emac'`: Smoothed Hansen Heiken Ashi close values.
  - `'emao'`: Smoothed Hansen Heiken Ashi open values.

### Notes

- The HHA indicator is particularly effective in volatile markets for identifying trends with reduced noise.
- The modified `hhopen` calculation differs from traditional Heiken Ashi, potentially providing improved trend clarity.

---

## Heiken Ashi

### Description

**Heiken Ashi** charts are a modified form of candlestick charts that smooth out price action, making it easier to identify trends. Optional pre- and post-smoothing can further refine the visual representation of the trend.

### Interpretation

- **Heiken Ashi Candles** help reduce noise and make trend-following easier. When the Heiken Ashi close is higher than the open, the market is in an uptrend, and vice versa.

### Usage Example

```python
ha_df = bta.heiken_ashi(df)
df['ha_open'] = ha_df['ha_open']
df['ha_high'] = ha_df['ha_high']
df['ha_low'] = ha_df['ha_low']
df['ha_close'] = ha_df['ha_close']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame with columns `open`, `high`, `low`, and `close`.
- `pre_smoothing_period` (int, optional): If provided, smooths data before Heiken Ashi calculations.
- `post_smoothing_period` (int, optional): If provided, smooths the Heiken Ashi values after calculation.

### Returns

- **DataFrame**: A DataFrame with four columns:
  - `'ha_open'`: Heiken Ashi open.
  - `'ha_high'`: Heiken Ashi high.
  - `'ha_low'`: Heiken Ashi low.
  - `'ha_close'`: Heiken Ashi close.

---

## Smoothed Heiken Ashi (smoothed_heiken_ashi)

### Description

**Smoothed Heiken Ashi** is a type of candlestick chart that uses the Heiken Ashi method to smooth out price action. It's an extension of the standard Heiken Ashi which adds two more moving averages, one for open and high values and another for low and close values.

### Usage Example

```python
sha_result = bta.smoothed_heiken_ashi(df, len_=10, len2=10)
df["sha_open"] = sha_result["sha_open"]
df["sha_high"] = sha_result["sha_high"]
df["sha_low"] = sha_result["sha_low"]
df["sha_close"] = sha_result["sha_close"]
df["sha_color"] = sha_result["sha_color"]
```

### output DataFrame columns

- `sha_open`: The open price of the Heiken Ashi candlestick.
- `sha_high`: The high price of the Heiken Ashi candlestick.
- `sha_low`: The low price of the Heiken Ashi candlestick.
- `sha_close`: The close price of the Heiken Ashi candlestick.
- `sha_color`: Indicates bullish (green), bearish (red), or sideways (gray) candlesticks.

### Interpretation

- The `sha_color` column in the output DataFrame indicates bullish (green), bearish (red), or sideways (gray) candlesticks.
- A bullish candlestick is a green one with an open price less than its close, indicating that the market was upwards moving after the previous day.
- A bearish candlestick is a red one with an open price greater than its close, indicating that the market was downward moving after the previous day.
- A sideways candlestick is gray in color, indicating no significant change in the market's direction.
- The `sha_open`, `sha_high`, `sha_low` and `sha_close` columns represent the Heiken Ashi values for each period. These can be used to plot a candlestick chart or other technical analysis tools.
- The smoothing helps reduce noise in the data and makes it easier to identify trends and potential buy/sell signals.

---

## Linear Regression Candles

### Description

**Linear Regression Candles** smooth out price action using a linear regression algorithm. An optional signal line can be added to indicate potential buy or sell signals based on trend strength.

### Interpretation

- **Linear Regression Candles** smooth price action, helping traders identify trends and make decisions based on the slope of the linear regression lines.
- The **Signal Line** adds a moving average of the regression candle close, which can serve as a trend confirmation.

### Usage Example

```python
lr_df = bta.linear_regression_candles(df)
df['lrc_open'] = lr_df['bopen']
df['lrc_high'] = lr_df['bhigh']
df['lrc_low'] = lr_df['blow']
df['lrc_close'] = lr_df['bclose']
df['lrc_signal'] = lr_df['signal']
```

### Parameters

- `df` (pandas.DataFrame): Input DataFrame with columns `open`, `high`, `low`, and `close`.
- `linreg_length` (int): Lookback period for linear regression. Default is `11`.
- `sma_signal` (bool): If `True`, uses SMA for the signal line. If `False`, uses EMA. Default is `True`.
- `signal_length` (int): Lookback period for the signal line. Default is `11`.

### Returns

- **DataFrame**: A DataFrame with five columns:
  - `'bopen'`: Linear regression open.
  - `'bhigh'`: Linear regression high.
  - `'blow'`: Linear regression low.
  - `'bclose'`: Linear regression close.
  - `'signal'`: Signal line (SMA or EMA).
