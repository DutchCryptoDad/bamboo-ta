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
