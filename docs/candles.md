# Bamboo TA Indicators Module

## Candles

Contains indicators related to candlestick patterns.

### Indicators

- **HeikinAshi**: Heikin Ashi candlesticks with optional pre and post smoothing.
- **Usage**: 
    ```python
    ha_df = HeikinAshi(df, pre_smoothing_period=14, post_smoothing_period=14)
    df['HA_Close'] = ha_df['HA_Close']
    df['HA_Open'] = ha_df['HA_Open']
    df['HA_High'] = ha_df['HA_High']
    df['HA_Low'] = ha_df['HA_Low']
    ```
- **LinRegCandles**: Linear Regression Candles with optional signal line.
- **Usage**: 
    ```python
    lr_df = LinRegCandles(df, linreg_length=11, sma_signal=True, signal_length=11)
    df['LRC_Open'] = lr_df['bopen']
    df['LRC_High'] = lr_df['bhigh']
    df['LRC_Low'] = lr_df['blow']
    df['LRC_Close'] = lr_df['bclose']
    df['LRC_Signal'] = lr_df['signal']
    ```
- **Exhaustion_Bars**: Leledc Exhaustion Bars - Extended.
- **Usage**: 
    ```python
    exhaustion = Exhaustion_Bars(df)
    df['leledc_major'] = exhaustion['leledc_major']
    df['leledc_minor'] = exhaustion['leledc_minor']
    ```
- **Dynamic_Exhaustion_Bars**: Dynamic Leledc Exhaustion Bars.
- **Usage**: 
    ```python
    dynamic_exhaustion = Dynamic_Exhaustion_Bars(df)
    df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
    df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']
    ```
