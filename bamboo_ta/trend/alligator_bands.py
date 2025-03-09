# -*- coding: utf-8 -*-
# alligator_bands.py
import pandas as pd


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
    """Bill Williams Alligator Indicator"""
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


alligator_bands.__doc__ = """
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
"""
