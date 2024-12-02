# `volume` - Volume-Based Technical Indicators

## Accumulation/Distribution Index (ADI)

### Description
The **Accumulation/Distribution Index (ADI)** is a volume-based indicator that measures the cumulative flow of money into or out of a security. It uses the relationship between the price’s range (high and low) and its closing price to calculate the **Close Location Value (CLV)**.

### Usage Example
```python
df['adi'] = bta.accumulation_distribution_index(df, fillna=True)['adi']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'high'`, `'low'`, `'close'`, and `'volume'` columns.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with a single `'adi'` column.

---

## Chaikin Money Flow (CMF)

### Description
The **Chaikin Money Flow (CMF)** indicator measures the amount of Money Flow Volume over a specific period. It uses the relationship between the close price and the range (high and low) to evaluate buying or selling pressure.

### Usage Example
```python
df['cmf'] = bta.chaikin_money_flow(df, window=20, fillna=True)['cmf']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'high'`, `'low'`, `'close'`, and `'volume'` columns.
- `window` (int): Look-back period for the calculation. Default is `20`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with a single `'cmf'` column.

---

## Ease of Movement (EoM)

### Description
The **Ease of Movement (EoM)** indicator relates the price movement of an asset to its volume, helping assess trend strength. The **Signal Ease of Movement (SEoM)** is a smoothed version of EoM, calculated using a moving average.

### Usage Example
```python
eom_df = bta.ease_of_movement(df, eom_length=14, seom_length=14, fillna=True)
df['eom'] = eom_df['eom']
df['seom'] = eom_df['seom']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'high'`, `'low'`, and `'volume'` columns.
- `eom_length` (int): Period for the EoM calculation. Default is `14`.
- `seom_length` (int): Period for the SEoM calculation. Default is `14`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with `'eom'` and `'seom'` columns.

---

## Force Index (FI)

### Description
The **Force Index (FI)** measures the strength of price movements by combining price changes and volume. It helps illustrate the buying or selling pressure in the market.

### Usage Example
```python
df['fi'] = bta.force_index(df, window=13, fillna=True)['fi']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'close'` and `'volume'` columns.
- `window` (int): Period for the exponential moving average of the Force Index. Default is `13`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with a single `'fi'` column.

---

## Money Flow Index (MFI)

### Description
The **Money Flow Index (MFI)** is a momentum indicator that uses both price and volume data to measure buying and selling pressure. It is often referred to as a **volume-weighted RSI**.

### Usage Example
```python
df['mfi'] = bta.money_flow_index(df, window=14, fillna=True)['mfi']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'high'`, `'low'`, `'close'`, and `'volume'` columns.
- `window` (int): Look-back period for the MFI calculation. Default is `14`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with a single `'mfi'` column.

---

## Negative Volume Index (NVI)

### Description
The **Negative Volume Index (NVI)** accumulates the percentage rate of change in price on days when trading volume decreases compared to the previous day. It helps identify trends driven by low-volume days.

### Usage Example
```python
nvi_df = bta.negative_volume_index(df, signal_type='EMA', signal_length=255, fillna=True)
df['nvi'] = nvi_df['nvi']
df['nvi_signal'] = nvi_df['nvi_signal']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'close'` and `'volume'` columns.
- `signal_type` (str): Type of signal smoothing ('EMA' or 'SMA'). Default is `'EMA'`.
- `signal_length` (int): Length for the signal smoothing calculation. Default is `255`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with `'nvi'` and `'nvi_signal'` columns.

---

## On Balance Volume (OBV)

### Description
The **On Balance Volume (OBV)** indicator measures buying and selling pressure by adding volume when the close price is higher than the previous close and subtracting volume when the close price is lower.

### Usage Example
```python
obv_df = bta.on_balance_volume(df, signal_type='SMA', signal_length=21, show_signal=True, fillna=True)
df['obv'] = obv_df['obv']
df['signal'] = obv_df['signal']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'close'` and `'volume'` columns.
- `signal_type` (str): Type of signal smoothing ('SMA' or 'EMA'). Default is `'SMA'`.
- `signal_length` (int): Period for signal calculation. Default is `21`.
- `show_signal` (bool): If `True`, calculate and return the signal line. Default is `True`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with `'obv'` and `'signal'` columns.

---

## On Balance Volume Oscillator (OBV Oscillator)

### Description
The **On Balance Volume Oscillator** measures the difference between the OBV and its Exponential Moving Average (EMA). It helps identify trends and confirm price movements.

### Usage Example
```python
df['obv_oscillator'] = bta.on_balance_volume_oscillator(df, length=20, fillna=True)['obv_oscillator']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'close'` and `'volume'` columns.
- `length` (int): Length for the EMA calculation. Default is `20`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with a single `'obv_oscillator'` column.

---

## Positive Volume Index (PVI)

### Description
The **Positive Volume Index (PVI)** accumulates the percentage rate of change in price on days when trading volume increases compared to the previous day. It helps identify trends driven by high-volume days.

### Usage Example
```python
pvi_df = bta.positive_volume_index(df, signal_type='EMA', signal_length=255, fillna=True)
df['pvi'] = pvi_df['pvi']
df['pvi_signal'] = pvi_df['pvi_signal']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'close'` and `'volume'` columns.
- `signal_type` (str): Type of signal smoothing ('EMA' or 'SMA'). Default is `'EMA'`.
- `signal_length` (int): Length for signal calculation. Default is `255`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with `'pvi'` and `'pvi_signal'` columns.

---

## Price Volume Trend (PVT)

### Description
The **Price Volume Trend (PVT)** indicator combines price and volume to measure the strength of trends. It accumulates the volume proportional to the price movement.

### Usage Example
```python
pvt_df = bta.price_volume_trend(df, fillna=True, signal_type='EMA', signal_length=21, dropnans=True)
df['pvt'] = pvt_df['price_volume_trend']
df['pvt_signal'] = pvt_df['signal']
```

### Parameters
- `df` (p

andas.DataFrame): Input DataFrame containing `'close'` and `'volume'` columns.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.
- `smoothing_factor` (int, optional): Apply SMA smoothing to the PVT values.
- `signal_type` (str): Type of signal smoothing ('EMA' or 'SMA'). Default is `'SMA'`.
- `signal_length` (int): Length for signal calculation. Default is `21`.
- `dropnans` (bool): Drop NaN values after calculation. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with `'price_volume_trend'` and `'signal'` columns.

---

## Relative Volume (RVOL)

### Description
**Relative Volume (RVOL)** measures the current volume relative to its historical average over a specified lookback period. It is useful for identifying periods of unusually high or low trading activity, which can signify significant market events or conditions.

### Interpretation
- **High RVOL (> 1)**: Indicates that the current volume is above the historical average, potentially signifying increased trader interest or volatility.
- **Low RVOL (< 1)**: Indicates that the current volume is below the historical average, suggesting a lack of interest or quiet market conditions.

### Usage Example
```python
# Calculate Relative Volume with a 24-period SMA
df['rvol'] = bta.relative_volume(df, volume_col='volume', window=24)['rvol']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a volume column.
- `volume_col` (str, default=`'volume'`): Name of the column containing volume data.
- `window` (int, default=`24`): Lookback window for calculating the Simple Moving Average (SMA) of volume.

### Returns
- **DataFrame**: A DataFrame with the following additional column:
  - `'rvol'`: The Relative Volume values, computed as the ratio of the current volume to the SMA of the volume over the specified window.

### Notes
- This indicator is sensitive to the lookback period (`window`); shorter windows will make it more responsive to recent changes in volume, while longer windows provide a more stable comparison.
- Ensure the volume column contains non-zero values to avoid division by zero errors.

---

## Volume Weighted Average Price (VWAP)

### Description
The **Volume Weighted Average Price (VWAP)** represents the average price a security has traded at throughout the day, based on both volume and price. It is often used to assess whether a security is trading above or below its average price.

### Usage Example
```python
df['vwap'] = bta.volume_weighted_average_price(df, window=14, fillna=True)['volume_weighted_average_price']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'high'`, `'low'`, `'close'`, and `'volume'` columns.
- `window` (int): The number of periods for the rolling calculation. Default is `14`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with a single `'volume_weighted_average_price'` column.

---

## Volume-Weighted Average Price Bands (VWAPB)

### Description
The **Volume-Weighted Average Price Bands (VWAPB)** indicator calculates the Volume-Weighted Average Price (VWAP) along with upper and lower bands based on a rolling standard deviation. VWAP is a benchmark price that reflects the average price a security has traded at throughout the day, based on both volume and price.

### Interpretation
- **VWAP (`vwap`)**:
  - Represents the average price at which a security has traded, weighted by volume.
  - A commonly used intraday benchmark for trading decisions.
- **VWAP Low (`vwap_low`)**:
  - Represents the lower band.
- **VWAP High (`vwap_high`)**:
  - Represents the upper band.

These bands provide an indication of price volatility around the VWAP.

### Call with

```python
vwapb_result = bta.volume_weighted_average_price_bands(df, window_size=20, num_of_std=1.0)

# Integrate results into the original DataFrame
df['vwap_low'] = vwapb_result['vwap_low']
df['vwap'] = vwapb_result['vwap']
df['vwap_high'] = vwapb_result['vwap_high']
```

### Parameters
- **`df`** (*pandas.DataFrame*): Input DataFrame containing the following required columns:
  - `'close'`: Closing price for each interval.
  - `'high'`: High price for each interval.
  - `'low'`: Low price for each interval.
  - `'volume'`: Trading volume for each interval.
- **`window_size`** (*int*, default=`20`): The rolling window size for VWAP and standard deviation calculations.
- **`num_of_std`** (*float*, default=`1.0`): The number of standard deviations to calculate the upper and lower bands.

### Returns
- **`pd.DataFrame`**: A DataFrame containing the following columns:
  - **`vwap`**: The Volume-Weighted Average Price (VWAP).
  - **`vwap_low`**: The lower band (VWAP - num_of_std × rolling std deviation).
  - **`vwap_high`**: The upper band (VWAP + num_of_std × rolling std deviation).

### Usage Example

```python
# Example DataFrame
data = {
    'close': [100, 102, 101, 103, 104],
    'high': [101, 103, 102, 104, 105],
    'low': [99, 101, 100, 102, 103],
    'volume': [200, 220, 210, 230, 240]
}
df = pd.DataFrame(data)

# Calculate VWAP and bands
vwapb_result = bta.volume_weighted_average_price_bands(df, window_size=3, num_of_std=1.0)

# Integrate results into the original DataFrame
df['vwap_low'] = vwapb_result['vwap_low']
df['vwap'] = vwapb_result['vwap']
df['vwap_high'] = vwapb_result['vwap_high']

# Display the updated DataFrame
print(df)
```

### Notes
- The **VWAP** and bands (`vwap_low`, `vwap_high`) are computed using a rolling window, so the first `window_size - 1` rows will contain `NaN` values.
- Ensure the input DataFrame contains the required columns (`close`, `high`, `low`, `volume`); otherwise, the function will raise a `ValueError`.
- This indicator is most effective for intraday trading strategies.
