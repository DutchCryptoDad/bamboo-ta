# -*- coding: utf-8 -*-
from pandas import DataFrame
import math
import numpy as np
import pandas as pd
# from .bamboo_ta import *
from .volatility import *
# from .trend import SMA, EMA, LSMA, HMA, WMA
from .utility import *

def Alligator_Bands(
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
        alligator_result = bta.Alligator_Bands(df, 'close', 13, 8, 5, jaw_shift=8, teeth_shift=5, lips_shift=3)
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


def BollingerTrend(df, column="close", short_length=20, long_length=50, std_dev=2.0):
    """
    Bollinger Trend Indicator

    Call with:
        df['BBTrend'] = bta.BollingerTrend(df, "close", 20, 50, 2.0)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is "close".
    - short_length (int): The period for the short Bollinger Bands. Default is 20.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - stddev (float): The standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Returns:
    - pandas.Series: A series of BBTrend values.
    """
    # Calculate short Bollinger Bands
    short_bb = Bollinger_Bands(df, column=column, period=short_length, std_dev=std_dev)
    short_middle = short_bb['BB_middle']
    short_upper = short_bb['BB_upper']
    short_lower = short_bb['BB_lower']

    # Calculate long Bollinger Bands
    long_bb = Bollinger_Bands(df, column=column, period=long_length, std_dev=std_dev)
    long_middle = long_bb['BB_middle']
    long_upper = long_bb['BB_upper']
    long_lower = long_bb['BB_lower']

    # Calculate BBTrend
    bbtrend = (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper)) / short_middle * 100
    bbtrend = bbtrend.round(2)
    
    return bbtrend


def BollingerTrendFastWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14):
    """
    Bollinger Trend Indicator with selectable Moving Average

    This function calculates the Bollinger Trend (BBTrend) and applies a selected moving average to the BBTrend.

    Usage:
        BollingerTrendFast = bta.BollingerTrendFastWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14)
        
        df['BollingerTrendFast'] = BollingerTrendFast['BBTrend']
        df['BollingerTrendFastMA'] = BollingerTrendFast['BBTrendMA']

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is "close".
    - short_length (int): The period for the short Bollinger Bands. Default is 10.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - short_stddev (float): The standard deviation multiplier for the short Bollinger Bands. Default is 1.0.
    - long_stddev (float): The standard deviation multiplier for the long Bollinger Bands. Default is 2.0.
    - ma_type (str): The type of moving average to use ("SMA", "EMA", "LSMA", "HMA", "WMA"). Default is "SMA".
    - ma_length (int): The period for the moving average. Default is 14.

    Returns:
    - pandas.DataFrame: DataFrame with 'BBTrend' and 'MA' columns.
    
    Example:
        result = BollingerTrendWithMA(df, column="close", short_length=10, long_length=50, short_stddev=1.0, long_stddev=2.0, ma_type="SMA", ma_length=14)
        df['BBTrend'] = result['BBTrend']
        df['MA'] = result['MA']
    """

    # Calculate short Bollinger Bands
    short_bb = BollingerBands(df, column=column, period=short_length, std_dev=short_stddev)
    short_middle = short_bb['BB_middle']
    short_upper = short_bb['BB_upper']
    short_lower = short_bb['BB_lower']

    # Calculate long Bollinger Bands
    long_bb = BollingerBands(df, column=column, period=long_length, std_dev=long_stddev)
    long_middle = long_bb['BB_middle']
    long_upper = long_bb['BB_upper']
    long_lower = long_bb['BB_lower']

    # Calculate BBTrend
    bbtrend = (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper)) / short_middle * 100
    bbtrend = bbtrend.round(2)

    # Select and calculate the moving average
    if ma_type == "SMA":
        ma = SMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    elif ma_type == "EMA":
        ma = EMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    elif ma_type == "LSMA":
        ma = LSMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    elif ma_type == "HMA":
        ma = HMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    elif ma_type == "WMA":
        ma = WMA(df.assign(BBTrend=bbtrend), column="BBTrend", period=ma_length)
    else:
        raise ValueError("Unsupported moving average type")

    # Returning as DataFrame
    result = df.copy()
    result['BBTrend'] = bbtrend.round(2)
    result['BBTrendMA'] = ma.round(2)

    return result[['BBTrend', 'BBTrendMA']]


def Breakouts(df, length=20):
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
    
    return df_copy[['support_level', 'resistance_level', 'support_breakout', 'resistance_breakout', 'support_retest', 'potential_support_retest', 'resistance_retest', 'potential_resistance_retest']]



def EMA(df, column="close", period=21):
    """
    Exponential Moving Average (EMA)

    Call with:
        df['ema'] = bta.EMA(df, "close", 50)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EMA is to be calculated. Default is "close".
    - period (int): The period over which EMA is to be calculated. Default is 30.

    Returns:
    - pandas.Series: A series of EMA values.

    Description:
    The Exponential Moving Average gives more weight to recent prices and thus reacts more quickly to price changes than the Simple Moving Average.
    """

    ema = df[column].ewm(span=period, adjust=False).mean()
    
    return ema


def HMA(df, column="close", period=9):
    """
    Hull Moving Average (HMA)

    Call with:
        df['hma'] = bta.HMA(df, "close", 9)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which HMA is to be calculated. Default is "close".
    - period (int): The period over which HMA is to be calculated. Default is 9.

    Returns:
    - pandas.Series: A series of HMA values.

    Description:
    Hull Moving Average (HMA) is an improved moving average, responsive and with minimal lag. It involves the combination of WMA (Weighted Moving Average) with different periods.
    """

    # We're assuming that WMA is defined in the same file and thus is accessible here.
    half_length = math.floor(period / 2)
    sqrt_length = math.floor(math.sqrt(period))

    wma_half = WMA(df, column=column, period=half_length)
    wma_full = WMA(df, column=column, period=period)

    h = 2 * wma_half - wma_full
    h_df = DataFrame(h, columns=[column])
    hma = WMA(h_df, column=column, period=sqrt_length)

    return hma


def LSMA(df, column="close", period=21):
    """
    Least Squares Moving Average (LSMA)

    Call with:
        df['lsma'] = bta.LSMA(df, "close", 50)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which LSMA is to be calculated. Default is "close".
    - period (int): The period over which LSMA is to be calculated. Default is 21.

    Returns:
    - pandas.Series: A series of LSMA values.

    Description:
    LSMA uses linear regression to compute the trend of the data over a specified period. It fits a straight line to the data points using the method of least squares to depict the direction of movement.
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

    lsma = pd.Series(lsma_values, index=df.index[period - 1:])

    return lsma


def PCC(df, period=20, mult=2):
    """
    Percent Change Channel (PCC)
    PCC is like KC unless it uses percentage changes in price to set channel distance.
    https://www.tradingview.com/script/6wwAWXA1-MA-Streak-Change-Channel/

    Call with:
        upper, rangema, lower = bta.PCC(df, period=20, mult=2)
        df['pcc_upper'] = upper
        df['pcc_rangema'] = rangema
        df['pcc_lower'] = lower

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    period (int): Period for the ZEMA calculation. Default is 20.
    mult (int): Multiplier for the range. Default is 2.

    Returns:
    tuple: Upper, RangeMA, and Lower bands as Series.
    """
    df_copy = df.copy()

    df_copy['previous_close'] = df_copy['close'].shift()
    df_copy['close_change'] = (df_copy['close'] - df_copy['previous_close']) / df_copy['previous_close'] * 100
    df_copy['high_change'] = (df_copy['high'] - df_copy['close']) / df_copy['close'] * 100
    df_copy['low_change'] = (df_copy['low'] - df_copy['close']) / df_copy['close'] * 100
    df_copy['delta'] = df_copy['high_change'] - df_copy['low_change']
    mid = ZEMA(df_copy, period, 'close_change')
    rangema = ZEMA(df_copy, period, 'delta')
    upper = mid + rangema * mult
    lower = mid - rangema * mult
    
    return upper, rangema, lower


def RMA(series, period):
    """
    Relative Moving Average (RMA) calculation.
    
    Parameters:
    - series (pandas.Series): Input series on which RMA is to be calculated.
    - period (int): The period over which RMA is to be calculated.
    
    Returns:
    - pandas.Series: A series of RMA values.
    """
    return series.ewm(alpha=1/period, adjust=False).mean()


def SMA(df, column="close", period=21):
    """
    Simple Moving Average (SMA)

    Call with:
        df['sma'] = bta.SMA(df, "close", 50)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which SMA is to be calculated. Default is "close".
    - period (int): The period over which SMA is to be calculated. Default is 30.

    Returns:
    - pandas.Series: A series of SMA values.

    Description:
    The Simple Moving Average is the unweighted mean of the previous 'period' data points.
    """

    sma = df[column].rolling(window=period).mean()
    
    return sma


def SSLChannels(df, length=10, mode='sma'):
    """
    SSL Channels
    Source: https://www.tradingview.com/script/xzIoaIJC-SSL-channel/
    Source: https://github.com/freqtrade/technical/blob/master/technical/indicators/indicators.py#L1025

    Call with:
        ssl_down, ssl_up = bta.SSLChannels(df, length=10, mode='sma')
        df['ssl_down'] = ssl_down
        df['ssl_up'] = ssl_up

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    length (int): Period for the SMA calculation. Default is 10.
    mode (str): Type of moving average to use. Currently only 'sma' is supported.

    Returns:
    tuple: SSL Down and SSL Up series.
    """
    df_copy = df.copy()

    if mode not in ('sma'):
        raise ValueError(f"Mode {mode} not supported yet")
    
    df_copy['smaHigh'] = df_copy['high'].rolling(length).mean()
    df_copy['smaLow'] = df_copy['low'].rolling(length).mean()
    df_copy['hlv'] = np.where(df_copy['close'] > df_copy['smaHigh'], 1,
                              np.where(df_copy['close'] < df_copy['smaLow'], -1, np.NAN))
    df_copy['hlv'] = df_copy['hlv'].ffill()
    df_copy['sslDown'] = np.where(df_copy['hlv'] < 0, df_copy['smaHigh'], df_copy['smaLow'])
    df_copy['sslUp'] = np.where(df_copy['hlv'] < 0, df_copy['smaLow'], df_copy['smaHigh'])

    return df_copy['sslDown'], df_copy['sslUp']


def SSLChannelsATR(df, length=7):
    """
    SSL Channels with ATR
    SSL Channels with ATR: https://www.tradingview.com/script/SKHqWzql-SSL-ATR-channel/

    Call with:
        ssl_down, ssl_up = bta.SSLChannelsATR(df, length=7)
        df['ssl_atr_down'] = ssl_down
        df['ssl_atr_up'] = ssl_up

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    length (int): Period for the SMA calculation. Default is 7.

    Returns:
    tuple: SSL Down and SSL Up series.
    """
    df_copy = df.copy()

    df_copy['ATR'] = ATR(df_copy, period=14)
    df_copy['smaHigh'] = df_copy['high'].rolling(length).mean() + df_copy['ATR']
    df_copy['smaLow'] = df_copy['low'].rolling(length).mean() - df_copy['ATR']
    df_copy['hlv'] = np.where(df_copy['close'] > df_copy['smaHigh'], 1, np.where(df_copy['close'] < df_copy['smaLow'], -1, np.NAN))
    df_copy['hlv'] = df_copy['hlv'].ffill()
    df_copy['sslDown'] = np.where(df_copy['hlv'] < 0, df_copy['smaHigh'], df_copy['smaLow'])
    df_copy['sslUp'] = np.where(df_copy['hlv'] < 0, df_copy['smaLow'], df_copy['smaHigh'])
    
    return df_copy['sslDown'], df_copy['sslUp']


def STDEV(series, period):
    """
    Calculate the standard deviation over a specified period.

    Parameters:
    - series (pd.Series): The data series to calculate the standard deviation for.
    - period (int): The period over which to calculate the standard deviation.

    Returns:
    - pd.Series: The standard deviation of the series.
    """
    return series.rolling(window=period).std()


def T3(df, length=5):
    """
    T3 Average by HPotter
    https://www.tradingview.com/script/qzoC9H1I-T3-Average/

    Call with:
        df['t3_average'] = bta.T3(df, length=5)

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    length (int): Period for the EMA calculation. Default is 5.

    Returns:
    pd.Series: Series of T3 Average values.
    """
    df_copy = df.copy()

    df_copy['xe1'] = EMA(df_copy, column='close', period=length)
    df_copy['xe2'] = EMA(df_copy, column='xe1', period=length)
    df_copy['xe3'] = EMA(df_copy, column='xe2', period=length)
    df_copy['xe4'] = EMA(df_copy, column='xe3', period=length)
    df_copy['xe5'] = EMA(df_copy, column='xe4', period=length)
    df_copy['xe6'] = EMA(df_copy, column='xe5', period=length)
    
    b = 0.7
    c1 = -b*b*b
    c2 = 3*b*b+3*b*b*b
    c3 = -6*b*b-3*b-3*b*b*b
    c4 = 1+3*b+b*b*b+3*b*b
    
    df_copy['T3Average'] = c1 * df_copy['xe6'] + c2 * df_copy['xe5'] + c3 * df_copy['xe4'] + c4 * df_copy['xe3']
    
    return df_copy['T3Average']


def WMA(df, column="close", period=9):
    """
    TradingView-Style Weighted Moving Average (WMA)

    Call with:
        df['wma'] = bta.WMA(df, "close", 9)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which WMA is to be calculated. Default is "close".
    - period (int): The period over which WMA is to be calculated. Default is 9.

    Returns:
    - pandas.Series: A series of WMA values.

    Description:
    The Weighted Moving Average assigns weights linearly. The most recent data gets the highest weight.
    """
    weights = range(1, period + 1)
    numerator = df[column].rolling(window=period).apply(
        lambda x: sum(weights * x), raw=True)
    denominator = sum(weights)

    wma = numerator / denominator
    
    return wma


def ZEMA(df, period, column='close'):
    """
    Zero Lag Exponential Moving Average (ZEMA)
    Source: https://github.com/freqtrade/technical/blob/master/technical/indicators/overlap_studies.py#L79
    Modified slightly to use ta.EMA instead of technical ema

    Call with:
        df['zema'] = bta.ZEMA(df, period=21, column='close')

    Args:
    df (pd.DataFrame): DataFrame containing the data.
    period (int): Period for the EMA calculation.
    column (str): The column name on which the ZEMA is to be applied. Default is "close".

    Returns:
    pd.Series: Series of ZEMA values.
    """
    df_copy = df.copy()

    df_copy['ema1'] = EMA(df_copy, column=column, period=period)
    df_copy['ema2'] = EMA(df_copy, column='ema1', period=period)
    df_copy['d'] = df_copy['ema1'] - df_copy['ema2']
    df_copy['zema'] = df_copy['ema1'] + df_copy['d']
    
    return df_copy['zema']


def ZLEMA(df, column="close", period=21):
    """
    Zero Lag Exponential Moving Average (ZLEMA)

    Call with:
        df['zlema'] = bta.ZLEMA(df, "close", 21)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZLEMA is to be calculated. Default is "close".
    - period (int): The period over which ZLEMA is to be calculated. Default is 21.

    Returns:
    - pandas.Series: A series of ZLEMA values.

    Description:
    Zero Lag Exponential Moving Average (ZLEMA) is an EMA that adjusts for lag, making it more responsive to recent price changes. It uses lagged data differences to adjust the EMA calculation, thereby supposedly removing the inherent lag of EMA.
    """
    lag = int((period - 1) / 2)

    # Calculating the adjusted data series
    ema_data = df[column] + (df[column] - df[column].shift(lag))

    # Computing the EMA of the adjusted data series
    zlema = ema_data.ewm(span=period, adjust=False).mean()

    return zlema


