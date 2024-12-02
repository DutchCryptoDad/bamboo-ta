# `volatility` - Volatility Indicators

## Average True Range (ATR)

### Description
The **Average True Range (ATR)** is a measure of market volatility introduced by Welles Wilder in his book "New Concepts in Technical Trading Systems." It represents the average of the True Range over a given period, helping traders measure volatility.

### Usage Example
```python
df['atr'] = bta.average_true_range(df, period=14)['atr']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `'high'`, `'low'`, and `'close'` columns.
- `period` (int): The look-back period for calculating the ATR. Default is `14`.

### Returns
- **DataFrame**: A DataFrame with a single `'atr'` column containing the Average True Range.

---

## Bollinger Bands (BBANDS)

### Description
**Bollinger Bands** are a volatility indicator developed by John Bollinger. They consist of a **middle band** (a moving average), an **upper band** (typically 2 standard deviations above the moving average), and a **lower band** (typically 2 standard deviations below the moving average).

### Usage Example
```python
bb_result = bta.bollinger_bands(df, column='close', period=20, std_dev=2, ddof=0)
df['bb_upper'] = bb_result['bb_upper']
df['bb_middle'] = bb_result['bb_middle']
df['bb_lower'] = bb_result['bb_lower']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column on which to apply the Bollinger Bands calculation. Default is `'close'`.
- `period` (int): The look-back period for calculating the moving average. Default is `20`.
- `std_dev` (float): Number of standard deviations for the upper and lower bands. Default is `2.0`.
- `ddof` (int): Degrees of freedom to use when calculating the standard deviation. Default is `0`.

### Returns
- **DataFrame**: A DataFrame with `'bb_upper'`, `'bb_middle'`, and `'bb_lower'` columns representing the Bollinger Bands.

---

## Bollinger Band Width Expansion (BBW Expansion)

### Description
**BBW Expansion** detects significant expansions in the Bollinger Band Width (BBW), which can signal potential increases in market volatility. This is determined by comparing the most recent BBW value against a rolling maximum multiplied by a specified factor. The indicator requires the **Bollinger Bands** to be calculated beforehand using the `bta.bollinger_bands` function.

### Interpretation
- **BBW Expansion Indicator**:
  - A value of `1` indicates that the current BBW exceeds the rolling maximum by the specified multiplier, suggesting a possible volatility increase.
  - A value of `0` indicates no significant expansion in the Bollinger Band Width.

### Usage Example
```python
# First, calculate Bollinger Bands
df = bta.bollinger_bands(df, period=20)

# Then, detect BBW expansion
df['bbw_expansion'] = bta.bbw_expansion(df, upper_band='bb_upper', lower_band='bb_lower', 
                                         middle_band='bb_middle', mult=1.1, rolling_window=20)['bbw_expansion']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing columns for Bollinger Bands.
- `upper_band` (str, default=`'bb_upper'`): Column name for the upper Bollinger Band.
- `lower_band` (str, default=`'bb_lower'`): Column name for the lower Bollinger Band.
- `middle_band` (str, default=`'bb_middle'`): Column name for the middle Bollinger Band.
- `mult` (float, default=`1.1`): Multiplier to compare the last BBW value against the rolling maximum.
- `rolling_window` (int, default=`20`): Size of the rolling window for calculating the maximum BBW.

### Returns
- **DataFrame**: A DataFrame with the following additional columns:
  - `'bb_width'`: Bollinger Band Width values.
  - `'bbw_expansion'`: Indicator for expansion (`1` if expansion is detected, otherwise `0`).

### Notes
- The Bollinger Bands (`bb_upper`, `bb_middle`, `bb_lower`) must be computed before using this function.
- The multiplier (`mult`) can be adjusted to change sensitivity to expansions. A lower value increases sensitivity, while a higher value reduces it.
- Shortening the `rolling_window` makes the indicator more responsive to recent changes.

--- 

## True Range (TR)

### Description
The **True Range (TR)** is a volatility indicator that measures the range of a financial instrument, taking into account any gaps from the previous day's close. It is defined as the maximum of:
- The current high minus the current low.
- The absolute value of the current high minus the previous close.
- The absolute value of the current low minus the previous close.

### Usage Example
```python
df['true_range'] = bta.true_range(df)['true_range']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'high'`, `'low'`, and `'close'` columns.

### Returns
- **DataFrame**: A DataFrame with a single `'true_range'` column containing the True Range.

---

## Upcoming Indicators

The following indicators are planned for future implementation:
- **Keltner Channel** (with width).
- **Donchian Channel** (with width).
- **Ulcer Index**: A volatility indicator that measures the percentage drawdown over time, often used to assess risk.

For more information, check resources such as [StockCharts - Ulcer Index](https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ulcer_index).

---
