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
