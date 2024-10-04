# Bamboo TA Indicators Module

## Utility

Utility functions and helper methods for technical analysis.

### Indicators

- **CalculateFixedStopLossTakeProfitWithSignal**: Calculates stop loss, entry price, and take profit levels based on trade signals (long, short, or no trade).
  - **Usage**:
    ```python
    trade_cols = CalculateFixedStopLossTakeProfitWithSignal(
        df, 
        signal_column='trade_signal', 
        long_trade_signal='long_trade', 
        short_trade_signal='short_trade', 
        no_trade_signal='no_trade', 
        lookback_period=5, 
        long_risk_reward_ratio=2, 
        short_risk_reward_ratio=2, 
        buffer=0
    )
    df[['stop_loss', 'entry_price', 'take_profit', 'trade_active', 'exit_reason']] = trade_cols
    ```

- **ExhaustionCandles**: Calculate the average consecutive length of ups and downs.
  - **Usage**:
    ```python
    maj_qual, min_qual = ExhaustionCandles(df, window=1, multiplier=1)
    ```

- **ExhaustionLengths**: Calculate the average length of peaks and valleys.
  - **Usage**:
    ```python
    maj_len, min_len = ExhaustionLengths(df)
    ```

- **ConsecutiveCount**: Calculate the average consecutive count of non-zero differences.
  - **Usage**:
    ```python
    avg_consecutive = ConsecutiveCount(consecutive_diff)
    ```

- **CrossedAbove**: Check if one series crosses above another series.
  - **Usage**:
    ```python
    crossover = CrossedAbove(series1, series2)
    df['crossed_above'] = crossover
    ```

- **CrossedBelow**: Check if one series crosses below another series.
  - **Usage**:
    ```python
    crossover = CrossedBelow(series1, series2)
    df['crossed_below'] = crossover
    ```

- **LinearGrowth**: Simple linear growth function.
  - **Usage**:
    ```python
    growth_value = LinearGrowth(start, end, start_time, end_time, trade_time)
    ```

- **LinearDecay**: Simple linear decay function.
  - **Usage**:
    ```python
    decay_value = LinearDecay(start, end, start_time, end_time, trade_time)
    ```

- **PopulateLeledcMajorMinor**: Populate Leledc Major and Minor columns.
  - **Usage**:
    ```python
    df = PopulateLeledcMajorMinor(df, maj_qual, min_qual, maj_len, min_len)
    ```

- **CumulativeReturn**: Calculate cumulative return of a column.
  - **Usage**:
    ```python
    cr = CumulativeReturn(df, column='close', fillna=False)
    df['cumulative_return'] = cr
    ```

- **DailyReturn**: Calculate daily return of a column.
  - **Usage**:
    ```python
    dr = DailyReturn(df, column='close', fillna=False)
    df['daily_return'] = dr
    ```

- **DailyLogReturn**: Calculate daily log return of a column.
  - **Usage**:
    ```python
    dlr = DailyLogReturn(df, column='close', fillna=False)
    df['daily_log_return'] = dlr
    ```

- **ZScore**: Calculate the z-score of a series.
  - **Usage**:
    ```python
    zscore = ZScore(series, window=500)
    df['zscore'] = zscore
    ```

- **RegressionSlope**: Calculate the slope of a linear regression for a given lookback period.
  - **Usage**:
    ```python
    slope = RegressionSlope(df, lookback_period=20)
    df['slope'] = slope
    ```

- **StDev**: Calculate the standard deviation over a specified period.
  - **Usage**:
    ```python
    stdev = StDev(df['close'], period=20)
    df['stdev'] = stdev
    ```

- **GetMinMax**: Find the min or max value between two series for each index.
  - **Usage**:
    ```python
    min_max_series = GetMinMax(df['high'], df['low'], function="min")
    df['min_max'] = min_max_series
    ```

- **SameLength**: Ensures that the shorter array has the same length as the bigger array by padding with NaN values.
  - **Usage**:
    ```python
    padded_series = SameLength(df['high'].values, df['low'].values)
    df['padded_series'] = padded_series
    ```

- **DropNa**: Drop rows with 'NaN' values.
  - **Usage**:
    ```python
    df_clean = DropNa(df)
    ```

- **TrueRange**: Calculate True Range (TR).
  - **Usage**:
    ```python
    tr = IndicatorMixin._true_range(df['high'], df['low'], df['close'].shift(1))
    ```
