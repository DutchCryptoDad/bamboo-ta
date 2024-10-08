# `TODO: cycles` - Cycles-Based Indicators

## Introduction
This module contains technical indicators that help identify cyclical behavior in financial markets. These indicators are typically used to detect repeating patterns or oscillations in the market.

## Hilbert Transform - Instantaneous Trendline

### Description
The **Hilbert Transform - Instantaneous Trendline** is used to smooth out price action and help identify the underlying trend of the market. It is based on the **Hilbert Transform**, which helps filter out noise in price data and highlights the dominant cycle.

### Usage Example
```python
df['inst_trendline'] = bta.hilbert_instantaneous_trendline(df, 'close')
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a `'close'` column.
- `column` (str): Column to be used for the calculation. Default is `'close'`.

### Returns
- **DataFrame**: A DataFrame with a single `'inst_trendline'` column representing the smoothed trendline.

---

## Hilbert Transform - Dominant Cycle Period

### Description
The **Hilbert Transform - Dominant Cycle Period** is used to identify the dominant cycle present in the market by analyzing price data. It helps detect the most prominent periodic behavior in the market.

### Usage Example
```python
df['dominant_cycle_period'] = bta.hilbert_dominant_cycle_period(df, 'close')
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a `'close'` column.
- `column` (str): Column to be used for the calculation. Default is `'close'`.

### Returns
- **DataFrame**: A DataFrame with a single `'dominant_cycle_period'` column representing the dominant cycle length.

---

## Hilbert Transform - Dominant Cycle Phase

### Description
The **Hilbert Transform - Dominant Cycle Phase** measures the phase of the dominant cycle in the market. It can be used to identify turning points where price action shifts from one cycle phase to another.

### Usage Example
```python
df['dominant_cycle_phase'] = bta.hilbert_dominant_cycle_phase(df, 'close')
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a `'close'` column.
- `column` (str): Column to be used for the calculation. Default is `'close'`.

### Returns
- **DataFrame**: A DataFrame with a single `'dominant_cycle_phase'` column representing the phase of the dominant cycle.

---

## Hilbert Transform - Dominant Cycle Phase Slope

### Description
The **Hilbert Transform - Dominant Cycle Phase Slope** calculates the slope of the dominant cycle phase, which helps identify whether the cycle is accelerating or decelerating. This can be useful for detecting potential trend changes.

### Usage Example
```python
df['dominant_cycle_slope'] = bta.hilbert_dominant_cycle_phase_slope(df, 'close')
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a `'close'` column.
- `column` (str): Column to be used for the calculation. Default is `'close'`.

### Returns
- **DataFrame**: A DataFrame with a single `'dominant_cycle_slope'` column representing the slope of the dominant cycle phase.

---

## Sinewave Indicator

### Description
The **Sinewave Indicator** is a cycle-based indicator that helps identify potential turning points in the market by measuring the oscillation between bullish and bearish phases.

### Usage Example
```python
sinewave_df = bta.sinewave(df, 'close')
df['sinewave'] = sinewave_df['sinewave']
df['lead_sinewave'] = sinewave_df['lead_sinewave']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a `'close'` column.
- `column` (str): Column to be used for the calculation. Default is `'close'`.

### Returns
- **DataFrame**: A DataFrame with two columns:
  - `'sinewave'`: The sinewave component.
  - `'lead_sinewave'`: The leading sinewave component, which may give early warning of trend changes.

---

## Time Series Forecast

### Description
The **Time Series Forecast (TSF)** is used to forecast future prices based on past price data. It uses a linear regression model to predict future price movements based on a given look-back period.

### Usage Example
```python
df['tsf'] = bta.time_series_forecast(df, 'close', lookback=14)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a `'close'` column.
- `column` (str): Column to be used for the calculation. Default is `'close'`.
- `lookback` (int): Number of periods to look back for the forecast. Default is `14`.

### Returns
- **DataFrame**: A DataFrame with a single `'tsf'` column representing the forecasted price.

---

## Two-Pole Super Smoother

### Description
The **Two-Pole Super Smoother** is a smoothing filter that reduces noise in price data while maintaining responsiveness to price changes. It is particularly useful for filtering out short-term fluctuations while highlighting trends.

### Usage Example
```python
df['super_smoother'] = bta.two_pole_super_smoother(df, 'close', period=14)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a `'close'` column.
- `column` (str): Column to be used for the calculation. Default is `'close'`.
- `period` (int): Period for the smoothing calculation. Default is `14`.

### Returns
- **DataFrame**: A DataFrame with a single `'super_smoother'` column representing the smoothed values.

---
