# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from .bamboo_ta import *
from .trend import *


def accumulation_distribution_index(
    df: pd.DataFrame, fillna: bool = False
) -> pd.DataFrame:
    """
    Accumulation/Distribution Index (ADI)

    The ADI acts as a leading indicator of price movements. It is calculated using the
    high, low, close, and volume data.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - fillna (bool): If True, fill NaN values.

    Call with:
        df['adi'] = bta.accumulation_distribution_index(df, fillna=True)['adi']

    Returns:
    - pd.DataFrame: DataFrame with 'adi' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the ADI values
    clv = (
        (df_copy["close"] - df_copy["low"]) - (df_copy["high"] - df_copy["close"])
    ) / (df_copy["high"] - df_copy["low"])
    clv = clv.fillna(0.0)  # Handling division by zero
    adi = clv * df_copy["volume"]
    adi = adi.cumsum()

    if fillna:
        adi = adi.fillna(0)

    df_copy["adi"] = adi

    return df_copy[["adi"]]


def chaikin_money_flow(
    df: pd.DataFrame, window: int = 20, fillna: bool = False
) -> pd.DataFrame:
    """
    Chaikin Money Flow (CMF)

    The Chaikin Money Flow measures the amount of Money Flow Volume over a specific period.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): Number of periods for the calculation. Default is 20.
    - fillna (bool): If True, fill NaN values with 0.

    Call with:
        df['cmf'] = bta.chaikin_money_flow(df, window=20, fillna=True)['cmf']

    Returns:
    - pd.DataFrame: DataFrame with 'cmf' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the Money Flow Multiplier (MFV)
    mfv = (
        (df_copy["close"] - df_copy["low"]) - (df_copy["high"] - df_copy["close"])
    ) / (df_copy["high"] - df_copy["low"])
    mfv = mfv.fillna(0.0)  # Handling division by zero
    mfv *= df_copy["volume"]

    # Calculate CMF: sum of MFV over window divided by the sum of volume over the same window
    min_periods = 0 if fillna else window
    cmf = (
        mfv.rolling(window, min_periods=min_periods).sum()
        / df_copy["volume"].rolling(window, min_periods=min_periods).sum()
    )

    # Fill NaN values if fillna is True
    if fillna:
        cmf = cmf.fillna(0)

    df_copy["cmf"] = cmf

    return df_copy[["cmf"]]


def ease_of_movement(
    df: pd.DataFrame, eom_length: int = 14, seom_length: int = 14, fillna: bool = False
) -> pd.DataFrame:
    """
    Ease of Movement (EoM, EMV) and Signal Ease of Movement (SMA of EoM)

    Relates an asset's price change to its volume and is useful for assessing trend strength.
    The SMA of the EoM serves as a signal line for the indicator.

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
    - pd.DataFrame: DataFrame with 'eom' and 'seom' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the Ease of Movement (EoM) values
    emv = (
        (df_copy["high"].diff(1) + df_copy["low"].diff(1))
        * (df_copy["high"] - df_copy["low"])
    ) / (2 * df_copy["volume"])
    emv *= 100000000
    if fillna:
        emv = emv.fillna(0)

    df_copy["eom"] = emv / 100000  # No rounding per your preference

    # Calculate the Signal Ease of Movement (SMA of EoM)
    min_periods = 0 if fillna else seom_length
    sma_emv = df_copy["eom"].rolling(seom_length, min_periods=min_periods).mean()
    if fillna:
        sma_emv = sma_emv.fillna(0)

    df_copy["seom"] = sma_emv

    return df_copy[["eom", "seom"]]


def force_index(
    df: pd.DataFrame, window: int = 13, fillna: bool = False
) -> pd.DataFrame:
    """
    Force Index (FI)

    Illustrates how strong the actual buying or selling pressure is.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - window (int): Period for calculating the exponential moving average of the Force Index. Default is 13.
    - fillna (bool): If True, fill NaN values.

    Call with:
        df['fi'] = bta.force_index(df, window=13, fillna=True)['fi']

    Returns:
    - pd.DataFrame: DataFrame with 'fi' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate the Force Index values
    fi = (df_copy["close"] - df_copy["close"].shift(1)) * df_copy["volume"]
    fi_ema = fi.ewm(span=window, adjust=False).mean()
    if fillna:
        fi_ema = fi_ema.fillna(0)

    df_copy["fi"] = fi_ema

    return df_copy[["fi"]]


def money_flow_index(
    df: pd.DataFrame, window: int = 14, fillna: bool = False
) -> pd.DataFrame:
    """
    Money Flow Index (MFI)

    Uses both price and volume to measure buying and selling pressure.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): Period for calculating MFI. Default is 14.
    - fillna (bool): If True, fill NaN values.

    Call with:
        df['mfi'] = bta.money_flow_index(df, window=14, fillna=True)['mfi']

    Returns:
    - pd.DataFrame: DataFrame with 'mfi' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate typical price
    typical_price = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3.0
    up_down = np.where(
        typical_price > typical_price.shift(1),
        1,
        np.where(typical_price < typical_price.shift(1), -1, 0),
    )
    mfr = typical_price * df_copy["volume"] * up_down

    # Calculate positive and negative money flow
    min_periods = 0 if fillna else window
    n_positive_mf = mfr.rolling(window, min_periods=min_periods).apply(
        lambda x: np.sum(np.where(x >= 0.0, x, 0.0)), raw=True
    )
    n_negative_mf = abs(
        mfr.rolling(window, min_periods=min_periods).apply(
            lambda x: np.sum(np.where(x < 0.0, x, 0.0)), raw=True
        )
    )

    # Calculate Money Flow Index
    mfi = n_positive_mf / n_negative_mf
    mfi = 100 - (100 / (1 + mfi))
    if fillna:
        mfi = mfi.fillna(50)

    df_copy["mfi"] = mfi

    return df_copy[["mfi"]]


def negative_volume_index(
    df: pd.DataFrame,
    signal_type: str = "EMA",
    signal_length: int = 255,
    fillna: bool = False,
) -> pd.DataFrame:
    """
    Negative Volume Index (NVI) with Signal Smoothing

    The Negative Volume Index (NVI) measures price changes on days when trading volume decreases compared to the previous day.
    Informed traders are thought to be more active on low volume days, hence the NVI accumulates price rate of change only on such days.

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
    - pd.DataFrame: DataFrame with 'nvi' and 'nvi_signal' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate Rate of Change (ROC)
    df_copy["roc"] = df_copy["close"].pct_change() * 100

    # Initialize the NVI starting from the first valid value
    df_copy["nvi"] = 1000  # Starting point for NVI, common practice

    # Calculate NVI values only when volume decreases
    for i in range(1, len(df_copy)):
        if df_copy["volume"].iloc[i] < df_copy["volume"].iloc[i - 1]:
            df_copy.loc[df_copy.index[i], "nvi"] = (
                df_copy["nvi"].iloc[i - 1] + df_copy["roc"].iloc[i]
            )
        else:
            df_copy.loc[df_copy.index[i], "nvi"] = df_copy["nvi"].iloc[i - 1]

    # Calculate NVI Signal
    if signal_type == "EMA":
        df_copy["nvi_signal"] = (
            df_copy["nvi"].ewm(span=signal_length, adjust=False).mean()
        )
    elif signal_type == "SMA":
        df_copy["nvi_signal"] = (
            df_copy["nvi"].rolling(window=signal_length, min_periods=1).mean()
        )
    else:
        raise ValueError(f"Invalid signal_type: {signal_type}. Use 'EMA' or 'SMA'.")

    if fillna:
        df_copy["nvi"] = df_copy["nvi"].fillna(0)
        df_copy["nvi_signal"] = df_copy["nvi_signal"].fillna(0)

    return df_copy[["nvi", "nvi_signal"]]


def on_balance_volume(
    df: pd.DataFrame,
    signal_type: str = "SMA",
    signal_length: int = 21,
    show_signal: bool = True,
    fillna: bool = False,
) -> pd.DataFrame:
    """
    On Balance Volume (OBV) with Signal Smoothing

    The On Balance Volume (OBV) indicator measures buying and selling pressure by accumulating volume based on price movements.
    When the close price is higher than the previous close, the volume is added to the OBV; when lower, it's subtracted.
    Rising OBV indicates buying pressure, and falling OBV suggests selling pressure.

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
    - pd.DataFrame: DataFrame with 'obv' and 'signal' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate OBV
    df_copy["change"] = df_copy["close"].diff()
    df_copy["obv"] = np.where(
        df_copy["change"] > 0,
        df_copy["volume"],
        np.where(df_copy["change"] < 0, -df_copy["volume"], 0),
    )
    df_copy["obv"] = df_copy["obv"].cumsum()

    # Calculate Signal if requested
    if show_signal:
        if signal_type == "EMA":
            df_copy["signal"] = (
                df_copy["obv"].ewm(span=signal_length, adjust=False).mean()
            )
        elif signal_type == "SMA":
            df_copy["signal"] = (
                df_copy["obv"].rolling(window=signal_length, min_periods=1).mean()
            )
        else:
            raise ValueError(f"Invalid signal_type: {signal_type}. Use 'EMA' or 'SMA'.")
    else:
        df_copy["signal"] = np.nan

    # Fill NaN values if requested
    if fillna:
        df_copy["obv"] = df_copy["obv"].fillna(0)
        df_copy["signal"] = df_copy["signal"].fillna(0)

    return df_copy[["obv", "signal"]]


def on_balance_volume_oscillator(
    df: pd.DataFrame, length: int = 20, fillna: bool = False
) -> pd.DataFrame:
    """
    On Balance Volume (OBV) Oscillator

    The On Balance Volume (OBV) Oscillator measures the difference between the OBV and its Exponential Moving Average (EMA).
    It helps in identifying trends and confirming price movements. An increasing OBV oscillator indicates buying pressure, while a decreasing one indicates selling pressure.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'close' and 'volume' columns.
    - length (int): Length for the EMA calculation. Default is 20.
    - fillna (bool): If True, fill nan values with 0.

    Call with:
        df['obv_oscillator'] = bta.on_balance_volume_oscillator(df, length=20, fillna=True)['obv_oscillator']

    Returns:
    - pd.DataFrame: DataFrame with 'obv_oscillator' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate OBV
    df_copy["change"] = df_copy["close"].diff()
    df_copy["obv"] = np.where(
        df_copy["change"] > 0,
        df_copy["volume"],
        np.where(df_copy["change"] < 0, -df_copy["volume"], 0),
    )
    df_copy["obv"] = df_copy["obv"].cumsum()

    # Calculate OBV Oscillator
    df_copy["ema_obv"] = df_copy["obv"].ewm(span=length, adjust=False).mean()
    df_copy["obv_oscillator"] = df_copy["obv"] - df_copy["ema_obv"]

    # Fill NaN values if requested
    if fillna:
        df_copy["obv_oscillator"] = df_copy["obv_oscillator"].fillna(0)

    return df_copy[["obv_oscillator"]]


def positive_volume_index(
    df: pd.DataFrame,
    signal_type: str = "EMA",
    signal_length: int = 255,
    fillna: bool = False,
) -> pd.DataFrame:
    """
    Positive Volume Index (PVI) with Signal Smoothing

    The Positive Volume Index (PVI) measures price changes on days when the trading volume increases compared to the previous day. It accumulates the price rate of change on those days, helping to identify trends driven by high-volume activity.

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
    - pd.DataFrame: DataFrame with 'pvi' and 'pvi_signal' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate Rate of Change (ROC)
    df_copy["roc"] = df_copy["close"].pct_change() * 100

    # Initialize PVI column with appropriate dtype
    df_copy["pvi"] = 0.0

    # Calculate PVI
    pvi_condition = df_copy["volume"] > df_copy["volume"].shift(1)
    df_copy.loc[pvi_condition, "pvi"] = df_copy["roc"]
    df_copy["pvi"] = df_copy["pvi"].cumsum().shift(1).fillna(0)

    # Calculate PVI Signal
    if signal_type == "EMA":
        df_copy["pvi_signal"] = (
            df_copy["pvi"].ewm(span=signal_length, adjust=False).mean()
        )
    elif signal_type == "SMA":
        df_copy["pvi_signal"] = (
            df_copy["pvi"].rolling(window=signal_length, min_periods=1).mean()
        )
    else:
        raise ValueError(f"Invalid signal_type: {signal_type}. Use 'EMA' or 'SMA'.")

    if fillna:
        df_copy["pvi"] = df_copy["pvi"].fillna(0)
        df_copy["pvi_signal"] = df_copy["pvi_signal"].fillna(0)

    return df_copy[["pvi", "pvi_signal"]]


def price_volume_trend(
    df: pd.DataFrame,
    fillna: bool = False,
    smoothing_factor: int = None,
    signal_type: str = "SMA",
    signal_length: int = 21,
    dropnans: bool = False,
) -> pd.DataFrame:
    """
    Price Volume Trend (PVT)

    Based on cumulative volume that adds or subtracts a multiple of the percentage change in share price trend.
    PVT = [((CurrentClose - PreviousClose) / PreviousClose) x Volume] + PreviousPVT

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
    - pd.DataFrame: DataFrame with 'price_volume_trend' and 'signal' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Initialize PVT column
    df_copy["price_volume_trend"] = 0.0

    # Calculate PVT iteratively
    for i in range(1, len(df_copy)):
        prev_pvt = df_copy.at[i - 1, "price_volume_trend"]
        price_change = (
            df_copy.at[i, "close"] - df_copy.at[i - 1, "close"]
        ) / df_copy.at[i - 1, "close"]
        df_copy.at[i, "price_volume_trend"] = (
            price_change * df_copy.at[i, "volume"] + prev_pvt
        )

    # Optional smoothing
    if smoothing_factor:
        min_periods = 0 if fillna else smoothing_factor
        df_copy["price_volume_trend"] = (
            df_copy["price_volume_trend"]
            .rolling(smoothing_factor, min_periods=min_periods)
            .mean()
        )

    if dropnans:
        df_copy["price_volume_trend"] = df_copy["price_volume_trend"].dropna()

    if fillna:
        df_copy["price_volume_trend"] = df_copy["price_volume_trend"].fillna(0)

    # Calculate signal based on the specified type
    if signal_type == "SMA":
        df_copy["signal"] = (
            df_copy["price_volume_trend"]
            .rolling(window=signal_length, min_periods=1 if fillna else signal_length)
            .mean()
        )
    elif signal_type == "EMA":
        df_copy["signal"] = (
            df_copy["price_volume_trend"]
            .ewm(
                span=signal_length,
                adjust=False,
                min_periods=1 if fillna else signal_length,
            )
            .mean()
        )
    else:
        raise ValueError("signal_type must be either 'SMA' or 'EMA'")

    if dropnans:
        df_copy["signal"] = df_copy["signal"].dropna()

    if fillna:
        df_copy["signal"] = df_copy["signal"].fillna(0)

    return df_copy[["price_volume_trend", "signal"]]


def relative_volume(
    df: pd.DataFrame, volume_col: str = "volume", window: int = 24
) -> pd.DataFrame:
    """
    Relative Volume (RVOL)

    Computes the Relative Volume (RVOL) indicator, which compares the current volume
    to a moving average of volume over a specified window. This helps identify periods
    of unusually high or low trading activity.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing a volume column.
    - volume_col (str): Name of the column containing volume data. Default is 'volume'.
    - window (int): Lookback window for calculating the Simple Moving Average (SMA) of volume. Default is 24.

    Call with:
        df['rvol'] = bta.relative_volume(df, volume_col='volume', window=24)['rvol']

    Returns:
    - pd.DataFrame: DataFrame with an additional column:
        - 'rvol': The Relative Volume values.
    """
    # Create a copy of the DataFrame to prevent modifying the original
    df_copy = df.copy()

    # Calculate the SMA of the volume
    df_copy["volume_sma"] = df_copy[volume_col].rolling(window=window).mean()

    # Calculate Relative Volume
    df_copy["rvol"] = df_copy[volume_col] / df_copy["volume_sma"]

    # Return the DataFrame with the RVOL column
    return df_copy[["rvol"]]


def time_relative_volume_oscillator(
    df: pd.DataFrame,
    column: str = "close",
    relative_len: int = 6,
    delta_smoothing: int = 9,
    smoothing_line: bool = True,
    show_total_volume: bool = False,
) -> pd.DataFrame:
    """
    Time Relative Volume Oscillator (TRVO) - Delta Mode

    This indicator measures relative volume compared to historical values and differentiates
    between buy and sell volumes.

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

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing 'high', 'low', 'close', and 'volume'.
    - column (str): Column name for price source (default: "close").
    - relative_len (int): Number of previous periods used for relative volume calculation (default: 6).
    - delta_smoothing (int): Smoothing factor for the buy/sell volume difference (default: 9).
    - smoothing_line (bool): If True, applies EMA smoothing to buy/sell volume difference (default: True).
    - show_total_volume (bool): If True, includes the 'total_volume' column in the output DataFrame (default: False).

    Returns:
    - pd.DataFrame: A DataFrame containing:
        - "relative_buy_volume": Volume attributed to buyers.
        - "relative_sell_volume": Volume attributed to sellers (negative).
        - "buy_vs_sell": Difference between buy and sell volume percentages.
        - "smoothed_delta": EMA-smoothed buy/sell volume difference.
        - "total_volume" (optional): Raw total volume for each period (if show_total_volume=True).
    """

    df_copy = df.copy()

    # Compute 200-period SMA of volume (used for scaling)
    df_copy["volume_sma_200"] = df["volume"].rolling(200).mean()

    # Calculate Relative Volume using the past `relative_len` bars only (shifted by 1 to exclude the current bar)
    df_copy["total_volume"] = df["volume"].shift(1).rolling(relative_len).sum()
    df_copy["relative_volume"] = df["volume"] / (df_copy["total_volume"] / relative_len)

    # Apply Pine Script's sigmoid-like transformation to relative volume
    df_copy["osc"] = 4 / (1 + np.exp(-2 * df_copy["relative_volume"] + 3)) - 0.18

    # Compute final adjusted relative_plot (multiplied by volume_sma_200, no extra factor)
    df_copy["relative_plot"] = df_copy["osc"] * df_copy["volume_sma_200"]

    # Buy/Sell Volume Calculation (weighted by price position in high-low range)
    high_low_range = df["high"] - df["low"]
    df_copy["relative_buy_volume"] = np.where(
        high_low_range == 0,
        0,
        df_copy["relative_plot"] * (df["close"] - df["low"]) / high_low_range,
    )
    # Compute the sell volume as a positive value (for correct percentage calculations)
    df_copy["relative_sell_volume_pos"] = np.where(
        high_low_range == 0,
        0,
        df_copy["relative_plot"] * (df["high"] - df["close"]) / high_low_range,
    )

    # Compute Buy and Sell Volume Percentages using positive values
    eps = 1e-10
    vol_sum = df_copy["relative_buy_volume"] + df_copy["relative_sell_volume_pos"] + eps
    df_copy["buy_volume_percent"] = df_copy["relative_buy_volume"] / vol_sum
    df_copy["sell_volume_percent"] = df_copy["relative_sell_volume_pos"] / vol_sum

    # Compute Buy vs. Sell Difference
    df_copy["buy_vs_sell"] = (
        df_copy["buy_volume_percent"] - df_copy["sell_volume_percent"]
    )

    # Apply EMA Smoothing for Delta Mode
    df_copy["buy_vs_sell_short_ema"] = (
        df_copy["buy_vs_sell"].ewm(span=21, adjust=False).mean()
        * df_copy["volume_sma_200"]
        * 20
    )
    df_copy["buy_vs_sell_long_ema"] = (
        df_copy["buy_vs_sell"].ewm(span=36, adjust=False).mean()
        * df_copy["volume_sma_200"]
        * 20
    )
    df_copy["buy_vs_sell_diff"] = (
        df_copy["buy_vs_sell_short_ema"] - df_copy["buy_vs_sell_long_ema"]
    )

    if smoothing_line:
        df_copy["smoothed_delta"] = (
            df_copy["buy_vs_sell_diff"].ewm(span=delta_smoothing, adjust=False).mean()
        )
    else:
        df_copy["smoothed_delta"] = df_copy["buy_vs_sell_diff"]

    # Now, flip the sign of the sell volume for output (to match Pine Script's negative plotting)
    df_copy["relative_sell_volume"] = -df_copy["relative_sell_volume_pos"]

    # Return selected columns
    columns_to_return = [
        "relative_buy_volume",
        "relative_sell_volume",
        "buy_vs_sell",
        "smoothed_delta",
    ]
    if show_total_volume:
        columns_to_return.append("total_volume")

    return df_copy[columns_to_return]


def volume_weighted_average_price(
    df: pd.DataFrame, window: int = 14, fillna: bool = False
) -> pd.DataFrame:
    """
    Volume Weighted Average Price (VWAP)
    Equals the dollar value of all trading periods divided by the total trading volume for the current day.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain 'high', 'low', 'close', and 'volume' columns.
    - window (int): n period for rolling calculation.
    - fillna (bool): If True, fill nan values.

    Call with:
        df['vwap'] = bta.volume_weighted_average_price(df, window=14, fillna=True)['volume_weighted_average_price']

    Returns:
    - pd.DataFrame: DataFrame with 'volume_weighted_average_price' column.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ["high", "low", "close", "volume"]
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # Calculate typical price
    typical_price = (df_copy["high"] + df_copy["low"] + df_copy["close"]) / 3.0
    typical_price_volume = typical_price * df_copy["volume"]

    # Calculate VWAP over the rolling window
    min_periods = 0 if fillna else window
    total_pv = typical_price_volume.rolling(window, min_periods=min_periods).sum()
    total_volume = df_copy["volume"].rolling(window, min_periods=min_periods).sum()

    # VWAP calculation
    vwap = total_pv / total_volume
    if fillna:
        vwap = vwap.fillna(0)

    # Add the VWAP to the DataFrame
    df_copy["volume_weighted_average_price"] = vwap

    return df_copy[["volume_weighted_average_price"]]


def volume_weighted_average_price_bands(
    df: pd.DataFrame, window_size: int = 20, num_of_std: float = 1.0
) -> pd.DataFrame:
    """
    Volume-Weighted Average Price Bands (VWAPB)

    Calculates the Volume-Weighted Average Price (VWAP) along with upper and lower bands
    based on a rolling standard deviation.

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
    - pd.DataFrame: A DataFrame containing the following columns:
        - 'vwap': The Volume-Weighted Average Price (VWAP).
        - 'vwap_low': The lower band (VWAP - num_of_std × rolling std deviation).
        - 'vwap_high': The upper band (VWAP + num_of_std × rolling std deviation).
    """
    if not {"close", "high", "low", "volume"}.issubset(df.columns):
        raise ValueError(
            "DataFrame must contain 'close', 'high', 'low', and 'volume' columns."
        )

    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Calculate typical price
    df_copy["typical_price"] = (df_copy["close"] + df_copy["high"] + df_copy["low"]) / 3

    # Calculate cumulative VWAP
    df_copy["cum_typical_volume"] = (
        df_copy["typical_price"] * df_copy["volume"]
    ).cumsum()
    df_copy["cum_volume"] = df_copy["volume"].cumsum()
    df_copy["vwap"] = df_copy["cum_typical_volume"] / df_copy["cum_volume"]

    # Calculate rolling standard deviation for VWAP
    rolling_std = df_copy["vwap"].rolling(window=window_size).std()

    # Calculate VWAP bands
    df_copy["vwap_low"] = df_copy["vwap"] - (rolling_std * num_of_std)
    df_copy["vwap_high"] = df_copy["vwap"] + (rolling_std * num_of_std)

    # Return only the relevant columns
    return df_copy[["vwap_low", "vwap", "vwap_high"]]
