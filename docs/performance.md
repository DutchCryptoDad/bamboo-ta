# `TODO: performance` - Performance Indicators

## Introduction
This module contains functions and technical indicators that are used to evaluate the performance of trading strategies and assets. These indicators help measure returns, volatility, and other key performance metrics.

## Sharpe Ratio

### Description
The **Sharpe Ratio** is a measure of risk-adjusted return. It compares the excess return of an asset (or portfolio) over the risk-free rate to its standard deviation. A higher Sharpe Ratio indicates better risk-adjusted performance.

### Usage Example
```python
df['sharpe_ratio'] = bta.sharpe_ratio(df, risk_free_rate=0.01, window=252)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing asset returns in a column.
- `risk_free_rate` (float): The risk-free rate (e.g., treasury bond rate). Default is `0.01`.
- `window` (int): Look-back period for calculating the Sharpe Ratio. Default is `252` (typically used for daily data in a year).

### Returns
- **DataFrame**: A DataFrame with a single `'sharpe_ratio'` column.

---

## Sortino Ratio

### Description
The **Sortino Ratio** is a variation of the Sharpe Ratio that focuses only on downside volatility. It measures the risk-adjusted return by penalizing negative returns more than positive returns.

### Usage Example
```python
df['sortino_ratio'] = bta.sortino_ratio(df, risk_free_rate=0.01, window=252)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing asset returns in a column.
- `risk_free_rate` (float): The risk-free rate (e.g., treasury bond rate). Default is `0.01`.
- `window` (int): Look-back period for calculating the Sortino Ratio. Default is `252`.

### Returns
- **DataFrame**: A DataFrame with a single `'sortino_ratio'` column.

---

## Maximum Drawdown (MDD)

### Description
The **Maximum Drawdown (MDD)** measures the maximum observed loss from a peak to a trough of an asset or portfolio. It is used to assess the risk of large losses.

### Usage Example
```python
df['mdd'] = bta.maximum_drawdown(df, column='close')
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing price or return data.
- `column` (str): The column to calculate the maximum drawdown on. Default is `'close'`.

### Returns
- **DataFrame**: A DataFrame with a single `'mdd'` column representing the maximum drawdown.

---

## Calmar Ratio

### Description
The **Calmar Ratio** is a performance indicator that measures the return of an asset or portfolio relative to its maximum drawdown. It is a risk-adjusted return metric that emphasizes downside risk.

### Usage Example
```python
df['calmar_ratio'] = bta.calmar_ratio(df, window=252)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing return data.
- `window` (int): Look-back period for calculating the Calmar Ratio. Default is `252`.

### Returns
- **DataFrame**: A DataFrame with a single `'calmar_ratio'` column.

---

## Information Ratio

### Description
The **Information Ratio (IR)** compares the excess return of an asset or portfolio to a benchmark (e.g., an index) relative to the tracking error (standard deviation of excess returns). It is used to assess performance compared to a benchmark.

### Usage Example
```python
df['information_ratio'] = bta.information_ratio(df, benchmark_column='benchmark', window=252)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing returns of the asset and the benchmark.
- `benchmark_column` (str): The column containing benchmark returns.
- `window` (int): Look-back period for calculating the Information Ratio. Default is `252`.

### Returns
- **DataFrame**: A DataFrame with a single `'information_ratio'` column.

---

## Alpha

### Description
**Alpha** measures the excess return of an asset or portfolio relative to the return predicted by the Capital Asset Pricing Model (CAPM). Positive alpha indicates outperformance, while negative alpha indicates underperformance.

### Usage Example
```python
df['alpha'] = bta.alpha(df, benchmark_column='benchmark', risk_free_rate=0.01, window=252)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing asset and benchmark returns.
- `benchmark_column` (str): The column containing benchmark returns.
- `risk_free_rate` (float): The risk-free rate. Default is `0.01`.
- `window` (int): Look-back period for calculating Alpha. Default is `252`.

### Returns
- **DataFrame**: A DataFrame with a single `'alpha'` column.

---

## Beta

### Description
**Beta** measures the sensitivity of an asset's returns to the returns of the market (or a benchmark). A beta greater than 1 indicates that the asset is more volatile than the market, while a beta less than 1 indicates lower volatility.

### Usage Example
```python
df['beta'] = bta.beta(df, benchmark_column='benchmark', window=252)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing asset and benchmark returns.
- `benchmark_column` (str): The column containing benchmark returns.
- `window` (int): Look-back period for calculating Beta. Default is `252`.

### Returns
- **DataFrame**: A DataFrame with a single `'beta'` column.

---

## Treynor Ratio

### Description
The **Treynor Ratio** measures the return of an asset or portfolio relative to its market risk, as measured by beta. It is similar to the Sharpe Ratio but focuses on systematic risk instead of total risk.

### Usage Example
```python
df['treynor_ratio'] = bta.treynor_ratio(df, benchmark_column='benchmark', risk_free_rate=0.01, window=252)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing asset and benchmark returns.
- `benchmark_column` (str): The column containing benchmark returns.
- `risk_free_rate` (float): The risk-free rate. Default is `0.01`.
- `window` (int): Look-back period for calculating the Treynor Ratio. Default is `252`.

### Returns
- **DataFrame**: A DataFrame with a single `'treynor_ratio'` column.

---

## Jensen's Alpha

### Description
**Jensen's Alpha** measures the excess return of an asset or portfolio over its expected return based on the Capital Asset Pricing Model (CAPM). Positive Jensen's Alpha indicates outperformance, while negative alpha indicates underperformance.

### Usage Example
```python
df['jensens_alpha'] = bta.jensens_alpha(df, benchmark_column='benchmark', risk_free_rate=0.01, window=252)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing asset and benchmark returns.
- `benchmark_column` (str): The column containing benchmark returns.
- `risk_free_rate` (float): The risk-free rate. Default is `0.01`.
- `window` (int): Look-back period for calculating Jensen's Alpha. Default is `252`.

### Returns
- **DataFrame**: A DataFrame with a single `'jensens_alpha'` column.

---
