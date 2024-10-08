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

## Heikin Ashi

### Description
**Heikin Ashi** charts are a modified form of candlestick charts that smooth out price action, making it easier to identify trends. Optional pre- and post-smoothing can further refine the visual representation of the trend.

### Interpretation
- **Heikin Ashi Candles** help reduce noise and make trend-following easier. When the Heikin Ashi close is higher than the open, the market is in an uptrend, and vice versa.

### Usage Example
```python
ha_df = bta.heikin_ashi(df)
df['ha_open'] = ha_df['ha_open']
df['ha_high'] = ha_df['ha_high']
df['ha_low'] = ha_df['ha_low']
df['ha_close'] = ha_df['ha_close']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame with columns `open`, `high`, `low`, and `close`.
- `pre_smoothing_period` (int, optional): If provided, smooths data before Heikin Ashi calculations.
- `post_smoothing_period` (int, optional): If provided, smooths the Heikin Ashi values after calculation.

### Returns
- **DataFrame**: A DataFrame with four columns:
  - `'ha_open'`: Heikin Ashi open.
  - `'ha_high'`: Heikin Ashi high.
  - `'ha_low'`: Heikin Ashi low.
  - `'ha_close'`: Heikin Ashi close.

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

