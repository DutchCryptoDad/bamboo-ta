# Bamboo TA Indicators Module

## Trend

Includes trend-based indicators.

### Indicators

- **AlligatorBands**: Bill Williams Alligator Indicator.
- **Usage**: 
    ```python
    alligator_result = AlligatorBands(df, "high", 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
    df['jaw'] = alligator_result['jaw']
    df['teeth'] = alligator_result['teeth']
    df['lips'] = alligator_result['lips']
    ```
- **BollingerTrend**: Bollinger Trend Indicator.
- **Usage**: 
    ```python
    df['BBTrend'] = BollingerTrend(df, "close", 20, 50, 2.0)
    ```
- **BollingerTrendFastWithMA**: Bollinger Trend Indicator with selectable Moving Average.
- **Usage**: 
    ```python
    result = BollingerTrendFastWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14)
    df['BBTrend'] = result['BBTrend']
    df['BBTrendMA'] = result['BBTrendMA']
    ```
- **EMA**: Exponential Moving Average.
- **Usage**: 
    ```python
    df['ema'] = EMA(df, "close", 21)
    ```
- **HMA**: Hull Moving Average.
- **Usage**: 
    ```python
    df['hma'] = HMA(df, "close", 9)
    ```
- **LSMA**: Least Squares Moving Average.
- **Usage**: 
    ```python
    df['lsma'] = LSMA(df, "close", 50)
    ```
- **SMA**: Simple Moving Average.
- **Usage**: 
    ```python
    df['sma'] = SMA(df, "close", 50)
    ```
- **WMA**: Weighted Moving Average.
- **Usage**: 
    ```python
    df['wma'] = WMA(df, "close", 9)
    ```
- **ZLEMA**: Zero Lag Exponential Moving Average.
- **Usage**: 
    ```python
    df['zlema'] = ZLEMA(df, "close", 21)
    ```
- **Breakouts**: S/R Breakouts and Retests.
- **Usage**: 
    ```python
    breakout = Breakouts(df)
    df['support_level'] = breakout['support_level']
    df['resistance_level'] = breakout['resistance_level']
    df['support_breakout'] = breakout['support_breakout']
    df['resistance_breakout'] = breakout['resistance_breakout']
    df['support_retest'] = breakout['support_retest']
    df['potential_support_retest'] = breakout['potential_support_retest']
    df['resistance_retest'] = breakout['resistance_retest']
    df['potential_resistance_retest'] = breakout['potential_resistance_retest']
    ```
- **SSLChannels**: SSL Channels.
- **Usage**: 
    ```python
    ssl_down, ssl_up = SSLChannels(df, length=10, mode='sma')
    df['ssl_down'] = ssl_down
    df['ssl_up'] = ssl_up
    ```
- **SSLChannelsATR**: SSL Channels with ATR.
- **Usage**: 
    ```python
    ssl_down, ssl_up = SSLChannelsATR(df, length=7)
    df['ssl_atr_down'] = ssl_down
    df['ssl_atr_up'] = ssl_up
    ```
- **PCC**: Percent Change Channel.
- **Usage**: 
    ```python
    upper, rangema, lower = PCC(df, period=20, mult=2)
    df['pcc_upper'] = upper
    df['pcc_rangema'] = rangema
    df['pcc_lower'] = lower
    ```
- **T3**: T3 Average.
- **Usage**: 
    ```python
    df['t3_average'] = T3(df, length=5)
    ```
