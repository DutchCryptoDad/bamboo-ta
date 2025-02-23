# -*- coding: utf-8 -*-
from pandas import DataFrame
import math
import numpy as np
import pandas as pd
from .volatility import *
from .utility import *


def alligator_bands(
    df: pd.DataFrame,
    column: str = "close",
    jaw_period: int = 13,
    teeth_period: int = 8,
    lips_period: int = 5,
    jaw_shift: int = 8,
    teeth_shift: int = 5,
    lips_shift: int = 3,
) -> pd.DataFrame:
    """
    Bill Williams Alligator Indicator

    The Alligator Indicator is used to identify trends and their direction in the market.
    It consists of three smoothed moving averages known as the Jaw, Teeth, and Lips.

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
    - pd.DataFrame: DataFrame with 'jaw', 'teeth', and 'lips' columns.
    """
    df_copy = df.copy()

    df_copy["jaw"] = df_copy[column].rolling(window=jaw_period).mean().shift(jaw_shift)
    df_copy["teeth"] = (
        df_copy[column].rolling(window=teeth_period).mean().shift(teeth_shift)
    )
    df_copy["lips"] = (
        df_copy[column].rolling(window=lips_period).mean().shift(lips_shift)
    )

    df_copy["jaw"] = df_copy["jaw"]
    df_copy["teeth"] = df_copy["teeth"]
    df_copy["lips"] = df_copy["lips"]

    return df_copy[["jaw", "teeth", "lips"]]


def bollinger_trend(
    df: pd.DataFrame,
    column: str = "close",
    short_length: int = 20,
    long_length: int = 50,
    std_dev: float = 2.0,
) -> pd.DataFrame:
    """
    Bollinger Trend Indicator

    The Bollinger Trend Indicator calculates the trend based on the difference
    between short and long Bollinger Bands.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which BBTrend is to be calculated. Default is 'close'.
    - short_length (int): The period for the short Bollinger Bands. Default is 20.
    - long_length (int): The period for the long Bollinger Bands. Default is 50.
    - std_dev (float): The standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        df['bbtrend'] = bta.bollinger_trend(df, 'close', 20, 50, 2.0)['bbtrend']

    Returns:
    - pd.DataFrame: DataFrame with 'bbtrend' column.
    """
    df_copy = df.copy()

    # Calculate short Bollinger Bands
    short_bb = bollinger_bands(df, column=column, period=short_length, std_dev=std_dev)
    short_middle = short_bb["bb_middle"]
    short_upper = short_bb["bb_upper"]
    short_lower = short_bb["bb_lower"]

    # Calculate long Bollinger Bands
    long_bb = bollinger_bands(df, column=column, period=long_length, std_dev=std_dev)
    long_middle = long_bb["bb_middle"]
    long_upper = long_bb["bb_upper"]
    long_lower = long_bb["bb_lower"]

    # Calculate BBTrend
    bbtrend = (
        (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper))
        / short_middle
        * 100
    )

    # Fill NaN values that may arise from the calculation
    bbtrend = bbtrend.fillna(0)

    df_copy["bbtrend"] = bbtrend

    return df_copy[["bbtrend"]]


def bollinger_trend_fast_with_ma(
    df: pd.DataFrame,
    column: str = "close",
    short_length: int = 10,
    long_length: int = 50,
    short_stddev: float = 1.0,
    long_stddev: float = 2.0,
    ma_type: str = "SMA",
    ma_length: int = 14,
) -> pd.DataFrame:
    """
    Bollinger Trend Indicator with Selectable Moving Average

    This function calculates a more responsive Bollinger Trend (BBTrend) and applies a
    selected moving average to the BBTrend.

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
    - pd.DataFrame: DataFrame with 'bbtrend' and 'bbtrend_ma' columns.
    """
    df_copy = df.copy()

    # Calculate short Bollinger Bands
    short_bb = bollinger_bands(
        df, column=column, period=short_length, std_dev=short_stddev
    )
    short_middle = short_bb["bb_middle"]
    short_upper = short_bb["bb_upper"]
    short_lower = short_bb["bb_lower"]

    # Calculate long Bollinger Bands
    long_bb = bollinger_bands(
        df, column=column, period=long_length, std_dev=long_stddev
    )
    long_middle = long_bb["bb_middle"]
    long_upper = long_bb["bb_upper"]
    long_lower = long_bb["bb_lower"]

    # Calculate BBTrend
    bbtrend = (
        (np.abs(short_lower - long_lower) - np.abs(short_upper - long_upper))
        / short_middle
        * 100
    )
    bbtrend = bbtrend

    # Select and calculate the moving average
    bbtrend_df = df.assign(bbtrend=bbtrend)
    if ma_type == "SMA":
        ma = simple_moving_average(bbtrend_df, column="bbtrend", period=ma_length)
    elif ma_type == "EMA":
        ma = exponential_moving_average(bbtrend_df, column="bbtrend", period=ma_length)
    elif ma_type == "LSMA":
        ma = least_squares_moving_average(
            bbtrend_df, column="bbtrend", period=ma_length
        )
    elif ma_type == "HMA":
        ma = hull_moving_average(bbtrend_df, column="bbtrend", period=ma_length)
    elif ma_type == "WMA":
        ma = weighted_moving_average(bbtrend_df, column="bbtrend", period=ma_length)
    else:
        raise ValueError("Unsupported moving average type")

    # Returning as DataFrame
    result = df.copy()
    result["bbtrend"] = bbtrend
    result["bbtrend_ma"] = ma

    return result[["bbtrend", "bbtrend_ma"]]


def breakouts(df: pd.DataFrame, length: int = 20) -> pd.DataFrame:
    """
    S/R Breakouts and Retests

    Makes it easy to work with Support and Resistance.
    Find Retests, Breakouts, and the next levels.

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
    - pd.DataFrame: DataFrame with event columns populated.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    high = df_copy["high"]
    low = df_copy["low"]
    close = df_copy["close"]

    pl = low.rolling(window=length * 2 + 1).min()
    ph = high.rolling(window=length * 2 + 1).max()

    s_yLoc = low.shift(length + 1).where(
        low.shift(length + 1) > low.shift(length - 1), low.shift(length - 1)
    )
    r_yLoc = high.shift(length + 1).where(
        high.shift(length + 1) > high.shift(length - 1), high.shift(length + 1)
    )

    cu = close < s_yLoc.shift(length)
    co = close > r_yLoc.shift(length)

    s1 = (high >= s_yLoc.shift(length)) & (close <= pl.shift(length))
    s2 = (
        (high >= s_yLoc.shift(length))
        & (close >= pl.shift(length))
        & (close <= s_yLoc.shift(length))
    )
    s3 = (high >= pl.shift(length)) & (high <= s_yLoc.shift(length))
    s4 = (
        (high >= pl.shift(length))
        & (high <= s_yLoc.shift(length))
        & (close < pl.shift(length))
    )

    r1 = (low <= r_yLoc.shift(length)) & (close >= ph.shift(length))
    r2 = (
        (low <= r_yLoc.shift(length))
        & (close <= ph.shift(length))
        & (close >= r_yLoc.shift(length))
    )
    r3 = (low <= ph.shift(length)) & (low >= r_yLoc.shift(length))
    r4 = (
        (low <= ph.shift(length))
        & (low >= r_yLoc.shift(length))
        & (close > ph.shift(length))
    )

    df_copy["support_level"] = pl.diff().where(pl.diff().notna())
    df_copy["resistance_level"] = ph.diff().where(ph.diff().notna())

    df_copy["support_level"] = df_copy["support_level"].combine_first(
        df_copy["support_level"].shift()
    )
    df_copy["resistance_level"] = df_copy["resistance_level"].combine_first(
        df_copy["resistance_level"].shift()
    )

    df_copy["support_breakout"] = cu
    df_copy["resistance_breakout"] = co
    df_copy["support_retest"] = (s1 | s2 | s3 | s4).astype(int)
    df_copy["potential_support_retest"] = (s1 | s2 | s3).astype(int)
    df_copy["resistance_retest"] = (r1 | r2 | r3 | r4).astype(int)
    df_copy["potential_resistance_retest"] = (r1 | r2 | r3).astype(int)

    return df_copy[
        [
            "support_level",
            "resistance_level",
            "support_breakout",
            "resistance_breakout",
            "support_retest",
            "potential_support_retest",
            "resistance_retest",
            "potential_resistance_retest",
        ]
    ]


def exponential_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """
    Exponential Moving Average (EMA)

    The Exponential Moving Average gives more weight to recent prices and thus reacts
    more quickly to price changes than the Simple Moving Average.

    Call with:
        df['ema'] = bta.exponential_moving_average(df, "close", 21)

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which EMA is to be calculated. Default is 'close'.
    - period (int): The period over which EMA is to be calculated. Default is 21.

    Returns:
    - pd.DataFrame: DataFrame with 'ema' column, where first `period-1` values are NaN.
    """
    df_copy = df.copy()

    # Calculate Exponential Moving Average
    df_copy["ema"] = df_copy[column].ewm(span=period, adjust=False).mean()

    # Set first `period - 1` values to NaN using `.loc[]` to avoid chained assignment warning
    df_copy.loc[: period - 1, "ema"] = pd.NA

    return df_copy[["ema"]]


def hull_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 9
) -> pd.DataFrame:
    """
    Hull Moving Average (HMA)

    The Hull Moving Average (HMA) is an improved moving average that is responsive and
    has minimal lag. It involves the combination of WMA (Weighted Moving Average) with
    different periods.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which HMA is to be calculated. Default is 'close'.
    - period (int): The period over which HMA is to be calculated. Default is 9.

    Call with:
        df['hma'] = bta.hull_moving_average(df, 'close', 9)['hma']

    Returns:
    - pd.DataFrame: DataFrame with 'hma' column.
    """
    df_copy = df.copy()

    half_length = math.floor(period / 2)
    sqrt_length = math.floor(math.sqrt(period))

    wma_half = weighted_moving_average(df_copy, column=column, period=half_length)[
        "wma"
    ]
    wma_full = weighted_moving_average(df_copy, column=column, period=period)["wma"]

    h = 2 * wma_half - wma_full
    h_df = pd.DataFrame(h, columns=[column])
    hma = weighted_moving_average(
        h_df.assign(close=h), column="close", period=sqrt_length
    )["wma"]

    df_copy["hma"] = hma

    return df_copy[["hma"]]


def least_squares_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """
    Least Squares Moving Average (LSMA)

    LSMA uses linear regression to compute the trend of the data over a specified period.
    It fits a straight line to the data points using the method of least squares to depict
    the direction of movement.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which LSMA is to be calculated. Default is 'close'.
    - period (int): The period over which LSMA is to be calculated. Default is 21.

    Call with:
        df['lsma'] = bta.least_squares_moving_average(df, 'close', 50)['lsma']

    Returns:
    - pd.DataFrame: DataFrame with 'lsma' column.
    """
    lsma_values = []

    for i in range(period - 1, len(df)):
        # Extract the most recent N df points
        subset = df.iloc[i + 1 - period : i + 1]

        # Perform linear regression to fit a line
        x = np.arange(len(subset))
        y = subset[column].values
        slope, intercept = np.polyfit(x, y, 1)

        # Calculate the LSMA value using the linear equation
        lsma = intercept + slope * (period - 1)
        lsma_values.append(lsma)

    lsma_series = pd.Series(lsma_values, index=df.index[period - 1 :])

    df_copy = df.copy()
    df_copy["lsma"] = lsma_series

    return df_copy[["lsma"]]


def percent_price_channel(
    df: pd.DataFrame, period: int = 20, mult: int = 2
) -> pd.DataFrame:
    """
    Percent Change Channel (PCC)

    PCC is like KC unless it uses percentage changes in price to set channel distance.
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
    - pd.DataFrame: DataFrame with 'pcc_upper', 'pcc_rangema', and 'pcc_lower' columns.
    """
    df_copy = df.copy()

    df_copy["previous_close"] = df_copy["close"].shift()
    df_copy["close_change"] = (
        (df_copy["close"] - df_copy["previous_close"]) / df_copy["previous_close"] * 100
    )
    df_copy["high_change"] = (
        (df_copy["high"] - df_copy["close"]) / df_copy["close"] * 100
    )
    df_copy["low_change"] = (df_copy["low"] - df_copy["close"]) / df_copy["close"] * 100
    df_copy["delta"] = df_copy["high_change"] - df_copy["low_change"]

    mid = zero_exponential_moving_average(
        df_copy, column="close_change", period=period
    )["zema"]
    rangema = zero_exponential_moving_average(df_copy, column="delta", period=period)[
        "zema"
    ]

    df_copy["pcc_upper"] = mid + rangema * mult
    df_copy["pcc_rangema"] = rangema
    df_copy["pcc_lower"] = mid - rangema * mult

    return df_copy[["pcc_upper", "pcc_rangema", "pcc_lower"]]


def pmax(
    df: pd.DataFrame,
    period: int,
    multiplier: float,
    length: int,
    ma_type: str = "EMA",
    src: str = "close",
) -> pd.DataFrame:
    """
    Pmax Indicator

    A self-contained implementation of the Pmax indicator that calculates upper and lower
    bands based on a moving average and Average True Range (ATR). The function is independent
    of any external libraries.

    Inspired by: https://www.tradingview.com/script/sU9molfV/

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
    - pd.DataFrame: DataFrame with the following columns added:
        - 'pmax': Final Pmax values.
        - 'pmax_trend': Trend direction ('up' or 'down').
    """
    df_copy = df.copy()

    # Define the source price
    if src == "close":
        masrc = df_copy["close"]
    elif src == "hl2":
        masrc = (df_copy["high"] + df_copy["low"]) / 2
    elif src == "ohlc4":
        masrc = (
            df_copy["open"] + df_copy["high"] + df_copy["low"] + df_copy["close"]
        ) / 4
    else:
        raise ValueError(f"Invalid src value: {src}")

    # Moving average calculations
    if ma_type == "EMA":
        mavalue = masrc.ewm(span=length, adjust=False).mean()
    elif ma_type == "SMA":
        mavalue = masrc.rolling(window=length).mean()
    else:
        raise ValueError(f"Invalid ma_type value: {ma_type}")

    # ATR calculation (self-contained)
    df_copy["tr"] = np.maximum(
        df_copy["high"] - df_copy["low"],
        np.maximum(
            abs(df_copy["high"] - df_copy["close"].shift()),
            abs(df_copy["low"] - df_copy["close"].shift()),
        ),
    )
    df_copy["atr"] = df_copy["tr"].rolling(window=period).mean()

    # Calculate bands
    df_copy["basic_ub"] = mavalue + (multiplier * df_copy["atr"])
    df_copy["basic_lb"] = mavalue - (multiplier * df_copy["atr"])

    # Final upper and lower bands
    final_ub = np.full(len(df_copy), 0.00)
    final_lb = np.full(len(df_copy), 0.00)

    for i in range(period, len(df_copy)):
        final_ub[i] = (
            df_copy["basic_ub"].iloc[i]
            if df_copy["basic_ub"].iloc[i] < final_ub[i - 1]
            or mavalue.iloc[i - 1] > final_ub[i - 1]
            else final_ub[i - 1]
        )
        final_lb[i] = (
            df_copy["basic_lb"].iloc[i]
            if df_copy["basic_lb"].iloc[i] > final_lb[i - 1]
            or mavalue.iloc[i - 1] < final_lb[i - 1]
            else final_lb[i - 1]
        )

    # Determine the Pmax values
    pm_arr = np.full(len(df_copy), 0.00)
    for i in range(period, len(df_copy)):
        pm_arr[i] = (
            final_ub[i]
            if pm_arr[i - 1] == final_ub[i - 1] and mavalue.iloc[i] <= final_ub[i]
            else final_lb[i]
            if pm_arr[i - 1] == final_ub[i - 1] and mavalue.iloc[i] > final_ub[i]
            else final_lb[i]
            if pm_arr[i - 1] == final_lb[i - 1] and mavalue.iloc[i] >= final_lb[i]
            else final_ub[i]
            if pm_arr[i - 1] == final_lb[i - 1] and mavalue.iloc[i] < final_lb[i]
            else 0.00
        )

    # Mark the trend direction
    df_copy["pmax"] = pm_arr
    df_copy["pmax_trend"] = np.where(
        pm_arr > 0.00, np.where(mavalue < pm_arr, "down", "up"), np.NaN
    )

    return df_copy[["pmax", "pmax_trend"]]


def price_channel(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    """
    Price Channel (PPC)

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
    - pd.DataFrame: DataFrame with 'ppc_upper', 'ppc_mid', 'ppc_lower', and 'percent_p' columns.
    """
    df_copy = df.copy()

    df_copy["highest_high"] = (
        df_copy["high"].rolling(window=period, min_periods=1).max()
    )
    df_copy["lowest_low"] = df_copy["low"].rolling(window=period, min_periods=1).min()

    df_copy["ppc_upper"] = df_copy["highest_high"]
    df_copy["ppc_lower"] = df_copy["lowest_low"]
    df_copy["ppc_mid"] = (df_copy["ppc_upper"] + df_copy["ppc_lower"]) / 2

    df_copy["percent_p"] = (
        (df_copy["close"] - df_copy["ppc_lower"])
        / (df_copy["ppc_upper"] - df_copy["ppc_lower"])
        * 100
    )

    return df_copy[["ppc_upper", "ppc_mid", "ppc_lower", "percent_p"]]


def range_filter(
    df: pd.DataFrame,
    column: str = "close",
    period: int = 100,
    multiplier: float = 3.0,
    fillna: bool = False,
) -> pd.DataFrame:
    """
    Range Filter Buy and Sell Indicator

    This indicator smooths price action using a range filter based on a volatility-adjusted
    moving average. It identifies uptrends and downtrends while filtering out noise.

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
    - pd.DataFrame: DataFrame with 'range_filter', 'high_band', 'low_band', 'long_signal', 'short_signal'.
    """

    def ema(series, span):
        """Exponential Moving Average (EMA)"""
        return series.ewm(span=span, adjust=False).mean()

    # Compute smoothed range
    price = df[column]
    abs_diff = np.abs(price - price.shift(1))
    avg_range = ema(abs_diff, period)
    smooth_range = ema(avg_range, period * 2 - 1) * multiplier

    # Initialize filter
    filt = price.copy()

    for i in range(1, len(df)):
        prev_filt = filt.iloc[i - 1] if i > 0 else price.iloc[i]
        if price.iloc[i] > prev_filt:
            filt.iloc[i] = max(prev_filt, price.iloc[i] - smooth_range.iloc[i])
        elif price.iloc[i] < prev_filt:
            filt.iloc[i] = min(prev_filt, price.iloc[i] + smooth_range.iloc[i])
        else:
            filt.iloc[i] = prev_filt

    # Determine trend direction
    upward = np.zeros(len(df))
    downward = np.zeros(len(df))

    for i in range(1, len(df)):
        if filt.iloc[i] > filt.iloc[i - 1]:
            upward[i] = upward[i - 1] + 1
        elif filt.iloc[i] < filt.iloc[i - 1]:
            downward[i] = downward[i - 1] + 1
        else:
            upward[i] = upward[i - 1]
            downward[i] = downward[i - 1]

    # Calculate bands
    high_band = filt + smooth_range
    low_band = filt - smooth_range

    # Generate buy/sell signals
    long_signal = ((price > filt) & (price > price.shift(1)) & (upward > 0)) | (
        (price > filt) & (price < price.shift(1)) & (upward > 0)
    )

    short_signal = ((price < filt) & (price < price.shift(1)) & (downward > 0)) | (
        (price < filt) & (price > price.shift(1)) & (downward > 0)
    )

    # Ensure signal continuity
    cond_ini = np.zeros(len(df))
    for i in range(1, len(df)):
        if long_signal.iloc[i]:
            cond_ini[i] = 1
        elif short_signal.iloc[i]:
            cond_ini[i] = -1
        else:
            cond_ini[i] = cond_ini[i - 1]

    long_signal = long_signal & (pd.Series(cond_ini).shift(1) == -1)
    short_signal = short_signal & (pd.Series(cond_ini).shift(1) == 1)

    if fillna:
        filt.fillna(method="bfill", inplace=True)
        high_band.fillna(method="bfill", inplace=True)
        low_band.fillna(method="bfill", inplace=True)
        long_signal.fillna(False, inplace=True)
        short_signal.fillna(False, inplace=True)

    df_copy = df.copy()
    df_copy["range_filter"] = filt
    df_copy["high_band"] = high_band
    df_copy["low_band"] = low_band
    df_copy["long_signal"] = long_signal.astype(int)  # Convert boolean to int (0 or 1)
    df_copy["short_signal"] = short_signal.astype(int)

    return df_copy[
        ["range_filter", "high_band", "low_band", "long_signal", "short_signal"]
    ]


def rolling_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 14
) -> pd.DataFrame:
    """
    Rolling Moving Average (RMA) calculation.

    The RMA function calculates the Rolling Moving Average (RMA) of a specified column
    in a DataFrame over a given period. It uses an exponential moving average (EMA)
    calculation with a specified smoothing factor (alpha) and returns a DataFrame
    containing the RMA values. This function allows for flexible moving average
    calculations based on any column in the input DataFrame.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the specified column.
    - column (str): The column on which RMA is to be calculated.
    - period (int): The period over which RMA is to be calculated.

    Call with:
        df['rma'] = bta.rolling_moving_average(df, 'close', 14)['rma']

    Returns:
    - pd.DataFrame: DataFrame with 'rma' column.
    """
    df_copy = df.copy()
    df_copy["rma"] = df_copy[column].ewm(alpha=1 / period, adjust=False).mean()

    return df_copy[["rma"]]


def simple_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """
    Simple Moving Average (SMA)

    The Simple Moving Average is the unweighted mean of the previous 'period' data points.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which SMA is to be calculated. Default is 'close'.
    - period (int): The period over which SMA is to be calculated. Default is 21.

    Call with:
        df['sma'] = bta.simple_moving_average(df, 'close', 50)['sma']

    Returns:
    - pd.DataFrame: DataFrame with 'sma' column.
    """
    df_copy = df.copy()
    df_copy["sma"] = df_copy[column].rolling(window=period).mean()

    return df_copy[["sma"]]


def ssl_channels(df: pd.DataFrame, length: int = 10, mode: str = "sma") -> pd.DataFrame:
    """
    SSL Channels

    SSL Channels is an indicator based on the concept of using different moving averages
    to identify trends. This function calculates the SSL Down and SSL Up series.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the SMA calculation. Default is 10.
    - mode (str): Type of moving average to use. Currently only 'sma' is supported.

    Call with:
        ssl_result = bta.ssl_channels(df, length=10, mode='sma')
        df['ssl_down'] = ssl_result['ssl_down']
        df['ssl_up'] = ssl_result['ssl_up']

    Returns:
    - pd.DataFrame: DataFrame with 'ssl_down' and 'ssl_up' columns.
    """
    df_copy = df.copy()

    if mode != "sma":
        raise ValueError(f"Mode '{mode}' not supported yet")

    df_copy["sma_high"] = df_copy["high"].rolling(length).mean()
    df_copy["sma_low"] = df_copy["low"].rolling(length).mean()

    df_copy["hlv"] = np.where(
        df_copy["close"] > df_copy["sma_high"],
        1,
        np.where(df_copy["close"] < df_copy["sma_low"], -1, np.nan),
    )
    df_copy["hlv"] = df_copy["hlv"].ffill()

    df_copy["ssl_down"] = np.where(
        df_copy["hlv"] < 0, df_copy["sma_high"], df_copy["sma_low"]
    )
    df_copy["ssl_up"] = np.where(
        df_copy["hlv"] < 0, df_copy["sma_low"], df_copy["sma_high"]
    )

    return df_copy[["ssl_down", "ssl_up"]]


def ssl_channels_atr(
    df: pd.DataFrame, column: str = "close", length: int = 21, atr_period: int = 14
) -> pd.DataFrame:
    """
    SSL Channels with ATR

    The ssl_channels_atr function calculates the SSL (Safe and Secure Levels) channels using
    the Average True Range (ATR) to adjust the Simple Moving Averages (SMA) of the high
    and low prices over a specified period. It determines the trend direction based on
    the comparison of a chosen price column with these adjusted SMAs and generates the
    SSL ATR Down and Up levels accordingly.

    This indicator helps identify potential trend reversals and continuations by providing
    dynamic support and resistance levels.

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
    - pd.DataFrame: DataFrame with 'ssl_atr_down' and 'ssl_atr_up' columns.
    """

    def calculate_atr(df, period):
        high_low = df["high"] - df["low"]
        high_close = np.abs(df["high"] - df["close"].shift())
        low_close = np.abs(df["low"] - df["close"].shift())
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(window=period, min_periods=1).mean()
        return atr

    df_copy = df.copy()

    df_copy["atr"] = calculate_atr(df_copy, atr_period)
    df_copy["sma_high"] = df_copy["high"].rolling(length).mean() + df_copy["atr"]
    df_copy["sma_low"] = df_copy["low"].rolling(length).mean() - df_copy["atr"]

    df_copy["hlv"] = np.where(
        df_copy[column] > df_copy["sma_high"],
        1,
        np.where(df_copy[column] < df_copy["sma_low"], -1, np.nan),
    )
    df_copy["hlv"] = df_copy["hlv"].ffill()

    df_copy["ssl_atr_down"] = np.where(
        df_copy["hlv"] < 0, df_copy["sma_high"], df_copy["sma_low"]
    )
    df_copy["ssl_atr_up"] = np.where(
        df_copy["hlv"] < 0, df_copy["sma_low"], df_copy["sma_high"]
    )

    return df_copy[["ssl_atr_down", "ssl_atr_up"]]


def t3_average(df: pd.DataFrame, length: int = 5) -> pd.DataFrame:
    """
    T3 Average

    The T3 average is a smoothed moving average designed to reduce lag while maintaining
    responsiveness to price changes. This implementation uses multiple exponential moving
    averages (EMA) to achieve its smoothing effect.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame containing the data.
    - length (int): Period for the EMA calculation. Default is 5.

    Call with:
        df['t3_average'] = bta.t3_average(df, length=5)['t3_average']

    Returns:
    - pd.DataFrame: DataFrame with 't3_average' column.
    """
    df_copy = df.copy()

    # Calculating multiple EMA stages
    df_copy["xe1"] = exponential_moving_average(df_copy, column="close", period=length)[
        "ema"
    ]
    df_copy["xe2"] = exponential_moving_average(df_copy, column="xe1", period=length)[
        "ema"
    ]
    df_copy["xe3"] = exponential_moving_average(df_copy, column="xe2", period=length)[
        "ema"
    ]
    df_copy["xe4"] = exponential_moving_average(df_copy, column="xe3", period=length)[
        "ema"
    ]
    df_copy["xe5"] = exponential_moving_average(df_copy, column="xe4", period=length)[
        "ema"
    ]
    df_copy["xe6"] = exponential_moving_average(df_copy, column="xe5", period=length)[
        "ema"
    ]

    # Constants for T3 calculation
    b = 0.7
    c1 = -b * b * b
    c2 = 3 * b * b + 3 * b * b * b
    c3 = -6 * b * b - 3 * b - 3 * b * b * b
    c4 = 1 + 3 * b + b * b * b + 3 * b * b

    # T3 average calculation
    df_copy["t3_average"] = (
        c1 * df_copy["xe6"]
        + c2 * df_copy["xe5"]
        + c3 * df_copy["xe4"]
        + c4 * df_copy["xe3"]
    )

    return df_copy[["t3_average"]]


def ut_bot(
    df: pd.DataFrame,
    column: str = "close",
    key_value: float = 3.0,
    atr_period: int = 10,
) -> pd.DataFrame:
    """
    UT Bot Indicator

    A trend-following indicator that uses ATR to create a trailing stop that helps identify trend changes
    and potential entry/exit points. Originally created by HPotter.

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
    - pd.DataFrame: DataFrame with 'ut_bot_stop', 'ut_bot_position', 'ut_bot_buy', and 'ut_bot_sell' columns
    """
    df_copy = df.copy()
    src = df_copy[column]

    # Calculate ATR
    x_atr = average_true_range(df_copy, period=atr_period)["atr"]
    n_loss = key_value * x_atr

    # Initialize trailing stop array
    x_atr_trailing_stop = pd.Series(index=df_copy.index, dtype=float)

    # Calculate trailing stop
    for i in range(len(df_copy)):
        if i == 0:
            x_atr_trailing_stop.iloc[i] = src.iloc[i]
            continue

        prev_stop = x_atr_trailing_stop.iloc[i - 1]
        curr_src = src.iloc[i]
        prev_src = src.iloc[i - 1]

        if curr_src > prev_stop and prev_src > prev_stop:
            x_atr_trailing_stop.iloc[i] = max(prev_stop, curr_src - n_loss.iloc[i])
        elif curr_src < prev_stop and prev_src < prev_stop:
            x_atr_trailing_stop.iloc[i] = min(prev_stop, curr_src + n_loss.iloc[i])
        elif curr_src > prev_stop:
            x_atr_trailing_stop.iloc[i] = curr_src - n_loss.iloc[i]
        else:
            x_atr_trailing_stop.iloc[i] = curr_src + n_loss.iloc[i]

    # Calculate position
    position = pd.Series(0, index=df_copy.index)
    for i in range(1, len(df_copy)):
        prev_src = src.iloc[i - 1]
        curr_src = src.iloc[i]
        prev_stop = x_atr_trailing_stop.iloc[i - 1]

        if prev_src < prev_stop and curr_src > prev_stop:
            position.iloc[i] = 1
        elif prev_src > prev_stop and curr_src < prev_stop:
            position.iloc[i] = -1
        else:
            position.iloc[i] = position.iloc[i - 1]

    # Calculate buy/sell signals
    buy_signal = (src > x_atr_trailing_stop) & (
        src.shift(1) <= x_atr_trailing_stop.shift(1)
    )
    sell_signal = (src < x_atr_trailing_stop) & (
        src.shift(1) >= x_atr_trailing_stop.shift(1)
    )

    df_copy["ut_bot_stop"] = x_atr_trailing_stop
    df_copy["ut_bot_position"] = position
    df_copy["ut_bot_buy"] = buy_signal
    df_copy["ut_bot_sell"] = sell_signal

    return df_copy[["ut_bot_stop", "ut_bot_position", "ut_bot_buy", "ut_bot_sell"]]


def weighted_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 10
) -> pd.DataFrame:
    """
    Weighted Moving Average (WMA)

    The Weighted Moving Average (WMA) gives more weight to recent data points and
    less weight to older data points.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame.
    - column (str): The column to calculate the WMA on.
    - period (int): The period for the WMA calculation.

    Call with:
        df['wma'] = bta.weighted_moving_average(df, 'close', 10)['wma']

    Returns:
    - pd.DataFrame: DataFrame with 'wma' column.
    """
    df_copy = df.copy()
    weights = pd.Series(range(1, period + 1))
    df_copy["wma"] = (
        df_copy[column]
        .rolling(period)
        .apply(lambda prices: (prices * weights).sum() / weights.sum(), raw=True)
    )

    return df_copy[["wma"]]


def zero_exponential_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """
    Zero Exponential Moving Average (ZEMA)

    The Zero Exponential Moving Average (ZEMA) is an improved version of the Exponential
    Moving Average (EMA) that reduces lag by incorporating a zero-lag component.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZEMA is to be calculated. Default is 21.

    Call with:
        df['zema'] = bta.zero_exponential_moving_average(df, 'close', 21)['zema']

    Returns:
    - pd.DataFrame: DataFrame with 'zema' column.
    """
    df_copy = df.copy()

    # Calculate EMA components
    ema1 = df_copy[column].ewm(span=period, adjust=False).mean()
    ema2 = ema1.ewm(span=period, adjust=False).mean()

    # ZEMA calculation
    df_copy["zema"] = 2 * ema1 - ema2

    return df_copy[["zema"]]


def zero_lag_exponential_moving_average(
    df: pd.DataFrame, column: str = "close", period: int = 21
) -> pd.DataFrame:
    """
    Zero Lag Exponential Moving Average (ZLEMA)

    ZLEMA is an Exponential Moving Average (EMA) that adjusts for lag, making it more responsive
    to recent price changes. It uses lagged data differences to adjust the EMA calculation,
    thereby reducing the inherent lag of EMA.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain at least the column specified.
    - column (str): The column on which ZLEMA is to be calculated. Default is 'close'.
    - period (int): The period over which ZLEMA is to be calculated. Default is 21.

    Call with:
        df['zlema'] = bta.zero_lag_exponential_moving_average(df, 'close', 21)['zlema']

    Returns:
    - pd.DataFrame: DataFrame with 'zlema' column.
    """
    lag = int((period - 1) / 2)

    # Calculating the adjusted data series
    ema_data = df[column] + (df[column] - df[column].shift(lag))

    # Computing the EMA of the adjusted data series
    zlema = ema_data.ewm(span=period, adjust=False).mean()

    df_copy = df.copy()
    df_copy["zlema"] = zlema

    return df_copy[["zlema"]]
