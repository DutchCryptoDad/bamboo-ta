# `TODO: statistics` - Statistical Indicators

## Introduction
This module contains statistical functions and technical indicators used for analyzing price movements, correlations, and distributions in financial markets.

## Pearson Correlation Coefficient

### Description
The **Pearson Correlation Coefficient** measures the linear correlation between two variables (e.g., two assets). The coefficient value ranges between -1 and +1, where:
- **+1** indicates a perfect positive correlation.
- **-1** indicates a perfect negative correlation.
- **0** indicates no correlation.

### Usage Example
```python
df['pearson_corr'] = bta.pearson_correlation(df['asset1'], df['asset2'], window=30)
```

### Parameters
- `series1` (pd.Series): First input series.
- `series2` (pd.Series): Second input series.
- `window` (int): Look-back period for calculating the rolling Pearson correlation. Default is `30`.

### Returns
- **pd.Series**: Series containing the Pearson correlation values.

---

## Spearman Rank Correlation

### Description
The **Spearman Rank Correlation** measures the strength and direction of the monotonic relationship between two ranked variables. It is less sensitive to outliers compared to the Pearson correlation and is used for non-linear relationships.

### Usage Example
```python
df['spearman_corr'] = bta.spearman_correlation(df['asset1'], df['asset2'], window=30)
```

### Parameters
- `series1` (pd.Series): First input series.
- `series2` (pd.Series): Second input series.
- `window` (int): Look-back period for calculating the rolling Spearman correlation. Default is `30`.

### Returns
- **pd.Series**: Series containing the Spearman correlation values.

---

## Covariance

### Description
**Covariance** measures the directional relationship between two variables. A positive covariance indicates that the variables tend to move together, while a negative covariance suggests they move inversely.

### Usage Example
```python
df['covariance'] = bta.covariance(df['asset1'], df['asset2'], window=30)
```

### Parameters
- `series1` (pd.Series): First input series.
- `series2` (pd.Series): Second input series.
- `window` (int): Look-back period for calculating rolling covariance. Default is `30`.

### Returns
- **pd.Series**: Series containing the covariance values.

---

## Variance

### Description
**Variance** measures the dispersion of a dataset relative to its mean. It is a common measure of volatility in financial markets. Higher variance indicates more variability in the data.

### Usage Example
```python
df['variance'] = bta.variance(df['close'], window=30)
```

### Parameters
- `series` (pd.Series): Input series (e.g., price data).
- `window` (int): Look-back period for calculating the rolling variance. Default is `30`.

### Returns
- **pd.Series**: Series containing the variance values.

---

## Standard Deviation

### Description
**Standard Deviation** is a measure of the amount of variation or dispersion in a dataset. It is the square root of variance and is commonly used to assess the volatility of asset prices.

### Usage Example
```python
df['std_dev'] = bta.standard_deviation(df['close'], window=30)
```

### Parameters
- `series` (pd.Series): Input series (e.g., price data).
- `window` (int): Look-back period for calculating the rolling standard deviation. Default is `30`.

### Returns
- **pd.Series**: Series containing the standard deviation values.

---

## Z-Score

### Description
The **Z-Score** indicates how many standard deviations a data point is from the mean of the dataset. It is used to measure how unusual or extreme a data point is relative to the distribution.

### Usage Example
```python
df['zscore'] = bta.z_score(df['close'], window=500)
```

### Parameters
- `series` (pd.Series): Input series (e.g., price data).
- `window` (int): Look-back period for calculating the rolling Z-score. Default is `500`.

### Returns
- **pd.Series**: Series containing the Z-score values.

---

## Skewness

### Description
**Skewness** measures the asymmetry of the distribution of data points. Positive skewness indicates a longer or fatter right tail, while negative skewness indicates a longer or fatter left tail.

### Usage Example
```python
df['skewness'] = bta.skewness(df['close'], window=30)
```

### Parameters
- `series` (pd.Series): Input series (e.g., price data).
- `window` (int): Look-back period for calculating rolling skewness. Default is `30`.

### Returns
- **pd.Series**: Series containing the skewness values.

---

## Kurtosis

### Description
**Kurtosis** measures the "tailedness" of the distribution of data points. High kurtosis indicates heavy tails, suggesting the presence of outliers, while low kurtosis indicates light tails.

### Usage Example
```python
df['kurtosis'] = bta.kurtosis(df['close'], window=30)
```

### Parameters
- `series` (pd.Series): Input series (e.g., price data).
- `window` (int): Look-back period for calculating rolling kurtosis. Default is `30`.

### Returns
- **pd.Series**: Series containing the kurtosis values.

---

## Rolling Beta

### Description
The **Rolling Beta** measures the sensitivity of an asset's returns to the returns of a benchmark over a rolling window. It is used to assess how much an asset's price movement is influenced by the market.

### Usage Example
```python
df['rolling_beta'] = bta.rolling_beta(df['asset'], df['benchmark'], window=30)
```

### Parameters
- `series1` (pd.Series): Series of asset returns.
- `series2` (pd.Series): Series of benchmark returns.
- `window` (int): Look-back period for calculating rolling beta. Default is `30`.

### Returns
- **pd.Series**: Series containing the rolling beta values.

---
