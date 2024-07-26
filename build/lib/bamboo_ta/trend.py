# -*- coding: utf-8 -*-
from pandas import DataFrame
import math
import numpy as np
import pandas as pd
# from .bamboo_ta import *
from .volatility import *
# from .trend import SMA, EMA, LSMA, HMA, WMA
from .utility import *

def AlligatorBands(
    df: pd.DataFrame,
    column: str = 'close',
    jaw_period: int = 13,
    teeth_period: int = 8,
    lips_period: int = 5,
    jaw_shift: int = 8,
    teeth_shift: int = 5,
    lips_shift: int = 3
) -> pd.DataFrame:
    """
    Bill Williams Alligator Indicator

    The Alligator Indicator is used to identify trends and their direction in the market. It consists of three smoothed moving averages known as the Jaw, Teeth, and Lips.

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
        alligator_result = bta.AlligatorBands(df, 'close', 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
        df['jaw'] = alligator_result['jaw']
        df['teeth'] = alligator_result['teeth']
        df['lips'] = alligator_result['lips']

    Returns:
    - pd.DataFrame: DataFrame with 'jaw', 'teeth', and 'lips' columns.
    """
    df_copy = df.copy()

    df_copy['jaw'] = df_copy[column].rolling(window=jaw_period).mean().shift(jaw_shift)
    df_copy['teeth'] = df_copy[column].rolling(window=teeth_period).mean().shift(teeth_shift)
    df_copy['lips'] = df_copy[column].rolling(window=lips_period).mean().shift(lips_shift)

    df_copy['jaw'] = df_copy['jaw'].round(2)
    df_copy['teeth'] = df_copy['teeth'].round(2)
    df_copy['lips'] = df_copy['lips'].round(2)

    return df_copy[['jaw', 'teeth', 'lips']]


def BollingerTrend(df: pd.DataFrame, column: str = 'close', short_length: int = 20, long_length: int = 50, std_dev: float = 2.0) -> pd.DataFrame:
    """
    Bollinger Trend Indicator

    The Bollinger Trend Indicator calculates the trend based on the difference between short and long Bollinger Bands.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is 'close'.
    - short_length (int): The period for the short Bollinger Bands. Default is 20.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - std_dev (float): The standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        df['bbtrend'] = bta.BollingerTrend(df, 'close', 20, 50, 2.0)['bbtrend']

    Returns:
    - pd.DataFrame: DataFrame with 'bbtrend' column.
    """
    df_copy = df.copy()

    # Calculate short Bollinger Bands
    short_bb = BollingerBands(df, column=column, period=short_length, std_dev=std_dev)
    short_middle = short_bb['bb_middle']
    short_upper = short_bb['bb_upper']
    short_lower = short_bb['bb_lower']

    # Calculate long Bollinger Bands
    long_bb = BollingerBands(df, column=column, period=long_length, std_dev=std_dev)
    long_middle = long_bb['bb_middle']
    long_upper = long_bb['bb_upper']
    long_lower = long_bb['bb_lower']

    # Calculate BBTrend
    bbtrend = (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper)) / short_middle * 100

    # Fill NaN values that may arise from the calculation
    bbtrend = bbtrend.fillna(0)

    df_copy['bbtrend'] = bbtrend.round(2)

    return df_copy[['bbtrend']]


def BollingerTrendFastWithMA(
    df: pd.DataFrame,
    column: str = 'close',
    short_length: int = 10,
    long_length: int = 50,
    short_stddev: float = 1.0,
    long_stddev: float = 2.0,
    ma_type: str = 'SMA',
    ma_length: int = 14
) -> pd.DataFrame:
    """
    Bollinger Trend Indicator with Selectable Moving Average

    From: https://www.tradingview.com/script/rI3zj2j6-Bollinger-Bands-Fast-Trend-Indicator-DCD/

    This function calculates a more responsive Bollinger Trend (BBTrend) and applies a selected moving average to the BBTrend.

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
        result = bta.BollingerTrendFastWithMA(df, 'close', 10, 50, 1.0, 2.0, 'SMA', 14)
        df['bollinger_trend_fast'] = result['bbtrend']
        df['bollinger_trend_fast_ma'] = result['bbtrend_ma']

    Returns:
    - pd.DataFrame: DataFrame with 'bbtrend' and 'bbtrend_ma' columns.
    """
    df_copy = df.copy()

    # Calculate short Bollinger Bands
    short_bb = BollingerBands(df, column=column, period=short_length, std_dev=short_stddev)
    short_middle = short_bb['bb_middle']
    short_upper = short_bb['bb_upper']
    short_lower = short_bb['bb_lower']

    # Calculate long Bollinger Bands
    long_bb = BollingerBands(df, column=column, period=long_length, std_dev=long_stddev)
    long_middle = long_bb['bb_middle']
    long_upper = long_bb['bb_upper']
    long_lower = long_bb['bb_lower']

    # Calculate BBTrend
    bbtrend = (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper)) / short_middle * 100
    bbtrend = bbtrend.round(2)

    # Select and calculate the moving average
    bbtrend_df = df.assign(bbtrend=bbtrend)
    if ma_type == 'SMA':
        ma = SMA(bbtrend_df, column='bbtrend', period=ma_length)
    elif ma_type == 'EMA':
        ma = EMA(bbtrend_df, column='bbtrend', period=ma_length)
    elif ma_type == 'LSMA':
        ma = LSMA(bbtrend_df, column='bbtrend', period=ma_length)
    elif ma_type == 'HMA':
        ma = HMA(bbtrend_df, column='bbtrend', period=ma_length)
    elif ma_type == 'WMA':
        ma = WMA(bbtrend_df, column='bbtrend', period=ma_length)
    else:
        raise ValueError("Unsupported moving average type")

    # Returning as DataFrame
    result = df.copy()
    result['bbtrend'] = bbtrend.round(2)
    result['bbtrend_ma'] = ma.round(2)

    return result[['bbtrend', 'bbtrend_ma']]


def Breakouts(df: pd.DataFrame, length: int = 20) -> pd.DataFrame:
    """
    S/R Breakouts and Retests

    Makes it easy to work with Support and Resistance.
    Find Retests, Breakouts and the next levels.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', and 'close' columns.
    - length (int): Lookback period.

    Call with:
        breakout = bta.Breakouts(df, length=20)
        df['support_level'] = breakout['support_level']
        df['resistance_level'] = breakout['resistance_level']
        df['support_breakout'] = breakout['support_breakout']
        df['resistance_breakout'] = breakout['resistance_breakout']
        df['support_retest'] = breakout['support_retest']
        df['potential_support_retest'] = breakout['potential_support_retest']
        df['resistance_retest'] = breakout['resistance_retest']
        df['potential_resistance_retest'] = breakout['potential_resistance_retest']

    Returns:
    - pd.DataFrame: DataFrame with event columns populated.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    high = df_copy['high']
    low = df_copy['low']
    close = df_copy['close']

    pl = low.rolling(window=length * 2 + 1).min()
    ph = high.rolling(window=length * 2 + 1).max()
    
    s_yLoc = low.shift(length + 1).where(low.shift(length + 1) > low.shift(length - 1), low.shift(length - 1))
    r_yLoc = high.shift(length + 1).where(high.shift(length + 1) > high.shift(length - 1), high.shift(length + 1))

    cu = close < s_yLoc.shift(length)
    co = close > r_yLoc.shift(length)

    s1 = (high >= s_yLoc.shift(length)) & (close <= pl.shift(length))
    s2 = (high >= s_yLoc.shift(length)) & (close >= pl.shift(length)) & (close <= s_yLoc.shift(length))
    s3 = (high >= pl.shift(length)) & (high <= s_yLoc.shift(length))
    s4 = (high >= pl.shift(length)) & (high <= s_yLoc.shift(length)) & (close < pl.shift(length))

    r1 = (low <= r_yLoc.shift(length)) & (close >= ph.shift(length))
    r2 = (low <= r_yLoc.shift(length)) & (close <= ph.shift(length)) & (close >= r_yLoc.shift(length))
    r3 = (low <= ph.shift(length)) & (low >= r_yLoc.shift(length))
    r4 = (low <= ph.shift(length)) & (low >= r_yLoc.shift(length)) & (close > ph.shift(length))

    df_copy['support_level'] = pl.diff().where(pl.diff().notna())
    df_copy['resistance_level'] = ph.diff().where(ph.diff().notna())
    
    df_copy['support_level'] = df_copy['support_level'].combine_first(df_copy['support_level'].shift())
    df_copy['resistance_level'] = df_copy['resistance_level'].combine_first(df_copy['resistance_level'].shift())
    
    df_copy['support_breakout'] = cu
    df_copy['resistance_breakout'] = co
    df_copy['support_retest'] = (s1 | s2 | s3 | s4).astype(int)
    df_copy['potential_support_retest'] = (s1 | s2 | s3).astype(int)
    df_copy['resistance_retest'] = (r1 | r2 | r3 | r4).astype(int)
    df_copy['potential_resistance_retest'] = (r1 | r2 | r3).astype(int)
    
    return df_copy[['support_level', 'resistance_level', 'support_breakout', 'resistance_breakout', 'support_retest', 'potential_support_retest', 'resistance_retest', 'potential_resistance_retest']].round(2)


def EMA(df: pd.DataFrame, column: str = 'close', period: int = 21) -> pd.DataFrame:
    """
    Exponential Moving Average (EMA)

    The Exponential Moving Average gives more weight to recent prices and thus reacts more quickly to price changes than the Simple Moving Average.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EMA is to be calculated. Default is 'close'.
    - period (int): The period over which EMA is to be calculated. Default is 21.

    Call with:
        df['ema'] = bta.EMA(df, 'close', 50)['ema']

    Returns:
    - pd.DataFrame: DataFrame with 'ema' column.
    """
    df_copy = df.copy()
    df_copy['ema'] = df_copy[column].ewm(span=period, adjust=False).mean().round(2)
    
    return df_copy[['ema']]


def HMA(df: pd.DataFrame, column: str = 'close', period: int = 9) -> pd.DataFrame:
    """
    Hull Moving Average (HMA)

    The Hull Moving Average (HMA) is an improved moving average that is responsive and has minimal lag. It involves the combination of WMA (Weighted Moving Average) with different periods.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which HMA is to be calculated. Default is 'close'.
    - period (int): The period over which HMA is to be calculated. Default is 9.

    Call with:
        df['hma'] = bta.HMA(df, 'close', 9)['hma']

    Returns:
    - pd.DataFrame: DataFrame with 'hma' column.
    """
    df_copy = df.copy()

    half_length = math.floor(period / 2)
    sqrt_length = math.floor(math.sqrt(period))

    wma_half = WMA(df_copy, column=column, period=half_length)['wma']
    wma_full = WMA(df_copy, column=column, period=period)['wma']

    h = 2 * wma_half - wma_full
    h_df = pd.DataFrame(h, columns=[column])
    hma = WMA(h_df.assign(close=h), column='close', period=sqrt_length)['wma'].round(2)

    df_copy['hma'] = hma

    return df_copy[['hma']]


def LSMA(df: pd.DataFrame, column: str = 'close', period: int = 21) -> pd.DataFrame:
    """
    Least Squares Moving Average (LSMA)

    LSMA uses linear regression to compute the trend of the data over a specified period. It fits a straight line to the data points using the method of least squares to depict the direction of movement.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which LSMA is to be calculated. Default is 'close'.
    - period (int): The period over which LSMA is to be calculated. Default is 21.

    Call with:
        df['lsma'] = bta.LSMA(df, 'close', 50)['lsma']

    Returns:
    - pd.DataFrame: DataFrame with 'lsma' column.
    """
    lsma_values = []

    for i in range(period - 1, len(df)):
        # Extract the most recent N df points
        subset = df.iloc[i + 1 - period:i + 1]

        # Perform linear regression to fit a line
        x = np.arange(len(subset))
        y = subset[column].values
        slope, intercept = np.polyfit(x, y, 1)

        # Calculate the LSMA value using the linear equation
        lsma = intercept + slope * (period - 1)
        lsma_values.append(lsma)

    lsma_series = pd.Series(lsma_values, index=df.index[period - 1:]).round(2)

    df_copy = df.copy()
    df_copy['lsma'] = lsma_series

    return df_copy[['lsma']]


def PercentPriceChannel(df: pd.DataFrame, period: int = 20, mult: int = 2) -> pd.DataFrame:
    """
    Percent Change Channel (PCC)
    PCC is like KC unless it uses percentage changes in price to set channel distance.
    https://www.tradingview.com/script/6wwAWXA1-MA-Streak-Change-Channel/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - period (int): Period for the ZEMA calculation. Default is 20.
    - mult (int): Multiplier for the range. Default is 2.

    Call with:
        pcc_result = bta.PercentPriceChannel(df, period=20, mult=2)
        df['pcc_upper'] = pcc_result['pcc_upper']
        df['pcc_rangema'] = pcc_result['pcc_rangema']
        df['pcc_lower'] = pcc_result['pcc_lower']

    Returns:
    - pd.DataFrame: DataFrame with 'pcc_upper', 'pcc_rangema', and 'pcc_lower' columns.
    """
    df_copy = df.copy()

    df_copy['previous_close'] = df_copy['close'].shift()
    df_copy['close_change'] = ((df_copy['close'] - df_copy['previous_close']) / df_copy['previous_close'] * 100).round(2)
    df_copy['high_change'] = ((df_copy['high'] - df_copy['close']) / df_copy['close'] * 100).round(2)
    df_copy['low_change'] = ((df_copy['low'] - df_copy['close']) / df_copy['close'] * 100).round(2)
    df_copy['delta'] = (df_copy['high_change'] - df_copy['low_change']).round(2)

    mid = ZEMA(df_copy, column='close_change', period=period)['zema']
    rangema = ZEMA(df_copy, column='delta', period=period)['zema']

    df_copy['pcc_upper'] = (mid + rangema * mult).round(2)
    df_copy['pcc_rangema'] = rangema.round(2)
    df_copy['pcc_lower'] = (mid - rangema * mult).round(2)

    return df_copy[['pcc_upper', 'pcc_rangema', 'pcc_lower']]


def PriceChannel(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    Percent Price Channel (PPC)
    
    The Price Channel % PC indicator calculates the percent change of the price channel.
    It calculates the highest high and lowest low of the trailing number of bars specified by the input period. The price channel calculates the highest high and lowest low of the trailing number of bars specified by the input Length. When a market moves above the upper band, it is a sign of market strength. Conversely, when a market moves below the lower band, it is a sign of market weakness. A sustained move above or below the channel lines may indicate a significant breakout.

    The percent_p column in the PercentPriceChannel function represents the percentage position of the current closing price within the price channel defined by the highest high and lowest low over a specified period. It shows where the current closing price stands relative to the recent highest and lowest prices.

    Value Range:

    The percent_p values range from 0 to 100.
    A value of 0 indicates that the closing price is at the lowest low of the specified period.
    A value of 100 indicates that the closing price is at the highest high of the specified period.

    Trend Strength and Position:

    Above 50%: When percent_p is above 50%, the closing price is closer to the highest high. This suggests that the price is relatively strong and trading in the upper part of the range.
    Below 50%: When percent_p is below 50%, the closing price is closer to the lowest low. This suggests that the price is relatively weak and trading in the lower part of the range.

    Overbought and Oversold Conditions:

    Near 100%: When percent_p approaches 100%, it indicates that the price is near its recent peak, which might suggest an overbought condition.
    Near 0%: When percent_p approaches 0%, it indicates that the price is near its recent bottom, which might suggest an oversold condition.

    Breakout Indications:

    Sustained High Values: A sustained percent_p value above 80% could indicate strong upward momentum and a potential bullish breakout.
    Sustained Low Values: A sustained percent_p value below 20% could indicate strong downward momentum and a potential bearish breakout.

    Inspired by: https://www.tradingview.com/script/bQ2sg8b7-Price-Channel/
    and: https://help.tradestation.com/10_00/eng/tradestationhelp/elanalysis/indicator/price_channel__percent_pc_indicator_.htm

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - period (int): Period for the highest high and lowest low calculation. Default is 20.

    Call with:
        ppc_result = PriceChannel(df, period=20)
        df['ppc_upper'] = ppc_result['ppc_upper']
        df['ppc_mid'] = ppc_result['ppc_mid']
        df['ppc_lower'] = ppc_result['ppc_lower']
        df['percent_p'] = ppc_result['percent_p']

    Returns:
    - pd.DataFrame: DataFrame with 'ppc_upper', 'ppc_mid', 'ppc_lower', and 'percent_p' columns.
    """
    df_copy = df.copy()

    df_copy['highest_high'] = df_copy['high'].rolling(window=period, min_periods=1).max()
    df_copy['lowest_low'] = df_copy['low'].rolling(window=period, min_periods=1).min()

    df_copy['ppc_upper'] = df_copy['highest_high'].round(2)
    df_copy['ppc_lower'] = df_copy['lowest_low'].round(2)
    df_copy['ppc_mid'] = ((df_copy['ppc_upper'] + df_copy['ppc_lower']) / 2).round(2)

    df_copy['percent_p'] = ((df_copy['close'] - df_copy['ppc_lower']) / (df_copy['ppc_upper'] - df_copy['ppc_lower']) * 100).round(2)

    return df_copy[['ppc_upper', 'ppc_mid', 'ppc_lower', 'percent_p']]


def RMA(df: pd.DataFrame, column: str = 'close', period: int = 14) -> pd.DataFrame:
    """
    Rolling Moving Average (RMA) calculation.

    The RMA function calculates the Rolling Moving Average (RMA) of a specified column in a DataFrame over a given period. It uses an exponential moving average (EMA) calculation with a specified smoothing factor (alpha) and returns a DataFrame containing the RMA values rounded to two decimal places. This function allows for flexible moving average calculations based on any column in the input DataFrame

    Inspired by: https://www.tradingview.com/script/5BUyR2JA-rolling-moving-average/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which RMA is to be calculated.
    - period (int): The period over which RMA is to be calculated.

    Call with:
        df['rma'] = bta.RMA(df, 'close', 14)['rma']

    Returns:
    - pd.DataFrame: DataFrame with 'rma' column.
    """
    df_copy = df.copy()
    df_copy['rma'] = df_copy[column].ewm(alpha=1/period, adjust=False).mean().round(2)

    return df_copy[['rma']]


def SMA(df: pd.DataFrame, column: str = 'close', period: int = 21) -> pd.DataFrame:
    """
    Simple Moving Average (SMA)

    The Simple Moving Average is the unweighted mean of the previous 'period' data points.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which SMA is to be calculated. Default is 'close'.
    - period (int): The period over which SMA is to be calculated. Default is 21.

    Call with:
        df['sma'] = bta.SMA(df, 'close', 50)['sma']

    Returns:
    - pd.DataFrame: DataFrame with 'sma' column.
    """
    df_copy = df.copy()
    df_copy['sma'] = df_copy[column].rolling(window=period).mean().round(2)

    return df_copy[['sma']]


def SSLChannels(df: pd.DataFrame, length: int = 10, mode: str = 'sma') -> pd.DataFrame:
    """
    SSL Channels

    SSL Channels is an indicator based on the concept of using different moving averages to identify trends. This function calculates the SSL Down and SSL Up series.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the SMA calculation. Default is 10.
    - mode (str): Type of moving average to use. Currently only 'sma' is supported.

    Call with:
        ssl_result = bta.SSLChannels(df, length=10, mode='sma')
        df['ssl_down'] = ssl_result['ssl_down']
        df['ssl_up'] = ssl_result['ssl_up']

    Returns:
    - pd.DataFrame: DataFrame with 'ssl_down' and 'ssl_up' columns.
    """
    df_copy = df.copy()

    if mode not in ('sma'):
        raise ValueError(f"Mode {mode} not supported yet")
    
    df_copy['sma_high'] = df_copy['high'].rolling(length).mean()
    df_copy['sma_low'] = df_copy['low'].rolling(length).mean()
    df_copy['hlv'] = np.where(df_copy['close'] > df_copy['sma_high'], 1,
                              np.where(df_copy['close'] < df_copy['sma_low'], -1, np.NAN))
    df_copy['hlv'] = df_copy['hlv'].ffill()
    df_copy['ssl_down'] = np.where(df_copy['hlv'] < 0, df_copy['sma_high'], df_copy['sma_low'])
    df_copy['ssl_up'] = np.where(df_copy['hlv'] < 0, df_copy['sma_low'], df_copy['sma_high'])

    df_copy['ssl_down'] = df_copy['ssl_down'].round(2)
    df_copy['ssl_up'] = df_copy['ssl_up'].round(2)

    return df_copy[['ssl_down', 'ssl_up']]


def SSLChannelsATR(df: pd.DataFrame, column: str = 'close', length: int = 21, atr_period: int = 14) -> pd.DataFrame:
    """
    SSL Channels with ATR

    The SSLChannelsATR function calculates the SSL (Safe and Secure Levels) channels using the Average True Range (ATR) to adjust the Simple Moving Averages (SMA) of the high and low prices over a specified period. It determines the trend direction based on the comparison of a chosen price column with these adjusted SMAs and generates the SSL ATR Down and Up levels accordingly. This indicator helps identify potential trend reversals and continuations by providing dynamic support and resistance levels.

    Inspired by: https://www.tradingview.com/script/SKHqWzql-SSL-ATR-channel/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the SMA calculation. Default is 21.
    - atr_period (int): Period for the ATR calculation. Default is 14.
    - column (str): The column to use for the moving average calculations. Default is 'close'.

    Call with:
        ssl_result = bta.SSLChannelsATR(df, column='close', length=14, atr_period=7)
        df['ssl_atr_down'] = ssl_result['ssl_atr_down']
        df['ssl_atr_up'] = ssl_result['ssl_atr_up']

    Returns:
    - pd.DataFrame: DataFrame with 'ssl_atr_down' and 'ssl_atr_up' columns.
    """
    def calculate_atr(df, period):
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period, min_periods=1).mean()
        return atr

    df_copy = df.copy()

    df_copy['atr'] = calculate_atr(df_copy, atr_period)
    df_copy['sma_high'] = (df_copy['high'].rolling(length).mean() + df_copy['atr']).round(2)
    df_copy['sma_low'] = (df_copy['low'].rolling(length).mean() - df_copy['atr']).round(2)
    df_copy['hlv'] = np.where(df_copy[column] > df_copy['sma_high'], 1, 
                              np.where(df_copy[column] < df_copy['sma_low'], -1, np.nan))
    df_copy['hlv'] = df_copy['hlv'].ffill()
    df_copy['ssl_atr_down'] = np.where(df_copy['hlv'] < 0, df_copy['sma_high'], df_copy['sma_low'])
    df_copy['ssl_atr_up'] = np.where(df_copy['hlv'] < 0, df_copy['sma_low'], df_copy['sma_high'])

    df_copy['ssl_atr_down'] = df_copy['ssl_atr_down'].round(2)
    df_copy['ssl_atr_up'] = df_copy['ssl_atr_up'].round(2)

    return df_copy[['ssl_atr_down', 'ssl_atr_up']]


def T3(df: pd.DataFrame, length: int = 5) -> pd.DataFrame:
    """
    T3 Average 
    
    Inspired by: https://www.tradingview.com/script/qzoC9H1I-T3-Average/

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the EMA calculation. Default is 5.

    Call with:
        df['t3_average'] = bta.T3(df, length=5)['t3_average']

    Returns:
    - pd.DataFrame: DataFrame with 't3_average' column.
    """
    df_copy = df.copy()

    df_copy['xe1'] = EMA(df_copy, column='close', period=length)['ema']
    df_copy['xe2'] = EMA(df_copy, column='xe1', period=length)['ema']
    df_copy['xe3'] = EMA(df_copy, column='xe2', period=length)['ema']
    df_copy['xe4'] = EMA(df_copy, column='xe3', period=length)['ema']
    df_copy['xe5'] = EMA(df_copy, column='xe4', period=length)['ema']
    df_copy['xe6'] = EMA(df_copy, column='xe5', period=length)['ema']
    
    b = 0.7
    c1 = -b*b*b
    c2 = 3*b*b+3*b*b*b
    c3 = -6*b*b-3*b-3*b*b*b
    c4 = 1+3*b+b*b*b+3*b*b
    
    df_copy['t3_average'] = (c1 * df_copy['xe6'] + 
                             c2 * df_copy['xe5'] + 
                             c3 * df_copy['xe4'] + 
                             c4 * df_copy['xe3']).round(2)
    
    return df_copy[['t3_average']]


def WMA(df: pd.DataFrame, column: str = 'close', period: int = 10) -> pd.DataFrame:
    """
    Weighted Moving Average (WMA)
    
    The Weighted Moving Average (WMA) gives more weight to recent data points and less weight to older data points.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - column (str): The column to calculate the WMA on.
    - period (int): The period for the WMA calculation.

    Call with:
        df['wma'] = bta.WMA(df, 'close', 10)['wma']
    
    Returns:
    - pd.DataFrame: DataFrame with 'wma' column.
    """
    df_copy = df.copy()
    weights = pd.Series(range(1, period + 1))
    df_copy['wma'] = df_copy[column].rolling(period).apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True).round(2)
    
    return df_copy[['wma']]


def ZEMA(df: pd.DataFrame, column: str = 'close', period: int = 21) -> pd.DataFrame:
    """
    Zero Lag Exponential Moving Average (ZEMA)

    The Zero Lag Exponential Moving Average (ZEMA) is an improved version of the Exponential Moving Average (EMA) that reduces lag by incorporating a zero lag component.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZEMA is to be calculated. Default is 21.

    Call with:
        df['zema'] = bta.ZEMA(df, 'close', 21)['zema']

    Returns:
    - pd.DataFrame: DataFrame with 'zema' column.
    """
    df_copy = df.copy()
    ema1 = df_copy[column].ewm(span=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, adjust=False).mean()
    df_copy['zema'] = (2 * ema1 - ema2).round(2)

    return df_copy[['zema']]


def ZLEMA(df: pd.DataFrame, column: str = 'close', period: int = 21) -> pd.DataFrame:
    """
    Zero Lag Exponential Moving Average (ZLEMA)

    Inspired by: https://www.tradingview.com/script/Oxizu1k7-Zero-Lag-Exponential-Moving-Average/

    Call with:
        df['zlema'] = bta.ZLEMA(df, 'close', 21)['zlema']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZLEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZLEMA is to be calculated. Default is 21.

    Returns:
    - pd.DataFrame: DataFrame with 'zlema' column.

    Description:
    Zero Lag Exponential Moving Average (ZLEMA) is an EMA that adjusts for lag, making it more responsive to recent price changes. It uses lagged data differences to adjust the EMA calculation, thereby supposedly removing the inherent lag of EMA.
    """
    lag = int((period - 1) / 2)

    # Calculating the adjusted data series
    ema_data = df[column] + (df[column] - df[column].shift(lag))

    # Computing the EMA of the adjusted data series
    zlema = ema_data.ewm(span=period, adjust=False).mean().round(2)

    df_copy = df.copy()
    df_copy['zlema'] = zlema

    return df_copy[['zlema']]
