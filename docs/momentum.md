# Bamboo TA Indicators Module

## Momentum

Provides momentum-based indicators.

### Indicators

- **CMO**: Chande Momentum Oscillator.
- **Usage**: 
    ```python
    cmo = CMO(df, length=14)
    df['cmo'] = cmo['cmo']
    ```
- **EWO**: Elliott Wave Oscillator.
- **Usage**: 
    ```python
    df['ewo'] = EWO(df, "close", 5, 35)
    ```
- **MACD**: Moving Average Convergence Divergence.
- **Usage**: 
    ```python
    macd_result = MACD(df, "close", 12, 26, 9)
    df['macd'] = macd_result['macd']
    df['macd_signal'] = macd_result['macd_signal']
    df['macd_histogram'] = macd_result['macd_histogram']
    ```
- **MACD_Leader**: MACD Leader.
- **Usage**: 
    ```python
    macd_leader = MACD_Leader(df, 'close')
    df['macd_leader'] = macd_leader['macd_leader']
    ```
- **Inverse_Fisher_Transform**: Inverse Fisher Transform.
- **Usage**: 
    ```python
    ift = Inverse_Fisher_Transform(df)
    df['ift'] = ift['ift']
    # Optional levels
    df['level_1_35'] = 1.35
    df['level_0_5'] = 0.5
    df['level_0'] = 0
    df['level_minus_0_5'] = -0.5
    df['level_minus_1'] = -1
    ```
- **Waddah_Attar_Explosion**: Waddah Attar Explosion Indicator.
- **Usage**: 
    ```python
    WAE = Waddah_Attar_Explosion(df, sensitivity=150, fast_length=20, slow_length=40, channel_length=20, mult=2.0)
    df['trend_up'] = WAE['trend_up']
    df['trend_down'] = WAE['trend_down']
    df['explosion_line'] = WAE['explosion_line']
    df['dead_zone_line'] = WAE['dead_zone_line']
    ```
- **WaveTrend_Oscillator**: WaveTrend Oscillator.
- **Usage**: 
    ```python
    wt = WaveTrend_Oscillator(df, 'close', n1=8, n2=12)
    df['wavetrend'] = wt['wavetrend']
    ```
- **RSI**: Relative Strength Index.
- **Usage**: 
    ```python
    df['rsi'] = RSI(df, "close", 14)
    ```
- **Fisher_cg**: Fisher Stochastic Center of Gravity.
- **Usage**: 
    ```python
    fisher = Fisher_cg(df)
    df['fisher_cg'] = fisher['fisher_cg']
    df['fisher_sig'] = fisher['fisher_sig']
    ```
- **QQE_Mod**: QQE Mod Indicator.
- **Usage**: 
    ```python
    qqe_mod = QQE_Mod(df, rsi_period=6, rsi_smoothing=5, qqe_factor=3, threshold=3, bollinger_length=50, bb_multiplier=0.35,
                    rsi_period2=6, rsi_smoothing2=5, qqe_factor2=1.61, threshold2=3)
    df['QQE_Line'] = qqe_mod['QQE_Line']
    df['Histo2'] = qqe_mod['Histo2']
    df['QQE_Up'] = qqe_mod['QQE_Up']
    df['QQE_Down'] = qqe_mod['QQE_Down']
    ```
- **MAStreak**: MA Streak Indicator.
- **Usage**: 
    ```python
    df['mastreak'] = MAStreak(df, period=4, column='close')
    ```
- **RMI**: Relative Momentum Index.
- **Usage**: 
    ```python
    df['rmi'] = RMI(df, length=20, mom=5)
    ```
- **ROC**: Rate of Change.
- **Usage**: 
    ```python
    df['roc'] = ROC(df, column='close', period=21)
    ```
- **SROC**: Smoothed Rate of Change.
- **Usage**: 
    ```python
    df['sroc'] = SROC(df, roclen=21, emalen=13, smooth=21)
    ```

4. **performance**
   - **Description**: Contains performance-related indicators.

5. **statistics**
   - **Description**: Statistical indicators for trading analysis.

6. **trend**
   - **Description**: Includes trend-based indicators.
   - **Indicators**:
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

7. **utility**
   - **Description**: Utility functions and helper methods for technical analysis.
   - **Functions**:
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

8. **volatility**
   - **Description**: Volatility indicators.
   - **Indicators**:
     - **BollingerBands**: Calculates Bollinger Bands (upper, middle, lower bands).
       - **Usage**: 
         ```python
         bb_result = BollingerBands(df, "close", 21, 2, 0)
         df['bb_upper'] = bb_result['BB_upper']
         df['bb_middle'] = bb_result['BB_middle']
         df['bb_lower'] = bb_result['BB_lower']
         ```
     - **TR**: True Range (TR) calculation.
       - **Usage**: 
         ```python
         tr = TR(df)
         ```

9. **volume**
   - **Description**: Provides volume-based indicators.
   - **Indicators**:
     - **OBV_Oscillator**: On Balance Volume Oscillator.
       - **Usage**:
         ```python
         obv_osc = OBV_Oscillator(df, n1=10, n2=21)
         df['OBV_Oscillator'] = obv_osc['OBV_Oscillator']
         ```