# `utility` - Utility Functions for Technical Analysis

## calculate_atr_stop_loss_take_profit

### Description
This function calculates the **take profit**, **stop loss**, and **buy price** levels based on the **ATR (Average True Range)**, signal, and changes in trading advice. It checks when the trading signal changes (e.g., from `buy` to `sell`), and sets the take profit and stop loss accordingly.

### Usage Example
```python
atr_sl_tp_df = bta.calculate_atr_stop_loss_take_profit(df, signal_column='signal')
df['takeprofit'] = atr_sl_tp_df['takeprofit']
df['stoploss'] = atr_sl_tp_df['stoploss']
df['buyprice'] = atr_sl_tp_df['buyprice']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing columns `'signal'`, `'close'`, and `'atr'`.
- `signal_column` (str): Column with buy/sell signals. Default is `'signal'`.
- `atr_column` (str): Column with ATR values. Default is `'atr'`.
- `atr_sl_mult` (float): Multiplier for stop loss based on ATR. Default is `1`.
- `atr_tp_mult` (float): Multiplier for take profit based on ATR. Default is `2`.

### Returns
- **DataFrame**: A DataFrame with columns `'takeprofit'`, `'stoploss'`, and `'buyprice'`.

---

## calculate_stop_loss_take_profit

### Description
Calculates the **stop loss**, **take profit**, and **entry price** based on customizable trade signals for both long and short trades. It uses user-defined risk/reward ratios to determine the levels for both long and short trades.

### Usage Example
```python
stop_loss_take_profit = bta.calculate_stop_loss_take_profit(df, 
                                                            signal_column='trade_signal',
                                                            long_trade_signal='long_trade', 
                                                            short_trade_signal='short_trade', 
                                                            no_trade_signal='no_trade', 
                                                            lookback_period=5, 
                                                            long_reward_ratio=2, 
                                                            short_reward_ratio=1.5, 
                                                            buffer=0.5)
df['stop_loss'] = stop_loss_take_profit['stop_loss']
df['entry_price'] = stop_loss_take_profit['entry_price']
df['take_profit'] = stop_loss_take_profit['take_profit']
df['exit_reason'] = stop_loss_take_profit['exit_reason']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing trade signals and price data.
- `signal_column` (str): Column storing trade signals. Default is `'trade_signal'`.
- `long_trade_signal` (str): Value in the signal column that represents a long trade. Default is `'long_trade'`.
- `short_trade_signal` (str): Value in the signal column that represents a short trade. Default is `'short_trade'`.
- `no_trade_signal` (str): Value in the signal column that represents no trade. Default is `'no_trade'`.
- `lookback_period` (int): Lookback period for calculating stop loss. Default is `5`.
- `long_reward_ratio` (float): Reward-risk ratio for long trades. Default is `2`.
- `short_reward_ratio` (float): Reward-risk ratio for short trades. Default is `2`.
- `buffer` (float): Buffer added to stop loss. Default is `0.0`.

### Returns
- **DataFrame**: A DataFrame with columns `'stop_loss'`, `'take_profit'`, `'entry_price'`, and `'exit_reason'`.

---

## consecutive_count

### Description
Calculates the average consecutive count of non-zero differences in an array.

### Usage Example
```python
avg_count = bta.consecutive_count(consecutive_diff)
```

### Parameters
- `consecutive_diff` (np.ndarray): Array of consecutive differences.

### Returns
- **float**: Average consecutive count, or 0 if there are fewer than two non-zero differences.

---

## first_crossed_above_second

### Description
Checks if the first series crosses above the second series.

### Usage Example
```python
df['first_crossed_above_second'] = bta.first_crossed_above_second(series1, series2)
```

### Parameters
- `series1` (pd.Series): First input series.
- `series2` (pd.Series): Second input series.

### Returns
- **pd.Series**: Boolean series where `True` indicates a crossover above.

---

## first_crossed_below_second

### Description
Checks if the first series crosses below the second series.

### Usage Example
```python
df['first_crossed_below_second'] = bta.first_crossed_below_second(series1, series2)
```

### Parameters
- `series1` (pd.Series): First input series.
- `series2` (pd.Series): Second input series.

### Returns
- **pd.Series**: Boolean series where `True` indicates a crossover below.

---

## cumulative_return

### Description
Calculates the **Cumulative Return (CR)** of a specified column.

### Usage Example
```python
df['cumulative_return'] = bta.cumulative_return(df)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing price data.
- `column` (str): Column on which the cumulative return is calculated. Default is `'close'`.
- `fillna` (bool): If `True`, fills NaN values. Default is `False`.

### Returns
- **pd.Series**: Series of cumulative return values.

---

## daily_log_return

### Description
Calculates the **Daily Log Return (DLR)** of a specified column.

### Usage Example
```python
df['daily_log_return'] = bta.daily_log_return(df)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing price data.
- `column` (str): Column on which the daily log return is calculated. Default is `'close'`.
- `fillna` (bool): If `True`, fills NaN values. Default is `False`.

### Returns
- **pd.Series**: Series of daily log return values.

---

## daily_return

### Description
Calculates the **Daily Return (DR)** of a specified column.

### Usage Example
```python
df['daily_return'] = bta.daily_return(df)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing price data.
- `column` (str): Column on which the daily return is calculated. Default is `'close'`.
- `fillna` (bool): If `True`, fills NaN values. Default is `False`.

### Returns
- **pd.Series**: Series of daily return values.

---

## exhaustion_candles

### Description
Calculates **Exhaustion Candles** by dynamically adjusting major and minor quality values based on consecutive price movements.

### Usage Example
```python
maj_qual, min_qual = bta.exhaustion_candles(df, window=1, multiplier=1)
df['maj_qual'] = maj_qual
df['min_qual'] = min_qual
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing price data.
- `window` (int): Lookback window for the calculation. Default is `1`.
- `multiplier` (int): Scalar multiplier for both major and minor quality. Default is `1`.

### Returns
- **Tuple[np.ndarray, np.ndarray]**: Arrays of major and minor quality values.

---

## exhaustion_lengths

### Description
Calculates the average lengths of peaks and valleys in a price series, used to dynamically adjust exhaustion bands.

### Usage Example
```python
maj_len, min_len = bta.exhaustion_lengths(df)
df['maj_len'] = maj_len
df['min_len'] = min_len
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `'high'` and `'low'` columns.

### Returns
- **Tuple[int, int]**: Average peak distance (major length) and average valley distance (minor length).

---

## get_min_max

### Description
Returns the minimum or maximum value between two series for each index.

### Usage Example
```python
df['min_max'] = bta.get_min_max(df['open'], df['close'], 'max')
```

### Parameters
- `series1` (pd.Series): First input series.
- `series2` (pd.Series): Second input series.
- `function` (str): Function to apply, either `'min'` or `'max'`. Default is `'min'`.

### Returns
- **pd.Series**: Series with the min or max values for each index.

---

## linear_decay

### Description
Implements a linear decay function. The value decays linearly from a starting value to an ending value over a specified time range.

### Usage Example
```python
decayed_value = bta.linear_decay(start=100, end=0, start_time=10, end_time=60, trade_time=30)
```

### Parameters
- `start` (float): Starting value.
- `end` (float): Ending value.
- `start_time` (int): Time in minutes when decay starts.
- `end_time` (int): Time in minutes when decay ends.
- `trade_time` (int): Current trade time in minutes.

### Returns
- **float**: Decayed value.

---

## linear_growth

### Description
Implements a linear growth function. The value grows linearly from a starting value to an ending value over a specified time range.

### Usage Example
```python
grown_value = bta.linear_growth(start=0, end=100, start_time=10, end_time=60, trade_time=30)
```

### Parameters
- `start` (float): Starting value.
- `end` (float): Ending value.
- `start_time` (int): Time in minutes when growth starts.
- `end_time` (int): Time in minutes when growth ends.
- `trade_time` (int): Current trade time in minutes.

### Returns
- **float**: Grown value.

---

## Overbought/Oversold (OBOS) Indicator

### Description
The **Overbought/Oversold (OBOS) Indicator** identifies market conditions by analyzing indicator values to determine whether they exceed overbought or oversold thresholds. Additionally, it detects triggers based on recent indicator values, providing insights into potential market reversals.

### Interpretation
- **OBOS Conditions**:
  - **`overbought`**: Current value exceeds the overbought threshold.
  - **`oversold`**: Current value falls below the oversold threshold.
  - **`overbought_trigger`**: Neutral state, but one of the previous `previous_rows` values exceeded the overbought threshold.
  - **`oversold_trigger`**: Neutral state, but one of the previous `previous_rows` values fell below the oversold threshold.
  - **`neutral`**: No significant conditions detected.

### Call with

```python
obos = bta.overbought_oversold(
    df,
    indicator_col='indicator',  # Replace 'indicator' with the column name containing the indicator values
    overbought_value=75,       # Specify the overbought threshold (default: 75)
    oversold_value=30,         # Specify the oversold threshold (default: 30)
    previous_rows=5            # Number of previous rows to consider for trigger conditions (default: 5)
)

# Integrate results into the original DataFrame
df['obos_condition'] = obos
```

### Parameters
- **`df`** (*pandas.DataFrame*): The input DataFrame containing the indicator column.
- **`indicator_col`** (*str*): The name of the column containing the indicator values.
- **`overbought_value`** (*float*, default=`75`): The overbought threshold.
- **`oversold_value`** (*float*, default=`30`): The oversold threshold.
- **`previous_rows`** (*int*, default=`5`): The number of previous rows to consider for trigger conditions.

### Returns
- **`pd.Series`**: A Series containing the OBOS conditions:
  - **`overbought`**: Indicator exceeds the overbought threshold.
  - **`oversold`**: Indicator falls below the oversold threshold.
  - **`overbought_trigger`**: Neutral state but recent values exceeded the overbought threshold.
  - **`oversold_trigger`**: Neutral state but recent values fell below the oversold threshold.
  - **`neutral`**: No significant conditions detected.

### Example Usage

```python
# Example DataFrame
data = {
    'indicator': [50, 80, 85, 60, 25, 20, 40, 90, 95, 70]
}
df = pd.DataFrame(data)

# Calculate OBOS conditions
df['obos_condition'] = bta.overbought_oversold(
    df,
    indicator_col='indicator',
    overbought_value=75,
    oversold_value=30,
    previous_rows=3
)

# Display the updated DataFrame
print(df)
```

### Output Interpretation
- **Neutral**: No overbought/oversold conditions or triggers detected.
- **Overbought/Oversold**: Current value exceeds the respective threshold.
- **Triggers**:
  - **Overbought Trigger**: Recent values exceeded the overbought threshold, though the current value is neutral.
  - **Oversold Trigger**: Recent values fell below the oversold threshold, though the current value is neutral.

### Notes
- The **OBOS Indicator** can be applied to any column containing numeric values, such as Stochastic or RSI values.
- Ensure that the `indicator_col` exists in the input DataFrame; otherwise, the function will raise a `ValueError`.

---

## populate_leledc_major_minor

### Description
Populates the **Leledc Major** and **Leledc Minor** columns in a DataFrame based on major and minor quality values, as well as major and minor lengths.

### Usage Example
```python
leledc_major_minor = bta.populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len)
df['leledc_major'] = leledc_major_minor['leledc_major']
df['leledc_minor'] = leledc_major_minor['leledc_minor']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame.
- `maj_qual` (np.ndarray): Array of major quality values.
- `min_qual` (np.ndarray): Array of minor quality values.
- `maj_len` (int): Major length value.
- `min_len` (int): Minor length value.

### Returns
- **pd.DataFrame**: DataFrame with `'leledc_major'` and `'leledc_minor'` columns.

---

## Pump and Dump Protection Indicator

### Description
The **Pump and Dump Protection Indicator** detects abnormal trading volume changes and price movements to help identify potential pump-and-dump scenarios. This self-contained function avoids relying on a specific timeframe, making it adaptable to any dataset's granularity.


### Interpretation
This indicator outputs several metrics to identify potential pump-and-dump activity:

1. **Volume Metrics**:
   - **`volume_mean_short`**: The short-term average of trading volume over the last few intervals.
   - **`volume_mean_long`**: The long-term average of trading volume over a larger rolling window.
   - **`volume_change_percentage`**: Measures the relative change in volume:
     - High values (> 1.0) indicate the short-term volume is unusually high compared to the long-term volume.
     - Values > `volume_warn_threshold` suggest abnormal trading activity.
2. **RSI Metrics**:
   - **`rsi`**: The Relative Strength Index over a specified period, indicating market conditions:
     - **RSI < 30**: Oversold conditions (potential buy signals).
     - **RSI > 70**: Overbought conditions (potential sell signals).
   - **`pnd_volume_warn`**: A binary indicator:
     - `-1`: Abnormal short-term volume spike detected.
     - `0`: No significant volume spikes detected.

### Usage Example
```python
result = bta.pump_dump_protection_no_timeframe(
    df,
    rsi_period=14,
    short_volume_window=4,
    long_volume_window=48,
    volume_warn_threshold=5.0
)

# Integrate results into the original DataFrame
df['volume_mean_short'] = result['volume_mean_short']
df['volume_mean_long'] = result['volume_mean_long']
df['volume_change_percentage'] = result['volume_change_percentage']
df['rsi'] = result['rsi']
df['pnd_volume_warn'] = result['pnd_volume_warn']
```

### Parameters
- **`df`** (*pandas.DataFrame*): Input DataFrame with required columns:
  - `'close'`: Closing price.
  - `'high'`: High price for the interval.
  - `'low'`: Low price for the interval.
  - `'volume'`: Trading volume for the interval.
- **`rsi_period`** (*int*, default=`14`): Lookback period for RSI calculation.
- **`short_volume_window`** (*int*, default=`4`): Rolling window size for short-term volume mean.
- **`long_volume_window`** (*int*, default=`48`): Rolling window size for long-term volume mean.
- **`volume_warn_threshold`** (*float*, default=`5.0`): Threshold for abnormal short-term volume spikes.

### Returns
A DataFrame with the following additional columns:
- **`volume_mean_short`**: Rolling mean of volume over the last `short_volume_window` intervals.
- **`volume_mean_long`**: Rolling mean of volume over the last `long_volume_window` intervals.
- **`volume_change_percentage`**: Ratio of short-term volume to long-term volume.
- **`rsi`**: Calculated RSI values.
- **`pnd_volume_warn`**: Indicator (`-1` or `0`) for abnormal short-term volume spikes.

### Interpretation of Output
1. **Volume Spikes (`pnd_volume_warn`)**:
   - `-1`: A warning that the short-term volume is significantly higher than the long-term volume, which could indicate a potential pump-and-dump scenario.
   - `0`: No abnormal volume activity detected.
2. **Volume Change Percentage**:
   - Values > 1.0 suggest increased trading activity.
   - Higher values closer to the `volume_warn_threshold` should be reviewed carefully for abnormal activity.
3. **RSI (`rsi`)**:
   - RSI < 30: Potential oversold conditions, signaling a possible buy opportunity.
   - RSI > 70: Potential overbought conditions, signaling a possible sell opportunity.

### Notes
- The `volume_warn_threshold` parameter can be adjusted to fine-tune sensitivity to volume spikes. A lower value increases sensitivity, while a higher value reduces it.
- The function adapts dynamically to any dataset interval (e.g., 1-minute, 5-minute, hourly), making it versatile for different data granularities.

---

## regression_slope

### Description
Calculates the slope of a **linear regression** line fitted to the closing prices over a specified lookback period.

### Usage Example
```python
df['slope'] = bta.regression_slope(df, lookback_period=20)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `'close'` prices.
- `lookback_period` (int): Lookback period for the slope calculation. Default is `20`.

### Returns
- **pd.Series**: Series of regression slopes.

---

## same_length

### Description
Ensures that two arrays have the same length by padding the shorter array with `NaN` values.

### Usage Example
```python
padded_array = bta.same_length(bigger_array, shorter_array)
```

### Parameters
- `bigger` (np.ndarray): Larger array.
- `shorter` (np.ndarray): Smaller array.

### Returns
- **np.ndarray**: Shorter array padded with `NaN` values to match the length of the larger array.

---

## st_dev

### Description
Calculates the rolling **standard deviation** over a specified period.

### Usage Example
```python
df['std_dev'] = bta.st_dev(df['close'], period=14)
```

### Parameters
- `series` (pd.Series): Data series for the standard deviation calculation.
- `period` (int): Period over which to calculate the standard deviation.

### Returns
- **pd.Series**: Rolling standard deviation values.

---

## z_score

### Description
Calculates the **z-score** of a series, which indicates how far away a data point is from the mean in terms of standard deviations.

### Usage Example
```python
df['zscore'] = bta.z_score(df['close'], window=500)
```

### Parameters
- `series` (pd.Series): Input series.
- `window` (int): Lookback window for calculating the mean and standard deviation. Default is `500`.

### Returns
- **pd.Series**: Z-score series.

---

## drop_na

### Description
Drops rows with `NaN` values and replaces extremely large numbers and zeros in numeric columns with `NaN` before dropping them.

### Usage Example
```python
df_cleaned = bta.drop_na(df)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame.

### Returns
- **pd.DataFrame**: DataFrame with `NaN` values removed and extreme values handled.

---
