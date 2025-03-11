# -*- coding: utf-8 -*-
# filter_by_dates.py

import pandas as pd
from typing import Union, List


def filter_by_dates(df: pd.DataFrame, dates: Union[str, List[str]]) -> pd.DataFrame:
    """Filter DataFrame by Specific Dates"""
    # Create a copy of the DataFrame to avoid modifying the original
    df_copy = df.copy()

    # Validate input
    if dates is None:
        return df_copy

    # Convert single date to list if needed
    if not isinstance(dates, list):
        dates = [dates]

    # Filter DataFrame for specified dates
    try:
        # Convert string dates to datetime explicitly to avoid the FutureWarning
        if df_copy.index.dtype.kind == "M":  # Check if index is datetime
            # Convert all dates to pandas datetime objects
            dt_dates = pd.to_datetime(dates)
            # Filter using the converted dates
            filtered_df = df_copy[df_copy.index.isin(dt_dates)]
        else:
            # Use the original method for non-datetime indices
            filtered_df = df_copy[df_copy.index.isin(dates)]

        # If no dates were found, return original DataFrame
        if filtered_df.empty:
            return df_copy

        return filtered_df
    except Exception as e:
        # Handle potential issues with date filtering
        raise ValueError(f"Error filtering DataFrame by dates: {str(e)}")


filter_by_dates.__doc__ = """
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
"""


def test():
    """
    Test function for the filter_by_dates function.

    This function creates a simple test DataFrame with dates and tests
    the filter_by_dates functionality with various date selections.

    Returns:
        None: Displays the results to the console
    """
    try:
        # Create a test DataFrame with daily dates
        import numpy as np

        # Create a date range for all of 2023
        dates = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")

        # Create a test DataFrame
        test_df = pd.DataFrame(
            {
                "close": np.random.rand(len(dates)) * 100,
                "volume": np.random.randint(1000, 100000, len(dates)),
            },
            index=dates,
        )

        # Test case 1: Filter for a single date
        single_date = "2023-05-15"
        single_date_df = filter_by_dates(test_df, single_date)

        # Test case 2: Filter for multiple dates
        multi_dates = ["2023-03-01", "2023-06-15", "2023-09-30", "2023-12-25"]
        multi_date_df = filter_by_dates(test_df, multi_dates)

        # Test case 3: Filter for non-existent dates
        invalid_dates = ["2022-01-01", "2024-01-01"]
        invalid_date_df = filter_by_dates(test_df, invalid_dates)

        # Print results
        print(f"Original DataFrame shape: {test_df.shape}")

        print(f"\nSingle date filter ('{single_date}') results:")
        print(f"Result shape: {single_date_df.shape}")
        print(single_date_df)

        print(f"\nMultiple date filter {multi_dates} results:")
        print(f"Result shape: {multi_date_df.shape}")
        print(multi_date_df)

        print(f"\nInvalid date filter {invalid_dates} results:")
        print(f"Result shape: {invalid_date_df.shape}")
        if invalid_date_df.equals(test_df):
            print("Original DataFrame returned (as expected)")

    except Exception as e:
        print(f"Error during testing: {e}")


# Execute the test if this file is run directly
if __name__ == "__main__":
    test()
