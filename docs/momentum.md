# `momentum` - Technical Momentum Indicators

## Awesome Oscillator (AO)

### Description
The **Awesome Oscillator (AO)** is a momentum indicator used to measure market momentum by comparing the 5-period and 34-period simple moving averages (SMA) of the median price.

### Interpretation
- **AO** helps identify the strength of a market's trend. Positive values indicate bullish momentum, while negative values indicate bearish momentum.

### Usage Example
```python
df['ao'] = bta.awesome_oscillator(df, 'high', 'low', 5, 34)['ao']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `high` and `low` columns.
- `high_col` (str): Column name for the high prices. Default is `'high'`.
- `low_col` (str): Column name for the low prices. Default is `'low'`.
- `window1` (int): Short period for the SMA. Default is `5`.
- `window2` (int): Long period for the SMA. Default is `34`.
- `fillna` (bool): If `True`, fills NaN values with `0`. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with the `'ao'` column.

---

## Chande Momentum Oscillator (CMO)

### Description
The **Chande Momentum Oscillator (CMO)** measures the momentum of price changes over a specified period, developed by Tushar Chande.

### Interpretation
- **CMO** oscillates between -100 and 100. Positive values suggest upward momentum, while negative values suggest downward momentum.

### Usage Example
```python
df['cmo'] = bta.chande_momentum_oscillator(df)
df['cmo_signal'] = df['cmo'].rolling(window=10).mean()  # Using SMA for signal
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `close` column.
- `length` (int): Lookback period for the CMO calculation. Default is `14`.

### Returns
- **DataFrame**: A DataFrame with the `'cmo'` column.

---

## Elliott Wave Oscillator (EWO)

### Description
The **Elliott Wave Oscillator (EWO)** is used to identify trends and market patterns. It is calculated as the difference between two simple moving averages (SMA), then normalized by the price.

### Interpretation
- **EWO** helps traders identify the direction of the trend based on the relationship between short-term and long-term moving averages.

### Usage Example
```python
df['ewo'] = bta.elliott_wave_oscillator(df, 'close', 5, 35)
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the specified column.
- `column` (str): The column on which EWO is calculated. Default is `'close'`.
- `sma1_period` (int): Short period for the SMA. Default is `5`.
- `sma2_period` (int): Long period for the SMA. Default is `35`.

### Returns
- **DataFrame**: A DataFrame with the `'ewo'` column.

---

## Ehlers Fisher Stochastic Center of Gravity Indicator

### Description
The **Fisher Stochastic Center of Gravity Indicator**, developed by John Ehlers, identifies potential market turning points by calculating the center of gravity of price movements.

### Interpretation
- **CG** values above zero may indicate overbought conditions, while values below zero may suggest oversold conditions.

### Usage Example
```python
fscg = bta.ehlers_fisher_stochastic_center_of_gravity(df)
df['cg'] = fscg['cg']
df['trigger'] = fscg['trigger']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `high` and `low` columns.
- `length` (int): Lookback period for the indicator. Default is `8`.

### Returns
- **DataFrame**: A DataFrame with the `'cg'` and `'trigger'` columns.

---

## Intraday Momentum Index (IMI)

### Description
The **Intraday Momentum Index (IMI)** combines candlestick analysis with the principles of the Relative Strength Index (RSI) to measure intraday momentum. It evaluates the relationship between opening and closing prices to identify potential market trends and reversals.

### Interpretation
- **IMI Values**:
  - **`IMI > 70`**: Indicates overbought conditions, signaling a potential sell opportunity.
  - **`IMI < 30`**: Indicates oversold conditions, signaling a potential buy opportunity.
  - **`IMI Between 30 and 70`**: Indicates neutral market conditions.

The IMI is particularly useful for short-term trading, where the relationship between open and close prices is significant.

### Usage Example
```python
# Calculate IMI and add it to the DataFrame
df['imi'] = bta.calculate_intraday_momentum_index(df, length=14)
```

### Parameters
- **`df`** (*pandas.DataFrame*): The input DataFrame must contain the following columns:
  - `'open'`: Opening price.
  - `'close'`: Closing price.
- **`length`** (*int*, default=`14`): The lookback period over which gains and losses are summed to calculate the IMI.

### Returns
- **`pd.Series`**: A Pandas Series representing the Intraday Momentum Index (IMI) values.

### Notes
- The **IMI** is most effective in volatile markets or when analyzing short-term price movements.
- Ensure the input DataFrame contains the `'open'` and `'close'` columns; otherwise, the function will raise a `ValueError`.

---

## Kaufman's Adaptive Moving Average (KAMA)

### Description
The **Kaufman's Adaptive Moving Average (KAMA)** adjusts to market noise or volatility, closely following prices when price swings are small and adjusting when price swings widen.

### Interpretation
- **KAMA** helps identify the overall trend, time turning points, and filter price movements in volatile markets.

### Usage Example
```python
df['kama'] = bta.kaufmans_adaptive_moving_average(df)['kama']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `close` column.
- `close_col` (str): Column name for the close prices. Default is `'close'`.
- `window` (int): Period for the efficiency ratio. Default is `14`.
- `pow1` (int): Period for the fastest EMA constant. Default is `2`.
- `pow2` (int): Period for the slowest EMA constant. Default is `30`.
- `fillna` (bool): If `True`, fills NaN values with the close prices. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with the `'kama'` column.

Here is the extended documentation, including everything from the **MACD** function onward in the `momentum.py` module. The documentation follows the same format with descriptions, interpretations, usage examples, and parameter explanations.

---

## Moving Average Convergence Divergence (MACD)

### Description
The **MACD (Moving Average Convergence Divergence)** is a momentum indicator that shows the relationship between two moving averages of a security’s price. It is commonly used to spot trend direction and strength.

### Interpretation
- **MACD Line** (`macd`): The difference between the short-term and long-term EMAs. A positive value indicates bullish momentum, while a negative value suggests bearish momentum.
- **Signal Line** (`macd_signal`): A smoothed version of the MACD line, used to generate buy or sell signals.
- **MACD Histogram** (`macd_histogram`): The difference between the MACD line and the Signal line. Positive values suggest upward momentum, and negative values suggest downward momentum.

### Usage Example
```python
macd_result = bta.macd(df, 'close', 12, 26, 9)
df['macd'] = macd_result['macd']
df['macd_signal'] = macd_result['macd_signal']
df['macd_histogram'] = macd_result['macd_histogram']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the column to be used for calculation.
- `column` (str): The column on which MACD is to be calculated. Default is `'close'`.
- `short_window` (int): The short-term period for the EMA. Default is `12`.
- `long_window` (int): The long-term period for the EMA. Default is `26`.
- `signal_window` (int): The period for the signal EMA. Default is `9`.

### Returns
- **DataFrame**: A DataFrame with the `'macd'`, `'macd_signal'`, and `'macd_histogram'` columns.

---

## MACD Leader

### Description
The **MACD Leader** is a variation of the standard MACD that aims to provide an earlier signal using a different calculation method, focusing on faster reaction to market changes.

### Interpretation
- **MACD Leader** is used similarly to the standard MACD, but it attempts to signal trend changes earlier by using a different approach to EMA calculations.

### Usage Example
```python
df['macd_leader'] = bta.macd_leader(df, 'close')['macd_leader']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the source column.
- `src` (str): The column to use for calculations. Default is `'close'`.
- `fast_length` (int): Length for the fast EMA. Default is `12`.
- `slow_length` (int): Length for the slow EMA. Default is `26`.
- `signal_length` (int): Length for the signal EMA. Default is `9`.

### Returns
- **DataFrame**: A DataFrame with the `'macd_leader'` column.

---

## MA Streak Indicator

### Description
The **MA Streak Indicator** tracks the number of bars a given moving average is rising or falling, highlighting trends by color-coding them as positive (green) or negative (red).

### Interpretation
- **MA Streak** shows how long a moving average has been increasing or decreasing, helping to identify the strength and longevity of trends.

### Usage Example
```python
df['ma_streak'] = bta.ma_streak(df, length=10, src='close', matype=1)['ma_streak']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `length` (int): Period for the moving average calculation. Default is `10`.
- `src` (str): The column name to use for the moving average calculation. Default is `'close'`.
- `matype` (int): Type of moving average to use. Options are:
  1 - SMA, 2 - EMA, 3 - HMA, 4 - WMA, 5 - VWMA. Default is `1`.

### Returns
- **DataFrame**: A DataFrame with the `'ma_streak'` column.

---

## Momentum Divergence (momdiv)

### Description
The **Momentum Divergence (momdiv)** indicator identifies potential buy and sell signals by applying Bollinger Bands to a momentum calculation. It also checks if the current high or low breaches the highest high or lowest low over a specified lookback period, providing additional insights into price extremes.

### Interpretation
- **Buy Signal**:
  - Triggered when the momentum crosses **below** the lower Bollinger Band, indicating potential upward price movement.
- **Sell Signal**:
  - Triggered when the momentum crosses **above** the upper Bollinger Band, signaling potential downward price movement.
- **Highest High (coh)**:
  - Indicates the current high equals or exceeds the highest high over the lookback period.
- **Lowest Low (col)**:
  - Indicates the current low equals or falls below the lowest low over the lookback period.

### Usage Example
```python
momdiv_result = bta.momentum_divergence(df, mom_length=5, bb_length=5, bb_dev=1.0, lookback=5)
df['momentum_divergence_mom'] = momdiv_result['momentum_divergence_mom']
df['momentum_divergence_upperb'] = momdiv_result['momentum_divergence_upperb']
df['momentum_divergence_lowerb'] = momdiv_result['momentum_divergence_lowerb']
df['momentum_divergence_buy'] = momdiv_result['momentum_divergence_buy']
df['momentum_divergence_sell'] = momdiv_result['momentum_divergence_sell']
df['momentum_divergence_coh'] = momdiv_result['momentum_divergence_coh']
df['momentum_divergence_col'] = momdiv_result['momentum_divergence_col']
```

### Parameters
- **`df`** (*pandas.DataFrame*): The input DataFrame containing OHLC data with the following required columns:
  - `close`
  - `high`
  - `low`
- **`mom_length`** (*int*, default=`10`): The period for momentum calculation.
- **`bb_length`** (*int*, default=`20`): The period for Bollinger Bands calculation.
- **`bb_dev`** (*float*, default=`2.0`): The standard deviation multiplier for Bollinger Bands.
- **`lookback`** (*int*, default=`30`): The period for detecting the highest high and lowest low.

### Returns
A DataFrame with the following columns:
- **`momentum_divergence_mom`**: The calculated momentum values.
- **`momentum_divergence_upperb`**: The upper Bollinger Band for momentum.
- **`momentum_divergence_lowerb`**: The lower Bollinger Band for momentum.
- **`momentum_divergence_buy`**: Boolean column indicating buy signals (momentum crosses below the lower Bollinger Band).
- **`momentum_divergence_sell`**: Boolean column indicating sell signals (momentum crosses above the upper Bollinger Band).
- **`momentum_divergence_coh`**: Boolean column indicating the current high equals or exceeds the highest high over the lookback period.
- **`momentum_divergence_col`**: Boolean column indicating the current low equals or falls below the lowest low over the lookback period.

### Notes
- Adjusting `mom_length` can change the sensitivity of the momentum calculation. Shorter lengths respond more quickly to price changes.
- The `bb_dev` parameter controls how far the Bollinger Bands are from the mean. A higher value results in wider bands and fewer signals.

---

## Percentage Price Oscillator (PPO)

### Description
The **Percentage Price Oscillator (PPO)** is a momentum indicator similar to MACD, but it shows the percentage difference between two EMAs, which allows for better comparison across assets of varying prices.

### Interpretation
- **PPO** helps identify trend direction and momentum. The PPO histogram shows the difference between the PPO and the Signal line.

### Usage Example
```python
ppo = bta.percentage_price_oscillator(df)
df['ppo'] = ppo['ppo']
df['ppo_signal'] = ppo['ppo_signal']
df['ppo_hist'] = ppo['ppo_hist']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the close column.
- `close_col` (str): Column name for close prices. Default is `'close'`.
- `window_slow` (int): Long-term period for EMA. Default is `26`.
- `window_fast` (int): Short-term period for EMA. Default is `12`.
- `window_sign` (int): Period for the signal EMA. Default is `9`.
- `fillna` (bool): If `True`, fills NaN values with 0. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with the `'ppo'`, `'ppo_signal'`, and `'ppo_hist'` columns.

---

## Percentage Volume Oscillator (PVO)

### Description
The **Percentage Volume Oscillator (PVO)** compares the percentage difference between two volume-based EMAs, helping identify trends in trading volume.

### Interpretation
- **PVO** is used to assess the strength of volume trends. A positive value suggests increased volume, while a negative value suggests lower volume.

### Usage Example
```python
pvo = bta.percentage_volume_oscillator(df)
df['pvo'] = pvo['pvo']
df['pvo_signal'] = pvo['pvo_signal']
df['pvo_hist'] = pvo['pvo_hist']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the volume column.
- `volume_col` (str): Column name for volume data. Default is `'volume'`.
- `window_slow` (int): Long-term period for EMA. Default is `26`.
- `window_fast` (int): Short-term period for EMA. Default is `12`.
- `window_sign` (int): Period for the signal EMA. Default is `9`.
- `fillna` (bool): If `True`, fills NaN values with 0. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with the `'pvo'`, `'pvo_signal'`, and `'pvo_hist'` columns.

---

## Relative Momentum Index (RMI)

### Description
The **Relative Momentum Index (RMI)** applies the RSI formula to momentum rather than price, helping identify overbought or oversold conditions based on momentum.

### Interpretation
- **RMI** is similar to RSI but provides more sensitivity to momentum changes, making it useful for spotting potential trend reversals.

### Usage Example
```python
df['rmi'] = bta.relative_momentum_index(df, length=20, mom=5)['rmi']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `length` (int): Period for the EMA calculation. Default is `20`.
- `mom` (int): Momentum period. Default is `5`.

### Returns
- **DataFrame**: A DataFrame with the `'rmi'` column.

Sure! Below is the full documentation for all the indicators starting from **Relative Momentum Index (RMI)** onward in **Markdown** format. Due to the length, I will break it into multiple parts, but it will cover everything from where we left off.

---

## Rate of Change (ROC)

### Description
The **Rate of Change (ROC)** is a momentum oscillator that measures the percentage change in price between the current price and the price n periods ago.

### Interpretation
- **ROC** values above 0 indicate upward momentum, while values below 0 indicate downward momentum.

### Usage Example
```python
df['roc'] = bta.rate_of_change(df, column='close', period=21)['roc']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `column` (str): The column name on which ROC is applied. Default is `'close'`.
- `period` (int): Period for the ROC calculation. Default is `21`.

### Returns
- **DataFrame**: A DataFrame with the `'roc'` column.

---

## Smoothed Rate of Change (SROC)

### Description
The **Smoothed Rate of Change (SROC)** applies an exponential moving average (EMA) to the Rate of Change (ROC) to smooth out short-term fluctuations.

### Interpretation
- **SROC** provides a smoother momentum signal compared to regular ROC, making it useful for identifying longer-term trends.

### Usage Example
```python
df['sroc'] = bta.smoothed_rate_of_change(df, roclen=21, emalen=13, smooth=21)['sroc']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `roclen` (int): Period for the ROC calculation. Default is `21`.
- `emalen` (int): Period for the EMA calculation. Default is `13`.
- `smooth` (int): Smoothing period for the ROC calculation. Default is `21`.

### Returns
- **DataFrame**: A DataFrame with the `'sroc'` column.

---

## Waddah Attar Explosion (ATR)

### Description
The **Waddah Attar Explosion (ATR)** is used to identify potential breakout opportunities by combining the MACD and Bollinger Bands with an ATR-based dead zone line.

### Interpretation
- **Waddah Attar Explosion** helps traders identify breakout situations. The **trend_up** column signals bullish conditions, while **trend_down** indicates bearish conditions.

### Usage Example
```python
wae = bta.waddah_attar_explosion_atr(df)
df['trend_up'] = wae['trend_up']
df['trend_down'] = wae['trend_down']
df['explosion_line'] = wae['explosion_line']
df['dead_zone_line'] = wae['dead_zone_line']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `open`, `high`, `low`, and `close` columns.
- `sensitivity` (int): Sensitivity factor for the indicator. Default is `150`.
- `fast_length` (int): Length for the fast EMA. Default is `20`.
- `slow_length` (int): Length for the slow EMA. Default is `40`.
- `channel_length` (int): Length for the Bollinger Bands. Default is `20`.
- `mult` (float): Standard deviation multiplier for the Bollinger Bands. Default is `2.0`.

### Returns
- **DataFrame**: A DataFrame with `'trend_up'`, `'trend_down'`, `'explosion_line'`, and `'dead_zone_line'` columns.

---

## WaveTrend

### Description
The **WaveTrend** oscillator is used to identify overbought and oversold conditions in the market, providing insights into potential reversals or continuations of trends.

### Interpretation
- **WaveTrend** shows whether the market is overbought or oversold. It has two lines, **WT1** and **WT2**, that can be used to identify potential crossovers indicating buy or sell signals.

### Usage Example
```python
wt = bta.wave_trend(df, chlen=10, avg=21, smalen=4)
df['wt1'] = wt['wt1']
df['wt2'] = wt['wt2']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the data.
- `chlen` (int): Channel length for the EMA calculation. Default is `10`.
- `avg` (int): Average period for the EMA calculation. Default is `21`.
- `smalen` (int): Period for the SMA calculation. Default is `4`.

### Returns
- **DataFrame**: A DataFrame with `'wt1'` and `'wt2'` columns.

---

## WaveTrend Oscillator (WTO)

### Description
The **WaveTrend Oscillator (WTO)** is used to identify overbought and oversold conditions in the market by smoothing price data and analyzing trends. It combines two Exponential Moving Averages (EMAs) and measures deviations from them to produce the oscillator.

### Usage Example
```python
df['wto'] = bta.wave_trend_oscillator(df, 'close')['wavetrend']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the source column.
- `src` (str): Column to use for the oscillator calculation. Default is `'close'`.
- `n1` (int): Length for the first EMA. Default is `8`.
- `n2` (int): Length for the second EMA. Default is `12`.

### Returns
- **DataFrame**: A DataFrame with a `'wavetrend'` column representing the calculated oscillator.

---

## QQE Mod (Quantitative Qualitative Estimation Mod)

### Description
The **QQE Mod** is a technical analysis indicator that enhances the standard Relative Strength Index (RSI) by applying smoothing techniques and Bollinger Bands to generate buy and sell signals. It helps identify market trends and breakouts by smoothing out volatility.

### Usage Example
```python
qqe_mod_result = bta.qqe_mod(df, rsi_period=6, rsi_smoothing=5, qqe_factor=3, threshold=3, bollinger_length=50, bb_multiplier=0.35)
df['qqe_line'] = qqe_mod_result['qqe_line']
df['histo2'] = qqe_mod_result['histo2']
df['qqe_up'] = qqe_mod_result['qqe_up']
df['qqe_down'] = qqe_mod_result['qqe_down']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `'close'` column.
- `rsi_period` (int): Period for RSI calculation. Default is `6`.
- `rsi_smoothing` (int): Smoothing period for RSI. Default is `5`.
- `qqe_factor` (int): Fast QQE Factor. Default is `3`.
- `threshold` (int): Threshold value for buy/sell signals. Default is `3`.
- `bollinger_length` (int): Length for Bollinger Bands calculation. Default is `50`.
- `bb_multiplier` (float): Multiplier for Bollinger Bands. Default is `0.35`.
- `rsi_period2` (int): Period for the second RSI calculation. Default is `6`.
- `rsi_smoothing2` (int): Smoothing period for the second RSI. Default is `5`.
- `qqe_factor2` (float): QQE Factor for the second QQE. Default is `1.61`.
- `threshold2` (int): Threshold value for the second QQE. Default is `3`.

### Returns
- **DataFrame**: A DataFrame with the following columns:
  - `'qqe_line'`: The QQE line.
  - `'histo2'`: The histogram showing differences in price momentum.
  - `'qqe_up'`: Signals for upward price movement.
  - `'qqe_down'`: Signals for downward price movement.

---

## Relative Strength Index (RSI)

### Description
The **Relative Strength Index (RSI)** is a momentum oscillator that measures the speed and change of price movements. It is commonly used to identify overbought or oversold conditions in the market.

### Usage Example
```python
df['rsi'] = bta.relative_strength_index(df, column='close', period=14)['rsi']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing at least the column specified for the RSI calculation.
- `column` (str): The column on which RSI is calculated. Default is `'close'`.
- `period` (int): The look-back period for RSI calculation. Default is `14`.

### Returns
- **DataFrame**: A DataFrame with a `'rsi'` column containing the calculated RSI values.

---

## Stochastic Momentum Index (SMI)

### Description
The **Stochastic Momentum Index (SMI)** is a momentum indicator developed by William Blau that can help identify trend reversal points by measuring how close the current price is to its recent price range's midpoint.

### Interpretation
- **SMI** values closer to +100 indicate overbought conditions, while values closer to -100 suggest oversold conditions.

### Usage Example
```python
df['smi'] = bta.stochastic_momentum_index(df, k_length=9, d_length=3)['smi']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing `high`, `low`, and `close` columns.
- `k_length` (int): Period for %K. Default is `9`.
- `d_length` (int): Period for %D. Default is `3`.

### Returns
- **DataFrame**: A DataFrame with the `'smi'` column.

---

## Stochastic Oscillator

### Description
The **Stochastic Oscillator** is a momentum indicator that compares the closing price of a security to its price range over a specified period. It helps identify overbought or oversold conditions by measuring the current price relative to the high-low range over a given period.

### Usage Example
```python
stoch = bta.stochastics_oscillator(df, 'high', 'low', 'close', 14, 3)
df['stoch'] = stoch['stoch']
df['stoch_signal'] = stoch['stoch_signal']
df['stoch_hist'] = stoch['stoch_hist']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the price data.
- `high_col` (str): Column name for the high prices. Default is `'high'`.
- `low_col` (str): Column name for the low prices. Default is `'low'`.
- `close_col` (str): Column name for the close prices. Default is `'close'`.
- `window` (int): Lookback period for the Stochastic Oscillator calculation. Default is `14`.
- `smooth_window` (int): Lookback period for calculating the Stochastic Signal. Default is `3`.
- `fillna` (bool): If `True`, fill NaN values. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with the following columns:
  - `'stoch'`: The Stochastic %K line, representing the raw stochastic oscillator value.
  - `'stoch_signal'`: The Stochastic %D line, which is a smoothed version of %K.
  - `'stoch_hist'`: The Stochastic Histogram, which is the difference between %K and %D.

### Interpretation
- The **Stochastic Oscillator** fluctuates between 0 and 100. Values above 80 indicate overbought conditions, and values below 20 indicate oversold conditions.
- The **Stochastic Signal** (%D) is a smoothed version of the oscillator and can be used to generate buy/sell signals when it crosses above or below the %K line.
- The **Stochastic Histogram** represents the difference between the %K and %D lines, providing insight into the momentum of the trend.

---

## Stochastic RSI (StochasticRSI)

### Description
The **Stochastic RSI** is a technical analysis indicator that applies the Stochastic oscillator formula to RSI values, helping identify overbought and oversold conditions more accurately.

### Interpretation
- **Stochastic RSI** generates buy and sell signals when %K and %D lines cross, with %K above %D indicating a potential buy, and %K below %D signaling a potential sell.

### Usage Example
```python
stoch_rsi = bta.stochastic_rsi(df, length_rsi=14, length_stoch=14, smooth_k=3, smooth_d=3)
df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
df['stoch_rsi_d'] = stoch_rsi['stoch_rsi_d']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing a `'close'` column.
- `length_rsi` (int): Period for the RSI calculation. Default is `14`.
- `length_stoch` (int): Period for the Stochastic calculation. Default is `14`.
- `smooth_k` (int): Smoothing period for %K line. Default is `3`.
- `smooth_d` (int): Smoothing period for %D line. Default is `3`.

### Returns
- **DataFrame**: A DataFrame with `'stoch_rsi_k'` and `'stoch_rsi_d'` columns.

---

## True Strength Index (TSI)

### Description
The **True Strength Index (TSI)** shows both trend direction and overbought/oversold conditions by measuring the strength of price movements.

### Interpretation
- **TSI** above 0 indicates bullish momentum, while values below 0 suggest bearish momentum. It is often used with signal lines to confirm trends.

### Usage Example
```python
df['tsi'] = bta.true_strength_index(df, 'close', 25, 13)['tsi']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `close` column.
- `close_col` (str): Column name for the close prices. Default is `'close'`.
- `window_slow` (int): Long period. Default is `25`.
- `window_fast` (int): Short period. Default is `13`.
- `fillna` (bool): If `True`, fills NaN values with `0`. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with the `'tsi'` column.

---

## Ultimate Oscillator (UO)

### Description
The **Ultimate Oscillator (UO)** combines short-term, intermediate-term, and long-term price action into one oscillator, helping to spot potential reversals.

### Interpretation
- **UO** values above 70 suggest overbought conditions, while values

 below 30 indicate oversold conditions.

### Usage Example
```python
df['uo'] = bta.ultimate_oscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `high`, `low`, and `close` columns.
- `high_col` (str): Name of the column containing high price data. Default is `'high'`.
- `low_col` (str): Name of the column containing low price data. Default is `'low'`.
- `close_col` (str): Name of the column containing close price data. Default is `'close'`.
- `window1` (int): Short period. Default is `7`.
- `window2` (int): Medium period. Default is `14`.
- `window3` (int): Long period. Default is `28`.
- `weight1` (float): Weight of short BP average. Default is `4.0`.
- `weight2` (float): Weight of medium BP average. Default is `2.0`.
- `weight3` (float): Weight of long BP average. Default is `1.0`.
- `fillna` (bool): If `True`, fills NaN values with `50`. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with the `'uo'` column.

---

## Williams %R

### Description
The **Williams %R** is a momentum indicator that measures overbought and oversold levels in the market.

### Interpretation
- **Williams %R** values closer to `-100` indicate oversold conditions, while values closer to `0` suggest overbought conditions.

### Usage Example
```python
df['williams_r'] = bta.williams_r(df, 'high', 'low', 'close', 14)['williams_r']
```

### Parameters
- `df` (pandas.DataFrame): Input DataFrame containing the `high`, `low`, and `close` columns.
- `high_col` (str): Name of the column containing high price data. Default is `'high'`.
- `low_col` (str): Name of the column containing low price data. Default is `'low'`.
- `close_col` (str): Name of the column containing close price data. Default is `'close'`.
- `lbp` (int): Lookback period. Default is `14`.
- `fillna` (bool): If `True`, fills NaN values with `-50`. Default is `False`.

### Returns
- **DataFrame**: A DataFrame with the `'williams_r'` column.
