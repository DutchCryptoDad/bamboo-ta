# Bamboo TA Indicators Module

## Utility

Utility functions and helper methods for technical analysis.

### Indicators

- **Calculate_Exhaustion_Candles**: Calculate the average consecutive length of ups and downs.
- **Usage**:
    ```python
    maj_qual, min_qual = Calculate_Exhaustion_Candles(df, window, zscore_multi)
    ```
- **Calculate_Exhaustion_Lengths**: Calculate the average length of peaks and valleys.
- **Usage**:
    ```python
    maj_len, min_len = Calculate_Exhaustion_Lengths(df)
    ```
- **Consecutive_Count**: Calculate the average consecutive count of non-zero differences.
- **Usage**:
    ```python
    avg_consecutive = Consecutive_Count(consecutive_diff)
    ```
- **Linear_Growth**: Simple linear growth function.
- **Usage**:
    ```python
    growth_value = Linear_Growth(start, end, start_time, end_time, trade_time)
    ```
- **Linear_Decay**: Simple linear decay function.
- **Usage**:
    ```python
    decay_value = Linear_Decay(start, end, start_time, end_time, trade_time)
    ```
- **populate_leledc_major_minor**: Populate Leledc Major and Minor columns.
- **Usage**:
    ```python
    df = populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len)
    ```
- **True_Range**: Calculate True Range (TR).
- **Usage**:
    ```python
    tr = True_Range(df)
    ```
- **ZScore**: Calculate the z-score of a series.
- **Usage**:
    ```python
    zscore = ZScore(series, window=500)
    ```
- **ATR**: Calculate the Average True Range (ATR).
- **Usage**:
    ```python
    atr = ATR(df, period=14)
    ```
- **RMA**: Calculate the Relative Moving Average (RMA).
- **Usage**:
    ```python
    rma = RMA(series, period)
    ```
