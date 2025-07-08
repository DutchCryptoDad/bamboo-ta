# Bamboo TA Indicators Documentation

# Candles

## Candlestick Patterns
Name:
        Comprehensive Candlestick Patterns Detection

    Description:
        Detects a wide range of candlestick patterns, from basic single-candle types to complex
        multi-candle formations. This function analyzes price data to identify both individual
        candlestick types and pattern formations that may indicate trend continuations or reversals.
        
        The function categorizes patterns into:
        1. Single Candlestick Patterns (e.g., doji, hammer, marubozu)
        2. Two-Candlestick Patterns (e.g., engulfing, harami)
        3. Three-Candlestick Patterns (e.g., morning star, three white soldiers)
        4. Rare & Advanced Patterns (e.g., abandoned baby, island reversal)

    More info:
        https://www.investopedia.com/trading/candlestick-charting-what-is-it/
        https://www.babypips.com/learn/forex/japanese-candlesticks

    Parameters:
        - df (pandas.DataFrame): Input DataFrame which should contain columns:
            'open', 'high', 'low', and 'close'.
        - include_indicators (bool, optional): If True, provides a warning that indicator-based
            pattern detection has been removed. Default is False.

    Single Candlestick Types:
        - "doji": A candle with a very small body, indicating indecision.
        - "long_legged_doji": A doji with long upper and lower shadows, showing extreme indecision.
        - "dragonfly_doji": A doji with a long lower shadow and no upper shadow, often a bullish reversal signal.
        - "gravestone_doji": A doji with a long upper shadow and no lower shadow, often a bearish reversal signal.
        - "four_price_doji": An extremely rare doji where open, high, low, and close are virtually identical.
        - "hammer": A bullish reversal candle with a small body at the top and a long lower shadow.
        - "inverted_hammer": A bullish reversal candle with a small body at the bottom and a long upper shadow.
        - "hanging_man": A bearish reversal candle with a small body at the top and a long lower shadow.
        - "shooting_star": A bearish reversal candle with a small body at the bottom and a long upper shadow.
        - "bullish_belt_hold": A bullish candle with a large body and no or minimal lower shadow.
        - "bearish_belt_hold": A bearish candle with a large body and no or minimal upper shadow.
        - "bullish_marubozu": A bullish candle with a large body and no or minimal shadows.
        - "bearish_marubozu": A bearish candle with a large body and no or minimal shadows.
        - "high_wave": A candle with a small body and very long upper and lower shadows, indicating volatility.
        - "bullish_spinning_top": A bullish candle with a small body and significant upper and lower shadows.
        - "bearish_spinning_top": A bearish candle with a small body and significant upper and lower shadows.
        - "bullish": A standard bullish candle (close > open) that doesn't match any specific pattern.
        - "bearish": A standard bearish candle (close < open) that doesn't match any specific pattern.

    Multi-Candle Patterns:
        Two-Candle Patterns:
        - "bullish_engulfing": A bullish reversal pattern where a large bullish candle engulfs the previous bearish candle.
        - "bearish_engulfing": A bearish reversal pattern where a large bearish candle engulfs the previous bullish candle.
        - "bullish_harami": A bullish reversal pattern where a small bullish candle is contained within the previous bearish candle.
        - "bearish_harami": A bearish reversal pattern where a small bearish candle is contained within the previous bullish candle.
        - "bullish_harami_cross": A stronger bullish harami where the second candle is a doji.
        - "bearish_harami_cross": A stronger bearish harami where the second candle is a doji.
        - "piercing_line": A bullish reversal pattern where a bullish candle closes above the midpoint of the previous bearish candle.
        - "dark_cloud_cover": A bearish reversal pattern where a bearish candle opens above the previous high and closes below the midpoint.
        - "tweezer_tops": A bearish reversal pattern with two candles having the same or similar highs.
        - "tweezer_bottoms": A bullish reversal pattern with two candles having the same or similar lows.
        - "up_gap_side_by_side_white_lines": A bullish continuation pattern with two bullish candles separated by a gap up.
        - "down_gap_side_by_side_white_lines": A bearish continuation pattern with two bearish candles separated by a gap down.
        - "separating_lines_bullish": A bullish continuation pattern where a bullish candle follows a bearish one with the same open.
        - "separating_lines_bearish": A bearish continuation pattern where a bearish candle follows a bullish one with the same open.
        - "hook_reversal_bullish": A bullish reversal pattern similar to piercing line but less strong.
        - "hook_reversal_bearish": A bearish reversal pattern similar to dark cloud cover but less strong.
        - "on_neck_line": A bearish continuation pattern where a bullish candle closes at the previous low.
        - "in_neck_line": A bearish continuation pattern where a bullish candle closes slightly above the previous low.
        - "thrusting_pattern": A weak bearish continuation pattern where a bullish candle closes below the midpoint of the previous bearish candle.

        Three-Candle Patterns:
        - "morning_star": A bullish reversal pattern with a bearish candle, a small-bodied candle, and a bullish candle.
        - "evening_star": A bearish reversal pattern with a bullish candle, a small-bodied candle, and a bearish candle.
        - "abandoned_baby_bullish": A strong bullish reversal with a bearish candle, a gapped-down doji, and a gapped-up bullish candle.
        - "abandoned_baby_bearish": A strong bearish reversal with a bullish candle, a gapped-up doji, and a gapped-down bearish candle.
        - "three_white_soldiers": A strong bullish reversal with three consecutive bullish candles, each closing higher.
        - "three_black_crows": A strong bearish reversal with three consecutive bearish candles, each closing lower.
        - "three_inside_up": A bullish reversal starting with a bullish harami and followed by a confirming bullish candle.
        - "three_inside_down": A bearish reversal starting with a bearish harami and followed by a confirming bearish candle.
        - "three_outside_up": A bullish reversal starting with a bullish engulfing and followed by a confirming bullish candle.
        - "three_outside_down": A bearish reversal starting with a bearish engulfing and followed by a confirming bearish candle.
        - "rising_three_methods": A bullish continuation with a large bullish candle, three small bearish candles, and a final bullish candle.
        - "falling_three_methods": A bearish continuation with a large bearish candle, three small bullish candles, and a final bearish candle.
        - "mat_hold": A bullish continuation similar to rising three methods but with a gap.
        - "tri_star_bullish": A bullish reversal with three consecutive doji candles forming a bottom.
        - "tri_star_bearish": A bearish reversal with three consecutive doji candles forming a top.
        - "unique_three_river_bottom": A bullish reversal with a long bearish candle, a bearish candle with a new low, and a small bullish candle.
        - "concealing_baby_swallow": A rare bearish reversal pattern with four bearish candles.
        - "advance_block": A weakening bullish trend with three bullish candles of decreasing size and increasing upper shadows.
        - "deliberation": A warning of potential reversal after an uptrend, with two strong bullish candles followed by a small bullish candle.

        Complex Patterns:
        - "tower_top": A bearish reversal after an uptrend, with a series of rising candles followed by a strong bearish candle.
        - "tower_bottom": A bullish reversal after a downtrend, with a series of falling candles followed by a strong bullish candle.
        - "ladder_bottom": A bullish reversal after a downtrend, with three bearish candles followed by a strong bullish candle.
        - "ladder_top": A bearish reversal after an uptrend, with three bullish candles followed by a strong bearish candle.
        - "fry_pan_bottom": A bullish reversal forming a rounded bottom pattern.
        - "dumpling_top": A bearish reversal forming a rounded top pattern.
        - "island_reversal_bullish": A bullish reversal with an isolated low surrounded by gaps.
        - "island_reversal_bearish": A bearish reversal with an isolated high surrounded by gaps.

    Pattern Interpretation Guide:
        Bullish Reversal Patterns:
        - Hammer, Dragonfly Doji: Potential reversal after downtrend, shows buyers stepping in at lows
        - Bullish Engulfing, Morning Star: Strong reversal signals, especially after extended downtrends
        - Piercing Line: Moderate reversal signal, needs confirmation
        - Bullish Harami: Indicates indecision after downtrend, weaker signal than engulfing
        - Three White Soldiers: Very strong reversal signal, especially after a prolonged downtrend
        - Abandoned Baby Bullish: Rare but extremely strong reversal signal

        Bearish Reversal Patterns:
        - Shooting Star, Gravestone Doji: Potential reversal after uptrend, shows sellers stepping in at highs
        - Bearish Engulfing, Evening Star: Strong reversal signals, especially after extended uptrends
        - Dark Cloud Cover: Moderate reversal signal, needs confirmation
        - Bearish Harami: Indicates indecision after uptrend, weaker signal than engulfing
        - Three Black Crows: Very strong reversal signal, especially after a prolonged uptrend
        - Abandoned Baby Bearish: Rare but extremely strong reversal signal

        Continuation Patterns:
        - Rising/Falling Three Methods: Strong continuation signals during trends
        - Separating Lines: Moderate continuation signals
        - On Neck Line, In Neck Line, Thrusting Pattern: Weak bearish continuation signals

        Indecision Patterns:
        - Doji, Long-legged Doji: Market indecision, potential reversal if at support/resistance
        - Spinning Tops: Weak indecision signals, less significant than doji

    Trading Strategies:
        1. Reversal Trading:
           - Look for strong reversal patterns (Morning Star, Engulfing) at support/resistance levels
           - Confirm with volume increase and/or other technical indicators
           - Set stop loss below/above the pattern's low/high point

        2. Trend Continuation:
           - Use patterns like Three Methods during established trends
           - Enter in the direction of the primary trend when continuation patterns form
           - Tighter stop losses can be used compared to reversal trades

        3. Volatility Breakout:
           - Look for indecision patterns (Doji) followed by strong momentum candles
           - Enter in the direction of the breakout candle
           - Place stop loss below/above the Doji's low/high

        4. Multiple Timeframe Confirmation:
           - Confirm patterns on higher timeframes before trading on lower timeframes
           - Higher probability setups occur when patterns align across multiple timeframes

    Call with:
        # Detect candlestick types and patterns
        candlestick_df = bta.candlestick_patterns(df)
        
        # Add type and pattern columns to original DataFrame
        df['candlestick_type'] = candlestick_df['type']
        df['candlestick_pattern'] = candlestick_df['pattern']

    Returns:
        pd.DataFrame: DataFrame with 'type' column for individual candle types and 'pattern' column
        for multi-candle patterns.

## Dynamic Exhaustion Bars
Name:
    Dynamic Leledc Exhaustion Bars

Description:
    The lookback length and exhaustion bars adjust dynamically to the market conditions.

    This indicator dynamically adjusts the lookback length and the exhaustion 
    bars based on the market's behavior, helping to identify potential reversals
    and trend strength.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - window (int): Lookback window for z-score calculation. Default is 500.

Call with:
    dynamic_exhaustion = bta.dynamic_exhaustion_bars(df)
    df['dynamic_leledc_major'] = dynamic_exhaustion['leledc_major']
    df['dynamic_leledc_minor'] = dynamic_exhaustion['leledc_minor']

Returns:
    pd.DataFrame: DataFrame with 'leledc_major' and 'leledc_minor' columns.

## Exhaustion Bars
Name:
    Leledc Exhaustion Bars

Description:
    Infamous S/R Reversal Indicator

    Leledc exhaustion bars are a specific type of price action pattern used in
    technical analysis to identify potential reversals in the market trend.
    These bars are characterized by a sharp move in price with an increase in
    volume, often indicating that the current trend is losing momentum and may
    reverse direction soon. Traders use them to pinpoint the end of a trend
    and the beginning of a new one, thereby making more informed trading decisions.

More info:
    https://www.abundancetradinggroup.com/leledc-exhaustion-bar-mt4-indicator/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open',
        'high', 'low', and 'close' columns.
    - maj_qual (int): Major quality parameter. Default is 6.
    - maj_len (int): Major length parameter. Default is 30.
    - min_qual (int): Minor quality parameter. Default is 5.
    - min_len (int): Minor length parameter. Default is 5.
    - core_length (int): Core length parameter. Default is 4.

Call with:
    exhaustion = bta.exhaustion_bars(df)
    df['leledc_major'] = exhaustion['leledc_major']
    df['leledc_minor'] = exhaustion['leledc_minor']

Returns:
    pd.DataFrame: DataFrame with 'leledc_major' and 'leledc_minor' columns.

## Hansen Heiken Ashi
Name:
    Hansen Heiken Ashi (HHA)

Description:
    The Hansen Heiken Ashi is a modified version of the Heiken Ashi candlestick calculation
    with additional smoothing using a Simple Moving Average (SMA). It aims to reduce noise
    in the data for better trend visualization.

More info:
    https://www.investopedia.com/terms/h/heikenashi.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC (open, high, low, close) data.
    - period (int): Period for the Simple Moving Average (SMA) to smooth data. Default is 6.

Call with:
    hha_result = bta.hansen_heiken_ashi(df, period=6)
    df['hha_emac'] = hha_result['emac']
    df['hha_emao'] = hha_result['emao']

Returns:
    pd.DataFrame: DataFrame containing the smoothed 'emac' and 'emao' columns.

## Heiken Ashi
Name:
    Heiken Ashi

Description:
    Heiken Ashi (HA) with Optional Pre and Post Smoothing

    Heiken Ashi is a type of price chart that shares some characteristics with
    candlestick charts but differs due to the values used to plot them. This
    modified version allows for optional smoothing of the original data before
    the Heiken Ashi calculation and/or smoothing of the Heiken Ashi values
    themselves, aiming to provide a more refined and smoother representation
    of price action, making it easier to identify the trend.

More info:
    https://www.investopedia.com/terms/h/heikenashi.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns:
        'open', 'high', 'low', and 'close'.
    - pre_smoothing_period (int, optional): Period for EMA pre-smoothing of the
        original data. If provided, original price bars are smoothed before Heiken
        Ashi calculations.
    - post_smoothing_period (int, optional): Period for EMA post-smoothing of
        Heiken Ashi values. If provided, Heiken Ashi values are smoothed post calculations.

Call with:
    ha_df = bta.heiken_ashi(df)
    df['ha_open'] = ha_df['ha_open']
    df['ha_high'] = ha_df['ha_high']
    df['ha_low'] = ha_df['ha_low']
    df['ha_close'] = ha_df['ha_close']

Returns:
    pd.DataFrame: DataFrame with 'ha_open', 'ha_high', 'ha_low', and 'ha_close' columns.

## Linear Regression Candles
Name:
    Linear Regression Candles

Description:
    Linear Regression Candles with Optional Signal Line
    The Linear Regression Candles transform the traditional OHLC bars using a
    linear regression algorithm, providing a smoothed representation of price
    action. The function also provides an optional signal line, which can be
    either an SMA or an EMA of the Linear Regression Candle close. This signal
    line can help to identify trends and potential trading signals.

More info:
    https://www.investopedia.com/terms/l/linearregression.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns:
        'open', 'high', 'low', and 'close'.
    - linreg_length (int, optional): Period for linear regression calculation.
        Default is 11.
    - sma_signal (bool, optional): If True, uses SMA for the signal line. If
        False, uses EMA. Default is True.
    - signal_length (int, optional): Period for the moving average signal line.
        Default is 11.

Call with:
    lr_df = bta.linear_regression_candles(df)
    df['lrc_open'] = lr_df['bopen']
    df['lrc_high'] = lr_df['bhigh']
    df['lrc_low'] = lr_df['blow']
    df['lrc_close'] = lr_df['bclose']
    df['lrc_signal'] = lr_df['signal']

Returns:
    pd.DataFrame: DataFrame with 'bopen', 'bhigh', 'blow', 'bclose' as the
    Linear Regression Candles, and 'signal' as the signal line.

## Smoothed Heiken Ashi
Name:
    Smoothed Heiken Ashi Candles

Description:
    This function computes the Smoothed Heiken Ashi Candles using two levels of exponential 
    moving average (EMA) smoothing. The first smoothing is applied to the original OHLC 
    prices, and then the Heiken Ashi values are computed.
    A second smoothing is applied to the Heiken Ashi values to produce the final smoothed 
    candle values.

More info:
    https://www.investopedia.com/terms/h/heikenashi.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the columns 'open', 'high', 'low', and 'close'.
    - len_ (int): The period for the first level EMA smoothing of the original prices. Default is 10.
    - len2 (int): The period for the second level EMA smoothing of the Heiken Ashi values. Default is 10.
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    sha_result = bta.smoothed_heiken_ashi(df, len_=10, len2=10)
    df['sha_open'] = sha_result['sha_open']
    df['sha_high'] = sha_result['sha_high']
    df['sha_low'] = sha_result['sha_low']
    df['sha_close'] = sha_result['sha_close']
    df['sha_color'] = sha_result['sha_color']

Returns:
    pd.DataFrame: DataFrame with columns 'sha_open', 'sha_high', 'sha_low', 'sha_close', and 'sha_color'.

# Cycles

## Even Better Sinewave
Name:
    Even Better SineWave (EBSW)

Description:
    The Even Better SineWave (EBSW) indicator measures market cycles and uses a low pass filter 
    to remove noise. Its output is a bounded signal between -1 and 1, and the maximum length 
    of a detected trend is limited by its length input. This indicator can be used to identify 
    cyclical patterns in price movements and potential turning points in the market.

More info:
    https://www.prorealcode.com/prorealtime-indicators/even-better-sinewave/
    J.F.Ehlers 'Cycle Analytics for Traders', 2014

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Maximum cycle/trend period. Values between 40-48 work as expected 
      with minimum value of 39. Default is 40.
    - bars (int): Period of low pass filtering. Default is 10.

Call with:
    result = bta.even_better_sinewave(df)
    df['ebsw'] = result['ebsw']

Returns:
    pd.DataFrame: DataFrame with 'ebsw' column containing the Even Better SineWave values.

# Momentum

## Absolute Price Oscillator
Name:
    Absolute Price Oscillator

Description:
    The Absolute Price Oscillator (APO) is a momentum indicator that measures 
    the difference between two moving averages, typically an exponential 
    moving average (EMA). It's similar to the MACD (Moving Average Convergence 
    Divergence) but doesn't include a signal line. The APO helps identify the 
    momentum and trend direction of a security.

More info:
    https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/absolute-price-oscillator-apo/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - fast_length (int): Period for the faster moving average. Default is 12.
    - slow_length (int): Period for the slower moving average. Default is 26.
    - mamode (str): Moving average type, either 'sma' or 'ema'. Default is 'sma'.

Call with:
    df['apo'] = bta.absolute_price_oscillator(df)['apo']

For Signal line:
    df['apo_signal'] = df['apo'].rolling(window=9).mean()  # Using SMA for signal

Returns:
    pd.DataFrame: DataFrame with 'apo' column.

## Awesome Oscillator
Name:
    Awesome Oscillator

Description:
    The Awesome Oscillator is a momentum indicator used to measure market momentum.
    It is calculated by subtracting a 34-period simple moving average (SMA) of the
    median price from a 5-period SMA of the median price.

More info:
    https://www.investopedia.com/terms/a/awesomeoscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing 'high' and 'low' columns.
    - high_col (str): The name of the 'high' column. Default is 'high'.
    - low_col (str): The name of the 'low' column. Default is 'low'.
    - window1 (int, optional): Short period. Default is 5.
    - window2 (int, optional): Long period. Default is 34.
    - fillna (bool, optional): If True, fill nan values with 0. Default is False.

Call with:
    df['ao'] = bta.awesome_oscillator(df, 'high', 'low', 5, 34)['ao']

Returns:
    pd.DataFrame: DataFrame with the 'ao' column.

## Balance Of Power
Name:
    Balance of Power

Description:
    The Balance of Power (BOP) indicator measures the strength of buyers vs sellers
    by assessing the ability of each to push price to an extreme level. It is calculated
    by comparing the close and open prices relative to the high and low prices.
    
    Positive BOP values indicate buying pressure, while negative values indicate
    selling pressure. A zero line crossing can signal a potential shift in control
    between buyers and sellers.

More info:
    http://www.worden.com/TeleChartHelp/Content/Indicators/Balance_of_Power.htm

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low',
      and 'close' columns.
    - scalar (float): Factor to magnify the values. Default is 1.0.

Call with:
    df['bop'] = bta.balance_of_power(df)['bop']

For Signal line:
    df['bop_signal'] = df['bop'].rolling(window=14).mean()  # Using SMA for signal

Returns:
    pd.DataFrame: DataFrame with 'bop' column.

## Bias
Name:
    Bias

Description:
    The Bias indicator measures the percentage deviation of the current price from a
    moving average. It helps identify potential overbought or oversold conditions when
    the price deviates significantly from the moving average.

More info:
    This indicator is popular among Asian traders and is sometimes used to identify
    market extremes.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the moving average. Default is 26.
    - mamode (str): Moving average type, either 'sma' or 'ema'. Default is 'sma'.

Call with:
    df['bias'] = bta.bias(df)['bias']

Returns:
    pd.DataFrame: DataFrame with 'bias' column.

## Brar
Name:
    BR and AR

Description:
    BR (Bias Ratio) and AR (Arbiter Ratio) are momentum indicators commonly used
    in Asian markets. They measure buying and selling pressure by comparing price
    movements to open, high, low, and close values.
    
    AR compares the strength of the bulls (high - open) versus the bears (open - low).
    BR compares today's high with yesterday's close (bulls) versus yesterday's close
    with today's low (bears).
    
    Values above 100 indicate bullish strength, while values below 100 indicate
    bearish strength. Extreme readings may indicate overbought or oversold conditions.

More info:
    This indicator is particularly popular in Chinese and other Asian markets.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low',
      and 'close' columns.
    - length (int): Lookback period for calculations. Default is 26.
    - scalar (float): Multiplier for the ratio. Default is 100.
    - drift (int): The difference period for previous close. Default is 1.

Call with:
    result = bta.brar(df)
    df['ar'] = result['ar']
    df['br'] = result['br']

Returns:
    pd.DataFrame: DataFrame with 'ar' and 'br' columns.

## Calculate Intraday Momentum Index
Name:
    Intraday Momentum Index (IMI)

Description:
    The Intraday Momentum Index combines candlestick analysis with relative strength index (RSI)
    principles to measure intraday momentum based on the relationship between the open and close prices.

More info:
    https://www.investopedia.com/terms/i/intraday-momentum-index.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the following columns:
        - 'open': Opening price.
        - 'close': Closing price.
    - length (int, default=14): Lookback period for calculating the IMI.

Call with:
    df['imi'] = bta.calculate_intraday_momentum_index(df, length=14)

Returns:
    pd.Series: A Series representing the Intraday Momentum Index (IMI) values.

## Center Of Gravity
Name:
    Center of Gravity

Description:
    The Center of Gravity (CG) oscillator was developed by John Ehlers to identify 
    turning points in price with minimal lag. Unlike many other momentum oscillators, 
    the CG aims to be more responsive to price changes while maintaining some 
    smoothing characteristics.
    
    The implementation follows Ehlers' formula:
    CG = WMA(close, length) * length * (length + 1) / 2 / SUM(close, length)
    
    Where WMA is a weighted moving average that assigns more weight to recent prices.

More info:
    http://www.mesasoftware.com/papers/TheCGOscillator.pdf
    https://www.tradingview.com/script/yhhunbyq/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the CG calculation. Default is 10.
    - include_shifted (bool): If True, includes the CG value from the previous bar
      as a separate column. Default is True.

Call with:
    # Get both current and previous CG values
    cg_df = bta.center_of_gravity(df)
    df['cg'] = cg_df['cg']
    df['cg_prev'] = cg_df['cg_prev']
    
    # Or just the current CG value
    df['cg'] = bta.center_of_gravity(df, include_shifted=False)['cg']

Returns:
    pd.DataFrame: DataFrame with 'cg' column and optionally 'cg_prev' column.

## Chande Forecast Oscillator
Name:
    Chande Forecast Oscillator

Description:
    The Chande Forecast Oscillator (CFO) calculates the percentage difference between 
    the actual price and the Time Series Forecast (TSF), which is the endpoint of a 
    linear regression line. It helps identify potential price reversals when the 
    price deviates significantly from its forecasted value.
    
    Positive values indicate that the current price is above the forecasted value, 
    suggesting potential overbought conditions. Negative values indicate that the 
    current price is below the forecasted value, suggesting potential oversold conditions.

More info:
    https://www.fmlabs.com/reference/default.htm?url=ForecastOscillator.htm

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for linear regression calculation. Default is 9.
    - scalar (float): Multiplier for the percentage difference. Default is 100.

Call with:
    df['cfo'] = bta.chande_forecast_oscillator(df)['cfo']

Returns:
    pd.DataFrame: DataFrame with 'cfo' column.

## Chande Momentum Oscillator
Name:
    Chande Momentum Oscillator

Description:
    The Chande Momentum Oscillator (CMO) is a technical momentum indicator developed 
    by Tushar Chande. It measures the amount that an asset's price has changed over 
    a specified period of time.

More info:
    https://www.investopedia.com/terms/c/chandemomentumoscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Length for the CMO calculation. Default is 14.

Call with:
        df['cmo'] = bta.chande_momentum_oscillator(df)

For Signal line:
        df['cmo_signal'] = df['cmo'].rolling(window=10).mean()  # Using SMA for signal

Returns:
    pd.DataFrame: DataFrame with 'cmo' column.

## Commodity Channel Index
Name:
    Commodity Channel Index

Description:
    The Commodity Channel Index (CCI) is a momentum-based oscillator used to help determine 
    when an investment vehicle is reaching a condition of being overbought or oversold. 
    It is also used to assess price trend direction and strength. This information 
    helps traders and investors make buy/sell decisions.
    
    CCI measures the current price level relative to an average price level over a 
    given period of time. The indicator fluctuates above or below zero, moving 
    between overbought and oversold conditions.

More info:
    https://www.investopedia.com/terms/c/commoditychannelindex.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - length (int): The period for calculating CCI. Default is 14.
    - constant (float): Scaling factor. Default is 0.015.

Call with:
    df['cci'] = bta.commodity_channel_index(df)['cci']

Returns:
    pd.DataFrame: DataFrame with 'cci' column.

## Coppock Curve
Name:
    Coppock Curve

Description:
    The Coppock Curve is a long-term price momentum indicator developed by Edwin 
    Sedgwick Coppock. It was originally designed for monthly analysis of equity 
    indices, intended to identify major bottoms in the stock market. The indicator 
    uses rate of change and a weighted moving average to identify long-term trend changes.
    
    It's typically used as a buy signal when it crosses above zero from below. The indicator 
    is particularly effective in identifying major market bottoms following significant 
    declines.

More info:
    https://en.wikipedia.org/wiki/Coppock_curve
    https://www.investopedia.com/terms/c/coppockcurve.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the weighted moving average. Default is 10.
    - fast (int): The faster ROC period. Default is 11.
    - slow (int): The slower ROC period. Default is 14.

Call with:
    df['coppock'] = bta.coppock_curve(df)['coppock']

Returns:
    pd.DataFrame: DataFrame with 'coppock' column.

## Correlation Trend Indicator
Name:
    Correlation Trend Indicator

Description:
    The Correlation Trend Indicator (CTI) is an oscillator created by John Ehler. 
    It measures how closely prices follow a straight line over a given period. 
    The indicator calculates the correlation coefficient between price and time, 
    resulting in values that range from -1 to 1.
    
    A value near 1 indicates prices are following a strong uptrend (positively-sloping line).
    A value near -1 indicates prices are following a strong downtrend (negatively-sloping line).
    Values near 0 indicate no clear trend or sideways movement.

More info:
    https://www.mesasoftware.com/papers/TrendCorrelationIndicator.pdf

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for correlation calculation. Default is 12.

Call with:
    df['cti'] = bta.correlation_trend_indicator(df)['cti']

Returns:
    pd.DataFrame: DataFrame with 'cti' column.

## Directional Movement
Name:
    Directional Movement

Description:
    The Directional Movement (DM) indicator was developed by J. Welles Wilder to 
    determine which direction the price of an asset is moving. It compares prior 
    highs and lows to yield two series: +DM (positive directional movement) and 
    -DM (negative directional movement).
    
    +DM measures upward price movement, while -DM measures downward price movement.
    These values are often used as components in calculating the Directional Movement
    Index (DMI) and Average Directional Index (ADX).

More info:
    https://www.investopedia.com/terms/d/directionalmovement.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): The period for the moving average calculation. Default is 14.
    - mamode (str): Moving average type, one of 'rma', 'sma', or 'ema'. Default is 'rma'.
    - drift (int): The difference period for calculating movements. Default is 1.

Call with:
    result = bta.directional_movement(df)
    df['dmp'] = result['dmp']  # Positive Directional Movement
    df['dmn'] = result['dmn']  # Negative Directional Movement

Returns:
    pd.DataFrame: DataFrame with 'dmp' (+DM) and 'dmn' (-DM) columns.

## Efficiency Ratio
Name:
    Efficiency Ratio

Description:
    The Efficiency Ratio (ER) was developed by Perry J. Kaufman to measure market noise 
    or volatility. It quantifies the efficiency of price movement by comparing the net 
    directional movement to the total volatility over a specified period.
    
    The indicator ranges from 0 to 1, where values close to 1 indicate a strong trend 
    with minimal noise, and values close to 0 indicate a choppy market with high noise. 
    It's often used to adjust the responsiveness of other indicators based on market 
    conditions.

More info:
    https://www.investopedia.com/terms/k/kaufman-efficiency-ratio.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the efficiency calculation. Default is 10.
    - drift (int): The period for calculating price changes. Default is 1.

Call with:
    df['er'] = bta.efficiency_ratio(df)['er']

Returns:
    pd.DataFrame: DataFrame with 'er' column.

## Ehlers Fisher Stochastic Center Of Gravity
Name:
    Ehlers Fisher Stochastic Center of Gravity Indicator

Description:
    The Fisher Stochastic Center of Gravity indicator, developed by John Ehlers, 
    is used to identify potential turning points in the market by calculating 
    the center of gravity of price movements.

More info:
    https://ninjatraderecosystem.com/user-app-share-download/john-ehlers-the-fisher-stochastic-center-of-gravity/
    https://fxstill.com/indikators/the-fisher-stochastic-center-of-gravity
    https://viewer.mathworks.com/?viewer=plain_code&url=https%3A%2F%2Fes.mathworks.com%2Fmatlabcentral%2Fmlc-downloads%2Fdownloads%2F5a9e5f01-906c-4152-98c6-87484eed86bf%2F853ab8ad-8751-4bcd-ae00-60a9444e9182%2Ffiles%2Fmatlab%2FChapter4-Ehlers%2FEhlerStochCG.m&embed=web
    https://www.tradingview.com/script/TLjl71aL-Ehlers-Fisher-Stochastic-Center-Of-Gravity-CC/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high', 'low'.
    - length (int): Period for the indicator. Default is 8.

Call with:
    fscg = bta.ehlers_fisher_stochastic_center_of_gravity(df)
    df['cg'] = fscg['cg']
    df['trigger'] = fscg['trigger']

Returns:
    pd.DataFrame: DataFrame with 'CG' and 'Trigger' columns.

## Ehlers Ray Index
Name:
    Ehlers Ray Index

Description:
    The Ehlers Ray Index, also known as Elder Ray Index, was developed by Dr. Alexander 
    Elder. It consists of two separate indicators: Bull Power and Bear Power, which 
    are designed to measure the strength of buyers and sellers in the market.
    
    Bull Power measures the ability of buyers to push prices above an average consensus 
    value (the EMA). Positive values indicate buying pressure, with higher values 
    showing stronger buying pressure.
    
    Bear Power measures the ability of sellers to push prices below the same average 
    consensus value. Negative values indicate selling pressure, with lower values 
    showing stronger selling pressure.
    
    Both indicators are typically used together with trend analysis to identify 
    favorable entry points.

More info:
    https://www.investopedia.com/terms/e/elderray.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - length (int): The period for the EMA calculation. Default is 13.

Call with:
    result = bta.ehlers_ray_index(df)
    df['bull_power'] = result['bull_power']
    df['bear_power'] = result['bear_power']

Returns:
    pd.DataFrame: DataFrame with 'bull_power' and 'bear_power' columns.

## Elliott Wave Oscillator
Name:
    Elliott Wave Oscillator

Description:
    The Elliott Wave Oscillator (EWO) is a tool to help identify the trend and 
    overall market pattern, assisting in finding future trading opportunities.
    It is derived by calculating the difference between a short and long period 
    simple moving average, then normalizing the result with the close price.

More info:
    https://www.investopedia.com/terms/e/elliottwavetheory.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the 
      column specified.
    - column (str): The column on which EWO is to be calculated. Default is 'close'.
    - sma1_period (int): The period for the shorter SMA used in EWO calculation. 
      Default is 5.
    - sma2_period (int): The period for the longer SMA used in EWO calculation. 
      Default is 35.

Call with:
    df['ewo'] = bta.elliott_wave_oscillator(df, 'close', 5, 35)

Returns:
    pd.DataFrame: DataFrame with 'ewo' column.

## Fisher Transform
Name:
    Fisher Transform

Description:
    The Fisher Transform is a technical indicator created by John F. Ehlers that 
    converts prices into a Gaussian normal distribution. The indicator aims to 
    identify significant price reversals by normalizing prices over a specified 
    period and applying a mathematical formula to amplify and clarify price turning points.
    
    The indicator consists of two lines: the Fisher Transform line and its signal line. 
    A reversal signal is suggested when these two lines cross. The indicator helps 
    traders identify potential overbought and oversold conditions and price reversal points.

More info:
    https://www.investopedia.com/terms/f/fisher-transform.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): The period for price normalization. Default is 9.
    - signal (int): The period for the signal line. Default is 1.

Call with:
    result = bta.fisher_transform(df)
    df['fisher'] = result['fisher']
    df['fisher_signal'] = result['fisher_signal']

Returns:
    pd.DataFrame: DataFrame with 'fisher' and 'fisher_signal' columns.

## Inertia
Name:
    Inertia

Description:
    Inertia was developed by Donald Dorsey and was introduced in his article in 
    September 1995. It combines the Relative Vigor Index (RVI) with a Least Squares 
    Moving Average (LSQRMA) to create a momentum oscillator that attempts to identify 
    the "inertia" of price movement.
    
    The indicator is essentially the Relative Vigor Index smoothed by the Least 
    Squares Moving Average. Traditionally, values above 50 indicate positive inertia
    (bullish), while values below 50 indicate negative inertia (bearish).

More info:
    https://www.investopedia.com/terms/r/relative_vigor_index.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 
      'low', and 'close' columns.
    - length (int): The period for the linear regression calculation. Default is 20.
    - rvi_length (int): The period for the RVI calculation. Default is 14.
    - swma_length (int): The period for the SWMA used in RVI calculation. Default is 4.

Call with:
    df['inertia'] = bta.inertia(df)['inertia']

Returns:
    pd.DataFrame: DataFrame with 'inertia' column.

## Kaufmans Adaptive Moving Average
Name:
    Kaufman's Adaptive Moving Average (KAMA)

Description:
    Moving average designed to account for market noise or volatility. KAMA
    will closely follow prices when the price swings are relatively small and
    the noise is low. KAMA will adjust when the price swings widen and follow
    prices from a greater distance. This trend-following indicator can be
    used to identify the overall trend, time turning points, and filter price
    movements.

More info:
    https://www.investopedia.com/terms/k/kama.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - close_col (str): Column name for the close prices. Default is 'close'.
    - window (int): Number of periods for the efficiency ratio. Default is 10.
    - pow1 (int): Number of periods for the fastest EMA constant. Default is 2.
    - pow2 (int): Number of periods for the slowest EMA constant. Default is 30.
    - fillna (bool): If True, fill nan values with the close prices. Default is False.

Call with:
    df['kama'] = bta.kaufmans_adaptive_moving_average(df)['kama']

Returns:
    pd.DataFrame: DataFrame with 'kama' column.

## Kdj
Name:
    KDJ

Description:
    The KDJ indicator, also known as the Random Index, is a technical indicator used 
    to analyze market momentum and trend reversals. It is a modification of the 
    Stochastic Oscillator with an additional J line that represents the divergence 
    of the D value from the K.
    
    The indicator consists of three lines:
    - K line: Similar to %K in the Stochastic Oscillator
    - D line: Similar to %D in the Stochastic Oscillator
    - J line: Represents the divergence of D from K (calculated as 3K - 2D)
    
    Unlike the Stochastic Oscillator, which is bounded between 0 and 100, the J line 
    can go beyond these boundaries, providing additional signals about market extremes.

More info:
    https://www.investopedia.com/terms/s/stochasticoscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - length (int): The period for calculating highest high and lowest low. Default is 9.
    - signal (int): The smoothing period. Default is 3.

Call with:
    result = bta.kdj(df)
    df['k'] = result['k']
    df['d'] = result['d']
    df['j'] = result['j']

Returns:
    pd.DataFrame: DataFrame with 'k', 'd', and 'j' columns.

## Know Sure Thing
Name:
    Know Sure Thing

Description:
    The Know Sure Thing (KST) is a momentum oscillator developed by Martin Pring. 
    It is based on the Rate of Change (ROC) of different time periods, which are 
    then smoothed and weighted to create a composite momentum indicator.
    
    The KST uses four different ROC periods, each smoothed with a simple moving 
    average (SMA) and assigned different weights. These weighted values are then 
    summed to create the KST line. A signal line (typically a 9-period SMA of the KST) 
    is used to identify potential buy and sell signals.
    
    The indicator is designed to capture momentum across different timeframes, 
    making it potentially more responsive and less prone to false signals than 
    simpler momentum indicators.

More info:
    https://www.investopedia.com/terms/k/know-sure-thing-kst.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - roc1 (int): First ROC period. Default is 10.
    - roc2 (int): Second ROC period. Default is 15.
    - roc3 (int): Third ROC period. Default is 20.
    - roc4 (int): Fourth ROC period. Default is 30.
    - sma1 (int): SMA period for the first ROC. Default is 10.
    - sma2 (int): SMA period for the second ROC. Default is 10.
    - sma3 (int): SMA period for the third ROC. Default is 10.
    - sma4 (int): SMA period for the fourth ROC. Default is 15.
    - signal (int): Period for the signal line. Default is 9.

Call with:
    result = bta.know_sure_thing(df)
    df['kst'] = result['kst']
    df['kst_signal'] = result['kst_signal']

Returns:
    pd.DataFrame: DataFrame with 'kst' and 'kst_signal' columns.

## Ma Streak
Name:
    MA Streak Indicator

Description:
    This indicator tracks how many bars a given moving average is rising or falling.
    It's color-coded green (positive) or red (negative).

More info:
    https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/

Call with:
    df['ma_streak'] = bta.ma_streak(df, length=10, src='close', matype=1)['ma_streak']

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the moving average calculation. Default is 10.
    - src (str): The column name to use for the moving average calculation. Default is 'close'.
    - matype (int): Type of moving average to use. Default is 1 (SMA).

    MA types:
    1 - Simple Moving Average (SMA)
    2 - Exponential Moving Average (EMA)
    3 - Hull Moving Average (HMA)
    4 - Weighted Moving Average (WMA)
    5 - Volume Weighted Moving Average (VWMA)

Returns:
    pd.DataFrame: DataFrame with 'ma_streak' column.

## Momentum
Name:
    Momentum

Description:
    The Momentum indicator measures the amount that a security's price has changed over 
    a given time period. It simply shows the difference between the current price and 
    the price "n" periods ago.
    
    It is one of the simplest momentum indicators to use and understand. The momentum 
    indicator can be used as a trend-following oscillator similar to the Moving Average 
    Convergence Divergence (MACD). When used this way, buy signals are generated when 
    the indicator crosses above zero, and sell signals when it crosses below zero.

More info:
    https://www.investopedia.com/terms/m/momentum.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for momentum calculation. Default is 10.

Call with:
    df['mom'] = bta.momentum(df)['mom']

Returns:
    pd.DataFrame: DataFrame with 'mom' column.

## Momentum Divergence
Name:
    Momentum Divergence (momdiv)

Description:
    A self-contained implementation of the Momentum Divergence indicator. It calculates
    momentum and applies Bollinger Bands to identify potential buy and sell signals
    based on momentum divergence. Additionally, it detects if the current high or low
    breaks the highest high or lowest low over a specified lookback period.

More info:
    https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/

Call with:
    momdiv_result = bta.momentum_divergence(df, mom_length=5, bb_length=5, bb_dev=1.0, lookback=5)
    df['momentum_divergence_mom'] = momdiv_result['momentum_divergence_mom']
    df['momentum_divergence_upperb'] = momdiv_result['momentum_divergence_upperb']
    df['momentum_divergence_lowerb'] = momdiv_result['momentum_divergence_lowerb']
    df['momentum_divergence_buy'] = momdiv_result['momentum_divergence_buy']
    df['momentum_divergence_sell'] = momdiv_result['momentum_divergence_sell']
    df['momentum_divergence_coh'] = momdiv_result['momentum_divergence_coh']
    df['momentum_divergence_col'] = momdiv_result['momentum_divergence_col']

Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data.
    - mom_length (int, default=10): Lookback period for momentum calculation.
    - bb_length (int, default=20): Lookback period for Bollinger Bands calculation.
    - bb_dev (float, default=2.0): Number of standard deviations for Bollinger Bands.
    - lookback (int, default=30): Lookback period for detecting highest high and lowest low.

Returns:
    - pd.DataFrame: DataFrame with the following columns:
    - 'momentum_divergence_mom': Calculated momentum.
    - 'momentum_divergence_upperb': Upper Bollinger Band for momentum.
    - 'momentum_divergence_lowerb': Lower Bollinger Band for momentum.
    - 'momentum_divergence_buy': Boolean indicating a buy signal (momentum crossed below lower band).
    - 'momentum_divergence_sell': Boolean indicating a sell signal (momentum crossed above upper band).
    - 'momentum_divergence_coh': Boolean indicating the current high is the highest high over the lookback period.
    - 'momentum_divergence_col': Boolean indicating the current low is the lowest low over the lookback period.

## Moving Average Convergence Divergence
Name:
    Moving Average Convergence Divergence (MACD)

Description:
    MACD is a trend-following momentum indicator that shows the relationship 
    between two moving averages of a security's price.

More info:
    https://www.investopedia.com/terms/m/macd.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which MACD is to be calculated. Default is "close".
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - signal_window (int): The signal line period for EMA. Default is 9.

Call with:
    macd_result = bta.macd(df, 'close', 12, 26, 9)
    df['macd'] = macd_result['macd']
    df['macd_signal'] = macd_result['macd_signal']
    df['macd_histogram'] = macd_result['macd_histogram']

Returns:
    pd.DataFrame: DataFrame with 'macd', 'macd_signal', and 'macd_histogram' columns.

## Moving Average Convergence Divergence Leader
Name:
    MACD Leader

Description:
    The MACD Leader is a variation of the standard MACD that aims to provide an 
    earlier signal by using a different calculation method.

More info:
    https://www.investopedia.com/terms/m/macd.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - fast_length (int): Length for the fast EMA. Default is 12.
    - slow_length (int): Length for the slow EMA. Default is 26.
    - signal_length (int): Length for the signal EMA. Default is 9.

Call with:
    df['macd_leader'] = bta.macd_leader(df, 'close')['macd_leader']

Returns:
    pd.DataFrame: DataFrame with 'macd_leader' column.

## Moving Average Convergence Divergence V
Name:
    MACD-V (Volatility Normalized Momentum)

Description:
    The MACD-V is a refined version of the traditional MACD indicator, adjusted for volatility
    using the Average True Range (ATR). This normalization allows for more stable and comparable
    momentum readings across different markets and timeframes.

More info:
    https://www.investopedia.com/terms/m/macd.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which MACD-V is to be calculated. Default is "close".
    - short_window (int): The short-term period for EMA. Default is 12.
    - long_window (int): The long-term period for EMA. Default is 26.
    - atr_window (int): The period for ATR calculation. Default is 26.
    - signal_window (int): The period for the signal line EMA. Default is 9.
    - fillna (bool): If True, fill nan values. Default is False.

Call with:
    macd_v_result = bta.macd_v(df, 'close', 12, 26, 26, 9)
    df['macd_v'] = macd_v_result['macd_v']
    df['macd_v_signal'] = macd_v_result['macd_v_signal']

Returns:
    pd.DataFrame: DataFrame with 'macd_v' and 'macd_v_signal' columns.

## Percentage Price Oscillator
Name:
    Percentage Price Oscillator (PPO)

Description:
    The Percentage Price Oscillator (PPO) is a technical indicator that shows the relationship
    between two moving averages of a security's price. It is calculated by subtracting a slow
    exponential moving average (EMA) from a fast EMA and then dividing the result by the slow EMA.

More info:
    https://www.investopedia.com/terms/p/ppo.asp

Call with:
    ppo = bta.percentage_price_oscillator(df)
    df['ppo'] = ppo['ppo']
    df['ppo_signal'] = ppo['ppo_signal']
    df['ppo_hist'] = ppo['ppo_hist']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the close column.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window_slow (int): n period long-term. Default is 26.
    - window_fast (int): n period short-term. Default is 12.
    - window_sign (int): n period to signal. Default is 9.
    - fillna (bool): if True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with columns ['ppo', 'ppo_signal', 'ppo_hist'].

## Percentage Volume Oscillator
Name:
    Percentage Volume Oscillator (PVO)

Description:
    The Percentage Volume Oscillator (PVO) is a technical indicator that shows the relationship
    between two moving averages of a security's volume. It is calculated by subtracting a slow
    exponential moving average (EMA) from a fast EMA and then dividing the result by the slow EMA.

More info:
    https://www.investopedia.com/terms/p/pvo.asp
    https://www.tradingview.com/script/DdT7MmPa/

Call with:
    pvo = bta.percentage_volume_oscillator(df)
    df['pvo'] = pvo['pvo']
    df['pvo_signal'] = pvo['pvo_signal']
    df['pvo_hist'] = pvo['pvo_hist']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the volume column.
    - volume_col (str): Name of the column containing volume data. Default is 'volume'.
    - window_slow (int): n period long-term. Default is 26.
    - window_fast (int): n period short-term. Default is 12.
    - window_sign (int): n period to signal. Default is 9.
    - fillna (bool): if True, fill nan values. Default is False.


Returns:
    pd.DataFrame: DataFrame with columns ['pvo', 'pvo_signal', 'pvo_hist'].

## Pretty Good Oscillator
Name:
    Pretty Good Oscillator

Description:
    The Pretty Good Oscillator (PGO) was created by Mark Johnson to measure the distance 
    of the current close price from its N-day Simple Moving Average (SMA), expressed in 
    terms of an average true range (ATR) over a similar period.
    
    Unlike traditional oscillators that are bounded within specified ranges, the PGO's 
    values can extend beyond traditional bounds, providing signals for potentially strong 
    trending moves. Readings above +3.0 indicate potentially strong bullish price moves, 
    while readings below -3.0 indicate potentially strong bearish price moves.
    
    Johnson designed this as a breakout system for longer-term trades, going long when 
    the indicator is greater than 3.0 and short when less than -3.0.

More info:
    https://library.tradingtechnologies.com/trade/chrt-ti-pretty-good-oscillator.html

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - length (int): The period for calculations. Default is 14.

Call with:
    df['pgo'] = bta.pretty_good_oscillator(df)['pgo']

Returns:
    pd.DataFrame: DataFrame with 'pgo' column.

## Psychological Line
Name:
    Psychological Line

Description:
    The Psychological Line (PSL) is an oscillator-type indicator that calculates
    the percentage of bars that close higher over a given period. It measures the 
    buying pressure or market optimism by comparing the number of rising periods 
    to the total number of periods.
    
    When using the close-open mode, it calculates the percentage of bars where the 
    close is higher than the open. When using the close-close mode, it calculates 
    the percentage of bars where the close is higher than the previous close.
    
    Values range from 0 to 100. High values (typically above 70-80) indicate 
    potential overbought conditions, while low values (typically below 20-30) 
    indicate potential oversold conditions.

More info:
    https://www.quantshare.com/item-851-psychological-line

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column,
      and optionally the 'open' column.
    - length (int): The period for the calculation. Default is 12.
    - scalar (float): Multiplier for the result. Default is 100.
    - drift (int): The difference period for the close-close calculation. Default is 1.

Call with:
    df['psl'] = bta.psychological_line(df)['psl']

Returns:
    pd.DataFrame: DataFrame with 'psl' column.

## Qualitative Quantitative Estimation
Name:
    Qualitative Quantitative Estimation Modified (QQE Mod)

Description:
    The Qualitative Quantitative Estimation (QQE) is a technical indicator based on RSI 
    with a dynamic volatility-based trailing stop line. The modified version (QQE Mod) 
    incorporates two QQE calculations with different parameters and Bollinger Bands to 
    provide additional trading signals.

More info:
    https://www.tradingview.com/script/TpUW4muw-QQE-MOD/

Call with:
    qqe_df = bta.qqe_mod(df)
    df['qqe_line'] = qqe_df['qqe_line']
    df['hist'] = qqe_df['hist']
    df['qqe_up'] = qqe_df['qqe_up']
    df['qqe_down'] = qqe_df['qqe_down']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain a 'close' column.
    - rsi_period (int): Period for the first RSI calculation. Default is 6.
    - rsi_smoothing (int): Smoothing period for the first RSI. Default is 5.
    - qqe_factor (int): Multiplication factor for the first QQE ATR. Default is 3.
    - threshold (int): Threshold for the first QQE. Default is 3.
    - bollinger_length (int): Length for Bollinger Bands calculation. Default is 50.
    - bb_multiplier (float): Multiplier for Bollinger Bands standard deviation. Default is 0.35.
    - rsi_period2 (int): Period for the second RSI calculation. Default is 6.
    - rsi_smoothing2 (int): Smoothing period for the second RSI. Default is 5.
    - qqe_factor2 (float): Multiplication factor for the second QQE ATR. Default is 1.61.
    - threshold2 (int): Threshold for the second QQE. Default is 3.

Returns:
    pd.DataFrame: DataFrame with 'qqe_line', 'hist', 'qqe_up', and 'qqe_down' columns.

## Rate Of Change
Name:
    Rate of Change (ROC)

Description:
    The Rate of Change (ROC) is a momentum oscillator that measures the percentage
    change in price between the current price and the price n periods ago.

More info:
    https://www.investopedia.com/terms/r/rateofchange.asp

Call with:
    df['roc'] = bta.rate_of_change(df, column='close', period=21)['roc']

Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the ROC is to be applied. Default is 'close'.
    - period (int): Period for the ROC calculation. Default is 21.

Returns:
    pd.DataFrame: DataFrame with 'roc' column.

## Relative Momentum Index
Name:
    Relative Momentum Index (RMI)

Description:
    The Relative Momentum Index (RMI) is an oscillator that applies the RSI formula
    to momentum rather than price.

More info:
    https://www.tradingview.com/script/DdT7MmPa/
    https://github.com/freqtrade/technical/blob/master/technical/indicators/indicators.py#L912

Call with:
    df['rmi'] = bta.relative_momentum_index(df, length=20, mom=5)['rmi']

Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - length (int): Period for the EMA calculation. Default is 20.
    - mom (int): Momentum period. Default is 5.

Returns:
    pd.DataFrame: DataFrame with 'rmi' column.

## Relative Strength Index
Name:
    Relative Strength Index (RSI)

Description:
    RSI measures the magnitude of recent price changes to evaluate overbought or oversold
    conditions in the price of a stock or other asset. This implementation follows 
    the pandas-ta library approach, which uses EWM (Exponential Weighted Moving Average)
    with alpha=1/period to implement Wilder's RMA (Rolling Moving Average).

More info:
    https://www.investopedia.com/terms/r/rsi.asp
    https://github.com/twopirllc/pandas-ta/blob/main/pandas_ta/momentum/rsi.py

Call with:
    df['rsi'] = bta.relative_strength_index(df, column='close', period=14)['rsi']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which RSI is to be calculated. Default is "close".
    - period (int): The period over which RSI is to be calculated. Default is 14.
    - scalar (float): How much to magnify the result. Default is 100.

Returns:
    pd.DataFrame: DataFrame with 'rsi' column.

## Relative Strength Index Exponential
Name:
    Relative Strength Index Exponential (RSX)

Description:
    The Relative Strength Index Exponential (RSX) is based on the popular RSI indicator 
    and inspired by the work of Jurik Research. This enhanced version of the RSI reduces 
    noise and provides a clearer, only slightly delayed insight on momentum and velocity 
    of price movements.
    
    Like the traditional RSI, it's an oscillator that ranges from 0 to 100, with values 
    above 70 typically considered overbought and values below 30 considered oversold. 
    However, the RSX's smoother line can provide more reliable signals with less whipsaws.

More info:
    http://www.jurikres.com/catalog1/ms_rsx.htm
    https://www.prorealcode.com/prorealtime-indicators/jurik-rsx/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the RSX calculation. Default is 14.

Call with:
    df['rsx'] = bta.relative_strength_index_exponential(df)['rsx']

Returns:
    pd.DataFrame: DataFrame with 'rsx' column.

## Relative Vigor Index
Name:
    Relative Vigor Index

Description:
    The Relative Vigor Index (RVI) is a momentum oscillator that measures the 
    strength of a trend by comparing the closing price to the trading range. 
    It is based on the observation that during uptrends, prices tend to close 
    higher than they open, while during downtrends, prices tend to close lower 
    than they open.
    
    The indicator consists of two lines: the RVI line and its signal line.
    A buy signal may be generated when the RVI line crosses above the signal line,
    while a sell signal may occur when the RVI line crosses below the signal line.

More info:
    https://www.investopedia.com/terms/r/relative_vigor_index.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 
      'low', and 'close' columns.
    - length (int): The period for summing the SWMA values. Default is 14.
    - swma_length (int): The period for the Symmetrically Weighted Moving Average. 
      Default is 4.

Call with:
    result = bta.relative_vigor_index(df)
    df['rvi'] = result['rvi']
    df['rvi_signal'] = result['rvi_signal']

Returns:
    pd.DataFrame: DataFrame with 'rvi' and 'rvi_signal' columns.

## Schaff Trend Cycle
Name:
    Schaff Trend Cycle

Description:
    The Schaff Trend Cycle (STC) is an evolution of the Moving Average Convergence
    Divergence (MACD) indicator, incorporating two cascaded stochastic calculations
    with additional smoothing.
    
    Developed by Doug Schaff, this indicator attempts to improve upon the MACD by
    reducing lag and generating clearer buy/sell signals. The STC combines the 
    trend-following aspects of MACD with the cyclical properties of stochastics,
    making it potentially more responsive to price changes.

More info:
    https://school.stockcharts.com/doku.php?id=technical_indicators:schaff_trend_cycle

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - tc_length (int): SchaffTC signal-line length. Default is 10 (typically set to 
      half of the expected market cycle length).
    - fast (int): The short period for MACD calculation. Default is 12.
    - slow (int): The long period for MACD calculation. Default is 26.
    - factor (float): Smoothing factor for the final stochastic calculation. Default is 0.5.

Call with:
    result = bta.schaff_trend_cycle(df)
    df['stc'] = result['stc']  # Main indicator
    df['stc_macd'] = result['stc_macd']  # Underlying MACD line
    df['stc_stoch'] = result['stc_stoch']  # Intermediate stochastic calculation

Returns:
    pd.DataFrame: DataFrame with 'stc', 'stc_macd', and 'stc_stoch' columns.

## Smi Ergodic Indicator
Name:
    SMI Ergodic Indicator

Description:
    The SMI Ergodic Indicator is essentially the True Strength Index (TSI) developed 
    by William Blau, with the addition of a signal line. It uses double moving averages 
    of price changes over two time frames to identify momentum trends and potential 
    reversals.
    
    The indicator consists of three lines:
    - SMI: The main line, representing the smoothed ratio of momentum to absolute momentum
    - Signal: An EMA of the SMI line, used to generate potential trading signals
    - Histogram: The difference between SMI and Signal, which helps identify momentum shifts
    
    The trend is considered bullish when the SMI crosses above zero and bearish when it 
    crosses below zero. Trading signals can be generated when the SMI crosses its signal line.

More info:
    https://www.motivewave.com/studies/smi_ergodic_indicator.htm
    https://traderpedia.net/indicators/smi-ergodic-indicator/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - fast (int): The short smoothing period. Default is 5.
    - slow (int): The long smoothing period. Default is 20.
    - signal (int): The signal line period. Default is 5.
    - scalar (float): Multiplier for the result. Default is 1.0.

Call with:
    result = bta.smi_ergodic_indicator(df)
    df['smi'] = result['smi']
    df['smi_signal'] = result['smi_signal']
    df['smi_histogram'] = result['smi_histogram']

Returns:
    pd.DataFrame: DataFrame with 'smi', 'smi_signal', and 'smi_histogram' columns.

## Smoothed Rate Of Change
Name:
    Smoothed Rate of Change (SROC)

Description:
    The Smoothed Rate of Change (SROC) is a momentum oscillator that applies
    an exponential moving average (EMA) to the Rate of Change (ROC) to smooth
    out short-term fluctuations.

More info:
    https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/

Call with:
    df['sroc'] = bta.smoothed_rate_of_change(df, roclen=21, emalen=13, smooth=21)['sroc']

Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - roclen (int): Period for the ROC calculation. Default is 21.
    - emalen (int): Period for the EMA calculation. Default is 13.
    - smooth (int): Smoothing period for the ROC calculation. Default is 21.

Returns:
    pd.DataFrame: DataFrame with 'sroc' column.

## Stochastic Momentum Index
Name:
    Stochastic Momentum Index (SMI)

Description:
    The Stochastic Momentum Index (SMI) Indicator was developed by William Blau
    in 1993 and is considered to be a momentum indicator that can help identify
    trend reversal points.

More info:
    

Call with:
    df['smi'] = bta.stochastic_momentum_index(df, k_length=9, d_length=3)['smi']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - k_length (int): Period for %K. Default is 9.
    - d_length (int): Period for %D. Default is 3.

Returns:
    pd.DataFrame: DataFrame with 'smi' column populated.

## Stochastic Rsi
Name:
    Stochastic RSI (StochasticRSI)

Description:
    The Stochastic RSI is a technical momentum oscillator that combines Stochastic Oscillator
    and Relative Strength Index (RSI). It is used to identify overbought and oversold conditions
    in the market by applying the Stochastic formula to RSI values rather than price data.
    
    Originally developed by Tushar Chande and Stanley Kroll, it provides a more sensitive indicator
    than standard RSI or Stochastic oscillators alone, operating within a 0-100 range.

More info:
    https://www.investopedia.com/terms/s/stochrsi.asp

Calculation:
    - Calculate RSI for the given period (length_rsi) using Wilder's smoothing method
    - Find lowest and highest RSI values over the stochastic period (length_stoch)
    - Apply the Stochastic formula to RSI: 100 * (RSI - MinRSI) / (MaxRSI - MinRSI)
    - Smooth the %K line using SMA with period (smooth_k)
    - Smooth the %D line using SMA with period (smooth_d) on the %K line

Parameters:
    - df (pd.DataFrame): DataFrame containing the data with a 'close' column.
    - length_rsi (int): Period for the RSI calculation. Default is 14.
    - length_stoch (int): Period for the Stochastic calculation. Default is 14.
    - smooth_k (int): Smoothing period for %K line. Default is 3.
    - smooth_d (int): Smoothing period for %D line. Default is 3.
    - mamode (str): Moving average type for smoothing ('sma' or 'ema'). Default is 'sma'.

Call with:
    stoch_rsi = bta.stochastic_rsi(df, length_rsi=14, length_stoch=14, smooth_k=3, smooth_d=3)
    df['stoch_rsi_k'] = stoch_rsi['stoch_rsi_k']
    df["stoch_rsi_d"] = stoch_rsi["stoch_rsi_d"]

Returns:
    pd.DataFrame: DataFrame with 'stoch_rsi_k' and 'stoch_rsi_d' columns.

## Stochastics Oscillator
Name:
    Stochastic Oscillator, Stochastic Signal, and Histogram Combined.

Description:
    The Stochastic Oscillator is a momentum indicator comparing a particular
    closing price of a security to a range of its prices over a certain period of time.

Call with:
    stoch = bta.stochastics_oscillator(df, 'high', 'low', 'close', 14, 3)
    df['stoch'] = stoch['stoch']
    df['stoch_signal'] = stoch['stoch_signal']
    df['stoch_hist'] = stoch['stoch_hist']

Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - high_col (str): Column name for 'High' prices. Default is 'high'.
    - low_col (str): Column name for 'Low' prices. Default is 'low'.
    - close_col (str): Column name for 'Close' prices. Default is 'close'.
    - window (int): Lookback period for stochastic calculation. Default is 14.
    - smooth_window (int): Lookback period for signal calculation. Default is 3.
    - fillna (bool): If True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with 'stoch', 'stoch_signal', and 'stoch_hist' columns.

## Td Sequential
Name:
    TD Sequential

Description:
    Tom DeMark's Sequential indicator (TD Sequential) is a technical analysis tool 
    designed to identify potential price exhaustion points and trend reversals. 
    It counts specific price patterns to determine when a trend might be overextended.
    
    The indicator consists of two components:
    - TD Setup: A sequence of 9 consecutive closes higher (for sell setup) or 
      lower (for buy setup) than the close 4 bars earlier.
    - TD Countdown: Begins after a completed setup and identifies potential 
      exhaustion points through a 13-bar countdown process.
    
    This implementation displays the count of consecutive price bars meeting 
    the criteria for both bullish (td_up) and bearish (td_down) setups.

More info:
    https://www.tradingview.com/support/solutions/43000588817-td-sequential/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - asint (bool): If True, fills NaN values with 0 and converts to integers. Default is False.
    - show_all (bool): If True, shows all counts; if False, only shows counts between 6-9. Default is True.

Call with:
    result = bta.td_sequential(df)
    df['td_up'] = result['td_up']
    df['td_down'] = result['td_down']

Returns:
    pd.DataFrame: DataFrame with 'td_up' and 'td_down' columns.

## Triple Exponential Average
Name:
    Triple Exponential Average (TRIX)

Description:
    TRIX is a momentum oscillator developed by Jack Hutson in the early 1980s. 
    It calculates the rate of change of a triple exponentially smoothed moving 
    average, filtering out minor price movements to identify the major trend direction.
    
    The indicator oscillates around a zero line. Positive values suggest bullish 
    momentum, while negative values indicate bearish momentum. Trading signals 
    can be generated when TRIX crosses above or below the zero line, or when it 
    crosses its signal line.
    
    The triple smoothing helps to eliminate noise and identify the underlying trend 
    more clearly than simpler rate of change indicators.

More info:
    https://www.investopedia.com/terms/t/trix.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): The period for the exponential moving averages. Default is 30.
    - signal (int): The period for the signal line. Default is 9.
    - scalar (float): Multiplier to scale the values. Default is 100.
    - drift (int): The difference period for rate of change calculation. Default is 1.

Call with:
    result = bta.triple_exponential_average(df)
    df['trix'] = result['trix']
    df['trix_signal'] = result['trix_signal']

Returns:
    pd.DataFrame: DataFrame with 'trix' and 'trix_signal' columns.

## True Strength Index
Name:
    True Strength Index (TSI)

Description:
    The True Strength Index (TSI) shows both trend direction and overbought/oversold conditions.

Call with:
    df['tsi'] = bta.true_strength_index(df, 'close', 25, 13)['tsi']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the close column.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window_slow (int): High period. Default is 25.
    - window_fast (int): Low period. Default is 13.
    - fillna (bool): If True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with 'tsi' column.

## Ttm Squeeze
Name:
    TTM Squeeze

Description:
    The TTM (Trade the Markets) Squeeze indicator was developed by John Carter and 
    is discussed in his book "Mastering the Trade." It identifies periods of market 
    consolidation and expansion by comparing Bollinger Bands® and Keltner Channels.
    
    When Bollinger Bands are inside Keltner Channels, it indicates a "squeeze" 
    condition (low volatility) that often precedes significant price movements. 
    When Bollinger Bands expand outside Keltner Channels, it indicates the 
    "squeeze" has fired, signaling potential trading opportunities.
    
    This implementation offers both the standard version and a "Pro" version with 
    additional squeeze levels (wide, normal, and narrow). It also includes a momentum 
    component that helps identify the direction and strength of price movement when 
    the squeeze fires.

More info:
    https://www.tradingview.com/support/solutions/43000501971-ttm-squeeze/
    https://usethinkscript.com/threads/john-carters-squeeze-pro-indicator-for-thinkorswim-free.4021/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      and 'close' columns.
    - bb_length (int): The period for Bollinger Bands calculation. Default is 20.
    - bb_std (float): Number of standard deviations for Bollinger Bands. Default is 2.0.
    - kc_length (int): The period for Keltner Channels calculation. Default is 20.
    - kc_scalar (float): Multiplier for the Keltner Channels. Default is 1.5.
    - mom_length (int): The period for momentum calculation. Default is 12.
    - mom_smooth (int): The period for smoothing momentum. Default is 6.
    - use_tr (bool): If True, use True Range for Keltner Channels; otherwise, use High-Low range. Default is True.
    - mamode (str): Moving average type, either 'sma' or 'ema'. Default is 'sma'.
    - use_pro (bool): If True, use the Pro version with multiple squeeze levels. Default is False.
    - detailed (bool): If True, return additional data for visualization. Default is False.
    - kc_scalar_wide (float): Multiplier for wide Keltner Channels (Pro version only). Default is 2.0.
    - kc_scalar_narrow (float): Multiplier for narrow Keltner Channels (Pro version only). Default is 1.0.

Call with:
    # Basic usage:
    result = bta.ttm_squeeze(df)
    df['squeeze'] = result['squeeze']
    df['squeeze_on'] = result['squeeze_on']
    df['squeeze_off'] = result['squeeze_off']
    
    # Pro version:
    result = bta.ttm_squeeze(df, use_pro=True)
    df['squeeze'] = result['squeeze']
    df['squeeze_on_wide'] = result['squeeze_on_wide']
    df['squeeze_on_normal'] = result['squeeze_on_normal']
    df['squeeze_on_narrow'] = result['squeeze_on_narrow']

Returns:
    pd.DataFrame: DataFrame with various squeeze-related columns.

## Ultimate Oscillator
Name:
    Ultimate Oscillator

Description:
    The Ultimate Oscillator combines short-term, intermediate-term, and long-term
    price action into one oscillator.

Call with:
    df['uo'] = bta.ultimate_oscillator(df, 'high', 'low', 'close', 7, 14, 28)['uo']

Parameters:
    - df (pandas.DataFrame): DataFrame containing the data.
    - high_col (str): Name of the column containing high price data. Default is 'high'.
    - low_col (str): Name of the column containing low price data. Default is 'low'.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - window1 (int): Short period. Default is 7.
    - window2 (int): Medium period. Default is 14.
    - window3 (int): Long period. Default is 28.
    - weight1 (float): Weight of short BP average for UO. Default is 4.0.
    - weight2 (float): Weight of medium BP average for UO. Default is 2.0.
    - weight3 (float): Weight of long BP average for UO. Default is 1.0.
    - fillna (bool): If True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with 'uo' column.

## Waddah Attar Explosion
Name:
    Waddah Attar Explosion Indicator

Description:
    The Waddah Attar Explosion indicator is used to identify potential breakout
    opportunities by combining the MACD and Bollinger Bands.

    Inspired by: https://www.tradingview.com/script/iu3kKWDI-Waddah-Attar-Explosion-LazyBear/

Call with:
    wae = bta.waddah_attar_explosion(df)
    df['trend_up'] = wae['trend_up']
    df['trend_down'] = wae['trend_down']
    df['explosion_line'] = wae['explosion_line']
    df['dead_zone_line'] = wae['dead_zone_line']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - dead_zone (int): Dead zone factor for the indicator. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

Returns:
    pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.

## Waddah Attar Explosion Atr
Name:
    Waddah Attar Explosion ATR

Description:
    The Waddah Attar Explosion indicator is used to identify potential breakout
    opportunities by combining the MACD and Bollinger Bands. The dead zone line
    is based on ATR in this indicator.

    Inspired by: https://www.tradingview.com/script/d9IjcYyS-Waddah-Attar-Explosion-V2-SHK/

Call with:
    wae = bta.waddah_attar_explosion_atr(df)
    df['trend_up'] = wae['trend_up']
    df['trend_down'] = wae['trend_down']
    df['explosion_line'] = wae['explosion_line']
    df['dead_zone_line'] = wae['dead_zone_line']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

Returns:
    pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.

## Wave Trend
Name:
    WaveTrend

Description:
    The WaveTrend is used to identify overbought and oversold conditions in the market.

Inspired by:
    https://www.tradingview.com/script/jFQn4jYZ-WaveTrend-with-Crosses-LazyBear/

Call with:
    wt = bta.wave_trend(df, chlen=10, avg=21, smalen=4)
    df['wt1'] = wt['wt1']
    df['wt2'] = wt['wt2']

Parameters:
    - df (pd.DataFrame): DataFrame containing the data.
    - chlen (int): Channel length for the EMA calculation. Default is 10.
    - avg (int): Average period for the EMA calculation. Default is 21.
    - smalen (int): Period for the SMA calculation. Default is 4.

Returns:
    pd.DataFrame: DataFrame with 'wt1' and 'wt2' columns.

## Wave Trend Oscillator
Name:
    WaveTrend Oscillator

Description:
    The WaveTrend Oscillator is used to identify overbought and oversold conditions
    in the market.

    Inspired by:

Call with:
    df['wto'] = bta.wave_trend_oscillator(df, 'close')['wavetrend']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - n1 (int): Length for the first EMA. Default is 8.
    - n2 (int): Length for the second EMA. Default is 12.

Returns:
    pd.DataFrame: DataFrame with 'wavetrend' column.

## Williams R
Name:
    Williams %R

Description:
    The Williams %R is a momentum indicator that measures overbought and oversold levels.

More info:
    https://www.tradingview.com/support/solutions/43000501985/
    https://www.tradingview.com/script/REGZq58T-Williams-R/

Call with:
    df['williams_r'] = bta.williams_r(df, 'high', 'low', 'close', 14)['williams_r']

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the high, low, and close columns.
    - high_col (str): Name of the column containing high price data. Default is 'high'.
    - low_col (str): Name of the column containing low price data. Default is 'low'.
    - close_col (str): Name of the column containing close price data. Default is 'close'.
    - lbp (int): Lookback period. Default is 14.
    - fillna (bool): If True, fill nan values. Default is False.

Returns:
    pd.DataFrame: DataFrame with 'williams_r' column.

# Performance

# Statistics

# Trend

## Alligator Bands
Name:
    Bill Williams Alligator Indicator

Description:
    The Alligator Indicator is used to identify trends and their direction in the market.
    It consists of three smoothed moving averages known as the Jaw, Teeth, and Lips.

More info:
    https://www.investopedia.com/terms/a/alligator.asp

Parameters:
    - df (pandas.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the Alligator is to be applied. Default is 'close'.
    - jaw_period (int): Period for the Alligator's Jaw (blue line). Default is 13.
    - teeth_period (int): Period for the Alligator's Teeth (red line). Default is 8.
    - lips_period (int): Period for the Alligator's Lips (green line). Default is 5.
    - jaw_shift (int): Number of periods to shift the Jaw line into the future. Default is 8.
    - teeth_shift (int): Number of periods to shift the Teeth line into the future. Default is 5.
    - lips_shift (int): Number of periods to shift the Lips line into the future. Default is 3.

Call with:
    alligator_result = bta.alligator_bands(df, 'close', 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
    df['jaw'] = alligator_result['jaw']
    df['teeth'] = alligator_result['teeth']
    df['lips'] = alligator_result['lips']

Returns:
    pd.DataFrame: DataFrame with 'jaw', 'teeth', and 'lips' columns.

## Archer Moving Averages Trends
Name:
    Archer Moving Averages Trends (AMAT)

Description:
    The Archer Moving Averages Trends indicator identifies potential trend conditions
    by analyzing the relationship between fast and slow moving averages.
    
    The indicator generates two signals:
    - Long Run: Identifies potential bullish trends when both fast and slow moving
      averages are increasing over the lookback period, and the fast MA is above the slow MA.
    - Short Run: Identifies potential bearish trends when both fast and slow moving
      averages are decreasing over the lookback period, and the fast MA is below the slow MA.
    
    This indicator can be useful for trend identification, filtering trading signals,
    or as a component in more complex trading strategies.

More info:
    N/A (Original implementation by Kevin Johnson for Pandas TA)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - fast_length (int): The period for the fast moving average. Default is 8.
    - slow_length (int): The period for the slow moving average. Default is 21.
    - lookback (int): The period to check for consistent movement in the MAs. Default is 2.
    - ma_type (str): The type of moving average to use ('SMA', 'EMA', 'WMA'). Default is 'EMA'.
    - column (str): Name of the column to use for calculations. Default is 'close'.

Call with:
    result = bta.archer_moving_averages_trends(df, fast_length=8, slow_length=21, ma_type='EMA')
    df['amat_long'] = result['amat_long']  # Long trend signals (1 or 0)
    df['amat_short'] = result['amat_short']  # Short trend signals (1 or 0)

Returns:
    pd.DataFrame: DataFrame with 'amat_long' and 'amat_short' columns containing the indicator values.

## Arnaud Legoux Moving Average
Name:
    Arnaud Legoux Moving Average (ALMA)

Description:
    The Arnaud Legoux Moving Average (ALMA) was developed by Arnaud Legoux and Dimitrios Kouzis-Loukas.
    It uses the curve of the Normal (Gaussian) distribution to create a moving average with reduced lag
    while maintaining smoothness to filter out market noise.
    
    ALMA applies a Gaussian distribution curve across the moving average period, which can be shifted
    (using distribution_offset) to control the balance between smoothness and responsiveness. The sigma
    parameter controls the shape of the curve and the overall smoothness.
    
    This moving average excels at reducing the lag typically associated with traditional moving averages
    while still providing effective noise reduction.

More info:
    https://medium.com/analytics-vidhya/arnaud-legoux-moving-average-alma-7e1f35fc0b8e
    https://www.prorealcode.com/prorealtime-indicators/alma-arnaud-legoux-moving-average/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the ALMA calculation. Default is 10.
    - sigma (float): Controls the smoothness of the curve. Higher values = smoother. Default is 6.0.
    - distribution_offset (float): Controls the shape symmetry of the curve. 
      Range is 0-1, where 0 gives more smoothing and 1 provides more responsiveness. Default is 0.85.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.arnaud_legoux_moving_average(df)
    df['alma'] = result['alma']

Returns:
    pd.DataFrame: DataFrame with 'alma' column.

## Aroon
Name:
    Aroon & Aroon Oscillator (AROON)

Description:
    The Aroon indicator is a technical indicator used to identify trend changes in the 
    price of an asset, as well as the strength of that trend. It consists of two lines: 
    Aroon Up and Aroon Down.
    
    Aroon Up measures the time since the highest price within the look-back period, 
    while Aroon Down measures the time since the lowest price within that period. 
    The values are normalized to a range between 0 and 100.
    
    The Aroon Oscillator is calculated as the difference between Aroon Up and Aroon Down, 
    resulting in a single line that oscillates between -100 and 100.
    
    Typical interpretations:
    - Aroon Up > 70 and Aroon Down < 30: Strong uptrend
    - Aroon Down > 70 and Aroon Up < 30: Strong downtrend
    - Both Aroon Up and Aroon Down < 50: Indicates consolidation
    - Aroon Oscillator > 50: Uptrend
    - Aroon Oscillator < -50: Downtrend
    - Crossover of Aroon Up and Aroon Down: Potential trend reversal

More info:
    https://www.investopedia.com/terms/a/aroon.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): Look-back period for the calculation. Default is 14.
    - scalar (float): Scaling factor for the indicators. Default is 100.

Call with:
    result = bta.aroon(df)
    df['aroon_up'] = result['aroon_up']
    df['aroon_down'] = result['aroon_down']
    df['aroon_osc'] = result['aroon_osc']

Returns:
    pd.DataFrame: DataFrame with 'aroon_up', 'aroon_down', and 'aroon_osc' columns.

## Average Directional Index
Name:
    Average Directional Movement Index (ADX)

Description:
    The Average Directional Index (ADX) is a technical analysis indicator used to 
    quantify trend strength. It was developed by J. Welles Wilder and is part of 
    the Directional Movement System.
    
    The ADX is non-directional; it registers trend strength whether price is trending 
    up or down. The indicator typically ranges from 0 to 100, with readings above 25 
    indicating a strong trend and readings below 20 indicating a weak or non-trending 
    market.
    
    The ADX is calculated using the Positive Directional Indicator (+DI) and Negative 
    Directional Indicator (-DI), which measure upward and downward price movement 
    respectively. These indicators are included in the output of this function as 
    'dmp' and 'dmn'.
    
    Typical interpretation:
    - ADX > 25: Strong trend (direction determined by +DI and -DI)
    - ADX < 20: Weak or absent trend
    - When +DI crosses above -DI: Potential bullish signal
    - When -DI crosses above +DI: Potential bearish signal

More info:
    https://www.investopedia.com/terms/a/adx.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): Period for calculating directional movement. Default is 14.
    - signal_length (int): Smoothing period for ADX calculation. Default is equal to length.
    - scalar (float): Scaling factor for the indicators. Default is 100.
    - drift (int): The difference period for directional movement. Default is 1.

Call with:
    result = bta.average_directional_index(df)
    df['adx'] = result['adx']
    df['plus_di'] = result['dmp']
    df['minus_di'] = result['dmn']

Returns:
    pd.DataFrame: DataFrame with 'adx', 'dmp' (plus DI), and 'dmn' (minus DI) columns.

## Bollinger Trend
Name:
    Bollinger Trend Indicator

Description:
    The Bollinger Trend Indicator calculates the trend based on the difference
    between short and long Bollinger Bands.

More info:
    https://www.tradingview.com/script/UtMK7hNw-Bollinger-Trend/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is 'close'.
    - short_length (int): The period for the short Bollinger Bands. Default is 20.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - std_dev (float): The standard deviation multiplier for the Bollinger Bands. Default is 2.0.

Call with:
    df['bbtrend'] = bta.bollinger_trend(df, 'close', 20, 50, 2.0)['bbtrend']

Returns:
    pd.DataFrame: DataFrame with 'bbtrend' column.

## Bollinger Trend Fast With Ma
Name:
    Bollinger Trend Indicator with Selectable Moving Average

Description:
    This function calculates a more responsive Bollinger Trend (BBTrend) and applies a
    selected moving average to the BBTrend.

More info:
    https://www.tradingview.com/script/UtMK7hNw-Bollinger-Trend/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is 'close'.
    - short_length (int): The period for the short Bollinger Bands. Default is 10.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - short_stddev (float): The standard deviation multiplier for the short Bollinger Bands. Default is 1.0.
    - long_stddev (float): The standard deviation multiplier for the long Bollinger Bands. Default is 2.0.
    - ma_type (str): The type of moving average to use ('SMA', 'EMA', 'LSMA', 'HMA', 'WMA'). Default is 'SMA'.
    - ma_length (int): The period for the moving average. Default is 14.

Call with:
    result = bta.bollinger_trend_fast_with_ma(df, 'close', 10, 50, 1.0, 2.0, 'SMA', 14)
    df['bollinger_trend_fast'] = result['bbtrend']
    df['bollinger_trend_fast_ma'] = result['bbtrend_ma']

Returns:
    pd.DataFrame: DataFrame with 'bbtrend' and 'bbtrend_ma' columns.

## Breakouts
Name:
    S/R Breakouts and Retests

Description:
    Makes it easy to work with Support and Resistance.
    Find Retests, Breakouts, and the next levels.

More info:
    https://www.tradingview.com/script/iHKi8BGJ-S-R-Breakouts-and-Retests/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): Lookback period.

Call with:
    breakout = bta.breakouts(df, length=20)
    df['support_level'] = breakout['support_level']
    df['resistance_level'] = breakout['resistance_level']
    df['support_breakout'] = breakout['support_breakout']
    df['resistance_breakout'] = breakout['resistance_breakout']
    df['support_retest'] = breakout['support_retest']
    df['potential_support_retest'] = breakout['potential_support_retest']
    df['resistance_retest'] = breakout['resistance_retest']
    df['potential_resistance_retest'] = breakout['potential_resistance_retest']

Returns:
    pd.DataFrame: DataFrame with event columns populated.

## Chande Kroll Stop
Name:
    Chande Kroll Stop (CKSP)

Description:
    The Chande Kroll Stop was developed by Tushar Chande and Stanley Kroll in their book
    "The New Technical Trader". It is a trend-following indicator that creates dynamic 
    stop-loss levels based on market volatility measured by the Average True Range (ATR).
    
    The indicator generates two lines:
    - Long Stop: Used as a trailing stop for long positions
    - Short Stop: Used as a trailing stop for short positions
    
    The calculation can be done in two modes:
    - TradingView mode: Uses RMA for ATR and defaults to (10, 1, 9) for parameters
    - Book mode: Uses SMA for ATR and defaults to (10, 3, 20) for parameters
    
    Traditional usage involves:
    - Selling when price closes below the Long Stop
    - Buying when price closes above the Short Stop
    - Using the stops as trailing stop-loss levels to protect profits

More info:
    https://www.multicharts.com/discussion/viewtopic.php?t=48914
    "The New Technical Trader", Wiley 1st ed. ISBN 9780471597803, page 95

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - atr_length (int): Period for ATR and first stop calculation. Default is 10.
    - atr_scalar (float): ATR multiplier for stop calculation. Default is 1.0 in TradingView mode, 3.0 in book mode.
    - stop_length (int): Length for the final stop calculation. Default is 9 in TradingView mode, 20 in book mode.
    - trading_view_mode (bool): If True, uses TradingView implementation (RMA for ATR), otherwise uses book implementation (SMA for ATR). Default is True.

Call with:
    result = bta.chande_kroll_stop(df)
    df['long_stop'] = result['long_stop']
    df['short_stop'] = result['short_stop']

Returns:
    pd.DataFrame: DataFrame with 'long_stop' and 'short_stop' columns.

## Choppiness Index
Name:
    Choppiness Index (CHOP)

Description:
    The Choppiness Index was created by Australian commodity trader E.W. Dreiss and is 
    designed to determine if the market is choppy (trading sideways) or not choppy 
    (trading within a trend in either direction).
    
    The indicator oscillates between 0 and 100, where:
    - Values closer to 100 indicate a choppy, sideways market with no clear trend
    - Values closer to 0 indicate a trending market (either up or down)
    
    This indicator is useful for determining whether to use trend-following strategies 
    or range-bound strategies. It can also help identify potential breakouts when transitioning 
    from a choppy to a trending market.
    
    Note that this is a non-directional indicator; it does not indicate whether the trend is 
    up or down, only the degree to which the market is trending or not trending.

More info:
    https://www.tradingview.com/scripts/choppinessindex/
    https://www.motivewave.com/studies/choppiness_index.htm

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for the Choppiness Index calculation. Default is 14.
    - atr_length (int): The period for the ATR calculation. Default is 1.
    - use_natural_log (bool): If True, natural logarithm (ln) is used instead of log base 10. Default is False.
    - scalar (float): Scaling factor for the indicator. Default is 100.

Call with:
    result = bta.choppiness_index(df)
    df['chop'] = result['chop']

Returns:
    pd.DataFrame: DataFrame with 'chop' column.

## Cross Signals
Name:
    Cross Signals

Description:
    Cross Signals generates trading signals based on a signal series crossing specific levels.
    It returns the trend, trades, entries, and exits as a set of columns that can be used 
    for analysis or trading signal generation.
    
    The indicator has two primary modes controlled by the 'above' parameter:
    - When above=True (default): Generates entry signals when the signal crosses above level_a,
      and exit signals when it crosses below level_b.
    - When above=False: Generates entry signals when the signal crosses below level_a,
      and exit signals when it crosses above level_b.
    
    This is particularly useful for oscillators like RSI, Stochastic, or Z-Score where
    crossing specific thresholds can indicate potential trade opportunities.
    
    The 'long' parameter determines whether to interpret the signals as long positions (true)
    or short positions (false).

More info:
    N/A (Original implementation by Kevin Johnson for Pandas TA)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified signal column.
    - signal_column (str): Name of the column containing the signal series to evaluate.
    - level_a (float): The first threshold level for generating entry signals.
    - level_b (float): The second threshold level for generating exit signals.
    - above (bool): Determines the signal crossing mode. Default is True.
    - long (bool): Whether to interpret signals as long positions. When False,
      interprets signals as short positions. Default is True.
    - as_bool (bool): If True, converts the trends, entries, and exits to boolean values.
      Default is False.
    - trade_offset (int): Value used to shift the trade entries/exits. Use 1 for backtesting
      and 0 for live trading. Default is 0.

Call with:
    # Example for RSI crossing above 30 (entry) and below 70 (exit)
    result = bta.cross_signals(df, signal_column='rsi', level_a=30, level_b=70, above=True)
    df['cross_trend'] = result['cross_trend']
    df['cross_entries'] = result['cross_entries']
    df['cross_exits'] = result['cross_exits']
    df['cross_long'] = result['cross_long']
    df['cross_short'] = result['cross_short']

Returns:
    pd.DataFrame: DataFrame with 'cross_trend', 'cross_trades', 'cross_entries', 'cross_exits',
    'cross_long', and 'cross_short' columns.

## Decay
Name:
    Decay Indicator

Description:
    The Decay indicator creates a curve that gradually decays moving forward from 
    prior signals, like crosses or other events. This can be useful for trailing 
    signals or creating trailing stops that gradually decrease over time.
    
    The indicator supports two decay modes:
    - Linear: Applies a constant rate of decay based on 1/length
    - Exponential: Applies an exponential decay based on exp(-length)
    
    In both cases, the indicator ensures the decay value never falls below 0 and 
    resets when a new price exceeds the decaying value, creating a sawtooth-like pattern.
    
    This can be particularly useful for:
    - Creating trailing stops that decay over time
    - Generating fading signals after indicator crosses
    - Implementing time-based exits from positions

More info:
    https://tulipindicators.org/decay

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for decay calculation. Higher values result in slower decay. Default is 5.
    - mode (str): Decay mode, either 'linear' or 'exponential' (can also use 'exp'). Default is 'linear'.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Linear decay
    result = bta.decay(df)
    df['decay_lin'] = result['decay_lin']
    
    # Exponential decay
    result = bta.decay(df, mode='exp')
    df['decay_exp'] = result['decay_exp']

Returns:
    pd.DataFrame: DataFrame with 'decay_lin' or 'decay_exp' column depending on the mode.

## Decreasing
Name:
    Decreasing Indicator

Description:
    The Decreasing indicator identifies whether a series is decreasing over a specified period.
    It returns True (or 1 if as_int=True) if the series is decreasing, False (or 0) otherwise.
    
    When strict=True, it checks if the series is continuously decreasing over each period
    within the specified length. When strict=False (default), it simply checks if the
    value has decreased over the entire length period.
    
    The percent parameter allows for a percentage-based adjustment to the series, which
    can be useful for filtering out minor fluctuations.
    
    This indicator can be useful for trend identification, filtering trading signals,
    or as a component in more complex trading strategies.

More info:
    N/A (Original implementation by Kevin Johnson for Pandas TA)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The period over which to check for decreasing values. Default is 1.
    - strict (bool): If True, checks if the series is continuously decreasing over each
      period within the length. Default is False.
    - as_int (bool): If True, returns 1 for decreasing, 0 otherwise. If False, returns
      boolean values. Default is True.
    - percent (float): Percentage adjustment to apply to the series. If specified, compares
      against (1 - 0.01 * percent) * series. Default is None.
    - drift (int): The difference period for comparison. Default is 1.
    - column (str): Name of the column to check. Default is 'close'.

Call with:
    result = bta.decreasing(df, length=5, strict=True)
    df['decreasing'] = result['decreasing']

Returns:
    pd.DataFrame: DataFrame with 'decreasing' column containing the indicator values.

## Detrended Price Oscillator
Name:
    Detrended Price Oscillator (DPO)

Description:
    The Detrended Price Oscillator (DPO) is an indicator designed to remove trend from 
    price and make it easier to identify cycles. Unlike other oscillators, the DPO is 
    not a momentum indicator. It instead highlights cycles by removing the underlying 
    trend from the price data.
    
    The DPO accomplishes this by comparing the current price (or a displaced price) to 
    a moving average from a displaced period in the past. By doing this, it attempts to 
    eliminate the trend component from the price action, leaving the cyclical components.
    
    The indicator can be calculated in two modes:
    - Centered (default): Uses future data for alignment, suitable for historical analysis
    - Non-centered: Uses only historical data, suitable for real-time trading
    
    When the DPO is above zero, it indicates that price is above the displaced moving average.
    When it's below zero, price is below the displaced moving average.

More info:
    https://www.tradingview.com/scripts/detrendedpriceoscillator/
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/dpo
    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:detrended_price_osci

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the moving average calculation. Default is 20.
    - centered (bool): Whether to center the calculation (shifts result for better alignment). 
                      True is for historical analysis, False for real-time. Default is True.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.detrended_price_oscillator(df)
    df['dpo'] = result['dpo']

Returns:
    pd.DataFrame: DataFrame with 'dpo' column.

## Double Exponential Moving Average
Name:
    Double Exponential Moving Average (DEMA)

Description:
    The Double Exponential Moving Average attempts to create a smoother average with less
    lag than the standard Exponential Moving Average (EMA). It was developed by Patrick Mulloy
    and first published in the February 1994 issue of "Technical Analysis of Stocks & Commodities" magazine.
    
    The DEMA uses multiple EMA calculations to reduce the lag of traditional moving averages.
    By giving more weight to recent prices and reducing the lag associated with traditional
    moving averages, the DEMA can be more responsive to price changes.

More info:
    https://www.tradingview.com/support/solutions/43000502589-double-exponential-moving-average-dema/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the DEMA calculation. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.double_exponential_moving_average(df)
    df['dema'] = result['dema']

Returns:
    pd.DataFrame: DataFrame with 'dema' column.

## Exponential Moving Average
Name:
    Exponential Moving Average (EMA)

Description:
    The Exponential Moving Average gives more weight to recent prices and thus reacts
    more quickly to price changes than the Simple Moving Average.

More info:
    https://www.investopedia.com/terms/e/ema.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EMA is to be calculated. Default is 'close'.
    - period (int): The period over which EMA is to be calculated. Default is 21.

Call with:
    df['ema'] = bta.exponential_moving_average(df, "close", 21)['ema']

Returns:
    pd.DataFrame: DataFrame with 'ema' column, where first `period-1` values are NaN.

## Fractal Weighted Moving Average
Name:
    Fractal Weighted Moving Average (FWMA)

Description:
    The Fractal Weighted Moving Average is a variation of the Weighted Moving Average
    where the weights are based on the Fibonacci sequence. The Fibonacci sequence is
    a series of numbers where each number is the sum of the two preceding ones, usually
    starting with 1 and 1. 
    
    By using the Fibonacci sequence as weights, more emphasis is placed on certain
    periods based on the natural mathematical progression found throughout nature.
    This creates a moving average that may better align with natural market cycles.

More info:
    https://www.investopedia.com/terms/f/fibonacci-retracement.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the FWMA calculation. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.fractal_weighted_moving_average(df)
    df['fwma'] = result['fwma']

Returns:
    pd.DataFrame: DataFrame with 'fwma' column.

## Gaussian Channel
Name:
    Gaussian Channel

Description:
    The Gaussian Channel is an experimental indicator utilizing the Ehlers Gaussian Filter 
    technique combined with lag reduction techniques and true range to analyze trend activity.
    Gaussian filters are exponential moving averages applied multiple times.
    
    The indicator calculates beta and alpha based on the sampling period and number of poles 
    specified. The data can be given a truncation option for reduced lag. Then the alpha 
    and source values are used to calculate the filter and filtered true range of the dataset.
    Filtered true range with a specified multiplier is then added to and subtracted from the 
    filter, generating a channel.
    
    A one pole filter with an N pole alpha can be averaged with the filter to generate a 
    faster filter (Fast Response Mode).

More info:
    Original Pine Script by DonovanWall
    Based on John Ehlers' Gaussian Filter technique
    https://www.tradingview.com/script/NaN/ (Pine Script reference)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
      For 'ohlc4' source, 'open' column is also required.
    - source (str): Price source to use. Options: 'hlc3', 'close', 'open', 'hl2', 'ohlc4', 
      or any column name. Default is 'hlc3'.
    - poles (int): Number of poles for the Gaussian filter (1-9). Higher values create smoother 
      output with more lag. Default is 4.
    - period (int): Sampling period for the filter. Larger values result in smoother outputs 
      with increased lag. Default is 144.
    - multiplier (float): Multiplier for the filtered true range to create channel bands. 
      Default is 1.414.
    - reduced_lag (bool): Enable reduced lag mode for faster response. Default is False.
    - fast_response (bool): Enable fast response mode by averaging N-pole and 1-pole filters. 
      Default is False.

Call with:
    gc_result = bta.gaussian_channel(df, source='hlc3', poles=4, period=144, multiplier=1.414)
    df['gc_middle'] = gc_result['gc_middle']
    df['gc_upper'] = gc_result['gc_upper']
    df['gc_lower'] = gc_result['gc_lower']
    df['gc_direction'] = gc_result['gc_direction']
    df['gc_bar_signal'] = gc_result['gc_bar_signal']

Returns:
    pd.DataFrame: DataFrame with the following columns:
        - 'gc_middle': The main Gaussian filter line (centerline/middle of channel)
        - 'gc_upper': Upper channel band (middle + filtered_tr * multiplier)
        - 'gc_lower': Lower channel band (middle - filtered_tr * multiplier)
        - 'gc_direction': Filter direction (1=up, -1=down, 0=neutral)
        - 'gc_bar_signal': Bar color signal based on price position relative to filter and bands:
            2: Strong bullish (price rising above upper band)
            1: Bullish (price rising above filter, within channel)
            3: Weak bullish (price above filter but declining)
            -2: Strong bearish (price falling below lower band)
            -1: Bearish (price falling below filter, within channel)
            -3: Weak bearish (price below filter but rising)
            0: Neutral/choppy (sideways movement)

## Holt Winters Moving Average
Name:
    Holt-Winters Moving Average (HWMA)

Description:
    The Holt-Winters Moving Average is a triple exponential smoothing method that accounts
    for trend and seasonality in time series data. It uses three parameters (alpha, beta, gamma)
    to control the smoothing of the level, trend, and seasonality components.
    
    This implementation is based on the Holt-Winters method but simplified for use as a
    moving average indicator in technical analysis. It's particularly useful for data that
    exhibits both trend and cyclical patterns.

More info:
    https://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - alpha (float): Smoothing parameter for the level component (0 < alpha < 1). Default is 0.2.
    - beta (float): Smoothing parameter for the trend component (0 < beta < 1). Default is 0.1.
    - gamma (float): Smoothing parameter for the seasonality component (0 < gamma < 1). Default is 0.1.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.holt_winters_moving_average(df)
    df['hwma'] = result['hwma']

Returns:
    pd.DataFrame: DataFrame with 'hwma' column.

## Hull Moving Average
Name:
    Hull Moving Average (HMA)

Description:
    The Hull Moving Average (HMA) is an improved moving average that is responsive and
    has minimal lag. It involves the combination of WMA (Weighted Moving Average) with
    different periods.

More info:
    https://alanhull.com/hull-moving-average

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which HMA is to be calculated. Default is 'close'.
    - period (int): The period over which HMA is to be calculated. Default is 9.

Call with:
    df['hma'] = bta.hull_moving_average(df, 'close', 9)['hma']

Returns:
    pd.DataFrame: DataFrame with 'hma' column.

## Increasing
Name:
    Increasing Indicator

Description:
    The Increasing indicator identifies when a series is increasing over a specified period.
    It returns True (or 1) if the series is increasing, and False (or 0) otherwise.
    
    The indicator has two modes:
    - Standard: Returns True if the current value is greater than the value 'length' periods ago
    - Strict: Returns True only if the series has been continuously increasing over the entire period
    
    Additionally, a percentage parameter can be used to adjust the comparison threshold,
    allowing for a more flexible definition of what constitutes "increasing."
    
    This indicator is useful for identifying uptrends, determining when to exit short positions,
    or finding potential entry points for long positions.

More info:
    None

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The lookback period for comparison. Default is 1.
    - strict (bool): If True, checks if the series is continuously increasing over the period. Default is False.
    - as_int (bool): If True, returns the result as integers (1 for True, 0 for False). Default is True.
    - percent (float): Optional percentage threshold adjustment. Default is None.
    - drift (int): The lag period for comparison in strict mode. Default is 1.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Standard increasing check
    result = bta.increasing(df)
    df['increasing'] = result['increasing']
    
    # Strict increasing check with longer period
    result = bta.increasing(df, length=5, strict=True)
    df['strict_increasing'] = result['strict_increasing']
    
    # Increasing with percentage threshold
    result = bta.increasing(df, percent=1.5)
    df['increasing_1.5pct'] = result['increasing_1.5pct']

Returns:
    pd.DataFrame: DataFrame with a column indicating increasing status (name varies based on parameters).

## Jurik Moving Average
Name:
    Jurik Moving Average (JMA)

Description:
    Mark Jurik's Moving Average (JMA) is an advanced adaptive moving average that attempts
    to eliminate market noise to reveal the underlying trend. Developed by Mark Jurik, this
    indicator features extremely low lag, smooth output, and responsiveness to market gaps.
    
    The JMA uses a combination of techniques including dynamic volatility bands, preliminary
    smoothing with an adaptive EMA, additional smoothing with a Kalman filter, and final
    processing with a unique Jurik adaptive filter. This multi-stage process results in a
    highly responsive yet smooth indicator.
    
    The phase parameter allows fine-tuning the behavior between more responsive (positive values)
    or smoother (negative values) output.

More info:
    https://www.tradingview.com/script/nZuBWW9j-Jurik-Moving-Average-JMA/
    https://www.prorealcode.com/prorealtime-indicators/jurik-volatility-bands/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the JMA calculation. Default is 7.
    - phase (float): Controls how heavy/light the average is. Range [-100, 100], 
      where negative values create a smoother average and positive values create a more responsive average.
      Default is 0.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.jurik_moving_average(df)
    df['jma'] = result['jma']

Returns:
    pd.DataFrame: DataFrame with 'jma' column.

## Least Squares Moving Average
Name:
    Least Squares Moving Average (LSMA)

Description:
    LSMA uses linear regression to compute the trend of the data over a specified period.
    It fits a straight line to the data points using the method of least squares to depict
    the direction of movement.

More info:
    https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/lsma

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which LSMA is to be calculated. Default is 'close'.
    - period (int): The period over which LSMA is to be calculated. Default is 21.

Call with:
    df['lsma'] = bta.least_squares_moving_average(df, 'close', 50)['lsma']

Returns:
    pd.DataFrame: DataFrame with 'lsma' column.

## Long Run
Name:
    Long Run Indicator

Description:
    The Long Run indicator identifies potential long/bullish conditions by analyzing 
    the relationship between a fast and slow series. It returns True (or 1) when 
    either of the following conditions is met:
    
    1. Potential Bottom: The fast series is increasing while the slow series is 
       decreasing, which may indicate a potential bottom formation or reversal.
    
    2. Both Increasing: Both the fast and slow series are increasing, which 
       indicates a potential ongoing bullish trend.
    
    This indicator can be used with any two series, but it's commonly applied to:
    - Fast and slow moving averages
    - Price and a moving average
    - A momentum indicator and its signal line
    
    The Long Run indicator is particularly useful for identifying potential entry 
    points for long positions or for confirming an existing bullish trend.

More info:
    None

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified columns.
    - fast_column (str): The column name for the fast series.
    - slow_column (str): The column name for the slow series.
    - length (int): The lookback period for determining whether series are increasing/decreasing. Default is 2.
    - as_int (bool): If True, returns the result as integers (1 for True, 0 for False). Default is True.

Call with:
    # Using two moving averages
    result = bta.long_run(df, 'sma_20', 'sma_50')
    df['long_run'] = result['long_run']
    
    # Using price and a moving average
    result = bta.long_run(df, 'close', 'sma_50')
    df['long_run'] = result['long_run']

Returns:
    pd.DataFrame: DataFrame with 'long_run' column indicating potential long conditions.

## Mcginley Dynamic
Name:
    McGinley Dynamic Indicator

Description:
    The McGinley Dynamic indicator was developed by John R. McGinley, a Certified Market
    Technician, as an improved moving average that minimizes price separation, reduces
    whipsaws, and hugs prices more closely than traditional moving averages.
    
    What makes the McGinley Dynamic unique is its adaptive nature. It speeds up in downtrends
    to follow prices more closely, yet moves more slowly in uptrends. This is achieved by
    incorporating a dynamic smoothing factor that adjusts based on the relationship between
    the current price and the indicator's previous value.
    
    The constant parameter allows for additional fine-tuning, with lower values (e.g., 0.6)
    making the indicator more responsive to price changes.

More info:
    https://www.investopedia.com/articles/forex/09/mcginley-dynamic-indicator.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:mcginley_dynamic

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the calculation. Default is 10.
    - constant (float): Multiplier for the denominator, sometimes set to 0.6 for more
      responsiveness. Default is 1.0.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.mcginley_dynamic(df)
    df['mcgd'] = result['mcgd']

Returns:
    pd.DataFrame: DataFrame with 'mcgd' column.

## Nadaraya Watson Smoothers
Name:
    Nadaraya-Watson Smoothers

Description:
    The Nadaraya-Watson Smoothers indicator is a sophisticated smoothing technique that uses 
    Gaussian kernel regression to create a smooth representation of price action. It applies 
    a Gaussian weight function to nearby data points, giving more weight to closer points 
    and less weight to farther points.
    
    This indicator can operate in two modes:
    - Repainting mode: Recalculates all historical values as new data arrives, providing 
      the smoothest possible curve but changing historical values
    - Non-repainting mode: Uses an endpoint method that doesn't change historical values, 
      making it suitable for backtesting and live trading
    
    The indicator also identifies trend direction changes and potential reversal points,
    making it useful for trend following strategies and entry/exit timing.

More info:
    The Nadaraya-Watson estimator is a non-parametric regression technique that estimates
    the conditional expectation of a random variable. In trading applications, it creates
    a smooth trend line that adapts to price movements while filtering out noise.
    
    https://en.wikipedia.org/wiki/Kernel_regression

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified source column.
    - src (str): The column to use for calculations. Default is 'close'.
    - bandwidth (float): Controls the smoothness of the estimator. Higher values create 
      smoother lines but with more lag. Default is 8.0.
    - repaint (bool): If True, uses repainting mode for smoothest results. If False, 
      uses non-repainting endpoint method. Default is True.
    - lookback (int): Maximum number of bars to look back for calculations. Default is 500.

Call with:
    nw_result = bta.nadaraya_watson_smoothers(df, src='close', bandwidth=8.0, repaint=True)
    df['nwe'] = nw_result['nwe']
    df['nwe_trend'] = nw_result['nwe_trend']
    df['nwe_reversal'] = nw_result['nwe_reversal']
    df['nwe_bullish'] = nw_result['nwe_bullish']
    df['nwe_bearish'] = nw_result['nwe_bearish']

Returns:
    pd.DataFrame: DataFrame with the following columns:
    - 'nwe': The Nadaraya-Watson Estimator values
    - 'nwe_trend': Trend direction (1 for up, -1 for down, 0 for sideways)
    - 'nwe_reversal': Reversal signals (1 for bullish reversal, -1 for bearish reversal, 0 for no reversal)
    - 'nwe_bullish': NWE values when trend is bullish (for plotting in green)
    - 'nwe_bearish': NWE values when trend is bearish (for plotting in red)

## Parabolic Sar
Name:
    Parabolic Stop and Reverse (PSAR)

Description:
    The Parabolic SAR (Stop and Reverse) is a trend-following indicator developed by 
    J. Welles Wilder. It is used to determine the direction of a trend and identify 
    potential reversal points in price.
    
    The indicator appears as a series of dots placed either above or below the price, 
    depending on the trend direction:
    - Dots below the price indicate an uptrend (stored in 'psar_long')
    - Dots above the price indicate a downtrend (stored in 'psar_short')
    
    The distance between the price and the dots gradually decreases as the trend continues,
    eventually causing a reversal when the price crosses the SAR value. At this point, the
    SAR "stops and reverses" to the other side of the price.
    
    The indicator uses an acceleration factor (AF) that increases as the trend continues
    in the same direction, causing the SAR to accelerate toward the price.
    
    This implementation returns four components:
    - psar_long: SAR values during uptrends (appears below price)
    - psar_short: SAR values during downtrends (appears above price)
    - psar_af: Current acceleration factor value
    - psar_reversal: Binary indicator (1/0) showing when SAR reversals occur

More info:
    https://www.investopedia.com/trading/introduction-to-parabolic-sar/
    https://school.stockcharts.com/doku.php?id=technical_indicators:parabolic_sar

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns, 
      and optionally 'close' if use_close is True.
    - initial_af (float): Initial acceleration factor. Default is 0.02.
    - af_step (float): Acceleration factor increment. Default is 0.02.
    - max_af (float): Maximum acceleration factor. Default is 0.2.
    - use_close (bool): Whether to use close price for initial SAR calculation. Default is False.

Call with:
    result = bta.parabolic_sar(df)
    df['psar_long'] = result['psar_long']  # SAR values during uptrends (below price)
    df['psar_short'] = result['psar_short']  # SAR values during downtrends (above price)
    df['psar_af'] = result['psar_af']  # Current acceleration factor
    df['psar_reversal'] = result['psar_reversal']  # Binary indicator for SAR reversals

Returns:
    pd.DataFrame: DataFrame with 'psar_long', 'psar_short', 'psar_af', and 'psar_reversal' columns.

## Pascals Weighted Moving Average
Name:
    Pascal's Weighted Moving Average (PWMA)

Description:
    Pascal's Weighted Moving Average is a type of weighted moving average where the
    weights are based on Pascal's Triangle. This creates a symmetric bell-curved weight
    distribution that gives more importance to the middle values in the calculation window.
    
    Pascal's Triangle is a triangular array of numbers where each number is the sum of the
    two numbers directly above it. When used as weights for a moving average, it creates
    a naturally balanced weight distribution that can effectively filter price noise while
    maintaining responsiveness to significant price movements.

More info:
    https://en.wikipedia.org/wiki/Pascal%27s_triangle
    https://www.investopedia.com/terms/w/weighted_average.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the PWMA calculation. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.pascals_weighted_moving_average(df)
    df['pwma'] = result['pwma']

Returns:
    pd.DataFrame: DataFrame with 'pwma' column.

## Percent Price Channel
Name:
    Percent Change Channel (PCC)

Description:
    PCC is like KC unless it uses percentage changes in price to set channel distance.
    This channel creates bands based on the percentage change of price rather than
    absolute price movements, making it more adaptive to different price levels.

More info:
    https://www.tradingview.com/script/6wwAWXA1-MA-Streak-Change-Channel/

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - period (int): Period for the ZEMA calculation. Default is 20.
    - mult (int): Multiplier for the range. Default is 2.

Call with:
    pcc_result = bta.percent_price_channel(df, period=20, mult=2)
    df['pcc_upper'] = pcc_result['pcc_upper']
    df['pcc_rangema'] = pcc_result['pcc_rangema']
    df['pcc_lower'] = pcc_result['pcc_lower']

Returns:
    pd.DataFrame: DataFrame with 'pcc_upper', 'pcc_rangema', and 'pcc_lower' columns.

## Pmax
Name:
    Pmax Indicator

Description:
    A self-contained implementation of the Pmax indicator that calculates upper and lower
    bands based on a moving average and Average True Range (ATR). The function is independent
    of any external libraries.

More info:
    https://www.tradingview.com/script/sU9molfV/

Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data.
    - period (int): Lookback period for ATR calculation.
    - multiplier (float): ATR multiplier to calculate bands.
    - length (int): Lookback period for the moving average.
    - ma_type (str, default='EMA'): Type of moving average to use. Options are:
        - 'EMA' (Exponential Moving Average)
        - 'SMA' (Simple Moving Average)
    - src (str, default='close'): Source price for calculation. Options are:
        - 'close' (default)
        - 'hl2' (average of high and low)
        - 'ohlc4' (average of open, high, low, and close)

Call with:
    pmax_result = bta.pmax(df, period=14, multiplier=2.0, length=20, ma_type='EMA', src='close')
    df['pmax'] = pmax_result['pmax']
    df['pmax_trend'] = pmax_result['pmax_trend']

Returns:
    pd.DataFrame: DataFrame with the following columns added:
        - 'pmax': Final Pmax values.
        - 'pmax_trend': Trend direction ('up' or 'down').

## Price Channel
Name:
    Price Channel (PPC)

Description:
    The Price Channel % PC indicator calculates the percent change of the price channel.
    It calculates the highest high and lowest low of the trailing number of bars specified
    by the input period. The price channel calculates the highest high and lowest low of
    the trailing number of bars specified by the input period.

    When a market moves above the upper band, it is a sign of market strength. Conversely,
    when a market moves below the lower band, it is a sign of market weakness. A sustained
    move above or below the channel lines may indicate a significant breakout.

    The `percent_p` column represents the percentage position of the current closing price
    within the price channel defined by the highest high and lowest low over a specified
    period. It shows where the current closing price stands relative to the recent highest
    and lowest prices.

More info:
    https://www.investopedia.com/terms/p/price-channel.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - period (int): Period for the highest high and lowest low calculation. Default is 20.

Call with:
    ppc_result = bta.price_channel(df, period=20)
    df['ppc_upper'] = ppc_result['ppc_upper']
    df['ppc_mid'] = ppc_result['ppc_mid']
    df['ppc_lower'] = ppc_result['ppc_lower']
    df['percent_p'] = ppc_result['percent_p']

Returns:
    pd.DataFrame: DataFrame with 'ppc_upper', 'ppc_mid', 'ppc_lower', and 'percent_p' columns.

## Q Stick
Name:
    Q Stick Indicator

Description:
    The Q Stick indicator, developed by Tushar Chande, attempts to quantify and
    identify trends in candlestick charts by measuring the relationship between
    opening and closing prices over a specified period.
    
    A positive Q Stick value indicates buying pressure (more closes above opens),
    while a negative value indicates selling pressure (more closes below opens).
    Values near zero suggest a balance between buying and selling pressure.
    
    This implementation allows for different types of moving averages to be applied
    to the difference between close and open prices.

More info:
    https://library.tradingtechnologies.com/trade/chrt-ti-qstick.html

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open' and 'close' columns.
    - length (int): Period for the moving average calculation. Default is 10.
    - ma_type (str): The type of moving average to use. Options include:
      'SMA' (Simple), 'EMA' (Exponential), 'DEMA' (Double Exponential),
      'WMA' (Weighted), 'HMA' (Hull), 'RMA' (Running/Rolling). Default is 'SMA'.

Call with:
    result = bta.q_stick(df, length=10, ma_type='EMA')
    df['q_stick'] = result['q_stick']

Returns:
    pd.DataFrame: DataFrame with 'q_stick' column containing the indicator values.

## Range Filter
Name:
    Range Filter Buy and Sell Indicator

Description:
    This indicator smooths price action using a range filter based on a volatility-adjusted
    moving average. It identifies uptrends and downtrends while filtering out noise.

More info:
    https://www.tradingview.com/script/J3TL15C9-Range-Filter-Strategy/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the "close" column.
    - column (str): The column on which the range filter is calculated. Default is "close".
    - period (int): Sampling period for smoothing range calculation. Default is 100.
    - multiplier (float): Multiplier for the smoothed range. Default is 3.0.
    - fillna (bool): If True, fills nan values. Default is False.

Call with:
    range_filter_result = bta.range_filter(df, "close", 100, 3.0)
    df["range_filter"] = range_filter_result["range_filter"]
    df["high_band"] = range_filter_result["high_band"]
    df["low_band"] = range_filter_result["low_band"]
    df["long_signal"] = range_filter_result["long_signal"]
    df["short_signal"] = range_filter_result["short_signal"]

Returns:
    pd.DataFrame: DataFrame with 'range_filter', 'high_band', 'low_band', 'long_signal', 'short_signal'.

## Rolling Moving Average
Name:
    Rolling Moving Average (RMA)

Description:
    The RMA function calculates the Rolling Moving Average (RMA) of a specified column
    in a DataFrame over a given period. It uses an exponential moving average (EMA)
    calculation with a specified smoothing factor (alpha) and returns a DataFrame
    containing the RMA values. This function allows for flexible moving average
    calculations based on any column in the input DataFrame.

More info:
    The RMA is similar to an EMA but with a different smoothing factor calculation.
    It's used in indicators like RSI.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which RMA is to be calculated.
    - period (int): The period over which RMA is to be calculated.

Call with:
    df['rma'] = bta.rolling_moving_average(df, 'close', 14)['rma']

Returns:
    pd.DataFrame: DataFrame with 'rma' column.

## Sequential Weighted Moving Average
Name:
    Sequential Weighted Moving Average (SWMA)

Description:
    A weighted moving average where weights are based on a symmetric triangle pattern.
    For example: n=3 -> [1/4, 2/4, 1/4], n=4 -> [1/6, 2/6, 2/6, 1/6], etc.
    This creates a symmetric weight distribution that gives more importance to the
    middle values in the calculation window.
    
    This moving average has variable length in contrast to TradingView's fixed
    length of 4. It effectively smooths price data while reducing lag and maintaining
    responsiveness to significant price movements.

More info:
    https://www.tradingview.com/study-script-reference/#fun_swma

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the SWMA calculation. Default is 10.
    - asc (bool): Whether recent values should weigh more. Default is True.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.sequential_weighted_moving_average(df)
    df['swma'] = result['swma']

Returns:
    pd.DataFrame: DataFrame with 'swma' column.

## Short Run
Name:
    Short Run Indicator

Description:
    The Short Run indicator identifies potential short/bearish conditions by analyzing 
    the relationship between a fast and slow series. It returns True (or 1) when 
    either of the following conditions is met:
    
    1. Potential Top: The fast series is decreasing while the slow series is 
       increasing, which may indicate a potential top formation or reversal.
    
    2. Both Decreasing: Both the fast and slow series are decreasing, which 
       indicates a potential ongoing bearish trend.
    
    This indicator can be used with any two series, but it's commonly applied to:
    - Fast and slow moving averages
    - Price and a moving average
    - A momentum indicator and its signal line
    
    The Short Run indicator is particularly useful for identifying potential entry 
    points for short positions or for confirming an existing bearish trend.

More info:
    None

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified columns.
    - fast_column (str): The column name for the fast series.
    - slow_column (str): The column name for the slow series.
    - length (int): The lookback period for determining whether series are increasing/decreasing. Default is 2.
    - as_int (bool): If True, returns the result as integers (1 for True, 0 for False). Default is True.

Call with:
    # Using two moving averages
    result = bta.short_run(df, 'sma_20', 'sma_50')
    df['short_run'] = result['short_run']
    
    # Using price and a moving average
    result = bta.short_run(df, 'close', 'sma_50')
    df['short_run'] = result['short_run']

Returns:
    pd.DataFrame: DataFrame with 'short_run' column indicating potential short conditions.

## Simple Moving Average
Name:
    Simple Moving Average (SMA)

Description:
    The Simple Moving Average is the unweighted mean of the previous 'period' data points.

More info:
    https://www.investopedia.com/terms/s/sma.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which SMA is to be calculated. Default is 'close'.
    - period (int): The period over which SMA is to be calculated. Default is 21.

Call with:
    df['sma'] = bta.simple_moving_average(df, 'close', 50)['sma']

Returns:
    pd.DataFrame: DataFrame with 'sma' column.

## Sine Weighted Moving Average
Name:
    Sine Weighted Moving Average (SINWMA)

Description:
    A weighted moving average where the weights are based on a sine function.
    This gives more weight to the middle values in the calculation window,
    creating a more responsive indicator that reduces lag compared to a simple
    moving average while still smoothing price action effectively.
    
    The weights follow a sine wave pattern, with the highest weights in the middle
    of the window and lower weights at the beginning and end. This creates a
    bell-shaped weighting scheme that can help filter out noise while maintaining
    sensitivity to significant price changes.

More info:
    https://www.tradingview.com/script/6MWFvnPO-Sine-Weighted-Moving-Average/
    Created by Everget on TradingView

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the SINWMA calculation. Default is 14.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.sine_weighted_moving_average(df)
    df['sinwma'] = result['sinwma']

Returns:
    pd.DataFrame: DataFrame with 'sinwma' column.

## Ssl Channels
Name:
    SSL Channels

Description:
    SSL Channels is an indicator based on the concept of using different moving averages
    to identify trends. This function calculates the SSL Down and SSL Up series.

More info:
    https://www.tradingview.com/script/xl7XbPTM-SSL-Channel-Chart/

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the SMA calculation. Default is 10.
    - mode (str): Type of moving average to use. Currently only 'sma' is supported.

Call with:
    ssl_result = bta.ssl_channels(df, length=10, mode='sma')
    df['ssl_down'] = ssl_result['ssl_down']
    df['ssl_up'] = ssl_result['ssl_up']

Returns:
    pd.DataFrame: DataFrame with 'ssl_down' and 'ssl_up' columns.

## Ssl Channels Atr
Name:
    SSL Channels with ATR

Description:
    The ssl_channels_atr function calculates the SSL (Safe and Secure Levels) channels using
    the Average True Range (ATR) to adjust the Simple Moving Averages (SMA) of the high
    and low prices over a specified period. It determines the trend direction based on
    the comparison of a chosen price column with these adjusted SMAs and generates the
    SSL ATR Down and Up levels accordingly.

    This indicator helps identify potential trend reversals and continuations by providing
    dynamic support and resistance levels.

More info:
    https://www.tradingview.com/script/xl7XbPTM-SSL-Channel-Chart/

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the SMA calculation. Default is 21.
    - atr_period (int): Period for the ATR calculation. Default is 14.
    - column (str): The column to use for the moving average calculations. Default is 'close'.

Call with:
    ssl_result = bta.ssl_channels_atr(df, column='close', length=14, atr_period=7)
    df['ssl_atr_down'] = ssl_result['ssl_atr_down']
    df['ssl_atr_up'] = ssl_result['ssl_atr_up']

Returns:
    pd.DataFrame: DataFrame with 'ssl_atr_down' and 'ssl_atr_up' columns.

## Supertrend
Name:
    Supertrend

Description:
    The Supertrend indicator is a trend-following indicator that uses Average True Range (ATR)
    to calculate dynamic support and resistance levels. It helps identify trend direction and
    potential entry/exit points. The indicator creates upper and lower bands around price action
    and switches between them based on price closes relative to the previous period's bands.

    The Supertrend line acts as:
    - Support during uptrends (when price is above the line)
    - Resistance during downtrends (when price is below the line)
    
    Direction changes occur when:
    - Price closes above the previous upper band (bullish signal)
    - Price closes below the previous lower band (bearish signal)

More info:
https://www.tradingview.com/script/VLWVV7tH-SuperTrend/
    - http://www.freebsensetips.com/blog/detail/7/What-is-supertrend-indicator-its-calculation
    - https://www.investopedia.com/articles/active-trading/121014/using-supertrend-indicator-develop-trading-system.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high', 'low', 'close'.
    - length (int): The period for HL2 calculation. Default is 7.
    - atr_length (int): The period for ATR calculation. If None, uses length value. Default is None.
    - multiplier (float): Coefficient for upper and lower band distance from HL2. Default is 3.0.
    - atr_mamode (str): Moving average type for ATR calculation. Options: 'sma', 'ema', 'rma', 'wma'. Default is 'rma'.

Call with:
    result = bta.supertrend(df, length=7, multiplier=3.0)
    df['supertrend'] = result['supertrend_7_3.0']
    df['supertrend_direction'] = result['supertrend_direction_7_3.0']
    df['supertrend_long'] = result['supertrend_long_7_3.0']
    df['supertrend_short'] = result['supertrend_short_7_3.0']

Returns:
    pd.DataFrame: DataFrame with multiple columns:
        - 'supertrend_{length}_{multiplier}': Main Supertrend line values
        - 'supertrend_direction_{length}_{multiplier}': Trend direction (1 for up, -1 for down)
        - 'supertrend_long_{length}_{multiplier}': Long trend values (lower band when trending up)
        - 'supertrend_short_{length}_{multiplier}': Short trend values (upper band when trending down)
        - 'supertrend_upper_band_{length}_{multiplier}': Upper band values
        - 'supertrend_lower_band_{length}_{multiplier}': Lower band values

## T3 Average
Name:
    T3 Average

Description:
    The T3 average is a smoothed moving average designed to reduce lag while maintaining
    responsiveness to price changes. This implementation uses multiple exponential moving
    averages (EMA) to achieve its smoothing effect.

More info:
    Tim Tillson's T3 indicator: 
    https://www.investopedia.com/terms/t/t3-oscillator.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the EMA calculation. Default is 5.

Call with:
    df['t3_average'] = bta.t3_average(df, length=5)['t3_average']

Returns:
    pd.DataFrame: DataFrame with 't3_average' column.

## Trend Signals
Name:
    Trend Signals

Description:
    Given a trend column, Trend Signals returns the trend, trades, entries, and exits
    as a set of columns that can be used for analysis or trading signal generation.
    
    A trend can be as simple as a boolean series where True represents an uptrend
    (e.g., 'close' > 'moving average'), or something more complex that results in
    a boolean or integer (0 or 1) series.
    
    This indicator is particularly useful for converting technical indicators or
    conditions into actionable trading signals. When 'as_bool=True', it returns
    trend, entries, and exits as boolean values, which can be helpful for backtesting.
    
    The function calculates:
    - trend: The input trend (0 or 1, or True/False if as_bool=True)
    - trades: Change in trend (1 for entry, -1 for exit, 0 otherwise)
    - entries: Points where trades change to positive (1 or True, 0 or False otherwise)
    - exits: Points where trades change to negative (1 or True, 0 or False otherwise)

More info:
    N/A (Original implementation by Kevin Johnson for Pandas TA)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified trend column.
    - trend_column (str): Name of the column containing the trend values (must be 0/1 or True/False).
    - as_bool (bool): If True, converts the trend, entries, and exits to boolean values. Default is False.
    - trade_offset (int): Value used to shift the trade entries/exits. Use 1 for backtesting 
      and 0 for live trading. Default is 0.
    - drift (int): The difference period for calculating changes in trend. Default is 1.

Call with:
    # Assuming you have a DataFrame with a trend column (e.g., 'sma_trend' = close > sma)
    result = bta.trend_signals(df, trend_column='sma_trend', as_bool=False)
    df['trend'] = result['trend']  # The trend (0 or 1)
    df['trades'] = result['trades']  # Trade signals (1: entry, -1: exit, 0: no change)
    df['entries'] = result['entries']  # Entry points (1 or 0)
    df['exits'] = result['exits']  # Exit points (1 or 0)

Returns:
    pd.DataFrame: DataFrame with 'trend', 'trades', 'entries', and 'exits' columns.

## Triangular Moving Average
Name:
    Triangular Moving Average (TRIMA)

Description:
    A Triangular Moving Average (TRIMA) is a weighted moving average where the weights
    form a triangular pattern, with the greatest weight given to the middle of the period.
    This is accomplished by calculating a Simple Moving Average (SMA) of another SMA.
    
    The TRIMA provides a smoother representation of price action compared to a standard
    Simple Moving Average, making it useful for identifying the underlying trend while
    filtering out short-term price fluctuations and noise.

More info:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triangular-moving-average-trima/
    https://www.investopedia.com/terms/t/triangularMovingAverage.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the TRIMA calculation. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.triangular_moving_average(df)
    df['trima'] = result['trima']

Returns:
    pd.DataFrame: DataFrame with 'trima' column.

## Triple Exponential Moving Average
Name:
    Triple Exponential Moving Average (TEMA)

Description:
    Triple Exponential Moving Average (TEMA) is a technical indicator designed to smooth 
    price data while reducing lag. It's more responsive than traditional moving averages,
    making it useful for identifying trend changes earlier.
    
    TEMA uses multiple EMAs and a specific calculation to reduce the lag typically 
    associated with moving averages. It achieves this by applying a formula that gives 
    more weight to recent price movements while maintaining a reasonable smoothing effect.

More info:
    https://www.investopedia.com/terms/t/triple-exponential-moving-average.asp
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/triple-exponential-moving-average-tema/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the EMA calculations. Default is 10.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.triple_exponential_moving_average(df)
    df['tema'] = result['tema']

Returns:
    pd.DataFrame: DataFrame with 'tema' column.

## Ttm Trend
Name:
    TTM Trend

Description:
    The TTM Trend indicator is from John Carter's book "Mastering the Trade" and is designed
    to identify the current trend direction. It compares the current closing price to the
    average price of the previous 'length' bars.
    
    The indicator returns:
    - 1 (bullish/uptrend) when the close is above the average price
    - -1 (bearish/downtrend) when the close is below the average price
    
    In traditional implementations, this indicator is used to color price bars green (bullish)
    or red (bearish). A common trading strategy is to consider a change in trend after two
    consecutive bars of the opposite color.
    
    This indicator can help traders stay in a trade until the trend changes, providing a
    simple yet effective way to identify potential entry and exit points.

More info:
    https://www.prorealcode.com/prorealtime-indicators/ttm-trend-price/
    John Carter's book "Mastering the Trade"

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The number of bars to include in the average price calculation. Default is 6.

Call with:
    result = bta.ttm_trend(df, length=6)
    df['ttm_trend'] = result['ttm_trend']  # 1 for bullish, -1 for bearish

Returns:
    pd.DataFrame: DataFrame with 'ttm_trend' column containing the indicator values (1 or -1).

## Ut Bot
Name:
    UT Bot Indicator

Description:
    A trend-following indicator that uses ATR to create a trailing stop that helps identify trend changes
    and potential entry/exit points. Originally created by HPotter.

More info:
    https://www.tradingview.com/script/jKqk8tWu-UT-BOT-1-3/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain OHLC data
    - column (str): The column name to use for calculations. Default is 'close'
    - key_value (float): Sensitivity multiplier for the ATR. Default is 3.0
    - atr_period (int): Period for ATR calculation. Default is 10

Call with:
    result = bta.ut_bot(df, 'close', 3.0, 10)
    df['ut_bot_stop'] = result['ut_bot_stop']
    df['ut_bot_position'] = result['ut_bot_position']
    df['ut_bot_buy'] = result['ut_bot_buy']
    df['ut_bot_sell'] = result['ut_bot_sell']

Returns:
    pd.DataFrame: DataFrame with 'ut_bot_stop', 'ut_bot_position', 'ut_bot_buy', and 'ut_bot_sell' columns

## Variable Index Dynamic Average
Name:
    Variable Index Dynamic Average (VIDYA)

Description:
    The Variable Index Dynamic Average (VIDYA) was developed by Tushar Chande in 1992.
    It is an adaptive moving average that adjusts its sensitivity based on market volatility.
    
    VIDYA uses the Chande Momentum Oscillator (CMO) to determine volatility. When volatility 
    is high, VIDYA reacts faster to price changes, making it more responsive than traditional
    moving averages. When volatility is low, it behaves more like a standard exponential 
    moving average.
    
    This indicator can be particularly useful for traders who want a moving average that 
    automatically adjusts to changing market conditions, potentially reducing lag during 
    volatile periods.

More info:
    https://www.tradingview.com/script/hdrf0fXV-Variable-Index-Dynamic-Average-VIDYA/
    https://www.perfecttrendsystem.com/blog_mt4_2/en/vidya-indicator-for-mt4

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for the VIDYA calculation. Default is 14.
    - column (str): The column name to use for calculations. Default is 'close'.
    - drift (int): The period for momentum calculation in CMO. Default is 1.

Call with:
    result = bta.variable_index_dynamic_average(df)
    df['vidya'] = result['vidya']

Returns:
    pd.DataFrame: DataFrame with 'vidya' column.

## Vertical Horizontal Filter
Name:
    Vertical Horizontal Filter (VHF)

Description:
    The Vertical Horizontal Filter (VHF) was created by Adam White to identify
    trending and ranging markets. It measures the ratio of the largest price
    movement (vertical movement) to the sum of price changes (horizontal movement)
    over a specified period.
    
    Higher VHF values indicate a strong trend (either up or down), while
    lower values suggest a ranging or sideways market. Traders often use this
    indicator to select appropriate trading strategies based on market conditions:
    trend-following strategies for high VHF values, and range-trading strategies
    for low VHF values.
    
    VHF is particularly useful as a precursor to applying other technical indicators,
    as it helps determine whether trend-following or oscillator-based indicators
    would be more appropriate for the current market conditions.

More info:
    https://www.incrediblecharts.com/indicators/vertical_horizontal_filter.php

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The period for calculating VHF. Default is 28.
    - drift (int): The period difference to calculate price changes. Default is 1.
    - column (str): Name of the column to use for calculations. Default is 'close'.

Call with:
    result = bta.vertical_horizontal_filter(df, length=28)
    df['vhf'] = result['vhf']

Returns:
    pd.DataFrame: DataFrame with 'vhf' column containing the indicator values.

## Volumatic Variable Index Dynamic Average
Name:
    Volumatic Variable Index Dynamic Average (VIDYA)

Description:
    The Volumatic Variable Index Dynamic Average (VIDYA) is an advanced indicator that combines
    the Variable Index Dynamic Average with volume analysis and support/resistance detection.
    
    This indicator uses the Chande Momentum Oscillator (CMO) to determine volatility and adapts
    the moving average sensitivity accordingly. When volatility is high, VIDYA reacts faster to
    price changes. The indicator also incorporates volume analysis to identify buying and selling
    pressure, and detects pivot points for support and resistance levels.
    
    Key features:
    - Adaptive moving average based on market volatility
    - Volume-weighted trend analysis
    - Automatic support and resistance detection via pivot points
    - Dynamic upper and lower bands based on ATR
    - Trend change signals with volume confirmation

More info:
    Based on the Volumatic VIDYA indicator by BigBeluga
    Original PineScript: https://creativecommons.org/licenses/by-nc-sa/4.0/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low', 'close', 'volume' columns.
    - vidya_length (int): Length of the VIDYA calculation. Default is 10.
    - vidya_momentum (int): Momentum length for VIDYA calculation. Default is 20.
    - band_distance (float): Distance factor for upper/lower bands. Default is 2.0.
    - atr_length (int): Period for ATR calculation. Default is 200.
    - pivot_left_bars (int): Left side bars for pivot detection. Default is 3.
    - pivot_right_bars (int): Right side bars for pivot detection. Default is 3.
    - smooth_length (int): Smoothing period for VIDYA. Default is 15.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.volumatic_variable_index_dynamic_average(df)
    df['vidya'] = result['vidya']
    df['vidya_smoothed'] = result['vidya_smoothed']
    df['upper_band'] = result['upper_band']
    df['lower_band'] = result['lower_band']
    df['smoothed_value'] = result['smoothed_value']
    df['trend_up'] = result['trend_up']
    df['trend_change_up'] = result['trend_change_up']
    df['trend_change_down'] = result['trend_change_down']
    df['pivot_high'] = result['pivot_high']
    df['pivot_low'] = result['pivot_low']
    df['up_volume'] = result['up_volume']
    df['down_volume'] = result['down_volume']
    df['volume_delta_pct'] = result['volume_delta_pct']
    df['atr'] = result['atr']

Returns:
    pd.DataFrame: DataFrame with columns:
        - 'vidya': Raw VIDYA values
        - 'vidya_smoothed': Smoothed VIDYA values
        - 'upper_band': Upper band (VIDYA + ATR * distance)
        - 'lower_band': Lower band (VIDYA - ATR * distance)
        - 'smoothed_value': Trend-based smoothed value
        - 'trend_up': Binary indicator for uptrend (1) or downtrend (0)
        - 'trend_change_up': Binary indicator for trend change to up
        - 'trend_change_down': Binary indicator for trend change to down
        - 'pivot_high': Binary indicator for pivot high points
        - 'pivot_low': Binary indicator for pivot low points
        - 'up_volume': Cumulative volume during uptrends
        - 'down_volume': Cumulative volume during downtrends
        - 'volume_delta_pct': Volume delta as percentage
        - 'atr': Average True Range values

## Volume Weighted Moving Average
Name:
    Volume Weighted Moving Average (VWMA)

Description:
    The Volume Weighted Moving Average (VWMA) is a technical analysis indicator that
    combines price and volume data to provide a more accurate representation of a
    security's average price over time. Unlike a simple moving average that gives
    equal weight to each price point, the VWMA gives more weight to price points
    with higher trading volumes.
    
    This weighting method can provide a more accurate representation of a security's
    true average price, as it accounts for the significance of price movements based
    on their trading volume. High-volume price movements are considered more significant
    and thus have a greater impact on the VWMA.

More info:
    https://www.investopedia.com/articles/trading/11/trading-with-vwap-mvwap.asp
    https://www.motivewave.com/studies/volume_weighted_moving_average.htm

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - length (int): The period for the VWMA calculation. Default is 10.

Call with:
    result = bta.volume_weighted_moving_average(df)
    df['vwma'] = result['vwma']

Returns:
    pd.DataFrame: DataFrame with 'vwma' column.

## Vortex Indicator
Name:
    Vortex Indicator

Description:
    The Vortex Indicator is a technical analysis indicator composed of two oscillating 
    lines - VI+ (positive) and VI- (negative). These lines capture positive and negative 
    trend movement and are designed to identify the start of a new trend or the continuation 
    of an existing trend.
    
    The indicator works by comparing the current price to the previous price, in relation 
    to the true range. When VI+ crosses above VI-, it may indicate the start of a new 
    uptrend. Conversely, when VI- crosses above VI+, it may signal the beginning of a 
    new downtrend.
    
    The Vortex Indicator is particularly useful for trend identification and confirmation,
    and is often used in conjunction with other technical indicators.

More info:
    https://school.stockcharts.com/doku.php?id=technical_indicators:vortex_indicator

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for calculating the indicator. Default is 14.
    - drift (int): The difference period for VM calculations. Default is 1.

Call with:
    result = bta.vortex_indicator(df, length=14)
    df['vi_plus'] = result['vi_plus']  # Positive Vortex Indicator line
    df['vi_minus'] = result['vi_minus']  # Negative Vortex Indicator line

Returns:
    pd.DataFrame: DataFrame with 'vi_plus' and 'vi_minus' columns containing the indicator values.

## Weighted Moving Average
Name:
    Weighted Moving Average (WMA)

Description:
    The Weighted Moving Average (WMA) gives more weight to recent data points and
    less weight to older data points.

More info:
    https://www.investopedia.com/articles/technical/060401.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - column (str): The column to calculate the WMA on.
    - period (int): The period for the WMA calculation.

Call with:
    df['wma'] = bta.weighted_moving_average(df, 'close', 10)['wma']

Returns:
    pd.DataFrame: DataFrame with 'wma' column.

## Zero Exponential Moving Average
Name:
    Zero Exponential Moving Average (ZEMA)

Description:
    The Zero Exponential Moving Average (ZEMA) is an improved version of the Exponential
    Moving Average (EMA) that reduces lag by incorporating a zero-lag component.

More info:
    The ZEMA applies the formula: 2 * EMA(period) - EMA(EMA(period)) to reduce lag.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZEMA is to be calculated. Default is 21.

Call with:
    df['zema'] = bta.zero_exponential_moving_average(df, 'close', 21)['zema']

Returns:
    pd.DataFrame: DataFrame with 'zema' column.

## Zero Lag Exponential Moving Average
Name:
    Zero Lag Exponential Moving Average (ZLEMA)

Description:
    ZLEMA is an Exponential Moving Average (EMA) that adjusts for lag, making it more responsive
    to recent price changes. It uses lagged data differences to adjust the EMA calculation,
    thereby reducing the inherent lag of EMA.

More info:
    Created by John Ehlers, the ZLEMA removes lag by subtracting older data from current data.
    https://en.wikipedia.org/wiki/Zero_lag_exponential_moving_average

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZLEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZLEMA is to be calculated. Default is 21.

Call with:
    df['zlema'] = bta.zero_lag_exponential_moving_average(df, 'close', 21)['zlema']

Returns:
    pd.DataFrame: DataFrame with 'zlema' column.

# Utility

## Calculate Atr Stop Loss Take Profit
Name:
    Calculate ATR Stop-Loss and Take-Profit

Description:
    This function calculates take-profit, stop-loss, and entry price levels based on the
    Average True Range (ATR) indicator and trading signals. The ATR is a volatility indicator
    that measures market volatility by decomposing the entire range of an asset price for
    a specific period.
    
    The function identifies when a trade signal changes (e.g., from neutral to buy) and
    calculates appropriate risk management levels based on the current ATR value. It uses
    configurable multipliers to determine the distance from entry for stop-loss and take-profit.

More info:
    Using ATR for stop-loss and take-profit placement is a common volatility-based risk
    management technique. The ATR helps adapt these levels to current market conditions:
    - In volatile markets, the ATR increases, resulting in wider stops to avoid premature exits
    - In calm markets, the ATR decreases, allowing for tighter stops to lock in profits

Parameters:
    - df (pd.DataFrame): Input DataFrame with required columns:
        - The signal column (by default 'signal')
        - 'close' price column
        - The ATR column (by default 'atr')
    - signal_column (str): Column with buy/sell signals. Default is 'signal'.
    - atr_column (str): Column containing ATR values. Default is 'atr'.
    - atr_sl_mult (float): Multiplier for stop-loss calculation. Default is 1.
    - atr_tp_mult (float): Multiplier for take-profit calculation. Default is 2.

Call with:
    # After calculating ATR and generating signals
    atr_sl_tp = bta.calculate_atr_stop_loss_take_profit(
        df, 
        signal_column='signal', 
        atr_column='atr_14',
        atr_sl_mult=1.5,
        atr_tp_mult=3.0
    )
    
    # Add results to original dataframe
    df['tp'] = atr_sl_tp['takeprofit']
    df['sl'] = atr_sl_tp['stoploss']
    df['entry'] = atr_sl_tp['buyprice']

Returns:
    pd.DataFrame: A DataFrame with three columns:
    - 'takeprofit': The price levels for taking profit
    - 'stoploss': The price levels for stop-loss
    - 'buyprice': The entry price levels

Important Notes:
    - This function REQUIRES that your DataFrame already contains specific columns:
      * A signal column (default name: 'signal') with values including 'buy'
      * An ATR column (default name: 'atr') with numeric ATR values
      * A 'close' column with the closing prices
    
    - The function will fail with a KeyError if these required columns are missing.
    
    - Before using this function, make sure to:
      1. Calculate the ATR indicator using the average_true_range() function
      2. Generate trading signals and assign them to a column named 'signal' (or specify
         a different column name using the signal_column parameter)
      3. Ensure your 'signal' column contains 'buy' values for entries (other values
         like 'sell' or 'neutral' can be used for non-entry conditions)
    
    - For testing purposes, you might need to create a wrapper that adds these
      required columns before calling this function.

## Calculate Stop Loss Take Profit
Name:
    Calculate Stop-Loss and Take-Profit

Description:
    This function calculates dynamic stop-loss and take-profit levels based on recent price action
    and customizable trade signals. It implements a swing-based risk management approach that 
    uses the lowest low (for long trades) or highest high (for short trades) within a lookback 
    period to establish stop-loss levels. Take-profit levels are then calculated based on 
    configurable reward-to-risk ratios.
    
    The function also tracks the status of trades, identifying when stop-loss or take-profit 
    levels have been hit, and provides exit reason information.

More info:
    This implementation follows a common risk management practice in trading:
    - For long trades: Stop-loss is placed below a recent swing low
    - For short trades: Stop-loss is placed above a recent swing high
    - Take-profit is calculated as a multiple of the risk (the distance to stop-loss)
    
    This approach adapts to market conditions by using actual price swings rather than 
    fixed percentages or arbitrary levels.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing price data and trade signals.
    - signal_column (str): Column name with trade signals. Default is 'trade_signal'.
    - long_trade_signal (str): Value indicating a long trade. Default is 'long_trade'.
    - short_trade_signal (str): Value indicating a short trade. Default is 'short_trade'.
    - no_trade_signal (str): Value indicating no trade. Default is 'no_trade'.
    - lookback_period (int): Period for finding swing highs/lows. Default is 5.
    - long_reward_ratio (float): Reward-risk ratio for long trades. Default is 2.
    - short_reward_ratio (float): Reward-risk ratio for short trades. Default is 2.
    - buffer (float): Additional buffer added to stop-loss. Default is 0.0.

Call with:
    # After generating trade signals
    risk_mgmt = bta.calculate_stop_loss_take_profit(
        df,
        signal_column='my_signal',
        long_trade_signal='buy',
        short_trade_signal='sell',
        no_trade_signal='neutral',
        lookback_period=10,
        long_reward_ratio=2.5,
        short_reward_ratio=2.0,
        buffer=0.2
    )
    
    # Add results to the original dataframe
    df['sl'] = risk_mgmt['stop_loss']
    df['tp'] = risk_mgmt['take_profit']
    df['entry'] = risk_mgmt['entry_price']
    df['exit_type'] = risk_mgmt['exit_reason']

Returns:
    pd.DataFrame: A DataFrame with four columns:
    - 'stop_loss': The calculated stop-loss prices
    - 'take_profit': The calculated take-profit prices
    - 'entry_price': The trade entry prices
    - 'exit_reason': The reason for exit ('stop_loss_exit', 'take_profit_hit', etc.)

Important Notes:
    - This function REQUIRES that your DataFrame already contains specific columns:
      * A trade signal column (default name: 'trade_signal') with values matching 
        those specified in long_trade_signal, short_trade_signal, and no_trade_signal
      * 'high', 'low', and 'close' price columns
    
    - The function will fail with a KeyError if these required columns are missing.
    
    - Before using this function, make sure to:
      1. Generate trading signals and assign them to a column (default: 'trade_signal')
      2. Ensure your signal column contains the expected values (by default: 'long_trade',
         'short_trade', and 'no_trade')
    
    - For testing purposes, you might need to create a wrapper that adds these
      required columns before calling this function.

## Compounded Annual Growth Rate
Name:
    Compounded Annual Growth Rate (CAGR)

Description:
    Calculates the Compounded Annual Growth Rate (CAGR) which represents
    the mean annual growth rate of an investment over a specified time period
    longer than one year. It measures the smoothed rate of return as if the
    investment had grown at a steady rate annually.

More info:
    CAGR is a widely used metric to evaluate the performance of investments
    over time. It's particularly useful when comparing investments with
    different time horizons as it standardizes returns to an annual basis.
    
    The formula is:
    CAGR = (Ending Value / Beginning Value)^(1 / Years) - 1

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified
      and have a DatetimeIndex or be organized by trading days.
    - column (str): The column to calculate CAGR on. Default is 'close'.

Call with:
    cagr_result = bta.compounded_annual_growth_rate(df)
    df['cagr'] = cagr_result['cagr'][0]  # Extract single value

Returns:
    pd.DataFrame: DataFrame with a single row containing the CAGR value in
    a column named 'cagr'.

## Consecutive Count
Name:
    Consecutive Count

Description:
    This utility function calculates the average distance between non-zero elements in an array.
    It's particularly useful for analyzing patterns in time series data, such as determining 
    the average number of periods between significant events (like price movements exceeding
    a threshold, trend changes, or signal triggers).

More info:
    In algorithmic trading, this can be used to measure:
    - Frequency of crossover signals
    - Average distance between price spikes
    - Periodicity of market movements
    - Interval analysis for mean reversion or momentum

Parameters:
    - consecutive_diff (np.ndarray): A numpy array containing the differences or signal
      values where non-zero elements represent significant events.

Call with:
    # Example: Find average bars between RSI crossovers of 50
    crossover_array = np.where(df['rsi'] > 50, 1, 0).diff().fillna(0).values
    avg_distance = bta.consecutive_count(crossover_array)

Returns:
    float: The average number of indices between consecutive non-zero elements.
    Returns 0 if there are fewer than two non-zero elements.

Important Notes:
    - This function returns a single float value, not a DataFrame.
    
    - When used with bamboo_ta's test_indicator function, it will fail with
      "Error: consecutive_count did not return a DataFrame" because test_indicator
      expects a DataFrame return type.
    
    - To use with test_indicator, you need to create a wrapper function:
      ```python
      def consecutive_count_wrapper(df):
          # Create a sample array with some non-zero elements
          sample_array = df['close'].diff().fillna(0).values
          
          # Call the actual function
          result = consecutive_count(sample_array)
          
          # Return as DataFrame for test_indicator compatibility
          return pd.DataFrame({'consecutive_count': [result]})
      ```
    
    - This function is not designed to be applied directly to a DataFrame column
      but to a prepared numpy array. It is typically used as part of a larger
      calculation rather than as a standalone indicator.

## Consecutive Higher Highs
Name:
    Consecutive Higher Highs

Description:
    Identifies patterns of consecutive higher highs in a series.
    
    When as_count=True, this function returns a count of how many consecutive 
    higher values have occurred at each point in the series.
    
    When as_count=False, this function returns a binary indicator (1/0) that 
    signals when there have been at least 'length' consecutive higher values.
    
    This function is useful for detecting momentum continuation patterns,
    which can be useful for trend-following strategies, breakout confirmation,
    or as a filter for other trading signals.

More info:
    The concept of consecutive higher highs is commonly used in technical analysis
    to identify strong uptrends, especially in price series. It complements other
    trend identification methods and can be a useful confirmation signal.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The minimum number of consecutive higher values required. Default is 2.
    - column (str): The column name to use for calculations. Default is 'high'.
    - as_count (bool): If True, returns the count of consecutive higher values.
        If False, returns a binary indicator (1/0) when length is reached. Default is False.

Call with:
    # Get binary indicator for 3 consecutive higher highs
    result = bta.consecutive_higher_highs(df, length=3)
    df['three_higher_highs'] = result['consec_higher_high_3']
    
    # Get count of consecutive higher values
    result = bta.consecutive_higher_highs(df, as_count=True)
    df['higher_high_count'] = result['consec_higher_high']

Returns:
    pd.DataFrame: DataFrame with one column containing either:
        - The count of consecutive higher values (when as_count=True)
        - A binary indicator (1/0) for when length is reached (when as_count=False)

## Consecutive Lower Lows
Name:
    Consecutive Lower Lows

Description:
    Identifies patterns of consecutive lower lows in a series.
    
    When as_count=True, this function returns a count of how many consecutive 
    lower values have occurred at each point in the series.
    
    When as_count=False, this function returns a binary indicator (1/0) that 
    signals when there have been at least 'length' consecutive lower values.
    
    This function is useful for detecting downtrend momentum patterns,
    which can be useful for trend-following strategies, breakdown confirmation,
    or as a filter for other trading signals.

More info:
    The concept of consecutive lower lows is commonly used in technical analysis
    to identify strong downtrends, especially in price series. It complements other
    trend identification methods and can be a useful confirmation signal.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - length (int): The minimum number of consecutive lower values required. Default is 2.
    - column (str): The column name to use for calculations. Default is 'low'.
    - as_count (bool): If True, returns the count of consecutive lower values.
        If False, returns a binary indicator (1/0) when length is reached. Default is False.

Call with:
    # Get binary indicator for 3 consecutive lower lows
    result = bta.consecutive_lower_lows(df, length=3)
    df['three_lower_lows'] = result['consec_lower_low_3']
    
    # Get count of consecutive lower values
    result = bta.consecutive_lower_lows(df, as_count=True)
    df['lower_low_count'] = result['consec_lower_low']

Returns:
    pd.DataFrame: DataFrame with one column containing either:
        - The count of consecutive lower values (when as_count=True)
        - A binary indicator (1/0) for when length is reached (when as_count=False)

## Cross
Name:
    Cross Indicator

Description:
    Determines when one series crosses above or below another series.
    This creates a binary indicator (or boolean) that can be used for
    generating signals or conditions in trading strategies.

More info:
    Crossovers are one of the most fundamental signals in technical analysis.
    They occur when one series (like a faster moving average) crosses either above or below
    another series (like a slower moving average). Crossing above is typically
    considered a bullish signal, while crossing below is typically a bearish signal.
    
    This function detects the exact point of crossing, which marks a change in direction
    or momentum. It returns 1 (or True) only at the candle where the crossing occurs.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the columns specified.
    - column_a (str): The column to check if it's crossing above/below column_b.
    - column_b (str): The column to compare against.
    - direction (str): The direction of the cross, either 'above' or 'below'. Default is 'above'.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Detect when fast EMA crosses above slow EMA
    df['ema_cross_up'] = bta.cross(df, 'ema_9', 'ema_21', 'above')['ema_9_xa_ema_21']
    
    # Detect when fast EMA crosses below slow EMA
    df['ema_cross_down'] = bta.cross(df, 'ema_9', 'ema_21', 'below')['ema_9_xb_ema_21']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 at points where column_a
    crosses above/below column_b (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column_a}_xa_{column_b}' for crossing above, or
    '{column_a}_xb_{column_b}' for crossing below.

## Cross Value
Name:
    Cross Value Indicator

Description:
    Determines when a series crosses above or below a specified constant value.
    This creates a binary indicator (or boolean) that can be used for
    generating signals or conditions in trading strategies.

More info:
    Value crossovers are fundamental signals in technical analysis.
    They occur when a series (like price or an oscillator) crosses either above or below
    a specific threshold or level. For example, RSI crossing above 70 or below 30,
    or price crossing above/below a key price level.
    
    This function detects the exact point of crossing, which marks a change in direction
    or momentum relative to the specified value. It returns 1 (or True) only at the 
    candle where the crossing occurs.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - column (str): The column to check for crossing above/below the value.
    - value (float): The constant value to compare against.
    - direction (str): The direction of the cross, either 'above' or 'below'. Default is 'above'.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Detect when RSI crosses above 70 (overbought)
    df['rsi_overbought'] = bta.cross_value(df, 'rsi', 70, 'above')['rsi_xav_70']
    
    # Detect when RSI crosses below 30 (oversold)
    df['rsi_oversold'] = bta.cross_value(df, 'rsi', 30, 'below')['rsi_xbv_30']
    
    # Detect when price crosses above a key level
    df['price_above_support'] = bta.cross_value(df, 'close', 100, 'above')['close_xav_100']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 at points where the specified
    column crosses above/below the value (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column}_xav_{value}' for crossing above, or
    '{column}_xbv_{value}' for crossing below.

## Cumulative Return
Name:
    Cumulative Return

Description:
    Cumulative Return measures the aggregate percentage return of an asset over a specific period.
    It calculates how much an initial investment would have grown or declined over time,
    expressed as a percentage. This is a fundamental metric in performance analysis to evaluate
    the total return generated by an asset or strategy.

More info:
    The cumulative return is calculated as: (Current Price / Initial Price - 1) * 100
    This provides the percentage change from the initial price to the current price.

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the specified column.
    - column (str): The column on which the cumulative return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with -1. Default is False.

Call with:
    df['cum_return'] = bta.cumulative_return(df)
    
    # To use a different price column:
    df['cum_return'] = bta.cumulative_return(df, column='adjusted_close')

Returns:
    pd.Series: Series of cumulative return values expressed as percentages.

## Daily Log Return
Name:
    Daily Log Return

Description:
    Daily Log Return calculates the logarithmic return between consecutive periods in a price series.
    It's a commonly used measure in financial analysis that represents the continuously compounded
    return and has statistical properties that make it useful for analysis, particularly for
    calculating volatility and performing statistical tests. Log returns are also more normally
    distributed than simple returns.

More info:
    The formula for daily log return is: ln(Pt/Pt-1) * 100, where Pt is the price at time t.
    Alternatively, it can be expressed as: (ln(Pt) - ln(Pt-1)) * 100.
    
    Compared to simple returns, log returns are:
    - Additive over time (making multi-period calculations easier)
    - More symmetrically distributed
    - Better for statistical analysis

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily log return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    df['log_return'] = bta.daily_log_return(df)
    
    # Using a different price column:
    df['log_return'] = bta.daily_log_return(df, column='adjusted_close')

Returns:
    pd.Series: Series of daily log return values expressed as percentages.

## Daily Return
Name:
    Daily Return

Description:
    Daily Return (also known as simple return) calculates the percentage change in price
    between consecutive periods. It's a fundamental measure in financial analysis that
    shows how much an investment has gained or lost over a single period, expressed as
    a percentage of the initial investment.

More info:
    The formula for daily return is: ((Pt/Pt-1) - 1) * 100, where Pt is the price at time t.
    
    This is the standard measure of return used in many financial applications. Unlike
    logarithmic returns, simple returns directly represent the actual percentage gain or
    loss experienced by an investor.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which the daily return is to be calculated. Default is "close".
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    df['daily_ret'] = bta.daily_return(df)
    
    # Using a different price column:
    df['daily_ret'] = bta.daily_return(df, column='adjusted_close')

Returns:
    pd.Series: Series of daily return values expressed as percentages.

Important Notes:
    - This function returns a pandas Series, not a DataFrame.
    
    - When used with bamboo_ta's test_indicator function, it will fail with
      "Error: daily_return did not return a DataFrame" because the test system
      expects a DataFrame return type.
    
    - For testing within the bamboo_ta framework, a wrapper function could be created:
      ```python
      def daily_return_wrapper(df):
          return_series = daily_return(df)
          # Convert the Series to a DataFrame for test_indicator compatibility
          return pd.DataFrame({'daily_return': return_series})
      ```
    
    - In actual usage, the Series return type is more convenient as it can be directly
      assigned to a DataFrame column as shown in the "Call with" examples.

## Drawdown
Name:
    Drawdown

Description:
    Drawdown is a peak-to-trough decline during a specific period for an investment,
    trading account, or fund. It measures the magnitude of a decline from a peak to
    a trough in the value of an asset or portfolio.
    
    The drawdown is typically quoted as the percentage between the peak and the
    subsequent trough, but this implementation also provides:
    - Absolute drawdown: The absolute difference between the peak and current price
    - Percentage drawdown: The percentage decline from peak (1 - price/max_price)
    - Logarithmic drawdown: The log difference between peak and current price
    
    Drawdown analysis is important for risk management as it helps assess the
    potential losses and volatility of an investment. Many traders use maximum
    drawdown as a risk metric when evaluating trading strategies.

More info:
    https://www.investopedia.com/terms/d/drawdown.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.drawdown(df)
    df['drawdown'] = result['drawdown']  # Absolute drawdown
    df['drawdown_pct'] = result['drawdown_pct']  # Percentage drawdown
    df['drawdown_log'] = result['drawdown_log']  # Logarithmic drawdown

Returns:
    pd.DataFrame: DataFrame with 'drawdown', 'drawdown_pct', and 'drawdown_log' columns.

## Drop Na
Name:
    Drop NA

Description:
    This utility function cleans a DataFrame by removing rows with NaN values and
    handling problematic values in numeric columns. It addresses three common issues
    in financial data:
    
    1. NaN (Not a Number) values which can cause calculation errors
    2. Extremely large values that might cause overflow issues in calculations
    3. Zero values which can cause division by zero errors in certain calculations
    
    The function is particularly useful as a pre-processing step before applying
    technical indicators or conducting analysis.

More info:
    Data cleaning is a critical step in any data analysis workflow. In financial
    time series data, missing values, zeros, and extremely large values can lead
    to errors or misleading results in technical indicators.
    
    This function uses a threshold of e^709 (approximately 8.22e+307) to identify
    extremely large values, which is close to the largest finite floating-point
    number in Python.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing financial data to be cleaned.

Call with:
    # Clean a dataframe before analysis
    clean_df = bta.drop_na(df)
    
    # Alternative: preserve original and use cleaned for calculations
    calc_df = bta.drop_na(df.copy())
    results = my_calculation_function(calc_df)

Returns:
    pd.DataFrame: A cleaned DataFrame with:
    - All rows containing NaN values removed
    - Extremely large values (>e^709) replaced with NaN and then removed
    - Zero values replaced with NaN and then removed

## Entropy
Name:
    Entropy

Description:
    Entropy, introduced by Claude Shannon in 1948, is a measure of randomness or
    unpredictability in a system. In financial markets, entropy can be used to
    quantify the uncertainty or disorder in price movements.
    
    Higher entropy values indicate more randomness and unpredictability in the price
    series, while lower values suggest more order and predictability. This can help
    traders identify periods of high volatility or uncertainty in the market.
    
    The calculation treats normalized prices as a probability distribution and applies
    the information entropy formula to this distribution over the specified period.

More info:
    https://en.wikipedia.org/wiki/Entropy_(information_theory)
    https://www.investopedia.com/terms/e/entropy.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the entropy calculation. Default is 10.
    - base (float): The logarithmic base to use in the entropy calculation. Default is 2.0.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.entropy(df, length=10, base=2.0)
    df['entropy'] = result['entropy']

Returns:
    pd.DataFrame: DataFrame with 'entropy' column containing the indicator values.

## Error Function
Name:
    Error Function (erf)

Description:
    Applies the error function (erf) to rolling standardized values of a price series.
    
    The error function, also called the Gauss error function, is a special function
    of sigmoid shape that occurs in probability, statistics, and partial differential
    equations. It is defined as:
    
    erf(x) = (2/√π) ∫(0 to x) e^(-t²) dt
    
    In this implementation, we:
    1. Take a rolling window of the specified length
    2. Standardize the latest value in the window
    3. Apply the error function to this standardized value
    
    This provides a measure of how many standard deviations the current price
    is from the mean, transformed through the erf function to range between -1 and 1.

More info:
    https://en.wikipedia.org/wiki/Error_function

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate on. Default is 'close'.

Call with:
    df['erf_30'] = bta.error_function(df)['erf_30']

Returns:
    pd.DataFrame: DataFrame with error function values in a column named 'erf_{length}'.

## Exhaustion Candles
Name:
    Exhaustion Candles

Description:
    This function calculates values for dynamically adjusting exhaustion bands based on
    the average consecutive length of price movements in the same direction. It helps
    identify potential price exhaustion points where trends might reverse.
    
    The function analyzes the pattern of consecutive up and down price movements within
    a specified window and calculates quality values that can be used to set dynamic
    band widths for detecting exhaustion points.

More info:
    Exhaustion is a market condition where a trend has extended for so long that it
    becomes unsustainable and is likely to reverse. This function helps identify
    such points by calculating values based on the consistency and length of price
    movements in a particular direction.

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the 'close' price series.
    - window (int, default=1): Lookback window for calculation.
    - multiplier (int, default=1): Scalar multiplier for both major and minor quality values.

Call with:
    maj_qual, min_qual = bta.exhaustion_candles(df, window=5, multiplier=2)
    df['maj_qual'] = maj_qual
    df['min_qual'] = min_qual

Returns:
    Tuple[np.ndarray, np.ndarray]: Two arrays containing major and minor quality values
    that can be used to set dynamic band widths for detecting exhaustion points.

## Exhaustion Lengths
Name:
    Exhaustion Lengths

Description:
    This function calculates the average distances between price peaks and valleys
    to help determine appropriate lengths for exhaustion bands. It identifies relative
    maxima in the 'high' prices and relative minima in the 'low' prices, then calculates
    the average distance between consecutive peaks and valleys, plus their standard
    deviations.
    
    These values can be used to dynamically adjust exhaustion bands based on the
    natural cycles present in the price data.

More info:
    Price action often follows cyclical patterns where peaks and troughs occur at
    somewhat regular intervals. By measuring the average distance between these
    extremes, traders can better calibrate indicators to match the natural rhythm
    of the market being analyzed.
    
    The function uses scipy's argrelextrema to find local maxima and minima in the
    price series, then calculates statistics about their spacing.

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing 'high' and 'low' columns.

Call with:
    maj_len, min_len = bta.exhaustion_lengths(df)
    df['maj_len'] = maj_len
    df['min_len'] = min_len

Returns:
    Tuple[int, int]: A tuple containing:
    - maj_len: Average peak distance plus standard deviation (for major cycles)
    - min_len: Average valley distance plus standard deviation (for minor cycles)
    Returns (0, 0) if there are insufficient peaks or valleys to calculate.

## Filter By Dates
Name:
    Filter DataFrame by Specific Dates

Description:
    Filters a DataFrame to include only data from specific dates provided in a list.
    This is useful for extracting data points from particular days of interest,
    such as earnings announcement days, economic event days, or specific trading days.

More info:
    This function allows selective extraction of data points when you're interested
    in analyzing specific events or dates rather than continuous periods. The function
    accepts either a single date string or a list of date strings.

Parameters:
    - df (pandas.DataFrame): Input DataFrame with a DatetimeIndex.
    - dates (str or List[str]): A single date string or a list of date strings
      to filter the DataFrame by. The dates should match the format of the
      DataFrame's index.

Call with:
    # Filter for a single date
    single_date_df = bta.filter_by_dates(df, "2023-01-15")
    
    # Filter for multiple dates
    multi_date_df = bta.filter_by_dates(df, ["2023-01-15", "2023-02-01", "2023-03-15"])

Returns:
    pd.DataFrame: DataFrame filtered to contain only data from the specified dates.
    If none of the specified dates are found in the DataFrame's index, returns the
    original DataFrame.

Important Notes:
    - This function explicitly converts string dates to datetime objects to
      avoid FutureWarning issues with pandas.
    - The function works best when your DataFrame has a proper DatetimeIndex.

## First Crossed Above Second
Name:
    First Crossed Above Second

Description:
    This function checks if the first series crosses above the second series.
    It returns a boolean series where True indicates the exact candle where
    the crossover occurred. This is useful for generating trading signals
    based on indicator crossovers.
    
    The function performs a vectorized comparison, making it efficient for
    large datasets.

More info:
    In technical analysis, crossovers often indicate potential trading signals.
    For example, when a faster moving average crosses above a slower moving average,
    it may indicate a bullish signal.

Parameters:
    - series1 (pd.Series): First input series to check for crossover (e.g., fast moving average).
    - series2 (pd.Series): Second input series to compare against (e.g., slow moving average).

Call with:
    df['cross_up'] = bta.first_crossed_above_second(df['ema5'], df['ema20'])

Returns:
    pd.Series: Boolean series where True indicates a crossover above.

## First Crossed Below Second
Name:
    First Crossed Below Second

Description:
    This function checks if the first series crosses below the second series.
    It returns a boolean series where True indicates the exact candle where
    the crossover occurred. This is useful for generating trading signals
    based on indicator crossovers.
    
    The function performs a vectorized comparison, making it efficient for
    large datasets.

More info:
    In technical analysis, crossovers often indicate potential trading signals.
    For example, when a faster moving average crosses below a slower moving average,
    it may indicate a bearish signal.

Parameters:
    - series1 (pd.Series): First input series to check for crossover (e.g., fast moving average).
    - series2 (pd.Series): Second input series to compare against (e.g., slow moving average).

Call with:
    df['cross_down'] = bta.first_crossed_below_second(df['ema5'], df['ema20'])

Returns:
    pd.Series: Boolean series where True indicates a crossover below.

## Geometric Mean
Name:
    Geometric Mean

Description:
    Calculates the rolling geometric mean of a price series over a specified window length.
    The geometric mean is defined as the nth root of the product of n numbers.
    It is less affected by extreme values than the arithmetic mean, making it useful
    for analyzing percentage changes or ratios like returns.

More info:
    https://en.wikipedia.org/wiki/Geometric_mean

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate geometric mean on. Default is 'close'.

Call with:
    df['gmean_30'] = bta.geometric_mean(df)['gmean_30']

Returns:
    pd.DataFrame: DataFrame with geometric mean values in a column named 'gmean_{length}'.

## Get Min Max
Name:
    Get Min Max

Description:
    This utility function compares two data series element by element and returns
    either the minimum or maximum value at each position, depending on the specified
    function parameter.
    
    It's particularly useful when you need to create support/resistance lines, 
    determine price extremes, or compare different indicators.

More info:
    This function uses NumPy's efficient array operations to quickly process 
    large datasets without loops.

Parameters:
    - series1 (pd.Series): First input series.
    - series2 (pd.Series): Second input series.
    - function (str): Function to apply, either "min" or "max". Default is "min".

Call with:
    df['min_values'] = bta.get_min_max(df['close'], df['sma20'], 'min')
    df['max_values'] = bta.get_min_max(df['high'], df['upper_band'], 'max')

Returns:
    pd.Series: A series containing the minimum or maximum values between the two input
    series at each position.

## Indicator Mixin
Utility mixin class for indicator calculations.

## Is Above
Name:
    Is Above Indicator

Description:
    Determines whether values in one series are greater than or equal to
    values in another series. This creates a binary indicator (or boolean) that
    can be used for generating signals or conditions in trading strategies.

More info:
    This indicator is useful for identifying when one indicator or price series
    crosses above another, which is often used as a bullish signal in technical analysis.
    Common applications include when a fast moving average crosses above a slow moving 
    average, or when price crosses above a key indicator level.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the columns specified.
    - column_a (str): The column to check if it's above column_b.
    - column_b (str): The column to compare against.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Check if the fast EMA is above the slow EMA
    df['ema_fast_above_slow'] = bta.is_above(df, 'ema_9', 'ema_21')['ema_9_above_ema_21']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 where column_a is above
    column_b, and 0 otherwise (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column_a}_above_{column_b}'.

## Is Above Value
Name:
    Is Above Value Indicator

Description:
    Determines whether values in a series are greater than or equal to
    a specified constant value. This creates a binary indicator (or boolean) that
    can be used for generating signals or conditions in trading strategies.

More info:
    This indicator is useful for identifying when a price or indicator exceeds a certain
    threshold or level, which can be used for breakout detection, overbought/oversold
    conditions, or other trading signals. It's simpler than comparing two series when
    one of the values is constant.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - column (str): The column to check if it's above the specified value.
    - value (float): The constant value to compare against.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Check if price is above a resistance level
    df['price_above_200'] = bta.is_above_value(df, 'close', 200)['close_above_200']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 where the specified column
    is above the value, and 0 otherwise (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column}_above_{value}'.

## Is Below
Name:
    Is Below Indicator

Description:
    Determines whether values in one series are less than or equal to
    values in another series. This creates a binary indicator (or boolean) that
    can be used for generating signals or conditions in trading strategies.

More info:
    This indicator is useful for identifying when one indicator or price series
    falls below another, which is often used as a bearish signal in technical analysis.
    Common applications include when a fast moving average crosses below a slow moving 
    average, or when price falls below a key support level or indicator.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the columns specified.
    - column_a (str): The column to check if it's below column_b.
    - column_b (str): The column to compare against.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Check if the fast EMA is below the slow EMA
    df['ema_fast_below_slow'] = bta.is_below(df, 'ema_9', 'ema_21')['ema_9_below_ema_21']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 where column_a is below
    column_b, and 0 otherwise (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column_a}_below_{column_b}'.

## Is Below Value
Name:
    Is Below Value Indicator

Description:
    Determines whether values in a series are less than or equal to
    a specified constant value. This creates a binary indicator (or boolean) that
    can be used for generating signals or conditions in trading strategies.

More info:
    This indicator is useful for identifying when a price or indicator falls below a certain
    threshold or level, which can be used for breakdown detection, overbought/oversold
    conditions, or other trading signals. It's simpler than comparing two series when
    one of the values is constant.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - column (str): The column to check if it's below the specified value.
    - value (float): The constant value to compare against.
    - as_int (bool): If True, returns 1 for True and 0 for False. If False, returns
      boolean values. Default is True.

Call with:
    # Check if price is below a support level
    df['price_below_50'] = bta.is_below_value(df, 'close', 50)['close_below_50']

Returns:
    pd.DataFrame: DataFrame with a single column containing 1 where the specified column
    is below the value, and 0 otherwise (if as_int=True), or boolean values (if as_int=False).
    The column is named '{column}_below_{value}'.

## Kurtosis
Name:
    Kurtosis

Description:
    Kurtosis is a statistical measure that describes the shape of a distribution's tails
    in relation to its overall shape. It quantifies whether the tails of a distribution
    contain extreme values compared to a normal distribution.
    
    In the context of financial markets:
    - High kurtosis (>3, leptokurtic): Indicates frequent extreme returns, fat tails
    - Normal kurtosis (=3, mesokurtic): Matches a normal distribution
    - Low kurtosis (<3, platykurtic): Indicates fewer extreme returns, thin tails
    
    Traders use kurtosis to:
    - Assess the risk of extreme price movements
    - Evaluate the appropriateness of normal distribution assumptions
    - Develop risk management strategies for handling outlier events

More info:
    https://www.investopedia.com/terms/k/kurtosis.asp
    https://en.wikipedia.org/wiki/Kurtosis

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the kurtosis calculation. Default is 30.
    - min_periods (int): Minimum number of observations required to calculate kurtosis.
      Default is the same as length.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.kurtosis(df, length=30)
    df['kurtosis'] = result['kurtosis']

Returns:
    pd.DataFrame: DataFrame with 'kurtosis' column containing the indicator values.

## Linear Decay
Name:
    Linear Decay

Description:
    A utility function that calculates a linear decay from a starting value to an ending value
    over a specified time period. The decay begins after the start_time and reaches the end value
    at end_time. This is particularly useful for time-based parameter adjustments in trading
    strategies, such as gradually reducing position sizes, dynamically adjusting stop-loss levels,
    or implementing time-based risk management.

More info:
    Linear decay follows the equation: 
    value = start - (start-end)/(end_time-start_time) * (current_time-start_time)
    
    The function ensures that:
    1. Decay starts only after start_time (returns start value before that)
    2. Value never goes below the end value

Parameters:
    - start (float): The starting value
    - end (float): The target end value (must be less than or equal to start)
    - start_time (int): The time (in minutes) when decay should begin
    - end_time (int): The time (in minutes) when decay should complete
    - trade_time (int): The current time (in minutes)

Call with:
    # Example: Decay a stop-loss from 2% to 1% between 30 and 120 minutes of a trade
    current_sl = bta.linear_decay(2.0, 1.0, 30, 120, minutes_in_trade)

Returns:
    float: The decayed value at the given trade_time

## Linear Growth
Name:
    Linear Growth

Description:
    A utility function that calculates a linear growth from a starting value to an ending value
    over a specified time period. The growth begins after the start_time and reaches the end value
    at end_time. This is particularly useful for time-based parameter adjustments in trading
    strategies, such as gradually increasing position sizes, dynamically adjusting take-profit levels,
    or implementing time-based risk management.

More info:
    Linear growth follows the equation: 
    value = start + (end-start)/(end_time-start_time) * (current_time-start_time)
    
    The function ensures that:
    1. Growth starts only after start_time (returns start value before that)
    2. Value never exceeds the end value

Parameters:
    - start (float): The starting value
    - end (float): The target end value (must be greater than or equal to start)
    - start_time (int): The time (in minutes) when growth should begin
    - end_time (int): The time (in minutes) when growth should complete
    - trade_time (int): The current time (in minutes)

Call with:
    # Example: Grow a take-profit from 1% to 3% between 30 and 120 minutes of a trade
    current_tp = bta.linear_growth(1.0, 3.0, 30, 120, minutes_in_trade)

Returns:
    float: The grown value at the given trade_time

## Linear Regression Slope
Name:
    Linear Regression Slope

Description:
    This indicator measures the slope of a linear regression curve, providing insights into
    the current trend's strength and momentum. It calculates a linear regression curve, 
    then derives the slope as the difference between consecutive points, smooths it using EMA,
    and creates a signal line using SMA.
    
    The indicator helps identify if a trend is accelerating or decelerating:
    - When the slope is above the signal line and positive, the uptrend is accelerating
    - When the slope is below the signal line and negative, the downtrend is accelerating
    - Other conditions indicate potential trend changes or consolidation

More info:
    This implementation is based on UCSgears' Linear Regression Slope indicator from TradingView.
    Linear regression is a statistical method used to model the relationship between variables
    by fitting a linear equation to observed data. In technical analysis, it helps identify
    the direction and momentum of price trends.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the 'close' price column.
    - curve_length (int): Number of periods for linear regression calculation. Default is 50.
    - slope_length (int): Period for EMA smoothing of the slope. Default is 5.
    - signal_length (int): Period for SMA calculation of the signal line. Default is 13.

Call with:
    # Calculate with default parameters
    lrs = bta.linear_regression_slope(df)
    df['lrs'] = lrs['lrs']       # Raw Linear Regression Slope
    df['slrs'] = lrs['slrs']     # Smoothed Linear Regression Slope (main indicator)
    df['alrs'] = lrs['alrs']     # Signal line
    df['trend'] = lrs['trend']   # Trend indicator (1: accelerating up, -1: accelerating down, 0: neutral)
    
    # Calculate with custom parameters
    lrs = bta.linear_regression_slope(df, curve_length=100, slope_length=10, signal_length=20)
    
    # Use for trading signals
    df['buy_signal'] = np.where((df['slrs'] > df['alrs']) & (df['slrs'] > 0), 1, 0)
    df['sell_signal'] = np.where((df['slrs'] < df['alrs']) & (df['slrs'] < 0), 1, 0)

Returns:
    pd.DataFrame: A DataFrame containing the following columns:
    - 'lrs': Raw Linear Regression Slope (difference between consecutive linear regression points)
    - 'slrs': Smoothed Linear Regression Slope (EMA of lrs)
    - 'alrs': Average Linear Regression Slope (SMA of slrs, signal line)
    - 'trend': Trend indicator (1: accelerating up, -1: accelerating down, 0: neutral)
    
    The first (curve_length + 1) values will contain NaNs due to the window calculations and differencing.

## Log Geometric Mean
Name:
    Logarithmic Geometric Mean

Description:
    Calculates the rolling logarithmic geometric mean of a price series over a specified window length.
    The log geometric mean is defined as exp(mean(log(x))) - 1 and is particularly useful for analyzing
    returns over multiple periods. It provides a more accurate measure of average growth rate than
    the arithmetic mean, especially when dealing with percentage changes.

More info:
    https://en.wikipedia.org/wiki/Geometric_mean#Relationship_with_logarithms

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate log geometric mean on. Default is 'close'.

Call with:
    df['log_gmean_30'] = bta.log_geometric_mean(df)['log_gmean_30']

Returns:
    pd.DataFrame: DataFrame with log geometric mean values in a column named 'log_gmean_{length}'.

## Log Return
Name:
    Log Return

Description:
    Calculates the logarithmic return of a price series. Logarithmic returns are useful
    in financial analysis because they are additive over time and better approximate
    normally distributed returns, which is important for statistical analysis.
    
    Two modes are available:
    1. Period-over-period log return (default): log(price_t / price_{t-length})
    2. Cumulative log return: log(price_t / price_0), measuring return since the beginning
    
    Log returns are especially useful for:
    - Comparing performance across different assets
    - Statistical analysis that assumes normality
    - Time series modeling and forecasting

More info:
    https://www.quantstart.com/articles/Returns-Arithmetic-and-Logarithmic/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The period for calculating returns. Default is 1.
    - cumulative (bool): If True, returns the cumulative log returns since the beginning.
      If False, returns period-over-period log returns. Default is False.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Period-over-period log returns
    result = bta.log_return(df, length=1)
    df['log_return'] = result['log_return']
    
    # Cumulative log returns
    result = bta.log_return(df, cumulative=True)
    df['cum_log_return'] = result['cum_log_return']

Returns:
    pd.DataFrame: DataFrame with 'log_return' or 'cum_log_return' column (depending on parameters).

## Mean Absolute Deviation
Name:
    Mean Absolute Deviation

Description:
    Mean Absolute Deviation (MAD) is a measure of variability that quantifies the average
    distance between each data point and the mean. Unlike standard deviation, which squares
    the differences, MAD uses the absolute differences, making it less sensitive to outliers.
    
    In financial markets, MAD can be used to:
    - Measure price volatility in a less outlier-sensitive way than standard deviation
    - Identify periods of market stability or instability
    - Develop trading systems that adapt to changing market conditions
    - Set more robust stop-loss levels that are less affected by extreme price movements
    
    The calculation is the mean of the absolute deviations from the mean: mean(|x - mean(x)|)

More info:
    https://en.wikipedia.org/wiki/Average_absolute_deviation
    https://www.investopedia.com/terms/a/absolute-deviation.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the MAD calculation. Default is 30.
    - min_periods (int): Minimum number of observations required to calculate MAD.
      Default is the same as length.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.mean_absolute_deviation(df, length=30)
    df['mad'] = result['mad']

Returns:
    pd.DataFrame: DataFrame with 'mad' column containing the indicator values.

## Median
Name:
    Median

Description:
    The Median indicator calculates the rolling median of a price series over a specified
    period. Unlike a simple moving average which can be skewed by outliers, the median
    represents the middle value in a series and is more robust to extreme values.
    
    In financial markets, the rolling median can be used to:
    - Identify the central tendency of price movements with less sensitivity to outliers
    - Filter out market noise in highly volatile conditions
    - Develop trading systems that are less affected by price spikes or flash crashes
    - Complement traditional moving averages for a more complete view of market conditions
    
    The median is often considered a more robust measure of central tendency compared to the mean
    when the price distribution contains outliers or exhibits skewness.

More info:
    https://www.incrediblecharts.com/indicators/median_price.php
    https://en.wikipedia.org/wiki/Median

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the median calculation. Default is 30.
    - min_periods (int): Minimum number of observations required to calculate median.
      Default is the same as length.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.median(df, length=30)
    df['median'] = result['median']

Returns:
    pd.DataFrame: DataFrame with 'median' column containing the indicator values.

## Month To Date
Name:
    Month-to-Date Filter

Description:
    Filters a DataFrame to include only data from the beginning of the current month
    to the present. This is useful for analyzing performance or trends within the
    current month.

More info:
    Month-to-date (MTD) is a period starting from the beginning of the current calendar
    month and continuing up to the present day. MTD information is useful for analyzing
    short-term business trends or comparing performance to previous months.

Parameters:
    - df (pandas.DataFrame): Input DataFrame with a DatetimeIndex.

Call with:
    mtd_df = bta.month_to_date(df)

Returns:
    pd.DataFrame: DataFrame filtered to contain only data from the beginning of
    the current month. If no data exists for the current month, returns the
    original DataFrame.

## Overbought Oversold
Name:
    Overbought/Oversold (OBOS) Indicator

Description:
    This function analyzes an oscillator-type indicator (like RSI, Stochastic, etc.)
    and categorizes market conditions as overbought, oversold, or in trigger states.
    It not only identifies when the indicator is currently in extreme territory but
    also detects when the indicator has recently been in extreme territory but has
    now returned to neutral levels - these are the "trigger" conditions that often
    represent good entry points.

More info:
    Oscillator indicators typically fluctuate between fixed boundaries (often 0-100)
    and help identify market extremes. Values above a certain threshold (e.g., 70-80)
    suggest overbought conditions, while values below another threshold (e.g., 20-30)
    suggest oversold conditions.
    
    The "trigger" conditions identified by this function are particularly valuable
    as they often represent potential reversal points with better risk/reward ratios
    than entering during extreme readings.

Parameters:
    - df (pd.DataFrame): The input DataFrame containing the indicator column.
    - indicator_col (str): The name of the column containing the indicator values
      (e.g., 'rsi', 'stoch_k', 'cci', etc.).
    - overbought_value (float, default=75): The threshold above which the market
      is considered overbought.
    - oversold_value (float, default=30): The threshold below which the market
      is considered oversold.
    - previous_rows (int, default=5): Number of previous rows to check when
      determining trigger conditions.

Call with:
    # Using RSI as the indicator
    df['obos'] = bta.overbought_oversold(df, indicator_col='rsi', 
                                          overbought_value=70, oversold_value=30)
    
    # Using Stochastic as the indicator
    df['stoch_obos'] = bta.overbought_oversold(df, indicator_col='stoch_k', 
                                               overbought_value=80, oversold_value=20)

Returns:
    pd.Series: A Series containing string values representing the market condition:
        - 'overbought': Current indicator value is above the overbought threshold
        - 'oversold': Current indicator value is below the oversold threshold
        - 'overbought_trigger': Indicator recently left overbought territory
        - 'oversold_trigger': Indicator recently left oversold territory
        - 'neutral': None of the above conditions are met

## Pascals Triangle
Name:
    Pascal's Triangle

Description:
    Generates a row of Pascal's Triangle, optionally weighted or inverse weighted.
    
    Pascal's Triangle is a triangular array of binomial coefficients, where each number
    is the sum of the two numbers directly above it. It has numerous applications in
    mathematics, particularly in combinatorics, probability, and algebra.
    
    This implementation can generate:
    1. The raw values of a specific row of Pascal's Triangle
    2. A weighted version where each value is divided by the sum of all values in the row
    3. An inverse weighted version (1 - weighted value)

More info:
    https://en.wikipedia.org/wiki/Pascal%27s_triangle

Parameters:
    - n (int): The row of Pascal's Triangle to generate (0-indexed). Default is 4.
    - weighted (bool): If True, returns each value divided by the sum of all values. Default is False.
    - inverse (bool): If True and weighted is True, returns 1 minus the weighted values. Default is False.

Call with:
    # Get raw Pascal's Triangle row
    df_pascal = bta.pascals_triangle(n=4)
    
    # Get weighted values
    df_weighted = bta.pascals_triangle(n=4, weighted=True)
    
    # Get inverse weighted values
    df_inverse = bta.pascals_triangle(n=4, weighted=True, inverse=True)

Returns:
    pd.DataFrame: DataFrame with a single column containing the requested values:
    - 'pascal': Raw Pascal's Triangle values
    - 'pascal_weights': Weighted values if weighted=True
    - 'pascal_inverse_weights': Inverse weighted values if weighted=True and inverse=True

## Percent Return
Name:
    Percent Return

Description:
    Calculates the percentage return of a price series, which measures the change in value
    of an asset or investment as a percentage of the initial investment.
    
    Two modes are available:
    1. Period-over-period percent return (default): (price_t / price_{t-length}) - 1
    2. Cumulative percent return: (price_t / price_0) - 1, measuring total return since the beginning
    
    Percentage returns are commonly used in finance for:
    - Performance measurement and comparison
    - Risk assessment
    - Investment decision making
    - Portfolio analysis

More info:
    https://www.investopedia.com/terms/r/return.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The period for calculating returns. Default is 1.
    - cumulative (bool): If True, returns the cumulative percentage returns since the beginning.
      If False, returns period-over-period percentage returns. Default is False.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Period-over-period percent returns
    result = bta.percent_return(df, length=1)
    df['percent_return'] = result['percent_return']
    
    # Cumulative percent returns
    result = bta.percent_return(df, cumulative=True)
    df['cum_percent_return'] = result['cum_percent_return']

Returns:
    pd.DataFrame: DataFrame with 'percent_return' or 'cum_percent_return' column (depending on parameters).

## Populate Leledc Major Minor
Name:
    Populate LELEDC Major and Minor

Description:
    LELEDC (Length and Extreme for Low Exhaustion and Determining Cycle) is an
    indicator system that identifies potential exhaustion points in price action.
    This function calculates both major and minor cycle signals based on quality
    parameters and specific price patterns.
    
    The major cycle identifies significant trend changes while the minor cycle
    identifies smaller retracements and continuations within the larger trend.
    
    LELEDC is particularly useful for identifying potential reversal points and
    for determining market cycles.

More info:
    The algorithm tracks consecutive movements in a specific direction and generates
    signals when price makes an extreme move (new high/low) after a sufficient number
    of consecutive moves in one direction, combined with a reversal candle pattern.
    
    Major signals (1/-1) indicate potential significant trend changes.
    Minor signals (1/-1) indicate smaller retracements or continuation patterns.

Parameters:
    - df (pd.DataFrame): Input DataFrame with OHLC price data.
    - maj_qual (np.ndarray): Array of major quality thresholds for each bar.
    - min_qual (np.ndarray): Array of minor quality thresholds for each bar.
    - maj_len (int): Lookback length for major cycle high/low comparisons.
    - min_len (int): Lookback length for minor cycle high/low comparisons.

Call with:
    # Usually used after calculating quality values and lengths:
    maj_qual, min_qual = bta.exhaustion_candles(df)
    maj_len, min_len = bta.exhaustion_lengths(df)
    
    result = bta.populate_leledc_major_minor(df, maj_qual, min_qual, maj_len, min_len)
    df['leledc_major'] = result['leledc_major']
    df['leledc_minor'] = result['leledc_minor']

Returns:
    pd.DataFrame: DataFrame with two columns:
    - 'leledc_major': Major cycle signals (1, -1, or NaN)
    - 'leledc_minor': Minor cycle signals (1, -1, or 0)

## Pump Dump Protection
Name:
    Pump and Dump Protection

Description:
    This indicator helps detect potential pump-and-dump schemes in cryptocurrency markets
    by monitoring abnormal volume activity and rapid price movements. It calculates several
    metrics including short and long-term volume averages, the relative change in volume,
    and the RSI to identify suspicious market behavior.
    
    Pump-and-dump schemes typically involve artificially inflating an asset's price through
    false recommendations and heavy volume (the "pump") followed by selling off shares at
    the higher price (the "dump"). This indicator can help traders avoid being caught in
    such manipulative schemes.

More info:
    Key warning signs that this indicator identifies:
    - Abnormal increases in trading volume (compared to recent history)
    - Extreme RSI values indicating overbought conditions
    - Sudden, dramatic price increases with volume spikes
    
    When the indicator detects these conditions, it sets the 'pnd_volume_warn' flag to -1,
    suggesting caution and potential manipulation in the market.

Parameters:
    - df (pd.DataFrame): Input DataFrame with required OHLCV columns.
    - rsi_period (int, default=14): Period for RSI calculation.
    - short_volume_window (int, default=4): Period for short-term volume average.
    - long_volume_window (int, default=48): Period for long-term volume average.
    - volume_warn_threshold (float, default=5.0): Threshold for volume spike warning.

Call with:
    # Get pump and dump protection indicators
    pnd_data = bta.pump_dump_protection(
        df,
        rsi_period=14,
        short_volume_window=6,
        long_volume_window=72,
        volume_warn_threshold=4.0
    )
    
    # Add results to the original dataframe
    df['vol_short'] = pnd_data['volume_mean_short']
    df['vol_long'] = pnd_data['volume_mean_long']
    df['vol_change'] = pnd_data['volume_change_percentage']
    df['rsi'] = pnd_data['rsi']
    df['pnd_warning'] = pnd_data['pnd_volume_warn']

Returns:
    pd.DataFrame: A DataFrame with the following columns:
    - 'volume_mean_short': Short-term volume average
    - 'volume_mean_long': Long-term volume average
    - 'volume_change_percentage': Ratio between short and long-term volume
    - 'rsi': Relative Strength Index values
    - 'pnd_volume_warn': Warning flag (-1 for potential pump-and-dump, 0 otherwise)

## Quantile
Name:
    Quantile

Description:
    The Quantile indicator calculates the specified quantile of a price series over a rolling
    window. Quantiles divide a dataset into equal parts, with the quantile value representing
    the threshold that divides the data in the specified proportion.
    
    Common quantiles include:
    - 0.5 (median): The middle value, dividing the dataset into two equal halves
    - 0.25 (first quartile): Divides the bottom 25% from the top 75%
    - 0.75 (third quartile): Divides the bottom 75% from the top 25%
    
    In financial markets, rolling quantiles can be used to:
    - Identify price levels that are historically significant
    - Develop trading systems based on statistical thresholds
    - Create adaptive indicators that adjust to changing market conditions
    - Filter outliers by focusing on specific segments of the price distribution

More info:
    https://en.wikipedia.org/wiki/Quantile
    https://www.investopedia.com/terms/q/quantile.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which must contain the specified column.
    - length (int): The rolling window period for the quantile calculation. Default is 30.
    - q (float): The quantile to calculate, must be between 0 and 1. Default is 0.5 (median).
    - min_periods (int): Minimum number of observations required to calculate the quantile.
      Default is the same as length.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    # Calculate the median (50th percentile)
    result = bta.quantile(df, length=30, q=0.5)
    df['quantile_0_5'] = result['quantile_0_5']
    
    # Calculate the first quartile (25th percentile)
    result = bta.quantile(df, length=30, q=0.25)
    df['quantile_0_25'] = result['quantile_0_25']

Returns:
    pd.DataFrame: DataFrame with a quantile column (name depends on the q parameter).

## Quarter To Date
Name:
    Quarter-to-Date Filter

Description:
    Filters a DataFrame to include only data from the beginning of the current quarter
    to the present. This is useful for analyzing quarterly performance or trends.
    
    Quarters are defined as:
    - Q1: January, February, March
    - Q2: April, May, June
    - Q3: July, August, September
    - Q4: October, November, December

More info:
    Quarter-to-date (QTD) is a period starting from the beginning of the current fiscal
    quarter and continuing up to the present day. QTD information is useful for analyzing
    medium-term business trends or comparing performance to previous quarters.

Parameters:
    - df (pandas.DataFrame): Input DataFrame with a DatetimeIndex.

Call with:
    qtd_df = bta.quarter_to_date(df)

Returns:
    pd.DataFrame: DataFrame filtered to contain only data from the beginning of
    the current quarter. If no data exists for the current quarter, returns the
    original DataFrame.

## Regression Slope
Name:
    Regression Slope

Description:
    This function calculates the slope of a linear regression line fitted to price data
    over a specified lookback period. The slope indicates the rate of change of price
    and can be used to identify the strength and direction of a trend.
    
    A positive slope indicates an uptrend, while a negative slope indicates a downtrend.
    The steepness of the slope corresponds to the strength of the trend.

More info:
    Linear regression is a statistical method used to model the relationship between
    a dependent variable (price) and an independent variable (time). In technical analysis,
    the slope of the regression line provides valuable information about trend direction
    and strength.
    
    The calculation uses the least squares method to find the line that minimizes the
    sum of squared distances between the line and the actual price points.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the 'close' price column.
    - lookback_period (int): Number of periods to use for the regression calculation.
      Default is 20.

Call with:
    # Calculate regression slope with default 20-period lookback
    result = bta.regression_slope(df)
    df['reg_slope'] = result['slope']
    
    # Calculate regression slope with custom lookback
    result = bta.regression_slope(df, lookback_period=50)
    df['reg_slope_50'] = result['slope']
    
    # Use with other indicators
    df['slope_signal'] = np.where(df['reg_slope'] > 0, 1, -1)

Returns:
    pd.DataFrame: A DataFrame containing the regression slope values in the 'slope' column.
    The first (lookback_period - 1) values will be NaN.

## Same Length
Name:
    Same Length

Description:
    This utility function ensures that two arrays have the same length by padding
    the shorter array with NaN values at the beginning. This is particularly useful
    when working with technical indicators that have different lookback periods,
    resulting in arrays of different lengths that need to be aligned for calculations
    or visualization.

More info:
    When calculating technical indicators, the initial periods often result in NaN values
    due to insufficient data for the calculation. Different indicators may have different
    lookback periods, resulting in varying numbers of initial NaN values. This function
    helps align these indicators by padding the shorter array appropriately.

Parameters:
    - bigger (np.ndarray): The array with the larger size.
    - shorter (np.ndarray): The array with the smaller size.

Call with:
    # Example: Aligning EMA with different periods
    ema_short = calculate_ema(df['close'], period=5)  # Has fewer NaN values
    ema_long = calculate_ema(df['close'], period=20)  # Has more NaN values
    aligned_ema_short = bta.same_length(ema_long, ema_short)

Returns:
    np.ndarray: The shorter array padded with NaN values at the beginning to match
    the size of the bigger array.

## Sharpe Ratio
Name:
    Sharpe Ratio

Description:
    Calculates the Sharpe ratio, which measures the performance of an investment 
    compared to a risk-free asset, after adjusting for its risk. It's defined as 
    the excess return per unit of deviation (typically standard deviation) of an
    investment asset or portfolio.

More info:
    The Sharpe ratio was developed by Nobel laureate William F. Sharpe and is used
    to help investors understand the return of an investment compared to its risk.
    The ratio is the average return earned in excess of the risk-free rate per unit
    of volatility or total risk.
    
    A higher Sharpe ratio indicates a better risk-adjusted performance.
    Generally, a Sharpe ratio greater than 1.0 is considered acceptable.
    A ratio higher than 2.0 is considered very good.
    A ratio of 3.0 or higher is considered excellent.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - benchmark_rate (float): The risk-free rate to compare against. Default is 0.0.
    - use_log_returns (bool): If True, uses logarithmic returns instead of percentage
      returns for calculation. Default is False.
    - use_cagr (bool): If True, uses CAGR (Compound Annual Growth Rate) instead of
      simple annualized returns for calculation. Default is False.
    - trading_days_per_year (int): Number of trading days in a year, used for
      annualizing returns and volatility. Default is 252.
    - column (str): The column to calculate the Sharpe ratio on. Default is 'close'.

Call with:
    sharpe_result = bta.sharpe_ratio(df, benchmark_rate=0.02)
    df['sharpe'] = sharpe_result['sharpe_ratio'][0]  # Extract single value

Returns:
    pd.DataFrame: DataFrame with a single row containing the Sharpe ratio value in
    a column named 'sharpe_ratio'.

## Skew
Name:
    Rolling Skew

Description:
    Calculates the rolling skew of a price series over a specified window length.
    Skew measures the asymmetry of the distribution of returns around its mean.
    Positive skew indicates a distribution with a long right tail, while negative 
    skew indicates a distribution with a long left tail.

More info:
    https://en.wikipedia.org/wiki/Skewness

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate skew on. Default is 'close'.

Call with:
    df['skew_30'] = bta.skew(df)['skew_30']

Returns:
    pd.DataFrame: DataFrame with skew values in a column named 'skew_{length}'.

## St Dev
Name:
    Standard Deviation

Description:
    Standard Deviation is a statistical measure of volatility or dispersion from a central value (mean).
    In finance, it's used to measure market volatility and asset price dispersion.
    Higher values indicate greater volatility and potentially higher risk.

More info:
    https://www.investopedia.com/terms/s/standarddeviation.asp

Parameters:
    - series (pd.Series): The data series to calculate the standard deviation for.
    - period (int): The period over which to calculate the standard deviation.

Call with:
    df['std_dev'] = bta.st_dev(df['close'], period=14)

Returns:
    pd.Series: The rolling standard deviation of the series over the specified period.

## Symmetric Triangle
Name:
    Symmetric Triangle

Description:
    Generates a symmetric triangular array of values, optionally weighted.
    
    The Symmetric Triangle is an array where values increase from both ends towards
    the middle. For even values of n, the middle two values are equal. For odd values
    of n, there is a single peak in the middle.
    
    Examples:
    - n=4: [1, 2, 2, 1]
    - n=5: [1, 2, 3, 2, 1]
    
    These triangular arrays are frequently used as weighting schemes in technical
    indicators like weighted moving averages, where you want to place more emphasis
    on the middle values and less on the ends.

More info:
    This is a common structure used in various technical analysis weighting schemes.

Parameters:
    - n (int): The size of the array to generate. Must be greater than or equal to 2. Default is 4.
    - weighted (bool): If True, returns each value divided by the sum of all values,
      making the weights sum to 1. Default is False.

Call with:
    # Get raw symmetric triangle
    df_tri = bta.symmetric_triangle(n=4)
    
    # Get weighted values
    df_weighted = bta.symmetric_triangle(n=4, weighted=True)

Returns:
    pd.DataFrame: DataFrame with a single column containing the requested values:
    - 'symtri': Raw symmetric triangle values
    - 'symtri_weights': Weighted values if weighted=True

## Top Percent Change
Name:
    Top Percent Change

Description:
    This indicator calculates the percentage change between a price and a reference price.
    When length=0, it measures the percent difference between the open and close of the current bar.
    When length>0, it measures the percent difference between the maximum open price over the
    lookback period and the current close price.
    
    The indicator is useful for identifying potential reversal points after significant price movements
    and can be used in momentum and mean-reversion strategies.

More info:
    https://www.investopedia.com/terms/p/percentage-change.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing OHLC data with required columns:
        'open' and 'close'.
    - length (int, default=0): Lookback period for calculating the range maximum. If 0,
      calculates the percentage change between the current open and close prices.

Call with:
    df['percent_change'] = bta.top_percent_change(df, length=3)

Returns:
    pd.Series: A Series representing the percentage change for each row in the DataFrame.

## Tos Standard Deviation All
Name:
    TD Ameritrade's Think or Swim Standard Deviation All

Description:
    A port of TD Ameritrade's Think or Swim Standard Deviation All indicator which
    returns the standard deviation of data for the entire plot or for the interval
    of the last bars defined by the length parameter.
    
    This indicator creates a linear regression line along with upper and lower bands
    at specified standard deviation levels. It can be used to identify potential
    price targets and areas of support and resistance.

More info:
    https://tlc.thinkorswim.com/center/reference/thinkScript/Functions/Statistical/StDevAll

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int, optional): Number of bars from current bar to use for calculations.
      If None, all available data is used. Default is None.
    - stds (list, optional): List of Standard Deviations in ascending order from the
      central Linear Regression line. Default is [1, 2, 3].
    - ddof (int): Delta Degrees of Freedom. The divisor used in calculations is N - ddof,
      where N represents the number of elements. Default is 1.
    - column (str): The column to calculate on. Default is 'close'.

Call with:
    tos_sd = bta.tos_standard_deviation_all(df)
    df['tos_lr'] = tos_sd['TOS_STDEVALL_LR']
    df['tos_lower_1'] = tos_sd['TOS_STDEVALL_L_1']
    df['tos_upper_1'] = tos_sd['TOS_STDEVALL_U_1']
    # ...and so on for other bands

Returns:
    pd.DataFrame: DataFrame with columns for the central linear regression line and
    pairs of lower and upper bands based on multiples of the standard deviation.

## Variance
Name:
    Rolling Variance

Description:
    Calculates the rolling variance of a price series over a specified window length.
    Variance measures how far a set of numbers is spread out from their average value.
    It is the square of the standard deviation.

More info:
    https://en.wikipedia.org/wiki/Variance

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the column specified.
    - length (int): The window size for the rolling calculation. Default is 30.
    - ddof (int): Delta Degrees of Freedom. The divisor used in calculations is N - ddof, 
      where N represents the number of elements. Default is 1.
    - min_periods (int, optional): Minimum number of observations required to calculate
      a value. If None, defaults to the length parameter value.
    - column (str): The column to calculate variance on. Default is 'close'.

Call with:
    df['var_30'] = bta.variance(df)['var_30']

Returns:
    pd.DataFrame: DataFrame with variance values in a column named 'var_{length}'.

## Year To Date
Name:
    Year-to-Date Filter

Description:
    Filters a DataFrame to include only data from the beginning of the current year
    to the present. This is useful for analyzing performance or trends within the
    current calendar year.

More info:
    Year-to-date (YTD) is a period starting from the beginning of the current calendar
    year and continuing up to the present day. YTD information is useful for analyzing
    business trends over time or comparing performance to previous years.

Parameters:
    - df (pandas.DataFrame): Input DataFrame with a DatetimeIndex.

Call with:
    ytd_df = bta.year_to_date(df)

Returns:
    pd.DataFrame: DataFrame filtered to contain only data from the beginning of
    the current year. If no data exists for the current year, returns the
    original DataFrame.

## Z Score
Name:
    Z-Score

Description:
    The Z-Score measures how many standard deviations a data point is from the mean 
    of a dataset. In finance, it helps identify when prices or indicators are statistically 
    abnormal relative to their historical values.
    
    A Z-Score of 0 means the value is exactly at the mean. Positive Z-Scores indicate
    values above the mean, while negative Z-Scores indicate values below the mean.
    
    Typical interpretation:
    - Z-Score > 2: Significantly higher than normal (potentially overbought)
    - Z-Score < -2: Significantly lower than normal (potentially oversold)

More info:
    https://www.investopedia.com/terms/z/zscore.asp

Parameters:
    - series (pd.Series): Input series of values to analyze.
    - window (int, default=500): Lookback window for calculating the mean and standard deviation.

Call with:
    df['zscore'] = bta.z_score(df['close'], window=200)

Returns:
    pd.Series: The Z-Score values for each point in the input series.

Important Notes:
    - This function requires a numeric Series as input and will raise an error 
      if provided with non-numeric data such as datetime values.
    
    - Error "Cannot aggregate non-numeric type: datetime64[ns]" may occur if you 
      inadvertently pass the date/timestamp column as input.
    
    - Always ensure you're passing a price series (like 'close', 'high', 'low') 
      or another numeric indicator, not the date index.
    
    - If you want to apply Z-Score to a datetime-based feature (e.g., time of day patterns),
      convert it to a numeric value first:
      ```python
      # Convert time of day to seconds from midnight
      seconds_series = df.index.map(lambda x: x.hour * 3600 + x.minute * 60 + x.second)
      df['time_zscore'] = bta.z_score(seconds_series)
      ```
    
    - For testing purposes, make sure to use a numeric column from the test DataFrame.

# Volatility

## Aberration Bands
Name:
    Aberration Bands (ABER)

Description:
    Aberration Bands are a volatility-based indicator similar to Keltner Channels.
    The indicator consists of three bands:
    - Middle band: Simple Moving Average of the typical price (HLC3)
    - Upper band: Middle band + Average True Range
    - Lower band: Middle band - Average True Range
    
    These bands can be used to identify overbought and oversold conditions,
    as well as potential breakout opportunities when price moves outside the bands.

More info:
    There are few definitive resources on this indicator, as it is less commonly used
    than other volatility-based bands like Bollinger Bands or Keltner Channels.

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for the SMA calculation. Default is 5.
    - atr_length (int): The period for the ATR calculation. Default is 15.

Call with:
    result = bta.aberration_bands(df)
    df['aber_middle'] = result['aber_middle']
    df['aber_upper'] = result['aber_upper']
    df['aber_lower'] = result['aber_lower']
    df['aber_atr'] = result['aber_atr']

Returns:
    pd.DataFrame: DataFrame with 'aber_middle', 'aber_upper', 'aber_lower', and 'aber_atr' columns.

## Acceleration Bands
Name:
    Acceleration Bands (ACCBANDS)

Description:
    Acceleration Bands, created by Price Headley, are volatility-based envelopes
    plotted above and below a simple moving average. The bands are based on a multiple
    of the high-low range, adjusted by the sum of the high and low.
    
    The bands widen and narrow based on market volatility, providing potential
    overbought and oversold levels. They can be used to identify potential
    price targets for trending markets or potential reversal points when the price
    reaches the upper or lower bands.

More info:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/acceleration-bands-abands/
    https://library.tradingtechnologies.com/trade/chrt-ti-acceleration-bands.html

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for the moving average calculation. Default is 20.
    - c (float): The multiplier for the high-low ratio. Default is 4.0.
    - ma_type (str): The type of moving average to use ('SMA' or 'EMA'). Default is 'SMA'.

Call with:
    result = bta.acceleration_bands(df)
    df['accbands_lower'] = result['accbands_lower']
    df['accbands_middle'] = result['accbands_middle']
    df['accbands_upper'] = result['accbands_upper']

Returns:
    pd.DataFrame: DataFrame with 'accbands_lower', 'accbands_middle', and 'accbands_upper' columns.

## Average True Range
Name:
    Average True Range (ATR)

Description:
    The Average True Range (ATR), smoothed by the Moving Average, is a measure of volatility. 
    It was introduced by Welles Wilder in his book 'New Concepts in Technical Trading Systems'.
    ATR is a volatility indicator that measures market volatility by decomposing the entire
    range of an asset price for a specific period.

More info:
    https://www.investopedia.com/terms/a/atr.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high', 'low', and 'close'.
    - period (int): Period for the ATR calculation. Default is 14.

Call with:
    df['atr'] = bta.average_true_range(df, 14)['atr']

Returns:
    pd.DataFrame: DataFrame with 'atr' column.

## Bbw Expansion
Name:
    Bollinger Band Width (BBW) Expansion Detector

Description:
    Detects if the Bollinger Band Width (BBW) of the last observation exceeds a 
    rolling maximum by a specified multiplier. This can signal a potential increase 
    in market volatility. The Bollinger Band Width is calculated as 
    (Upper Band - Lower Band) / Middle Band, and is a measure of volatility.
    This indicator requires the bta.bollinger_bands function to be used in the dataframe too.

More info:
    https://tradingview.com/support/solutions/43000501971-bollinger-bands-width/

Parameters:
    - df (pd.DataFrame): Input DataFrame containing Bollinger Band columns.
    - upper_band (str): Column name for the upper Bollinger Band. Default is 'bb_upper'.
    - lower_band (str): Column name for the lower Bollinger Band. Default is 'bb_lower'.
    - middle_band (str): Column name for the middle Bollinger Band. Default is 'bb_middle'.
    - mult (float): Multiplier to compare the last BBW value against the rolling maximum. Default is 1.05.
    - rolling_window (int): Rolling window size for calculating the maximum BBW. Default is 20.

Call with:
    df['bbw_expansion'] = bta.bbw_expansion(df, upper_band='bb_upper', lower_band='bb_lower', 
                                           middle_band='bb_middle', mult=1.05, rolling_window=20)['bbw_expansion']

Returns:
    pd.DataFrame: DataFrame with additional columns:
        - 'bb_width': Bollinger Band Width values.
        - 'bbw_expansion': Indicator for expansion (1 if condition met, 0 otherwise).

Important Notes:
    - This function REQUIRES that your DataFrame already contains Bollinger Bands columns:
      * Upper band column (default name: 'bb_upper')
      * Lower band column (default name: 'bb_lower')
      * Middle band column (default name: 'bb_middle')
    
    - These columns must be generated first using the bollinger_bands function:
      ```
      bb_df = bta.bollinger_bands(df)
      df['bb_upper'] = bb_df['upper']
      df['bb_middle'] = bb_df['middle']
      df['bb_lower'] = bb_df['lower']
      ```
    
    - The function will fail with a KeyError if the required Bollinger Band columns are missing.
    
    - For testing purposes, you might need to create a wrapper that calculates
      Bollinger Bands before calling this function.

## Bollinger Bands
Name:
    Bollinger Bands (BBANDS)

Description:
    Bollinger Bands are a type of statistical chart characterizing the prices and 
    volatility over time of a financial instrument or commodity. Bollinger Bands 
    consist of three lines: a middle band (SMA), an upper band, and a lower band.
    The upper and lower bands are calculated by adding and subtracting a standard
    deviation multiple from the middle band.

More info:
    https://www.investopedia.com/terms/b/bollingerbands.asp

Parameters:
    - df (pandas.DataFrame): DataFrame containing the data.
    - column (str): The column name on which the BBANDS is to be applied. Default is 'close'.
    - period (int): Look-back period to compute the moving average. Default is 20.
    - std_dev (float): Number of standard deviations to compute the upper and lower bands. Default is 2.0.
    - ddof (int): Degrees of Freedom to use in standard deviation calculation. Default is 0.

Call with:
    bb_result = bta.bollinger_bands(df, 'close', 20, 2, 0)
    df['bb_upper'] = bb_result['bb_upper']
    df['bb_middle'] = bb_result['bb_middle']
    df['bb_lower'] = bb_result['bb_lower']

Returns:
    pd.DataFrame: DataFrame with 'bb_upper', 'bb_middle', 'bb_lower' columns.

## Bollinger Bands Nadaraya Smoothed
Name:
    Bollinger Bands (Nadaraya Smoothed)

Description:
    This indicator implements Bollinger Bands with Nadaraya-Watson kernel smoothing.
    It creates multiple levels of Bollinger Bands using different periods and standard
    deviation multipliers, then applies Gaussian kernel smoothing to create smoother,
    less noisy band lines.
    
    The Nadaraya-Watson estimator is a non-parametric regression technique that uses
    a Gaussian kernel to weight nearby observations. This creates smoother bands that
    are less prone to whipsaws while maintaining responsiveness to price changes.
    
    The indicator provides four levels of bands:
    - Level 1: Short-term bands (default: 20 period, 3 std dev)
    - Level 2: Medium-term bands (default: 75 period, 3 std dev) 
    - Level 3: Long-term bands (default: 100 period, 4 std dev)
    - Level 4: Extended bands (default: 100 period, 4.25 std dev)
    
    **Note on TradingView Differences:**
    The calculations in this Python implementation may produce slightly different 
    values compared to the original TradingView Pine Script version due to differences 
    in floating-point precision, rounding methods, and internal mathematical libraries 
    between Python (NumPy/Pandas) and Pine Script. Additionally, the default lookback 
    period has been reduced from 499 to 100 bars for improved performance, which may 
    result in less smoothing compared to the TradingView version. For exact TradingView 
    matching, use n=499, though this will significantly increase computation time.

More info:
    Based on Flux Charts' TradingView indicator
    https://www.tradingview.com/script/v/bollinger-bands-nadaraya-smoothed/
    
    Nadaraya-Watson Estimator:
    https://en.wikipedia.org/wiki/Kernel_regression

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close' columns.
    - h (float): Smoothing factor (bandwidth) for the Nadaraya-Watson estimator. Higher values = more smoothing. Default is 6.0.
    - short_period (int): Period for short-term Bollinger Bands. Default is 20.
    - short_stdev (float): Standard deviation multiplier for short-term bands. Default is 3.0.
    - med_period (int): Period for medium-term Bollinger Bands. Default is 75.
    - med_stdev (float): Standard deviation multiplier for medium-term bands. Default is 4.0.
    - long_period (int): Period for long-term Bollinger Bands. Default is 100.
    - long_stdev (float): Standard deviation multiplier for long-term bands. Default is 4.25.
    - n (int): Number of historical bars to consider for smoothing. Default is 100 (reduced from 499 for performance).

Call with:
    result = bta.bollinger_bands_nadaraya_smoothed(df)
    df['bb_upper_1'] = result['bb_upper_1']
    df['bb_lower_1'] = result['bb_lower_1']
    df['bb_upper_2'] = result['bb_upper_2']
    df['bb_lower_2'] = result['bb_lower_2']
    df['bb_upper_3'] = result['bb_upper_3']
    df['bb_lower_3'] = result['bb_lower_3']
    df['bb_upper_4'] = result['bb_upper_4']
    df['bb_lower_4'] = result['bb_lower_4']
    df['upper_band_break'] = result['upper_band_break']
    df['lower_band_break'] = result['lower_band_break']

Returns:
    pd.DataFrame: DataFrame with the following columns:
    - 'bb_upper_1', 'bb_lower_1': Level 1 smoothed Bollinger Bands (main bands)
    - 'bb_upper_2', 'bb_lower_2': Level 2 smoothed Bollinger Bands
    - 'bb_upper_3', 'bb_lower_3': Level 3 smoothed Bollinger Bands
    - 'bb_upper_4', 'bb_lower_4': Level 4 smoothed Bollinger Bands
    - 'upper_band_break': Signal when price breaks above main upper band (1/0)
    - 'lower_band_break': Signal when price breaks below main lower band (1/0)
    - 'typical_price': HLC3 typical price used for calculations

## Donchian Channel
Name:
    Donchian Channel

Description:
    The Donchian Channel is a volatility indicator composed of three lines: 
    an upper band, a middle band, and a lower band. The upper band represents 
    the highest price of a security over a specified period, while the lower band 
    represents the lowest price. The middle band is simply the average of the 
    upper and lower bands.
    
    Donchian Channels are used to identify potential breakouts, determine market 
    volatility, and identify trend strength. They are particularly popular in trend-following 
    systems like the Turtle Trading system.

More info:
    https://www.investopedia.com/terms/d/donchianchannels.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high' and 'low'.
    - period (int): The lookback period to calculate the highest high and lowest low. Default is 20.

Call with:
    dc_result = bta.donchian_channel(df, 20)
    df['dc_upper'] = dc_result['dc_upper']
    df['dc_middle'] = dc_result['dc_middle']
    df['dc_lower'] = dc_result['dc_lower']
    df['dc_width'] = dc_result['dc_width']

Returns:
    pd.DataFrame: DataFrame with 'dc_upper', 'dc_middle', 'dc_lower', and 'dc_width' columns.

## Hurst Winter Channel
Name:
    Hurst-Winter Channel (HWC)

Description:
    The Hurst-Winter Channel (HWC) is a volatility-based channel indicator based on 
    the Holt-Winters triple exponential smoothing method. It creates a middle line using 
    the Holt-Winters Moving Average (HWMA) and upper/lower bands based on price deviation.
    
    The channel adapts to price movements using four smoothing parameters (na, nb, nc, nd)
    and can be adjusted with a scalar multiplier. It can also provide channel width and
    relative price position information for additional analysis.
    
    The Holt-Winters method is particularly good at capturing trends, seasonality, and
    adapting to changes in volatility, making this channel useful for identifying potential
    support/resistance levels and overbought/oversold conditions.

More info:
    https://www.mql5.com/en/code/20857
    https://en.wikipedia.org/wiki/Exponential_smoothing#Triple_exponential_smoothing

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - na (float): Parameter of the equation that describes a smoothed series (from 0 to 1). Default is 0.2.
    - nb (float): Parameter of the equation to assess the trend (from 0 to 1). Default is 0.1.
    - nc (float): Parameter of the equation to assess seasonality (from 0 to 1). Default is 0.1.
    - nd (float): Parameter of the channel equation (from 0 to 1). Default is 0.1.
    - scalar (float): Multiplier for the width of the channel calculated. Default is 1.0.
    - channel_eval (bool): Whether to return width and percentage price position metrics. Default is False.
    - column (str): The column name to use for calculations. Default is 'close'.

Call with:
    result = bta.hurst_winter_channel(df)
    df['hwc_middle'] = result['hwc_middle']
    df['hwc_upper'] = result['hwc_upper']
    df['hwc_lower'] = result['hwc_lower']
    
    # If channel_eval is True:
    df['hwc_width'] = result['hwc_width']
    df['hwc_pct_width'] = result['hwc_pct_width']

Returns:
    pd.DataFrame: DataFrame with 'hwc_middle', 'hwc_upper', 'hwc_lower' columns,
                  and optionally 'hwc_width' and 'hwc_pct_width' if channel_eval is True.

## Keltner Channel
Name:
    Keltner Channel

Description:
    The Keltner Channel is a volatility-based indicator that consists of three lines: 
    a middle line (typically an EMA), an upper band, and a lower band. The upper and 
    lower bands are calculated by adding and subtracting a multiple of the Average 
    True Range (ATR) from the middle line. 
    
    Unlike Bollinger Bands which use standard deviation, Keltner Channels use ATR, 
    making them more responsive to volatility changes based on trading ranges 
    rather than closing prices.

More info:
    https://www.investopedia.com/terms/k/keltnerchannel.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns 'high', 'low', and 'close'.
    - column (str): The column name to use for the middle line calculation. Default is 'close'.
    - ema_length (int): Period for the EMA calculation for the middle line. Default is 20.
    - atr_length (int): Period for the ATR calculation. Default is 10.
    - atr_mult (float): Multiplier for the ATR to determine the channel width. Default is 2.0.

Call with:
    kc_result = bta.keltner_channel(df, 'close', 20, 10, 2.0)
    df['kc_middle'] = kc_result['kc_middle']
    df['kc_upper'] = kc_result['kc_upper']
    df['kc_lower'] = kc_result['kc_lower']
    df['kc_width'] = kc_result['kc_width']

Returns:
    pd.DataFrame: DataFrame with 'kc_middle', 'kc_upper', 'kc_lower', and 'kc_width' columns.

## Mass Index
Name:
    Mass Index (MASSI)

Description:
    The Mass Index is a non-directional volatility indicator that utilizes the
    High-Low Range to identify trend reversals based on range expansions.
    
    Unlike many other technical indicators, the Mass Index doesn't follow price
    direction but instead identifies reversals by tracking changes in the range 
    between high and low prices. A Mass Index above 27 followed by a drop below 
    26.5 is often considered a "reversal bulge" signaling a potential trend change.
    
    The indicator is based on the idea that reversals are often preceded by 
    widening ranges as volatility increases, followed by narrowing ranges as 
    the market prepares to reverse.

More info:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:mass_index

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - fast_length (int): The period for the first and second EMA calculations. Default is 9.
    - slow_length (int): The period for summing the EMA ratio. Default is 25.

Call with:
    result = bta.mass_index(df)
    df['mass_index'] = result['mass_index']

Returns:
    pd.DataFrame: DataFrame with 'mass_index' column.

## Normalized Average True Range
Name:
    Normalized Average True Range (NATR)

Description:
    The Normalized Average True Range (NATR) is a modification of the Average True Range
    (ATR) indicator that attempts to normalize the average true range by dividing it by 
    the closing price and multiplying by a scalar (usually 100).
    
    Unlike the ATR, which is an absolute value that can vary significantly across different
    securities based on their price, the NATR expresses volatility as a percentage of the
    closing price. This makes it easier to compare volatility across different securities
    regardless of their price levels.
    
    The NATR is useful for:
    - Comparing volatility across different securities
    - Setting position sizes based on volatility
    - Identifying periods of high or low volatility

More info:
    https://www.tradingtechnologies.com/help/x-study/technical-indicator-definitions/normalized-average-true-range-natr/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): The period for calculating ATR. Default is 14.
    - scalar (float): Multiplier to scale the result (typically 100 for percentage). Default is 100.
    - column (str): The column name to use for normalization. Default is 'close'.

Call with:
    result = bta.normalized_average_true_range(df)
    df['natr'] = result['natr']

Returns:
    pd.DataFrame: DataFrame with 'natr' column.

## Percentage Distance
Name:
    Price Distance (PDIST)

Description:
    The Price Distance indicator measures the "distance" covered by price movements.
    It considers not only the high-low range, but also the relationship between opening
    and closing prices, both current and from a previous period (drift).
    
    This indicator is useful for analyzing volatility and understanding the magnitude
    of price movements within a given period. High PDIST values indicate more significant
    price movement or volatility, while low values indicate more stable or range-bound
    price action.
    
    The calculation weighs the high-low range more heavily (multiplier of 2) to emphasize
    the overall range of the period.

More info:
    https://www.prorealcode.com/prorealtime-indicators/pricedistance/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'open', 'high', 'low', and 'close' columns.
    - drift (int): The difference period for comparing with previous closes. Default is 1.

Call with:
    result = bta.percentage_distance(df)
    df['pdist'] = result['pdist']

Returns:
    pd.DataFrame: DataFrame with 'pdist' column.

## Relative Volatility Index
Name:
    Relative Volatility Index (RVI)

Description:
    The Relative Volatility Index (RVI) was created by Donald Dorsey in 1993 and 
    revised in 1995. It's a volatility indicator that works similarly to the 
    Relative Strength Index (RSI) but uses standard deviation instead of price changes.
    
    Instead of adding up price changes like RSI based on price direction, the RVI 
    adds up standard deviations based on price direction. This makes it more of a 
    measure of the "quality" of volatility rather than just the amount of volatility.
    
    The indicator has three calculation modes:
    - Standard: Uses only close prices
    - Refined: Uses the average of high and low calculations
    - Thirds: Uses the average of high, low, and close calculations
    
    The RVI oscillates between 0 and 100, with readings above 50 suggesting that 
    upward volatility is stronger, while readings below 50 suggest that downward 
    volatility is stronger.

More info:
    https://www.tradingview.com/wiki/Relative_Volatility_Index_(RVI)

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' column, 
      and 'high' and 'low' columns if using refined or thirds modes.
    - length (int): The period for calculations. Default is 14.
    - scalar (float): A multiplier for scaling the result. Default is 100.
    - refined (bool): Whether to use the 'refined' calculation (average of high and low). Default is False.
    - thirds (bool): Whether to use the 'thirds' calculation (average of high, low, and close). Default is False.
    - column (str): The column to use for calculations if not using refined or thirds modes. Default is 'close'.

Call with:
    # Standard mode
    result = bta.relative_volatility_index(df)
    df['rvi'] = result['rvi']
    
    # Refined mode
    result = bta.relative_volatility_index(df, refined=True)
    df['rvi_r'] = result['rvi_r']
    
    # Thirds mode
    result = bta.relative_volatility_index(df, thirds=True)
    df['rvi_t'] = result['rvi_t']

Returns:
    pd.DataFrame: DataFrame with 'rvi', 'rvi_r', or 'rvi_t' column depending on the mode.

## Thermometer
Name:
    Elders Thermometer (THERMO)

Description:
    Elder's Thermometer is a volatility indicator created by Dr. Alexander Elder. 
    It measures price volatility by comparing the current price range to historical 
    ranges.
    
    The indicator calculates the absolute change in high and low prices between 
    consecutive periods and selects the larger of the two. This value is then 
    compared to its moving average to determine if the market is experiencing 
    normal volatility, high volatility (potentially overbought), or low volatility 
    (potentially oversold).
    
    The indicator generates two signals:
    - Long signal: When the thermometer reading is less than a fraction (long_factor) 
      of its moving average, indicating low volatility.
    - Short signal: When the thermometer reading is greater than a multiple (short_factor) 
      of its moving average, indicating high volatility.

More info:
    https://www.motivewave.com/studies/elders_thermometer.htm
    https://www.tradingview.com/script/HqvTuEMW-Elder-s-Market-Thermometer-LazyBear/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - length (int): The period for the EMA calculation. Default is 20.
    - long_factor (float): The buy factor - thermometer < (thermometer_ma * long_factor). Default is 2.0.
    - short_factor (float): The sell factor - thermometer > (thermometer_ma * short_factor). Default is 0.5.
    - drift (int): The difference period for price changes. Default is 1.
    - as_int (bool): Whether to convert signal outputs to integers (0, 1). Default is True.

Call with:
    result = bta.thermometer(df)
    df['thermo'] = result['thermo']
    df['thermo_ma'] = result['thermo_ma']
    df['thermo_long'] = result['thermo_long']
    df['thermo_short'] = result['thermo_short']

Returns:
    pd.DataFrame: DataFrame with 'thermo', 'thermo_ma', 'thermo_long', 'thermo_short' columns.

## True Range
Name:
    True Range (TR)

Description:
    The True Range indicator measures market volatility. True Range is defined as the greatest of the following:
    - The current high minus the current low
    - The absolute value of the current high minus the previous close
    - The absolute value of the current low minus the previous close
    
    This measure accounts for gaps in price movement and provides a more comprehensive 
    measure of price volatility than simply looking at the high-low range.

More info:
    https://www.investopedia.com/terms/a/atr.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.

Call with:
    df['true_range'] = bta.true_range(df)['true_range']

Returns:
    pd.DataFrame: DataFrame with 'true_range' column.

## Ulcer Index
Name:
    Ulcer Index

Description:
    The Ulcer Index is a volatility indicator that measures downside risk. Unlike 
    standard deviation, which measures all volatility (both up and down), the 
    Ulcer Index only considers drawdowns from recent highs. This makes it a 
    better measure of investor pain because it focuses on losses.
    
    The indicator was created by Peter Martin and Byron McCann in 1987 and named 
    for the stomach ulcers that investors might get from worrying about downside 
    volatility in their investments.

More info:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ulcer_index

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing price data.
    - column (str): The column name to use for the calculation. Default is 'close'.
    - period (int): The lookback period for the calculation. Default is 14.

Call with:
    df['ui'] = bta.ulcer_index(df, 'close', 14)['ulcer_index']

Returns:
    pd.DataFrame: DataFrame with 'ulcer_index' column.

## Williams Vix Fix
Name:
    Williams VIX Fix

Description:
    The Williams VIX Fix indicator, developed by Larry Williams, measures market volatility 
    and identifies potential market bottoms when volatility spikes indicate oversold conditions.
    
    The indicator calculates the percentage difference between the highest high over a 
    specified period and the current low, relative to the highest high. This creates 
    a volatility measure that spikes during market stress and can signal potential 
    reversal points.
    
    The indicator includes:
    - Williams VIX Fix: The main volatility measure
    - Midline: Upper band (mean + standard deviation)
    - Lower Band: Lower band (mean - standard deviation)
    - Signal: Binary signal when VIX exceeds thresholds
    - Green Flash: Signal for potential market bottoms

More info:
    https://www.tradingview.com/script/xqJvYkWE-Williams-VIX-Fix-Finds-Market-Bottoms/
    https://www.stockcharts.com/school/doku.php?id=chart_school:technical_indicators:williams_vix_fix_fix

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high' and 'low' columns.
    - vix_length (int): Period for calculating the highest high. Default is 22.
    - mult (float): Multiplier for standard deviation bands. Default is 2.0.
    - bbl (int): Period for calculating Bollinger Band levels. Default is 20.
    - ph (float): Percentile threshold for range high signals. Default is 0.85.

Call with:
    vix_result = bta.williams_vix_fix(df, vix_length=22, mult=2.0, bbl=20, ph=0.85)
    df['williams_vix_fix'] = vix_result['williams_vix_fix']
    df['williams_vix_fix_upper_band'] = vix_result['williams_vix_fix_upper_band']
    df['williams_vix_fix_lower_band'] = vix_result['williams_vix_fix_lower_band']
    df['williams_vix_fix_mid_line'] = vix_result['williams_vix_fix_mid_line']
    df['williams_vix_fix_range_high'] = vix_result['williams_vix_fix_range_high']
    df['williams_vix_fix_signal'] = vix_result['williams_vix_fix_signal']
    df['williams_vix_fix_green_flash'] = vix_result['williams_vix_fix_green_flash']

Returns:
    pd.DataFrame: DataFrame with 'williams_vix_fix', 'williams_vix_fix_upper_band', 'williams_vix_fix_lower_band',
    'williams_vix_fix_mid_line', 'williams_vix_fix_range_high', 'williams_vix_fix_signal', and 'williams_vix_fix_green_flash' columns.

# Volume

## Accumulation Distribution Index
Name:
    Accumulation/Distribution Index (ADI)

Description:
    The ADI acts as a leading indicator of price movements. It is calculated using the
    high, low, close, and volume data. The indicator evaluates the relationship between 
    price and volume, aiming to identify divergences that may precede price movements.

More info:
    https://www.investopedia.com/terms/a/accumulationdistribution.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - fillna (bool): If True, fill NaN values.

Call with:
    df['adi'] = bta.accumulation_distribution_index(df, fillna=True)['adi']

Returns:
    pd.DataFrame: DataFrame with 'adi' column.

## Accumulation Distribution Oscillator
Name:
    Accumulation/Distribution Oscillator (ADOSC)

Description:
    The Accumulation/Distribution Oscillator, also known as the Chaikin Oscillator, 
    measures the momentum of the Accumulation/Distribution Index (ADI) using the 
    difference between fast and slow exponential moving averages of the ADI.
    
    The indicator helps identify when the Accumulation/Distribution Index is 
    changing direction, which can signal potential price reversals. It's particularly 
    useful for spotting divergences between price and volume flow.

More info:
    https://www.investopedia.com/articles/active-trading/031914/understanding-chaikin-oscillator.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:chaikin_oscillator

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - fast_length (int): The period for the fast EMA calculation. Default is 3.
    - slow_length (int): The period for the slow EMA calculation. Default is 10.
    - fillna (bool): If True, fill NaN values with 0. Default is False.

Call with:
    result = bta.accumulation_distribution_oscillator(df)
    df['adosc'] = result['adosc']

Returns:
    pd.DataFrame: DataFrame with 'adosc' column.

## Accumulation On Balance Volume
Name:
    Accumulation On Balance Volume (AOBV)

Description:
    The Accumulation On Balance Volume (AOBV) is an enhanced version of the classic
    On Balance Volume (OBV) indicator. It uses multiple moving averages of the OBV 
    to generate trading signals based on the relationship between these averages.
    
    This indicator also incorporates min/max values over specified lookback periods,
    as well as 'run' signals that indicate when the fast MA has been consistently above
    (long run) or below (short run) the slow MA for a specified number of periods.

More info:
    https://www.investopedia.com/terms/o/onbalancevolume.asp
    https://school.stockcharts.com/doku.php?id=technical_indicators:on_balance_volume_obv

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - fast_length (int): The fast period for the MA calculation. Default is 4.
    - slow_length (int): The slow period for the MA calculation. Default is 12.
    - max_lookback (int): The period for the rolling maximum calculation. Default is 2.
    - min_lookback (int): The period for the rolling minimum calculation. Default is 2.
    - ma_type (str): The type of moving average to use ('EMA' or 'SMA'). Default is 'EMA'.
    - run_length (int): The number of consecutive periods the fast MA must be above/below
                        the slow MA to trigger a long/short run signal. Default is 2.

Call with:
    result = bta.accumulation_on_balance_volume(df)
    df['obv'] = result['obv']
    df['obv_fast'] = result['obv_fast']
    df['obv_slow'] = result['obv_slow']
    df['obv_long_run'] = result['obv_long_run']
    df['obv_short_run'] = result['obv_short_run']

Returns:
    pd.DataFrame: DataFrame with columns 'obv', 'obv_min', 'obv_max', 
                 'obv_fast', 'obv_slow', 'obv_long_run', and 'obv_short_run'.

## Chaikin Money Flow
Name:
    Chaikin Money Flow (CMF)

Description:
    The Chaikin Money Flow measures the amount of Money Flow Volume over a specific period.
    It combines price and volume to form an indicator used to measure buying and selling 
    pressure. A positive value indicates buying pressure, while a negative value suggests 
    selling pressure.

More info:
    https://www.investopedia.com/terms/c/chaikinmoneyflow.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): Number of periods for the calculation. Default is 20.
    - fillna (bool): If True, fill NaN values with 0.

Call with:
    df['cmf'] = bta.chaikin_money_flow(df, window=20, fillna=True)['cmf']

Returns:
    pd.DataFrame: DataFrame with 'cmf' column.

## Ease Of Movement
Name:
    Ease of Movement (EoM, EMV)

Description:
    Ease of Movement (EoM, EMV) and Signal Ease of Movement (SMA of EoM)

    Relates an asset's price change to its volume and is useful for assessing trend strength.
    The SMA of the EoM serves as a signal line for the indicator. Positive values indicate 
    the price is increasing with relative ease, while negative values suggest price is 
    decreasing with relative ease.

More info:
    https://www.investopedia.com/terms/e/easeofmovement.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'volume' columns.
    - eom_length (int): Period for the EoM calculation. Default is 14.
    - seom_length (int): Period for the SMA of EoM calculation. Default is 14.
    - fillna (bool): If True, fill NaN values.

Call with:
    eom_df = bta.ease_of_movement(df, eom_length=14, seom_length=14, fillna=True)
    df['eom'] = eom_df['eom']
    df['seom'] = eom_df['seom']

Returns:
    pd.DataFrame: DataFrame with 'eom' and 'seom' columns.

## Force Index
Name:
    Force Index (FI)

Description:
    The Force Index (FI) illustrates how strong the actual buying or selling pressure is.
    It combines price movement and volume to quantify the force behind a price move.
    A rising FI indicates increasing buying pressure, while a falling FI suggests 
    increasing selling pressure.

More info:
    https://www.investopedia.com/terms/f/force-index.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - window (int): Period for calculating the exponential moving average of the Force Index. Default is 13.
    - fillna (bool): If True, fill NaN values.

Call with:
    df['fi'] = bta.force_index(df, window=13, fillna=True)['fi']

Returns:
    pd.DataFrame: DataFrame with 'fi' column.

## Klinger Volume Oscillator
Name:
    Klinger Volume Oscillator (KVO)

Description:
    The Klinger Volume Oscillator (KVO) was developed by Stephen J. Klinger. It is designed 
    to predict price reversals in a market by comparing volume to price. The KVO attempts to 
    determine long-term trends of money flow while remaining sensitive enough to detect 
    short-term fluctuations.
    
    The oscillator does this by using volume to emphasize price movements and divergences.
    It uses two EMAs of a volume force, which is calculated using volume and price changes,
    then finds the difference between these EMAs.

More info:
    https://www.investopedia.com/terms/k/klingeroscillator.asp
    https://www.daytrading.com/klinger-volume-oscillator

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - fast_length (int): The fast period for the EMA calculation. Default is 34.
    - slow_length (int): The slow period for the EMA calculation. Default is 55.
    - signal_length (int): The period for the signal line EMA calculation. Default is 13.

Call with:
    result = bta.klinger_volume_oscillator(df)
    df['kvo'] = result['kvo']
    df['kvo_signal'] = result['kvo_signal']
    df['kvo_hist'] = result['kvo_hist']

Returns:
    pd.DataFrame: DataFrame with 'kvo', 'kvo_signal', and 'kvo_hist' columns.

## Money Flow Index
Name:
    Money Flow Index (MFI)

Description:
    The Money Flow Index (MFI) uses both price and volume to measure buying and selling pressure.
    It is often referred to as volume-weighted RSI. MFI is a momentum indicator that analyzes
    the flow of money into and out of an asset. Values above 80 are considered overbought,
    while values below 20 are considered oversold.

More info:
    https://www.investopedia.com/terms/m/mfi.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): Period for calculating MFI. Default is 14.
    - fillna (bool): If True, fill NaN values.

Call with:
    df['mfi'] = bta.money_flow_index(df, window=14, fillna=True)['mfi']

Returns:
    pd.DataFrame: DataFrame with 'mfi' column.

## Negative Volume Index
Name:
    Negative Volume Index (NVI)

Description:
    The Negative Volume Index (NVI) measures price changes on days when trading volume 
    decreases compared to the previous day. Informed traders are thought to be more 
    active on low volume days, hence the NVI accumulates price rate of change only 
    on such days. The indicator can help identify trends led by smart money.

More info:
    https://www.investopedia.com/terms/n/nvi.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - signal_type (str): Type of signal smoothing ('EMA' or 'SMA'). Default is 'EMA'.
    - signal_length (int): Length for the EMA/SMA calculation. Default is 255.
    - fillna (bool): If True, fill NaN values.

Call with:
    nvi_df = bta.negative_volume_index(df, signal_type='EMA', signal_length=255, fillna=True)
    df['nvi'] = nvi_df['nvi']
    df['nvi_signal'] = nvi_df['nvi_signal']

Returns:
    pd.DataFrame: DataFrame with 'nvi' and 'nvi_signal' columns.

## On Balance Volume
Name:
    On Balance Volume (OBV)

Description:
    The On Balance Volume (OBV) indicator measures buying and selling pressure by accumulating 
    volume based on price movements. When the close price is higher than the previous close, 
    the volume is added to the OBV; when lower, it's subtracted. Rising OBV indicates buying 
    pressure, and falling OBV suggests selling pressure. This implementation includes an 
    optional signal line for additional trend confirmation.

More info:
    https://www.investopedia.com/terms/o/onbalancevolume.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - signal_type (str): Type of signal smoothing ('EMA' or 'SMA'). Default is 'SMA'.
    - signal_length (int): Length for the signal smoothing. Default is 21.
    - show_signal (bool): If True, calculate and return the signal line. Default is True.
    - fillna (bool): If True, fill nan values with 0. Default is False.

Call with:
    obv_df = bta.on_balance_volume(df, signal_type='SMA', signal_length=21, show_signal=True, fillna=True)
    df['obv'] = obv_df['obv']
    df['signal'] = obv_df['signal']

Returns:
    pd.DataFrame: DataFrame with 'obv' and 'signal' columns.

## On Balance Volume Oscillator
Name:
    On Balance Volume (OBV) Oscillator

Description:
    The On Balance Volume (OBV) Oscillator measures the difference between the OBV and its 
    Exponential Moving Average (EMA). It helps in identifying trends and confirming price 
    movements. An increasing OBV oscillator indicates buying pressure, while a decreasing 
    one indicates selling pressure. Crossovers of the zero line can be used as potential 
    trading signals.

More info:
    https://www.investopedia.com/terms/o/onbalancevolume.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - length (int): Length for the EMA calculation. Default is 20.
    - fillna (bool): If True, fill nan values with 0.

Call with:
    df['obv_oscillator'] = bta.on_balance_volume_oscillator(df, length=20, fillna=True)['obv_oscillator']

Returns:
    pd.DataFrame: DataFrame with 'obv_oscillator' column.

## Positive Volume Index
Name:
    Positive Volume Index (PVI)

Description:
    The Positive Volume Index (PVI) measures price changes on days when the trading volume 
    increases compared to the previous day. It accumulates the price rate of change on those 
    days, helping to identify trends driven by high-volume activity. The PVI is often used 
    in conjunction with the Negative Volume Index (NVI) to understand different aspects of 
    market behavior.

More info:
    https://school.stockcharts.com/doku.php?id=technical_indicators:positive_volume_index

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - signal_type (str): Type of signal smoothing ('EMA' or 'SMA'). Default is 'EMA'.
    - signal_length (int): Length for the EMA/SMA calculation. Default is 255.
    - fillna (bool): If True, fill nan values.

Call with:
    pvi_df = bta.positive_volume_index(df, signal_type='EMA', signal_length=255, fillna=True)
    df['pvi'] = pvi_df['pvi']
    df['pvi_signal'] = pvi_df['pvi_signal']

Returns:
    pd.DataFrame: DataFrame with 'pvi' and 'pvi_signal' columns.

## Price Volume
Name:
    Price-Volume (PVOL)

Description:
    The Price-Volume indicator is a simple measure that calculates the product of price 
    and volume. This gives a measure of the monetary value of transactions at each time period.
    
    When the 'signed' parameter is set to True, the indicator also takes into account 
    the direction of price movement, multiplying by +1 for price increases and -1 for 
    price decreases, which can help identify buying and selling pressure.

More info:
    https://www.investopedia.com/articles/technical/02/082702.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain specified price column and 'volume' column.
    - signed (bool): Whether to apply the sign of price changes to the result. Default is False.
    - column (str): The price column to use for calculations. Default is 'close'.

Call with:
    result = bta.price_volume(df)
    df['pvol'] = result['pvol']

Returns:
    pd.DataFrame: DataFrame with 'pvol' column.

## Price Volume Rank
Name:
    Price Volume Rank (PVR)

Description:
    The Price Volume Rank indicator was developed by Anthony J. Macek to classify price and 
    volume behavior into four distinct categories. It provides a simple numerical classification 
    that can help identify potential market turning points and trend continuations.
    
    The indicator assigns values from 1 to 4 based on the combination of price change and 
    volume change directions:
    
    1: Price up, Volume up (strong bullish)
    2: Price up, Volume down (weak bullish)
    3: Price down, Volume up (strong bearish)
    4: Price down, Volume down (weak bearish)
    
    The basic interpretation is to consider buying when the PVR is below 2.5 and 
    selling when it is above 2.5.

More info:
    https://www.fmlabs.com/reference/default.htm?url=PVrank.htm
    Technical Analysis of Stocks & Commodities Magazine, June 1994

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.

Call with:
    result = bta.price_volume_rank(df)
    df['pvr'] = result['pvr']

Returns:
    pd.DataFrame: DataFrame with 'pvr' column.

## Price Volume Trend
Name:
    Price Volume Trend (PVT)

Description:
    Based on cumulative volume that adds or subtracts a multiple of the percentage change in 
    share price trend. The PVT is similar to On Balance Volume (OBV) but instead of adding 
    or subtracting the entire volume, it adds or subtracts a portion of the volume based on 
    the percentage price change. This creates a more refined volume-based indicator that 
    responds proportionally to price movements.

More info:
    https://www.investopedia.com/terms/p/pvtrend.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - fillna (bool): If True, fill nan values.
    - smoothing_factor (int, optional): Will smooth PVT implementation with SMA.
    - signal_type (str): Type of signal smoothing ('SMA' or 'EMA').
    - signal_length (int): Length of the signal smoothing.
    - dropnans (bool): Drop NaN values after indicator calculated.

Call with:
    pvt_df = bta.price_volume_trend(df, fillna=True, signal_type='EMA', signal_length=21, dropnans=True)
    df['pvt'] = pvt_df['price_volume_trend']
    df['pvt_signal'] = pvt_df['signal']

Returns:
    pd.DataFrame: DataFrame with 'price_volume_trend' and 'signal' columns.

## Relative Volume
Name:
    Relative Volume (RVOL)

Description:
    Computes the Relative Volume (RVOL) indicator, which compares the current volume
    to a moving average of volume over a specified window. This helps identify periods
    of unusually high or low trading activity. Values greater than 1 indicate above-average 
    volume, while values less than 1 indicate below-average volume. Traders often look for 
    high relative volume to confirm breakouts or significant price movements.

More info:
    https://www.investopedia.com/terms/r/relative-volume.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing a volume column.
    - volume_col (str): Name of the column containing volume data. Default is 'volume'.
    - window (int): Lookback window for calculating the Simple Moving Average (SMA) of volume. Default is 24.

Call with:
    df['rvol'] = bta.relative_volume(df, volume_col='volume', window=24)['rvol']

Returns:
    pd.DataFrame: DataFrame with an additional column:
        - 'rvol': The Relative Volume values.

## Time Relative Volume Oscillator
Name:
    Time Relative Volume Oscillator (TRVO)

Description:
    Time Relative Volume Oscillator (TRVO) - Delta Mode
    
    This indicator measures relative volume compared to historical values and differentiates
    between buy and sell volumes. It first calculates a relative volume by comparing current
    volume to a historical average, then applies a sigmoid-like transformation to normalize
    the values. The volume is then split into buy and sell components based on where the close
    price sits within the high-low range. Finally, the indicator creates a "delta" or difference
    between short and long EMAs of the buy/sell percentage differences.

More info:
    This is a custom indicator inspired by volume profile analysis techniques used by 
    professional traders. The sigmoid transformation helps normalize volume spikes.

Parameters:
    - df (pd.DataFrame): Input DataFrame containing 'high', 'low', 'close', and 'volume'.
    - column (str): Column name for price source (default: "close").
    - relative_len (int): Number of previous periods used for relative volume calculation (default: 6).
    - delta_smoothing (int): Smoothing factor for the buy/sell volume difference (default: 9).
    - smoothing_line (bool): If True, applies EMA smoothing to buy/sell volume difference (default: True).
    - show_total_volume (bool): If True, includes the 'total_volume' column in the output DataFrame (default: False).

Call with:
    trvo_result = bta.time_relative_volume_oscillator(
        df,
        column="close",
        relative_len=6,
        delta_smoothing=9,
        smoothing_line=True,
        show_total_volume=False,
    )
    df["relative_buy_volume"] = trvo_result["relative_buy_volume"]
    df["relative_sell_volume"] = trvo_result["relative_sell_volume"]
    df["buy_vs_sell"] = trvo_result["buy_vs_sell"]
    df["smoothed_delta"] = trvo_result["smoothed_delta"]

Returns:
    pd.DataFrame: A DataFrame containing:
        - "relative_buy_volume": Volume attributed to buyers.
        - "relative_sell_volume": Volume attributed to sellers (negative).
        - "buy_vs_sell": Difference between buy and sell volume percentages.
        - "smoothed_delta": EMA-smoothed buy/sell volume difference.
        - "total_volume" (optional): Raw total volume for each period (if show_total_volume=True).

## Volume Profile
Name:
    Volume Profile (VP)

Description:
    The Volume Profile indicator divides the price range into a specified number of 
    price levels and calculates the trading volume that occurred at each level. This 
    provides insight into which price levels had the most trading activity.
    
    It differentiates between positive and negative volume based on whether the price 
    was rising or falling, allowing for more detailed analysis of buying and selling 
    pressure at different price levels.
    
    Note: Value Area is not calculated in this implementation.

More info:
    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:volume_by_price
    https://www.tradingview.com/wiki/Volume_Profile

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - width (int): How many price ranges to divide the data into. Default is 10.
    - sort_close (bool): Whether to sort data by close price before splitting into ranges. 
                          When False (default), data is split chronologically. When True, 
                          it's split by price level.

Call with:
    result = bta.volume_profile(df)
    # Access results with:
    low_prices = result['low_price']
    mean_prices = result['mean_price']
    high_prices = result['high_price']
    pos_volumes = result['pos_volume']
    neg_volumes = result['neg_volume']
    total_volumes = result['total_volume']

Returns:
    pd.DataFrame: DataFrame with columns 'low_price', 'mean_price', 'high_price', 
                 'pos_volume', 'neg_volume', and 'total_volume'.

## Volume Weighted Average Price
Name:
    Volume Weighted Average Price (VWAP)

Description:
    The Volume Weighted Average Price (VWAP) equals the dollar value of all trading periods 
    divided by the total trading volume for the current day. VWAP is often used by institutional 
    traders to determine the quality of execution. This implementation provides a rolling VWAP 
    over a specified window period, making it usable across multiple timeframes.

More info:
    https://www.investopedia.com/terms/v/vwap.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): n period for rolling calculation. Default is 14.
    - fillna (bool): If True, fill nan values.

Call with:
    df['vwap'] = bta.volume_weighted_average_price(df, window=14, fillna=True)['vwap']

Returns:
    pd.DataFrame: DataFrame with 'vwap' column.

## Volume Weighted Average Price Bands
Name:
    Volume-Weighted Average Price Bands (VWAPB)

Description:
    Calculates the Volume-Weighted Average Price (VWAP) along with upper and lower bands
    based on a rolling standard deviation. The VWAP provides a cumulative weighted average 
    price, while the bands create a channel that can help identify potential support and 
    resistance levels. Price movement outside these bands may indicate overbought or 
    oversold conditions.

More info:
    https://www.investopedia.com/terms/v/vwap.asp

Parameters:
    - df (pd.DataFrame): Input DataFrame containing the following required columns:
        - 'close': Closing price.
        - 'high': High price for each interval.
        - 'low': Low price for each interval.
        - 'volume': Trading volume for each interval.
    - window_size (int, default=20): The rolling window size for VWAP and standard deviation calculations.
    - num_of_std (float, default=1.0): The number of standard deviations to calculate the upper and lower bands.

Call with:
    vwapb_result = bta.volume_weighted_average_price_bands(df, window_size=20, num_of_std=1.0)
    df['vwap_low'] = vwapb_result['vwap_low']
    df['vwap'] = vwapb_result['vwap']
    df['vwap_high'] = vwapb_result['vwap_high']

Returns:
    pd.DataFrame: A DataFrame containing the following columns:
        - 'vwap': The Volume-Weighted Average Price (VWAP).
        - 'vwap_low': The lower band (VWAP - num_of_std × rolling std deviation).
        - 'vwap_high': The upper band (VWAP + num_of_std × rolling std deviation).

## Vwap Divergence
Name:
    VWAP Divergence

Description:
    The VWAP Divergence indicator identifies potential bullish and bearish divergences 
    between price action and the Volume Weighted Average Price (VWAP). A bullish 
    divergence occurs when price moves higher while VWAP moves lower, suggesting 
    potential upward momentum. A bearish divergence occurs when price moves lower 
    while VWAP moves higher, suggesting potential downward momentum.
    
    The indicator uses ATR (Average True Range) to filter out insignificant movements 
    and includes gap detection to avoid false signals during market gaps. It also 
    implements a minimum bar spacing between signals to prevent clustering of alerts.

More info:
    https://www.investopedia.com/terms/v/vwap.asp
    https://www.tradingview.com/script/fluxchart-vwap-divergence/

Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 
      'close', 'open', and volume columns.
    - divergence_lookback (int): Lookback period to determine price movement significance. 
      Default is 5.
    - divergence_atr_multiplier (float): ATR multiplier to determine minimum movement 
      threshold for divergence signals. Default is 3.0.
    - atr_length (int): Period for ATR calculation. Default is 14.
    - min_bars_between_signals (int): Minimum bars between divergence signals to 
      prevent clustering. Default is 15.
    - gap_threshold_multiplier (float): ATR multiplier for gap detection threshold. 
      Default is 1.0.
    - anchor (str): VWAP anchor period. Options: 'session', 'week', 'month'. 
      Default is 'session'.
    - source (str): Price source for VWAP calculation. Options: 'hlc3', 'hl2', 
      'ohlc4', 'close'. Default is 'hlc3'.
    - volume_col (str): Name of the volume column. Default is 'volume'.

Call with:
    result = bta.vwap_divergence(df)
    df['vwap'] = result['vwap']
    df['vwap_trend'] = result['vwap_trend']
    df['bullish_divergence'] = result['bullish_divergence']
    df['bearish_divergence'] = result['bearish_divergence']
    df['atr'] = result['atr']

Returns:
    pd.DataFrame: DataFrame with 'vwap', 'atr', 'vwap_trend', 'bullish_divergence', 
    and 'bearish_divergence' columns.

