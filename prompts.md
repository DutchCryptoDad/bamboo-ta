GPT Prompt:
1. You are a developer with extensive knowledge of Python and Pinescript. You have this project where you are converting Pinscripts into Python functions so that you can use these in a library for further data analysis in python. The project structure and code of the Python code will follow. After that wait for further instructions about the pinescript to convert. Is that understood?

2. The following pinsecript should be converted into a python function. If this pinescript is depending on other indicators from other libraries (e.g. pandas-ta), do not use that, but instead create additional functions that will take care of the missing indicators. If the indicators are already available in the given project, then use these indicators. Is this clear?

3. Further instructions based on output GPT.

GPT prompt

1. You are a developer with extensive knowledge of Python and Technical Indicators in Trading. You enherited a project where trading technical analsis indicators are programmed in a TA library with Python functions. However you noticed that the previous programmer was very inconsistent in its programming and functions are build in different ways. Your task is to refactor the code so that all the functions have the same building style, input method, calculation method and output method. Also watch for redundant code and if detected solve this too by pointing to the correct funtion.
The project structure and code of the Python code will follow next. After that wait for further instructions about the definitive way each function should be build for consistency.
Is that understood?

2. The code should be refactored into the same format style as previously mentioned. 
Please be extra aware of the naming convention of the functions, the way the descriptions are written, including the "call with:" example and the way the output is provided by means of the df_copy method and all the dataframe column names should be in lowercase, and keep the output limited to two decimals behind the comma or .. 
Please use the same function style and buildup, inputs and output style, example in the description like "call with" and more from the next example I will provide you next. So format to match the desired style and including a brief description of the indicator's purpose and functionality, with lowercase column names and limiting the output to two decimal places, ensure consistency in how single-column indicators are handled. After this prompt I will provide you with the different modules that have to be refactored.
Is this clear?

3. Here is the example function:

def Waddah_Attar_Explosion(df, sensitivity=150, fast_length=20, slow_length=40, channel_length=20, mult=2.0):
   '''
    Waddah Attar Explosion Indicator

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - sensitivity (int): Sensitivity factor for the indicator. Default is 150.
    - fast_length (int): Length for the fast EMA. Default is 20.
    - slow_length (int): Length for the slow EMA. Default is 40.
    - channel_length (int): Length for the Bollinger Bands. Default is 20.
    - mult (float): Standard deviation multiplier for the Bollinger Bands. Default is 2.0.

    Call with:
        WAE = bta.Waddah_Attar_Explosion(df)
        df['trend_up'] = WAE['trend_up']
        df['trend_down'] = WAE['trend_down']
        df['explosion_line'] = WAE['explosion_line']
        df['dead_zone_line'] = WAE['dead_zone_line']

    Returns:
    - pd.DataFrame: DataFrame with 'trend_up', 'trend_down', 'explosion_line', and 'dead_zone_line' columns.
    '''
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # print("DataFrame columns:", df.columns)  # Debug print
    # print("First few rows of the DataFrame:\n", df.head())  # Debug print

    # Calculate DEAD_ZONE
    dead_zone = RMA(TR(df), 100) * 3.7
    # print("DEAD_ZONE calculated")  # Debug print

    # Calculate MACD
    macd_fast = EMA(df, 'close', fast_length)
    macd_slow = EMA(df, 'close', slow_length)
    macd_diff = macd_fast - macd_slow
    t1 = (macd_diff - macd_diff.shift(1)) * sensitivity
    # print("MACD and t1 calculated")  # Debug print

    # Calculate Bollinger Bands
    bb = BollingerBands(df, column='close', period=channel_length, std_dev=mult)
    e1 = bb['BB_upper'] - bb['BB_lower']
    # print("Bollinger Bands calculated")  # Debug print

    trend_up = np.where(t1 >= 0, t1, 0)
    trend_down = np.where(t1 < 0, -t1, 0)

    df_copy['trend_up'] = trend_up.round(2)
    df_copy['trend_down'] = trend_down.round(2)
    df_copy['explosion_line'] = e1.round(2)
    df_copy['dead_zone_line'] = dead_zone.round(2)

    return df_copy[['trend_up', 'trend_down', 'explosion_line', 'dead_zone_line']]


GPT Prompt:
1. You are a developer with extensive knowledge of Python and Technical Indicators in Trading. You have this project where you are converting Third party Python code into your own TA library with Python functions so that you can use these within your own library in a consequent and familiar way for further data analysis in python. The project structure and code of the Python code will follow. After that wait for further instructions about the third party Python code to convert. Is that understood?

2. The following third party python should be converted into the same format as my own functions  and should also be added to their consequitive modules. Please check first if they already exist, if they do, then ignore these (but say that you will not create these). If the third party Python code is depending on other libraries (e.g. pandas-ta), do not use these external libraries, but instead create additional functions that will take care of the missing functions or indicators. If these dependend functions alreaty exist in your own project, then use those instead. Please be extra aware of the naming convention of these functions, the way the descriptions are written, including the "call with:" example and the way the output is provided by means of the df_copy method. 

3. Further instructions based on output GPT.


GPT Prompt:
1. I have a Readme file that is part of a complete python programm. It contains the descriptions of functions that are in the submoduled. However I have added more functions to these modules and I would like to recreate this Readme section so that it also contains the added funtions. In other words the Readme file is updated with the most current situation. 

I can give you the current modules Readme section now and later the complete contents of all other modules so that you can update the Readme section with this. Do you understand?


1. I now have a competely different question concerning the Readme file I have for this modules library. Can you help me with this too?


2. The original Readme file looks like this, but it now misses a lot of new functions we added to the different modules. Please rewrite this section with the information I give you in the next prompt. There you should extract the functions from the modules and add these to the Readme section in the same original style. Do you understand?

This is the original Readme section:

3. Further instructions based on output GPT.

ChatGPT prompt for refactoring:





[python] Here is an overview of the instructions used to refactor the code, ensuring consistency and clarity across all functions:

### Instructions for Refactoring the Code:

1. **Function Name and Description**:
   - Follow PEP-8 naming conventions.
   - Include a descriptive docstring detailing the function's purpose, parameters, usage example, and return values.
   - Start the docstring with a brief description of the indicator's purpose and functionality.

2. **Parameters**:
   - Clearly define parameters with default values where appropriate.
   - Explain each parameter in the docstring, including the data type and purpose.

3. **Input Validation**:
   - Ensure the input DataFrame contains the required columns.
   - Raise a `KeyError` if any required columns are missing.

4. **Calculations**:
   - Perform calculations step-by-step, with clear comments if necessary.
   - Use appropriate methods for moving averages (e.g., rolling mean for SMA, exponential weighted mean for EMA).

5. **Output**:
   - Return a DataFrame containing the new indicator columns.
   - Ensure all DataFrame column names are in lowercase.
   - Limit the output values to two decimal places using `.round(2)`.

6. **Example Calls**:
   - Include example calls in the docstring, showing how to use the function.
   - Demonstrate how to add the new columns to the original DataFrame.

### Example of a Refactored Function:

#### Heikin Ashi (HA) with Optional Pre and Post Smoothing:

```python
def heikin_ashi(df, pre_smoothing_period=None, post_smoothing_period=None):
    """
    Heikin Ashi (HA) with Optional Pre and Post Smoothing

    Heikin Ashi is a type of price chart that shares some characteristics with candlestick charts but differs due to the values used to plot them. 
    This modified version allows for optional smoothing of the original data before the Heikin Ashi calculation and/or smoothing of the Heikin Ashi values themselves, 
    aiming to provide a more refined and smoother representation of price action, making it easier to identify the trend.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - pre_smoothing_period (int, optional): Period for EMA pre-smoothing of the original data. If provided, original price bars are smoothed before Heikin Ashi calculations.
    - post_smoothing_period (int, optional): Period for EMA post-smoothing of Heikin Ashi values. If provided, Heikin Ashi values are smoothed post calculations.

    Call with:
        ha_df = bta.heikin_ashi(df)
        df['ha_close'] = ha_df['ha_close']
        df['ha_open'] = ha_df['ha_open']
        df['ha_high'] = ha_df['ha_high']
        df['ha_low'] = ha_df['ha_low']

    Returns:
    - pd.DataFrame: DataFrame with 'ha_open', 'ha_high', 'ha_low', and 'ha_close' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # If pre-smoothing is required
    if pre_smoothing_period:
        df_copy['open'] = ema(df_copy, 'open', pre_smoothing_period)
        df_copy['close'] = ema(df_copy, 'close', pre_smoothing_period)
        df_copy['high'] = ema(df_copy, 'high', pre_smoothing_period)
        df_copy['low'] = ema(df_copy, 'low', pre_smoothing_period)

    # Regular Heikin Ashi calculations
    df_copy['ha_close'] = (df_copy['open'] + df_copy['high'] +
                           df_copy['low'] + df_copy['close']) / 4
    df_copy.reset_index(inplace=True)
    ha_open = [(df_copy['open'][0] + df_copy['close'][0]) / 2]
    [ha_open.append((ha_open[i] + df_copy['ha_close'].values[i]) / 2)
     for i in range(0, len(df_copy) - 1)]
    df_copy['ha_open'] = ha_open
    df_copy.set_index('index', inplace=True)
    df_copy['ha_high'] = df_copy[['ha_open', 'ha_close', 'high']].max(axis=1)
    df_copy['ha_low'] = df_copy[['ha_open', 'ha_close', 'low']].min(axis=1)

    # If post-smoothing is required
    if post_smoothing_period:
        df_copy['ha_open'] = ema(df_copy, 'ha_open', post_smoothing_period)
        df_copy['ha_high'] = ema(df_copy, 'ha_high', post_smoothing_period)
        df_copy['ha_low'] = ema(df_copy, 'ha_low', post_smoothing_period)
        df_copy['ha_close'] = ema(df_copy, 'ha_close', post_smoothing_period)

    # Limit to two decimal places
    df_copy['ha_open'] = df_copy['ha_open'].round(2)
    df_copy['ha_high'] = df_copy['ha_high'].round(2)
    df_copy['ha_low'] = df_copy['ha_low'].round(2)
    df_copy['ha_close'] = df_copy['ha_close'].round(2)

    return df_copy[['ha_open', 'ha_high', 'ha_low', 'ha_close']]
```

#### Awesome Oscillator (AO):

```python
def awesome_oscillator(df, window1=5, window2=34, fillna=False):
    """
    Awesome Oscillator (AO)

    The Awesome Oscillator is a momentum indicator used to measure market momentum.
    It is calculated by subtracting a 34-period simple moving average (SMA) of the
    median price from a 5-period SMA of the median price.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high' and 'low'.
    - window1 (int, optional): Short period. Default is 5.
    - window2 (int, optional): Long period. Default is 34.
    - fillna (bool, optional): If True, fill nan values with 0. Default is False.

    Call with:
        df['ao'] = bta.awesome_oscillator(df)

    Returns:
    - pd.DataFrame: DataFrame with 'ao' column.
    """
    df_copy = df.copy()

    median_price = 0.5 * (df['high'] + df['low'])
    min_periods_s = 0 if fillna else window1
    min_periods_l = 0 if fillna else window2
    df_copy['ao'] = (
        median_price.rolling(window1, min_periods=min_periods_s).mean()
        - median_price.rolling(window2, min_periods=min_periods_l).mean()
    )
    if fillna:
        df_copy['ao'] = df_copy['ao'].fillna(0)

    df_copy['ao'] = df_copy['ao'].round(2)
    return df_copy[['ao']]
```

#### Chande Momentum Oscillator (CMO):

```python
def chande_momentum_oscillator(df, length=14):
    """
    Chande Momentum Oscillator (CMO)

    The Chande Momentum Oscillator (CMO) is a technical momentum indicator developed by Tushar Chande. 
    It measures the amount that an asset's price has changed over a specified period of time.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Length for the CMO calculation. Default is 14.

    Call with:
        df['cmo'] = bta.chande_momentum_oscillator(df)

    For Signal line:
        df['cmo_signal'] = df['cmo'].rolling(window=10).mean().round(2)  # Using SMA for signal

    Returns:
    - pd.DataFrame: DataFrame with 'cmo' column.
    """
    df_copy = df.copy()

    mom = df['close'].diff()
    pos_mom = mom.where(mom > 0, 0)
    neg_mom = -mom.where(mom < 0, 0)
    sm1 = pos_mom.rolling(window=length).sum()
    sm2 = neg_mom.rolling(window=length).sum()
    df_copy['cmo'] = 100 * (sm1 - sm2) / (sm1 + sm2)

    df_copy['cmo'] = df_copy['cmo'].round(2)
    return df_copy[['cmo']]
```

### General Refactoring Steps:

1. **Rename Functions and Columns to Lowercase**:
   - Ensure function names and DataFrame columns are in lowercase.

2. **Add Detailed Descriptions**:
   - Add a brief description of the indicator's purpose at the start of the docstring.
   - Include parameters, usage examples, and return types in the docstring.

3. **Ensure Consistent Output Format**:
   - Ensure that all functions return a DataFrame with the new indicator columns.
   - Limit numeric output to two decimal places using `.round(2)`.

By following these steps, you can ensure that all functions are refactored consistently, making it easier to maintain and understand the code in the future


# Another refactoring prompt:
Sure! Here is a comprehensive prompt you can use to repeat this refactoring exercise in the future:

---

**Refactoring Prompt for Trading Technical Analysis Indicators**

### Objective:
Refactor the code for trading technical analysis indicators to ensure consistency in function structure, input methods, calculation methods, and output methods. Pay special attention to naming conventions, descriptions, and formatting. All functions should return a DataFrame with the new indicator columns, and all column names should be in lowercase. Numeric outputs should be limited to two decimal places.

### Instructions:

1. **Function Name and Description**:
   - Follow PEP-8 naming conventions (e.g., `snake_case` for function names).
   - Include a descriptive docstring detailing the function's purpose, parameters, usage example, and return values.
   - Start the docstring with a brief description of the indicator's purpose and functionality.

2. **Parameters**:
   - Clearly define parameters with default values where appropriate.
   - Explain each parameter in the docstring, including the data type and purpose.

3. **Input Validation**:
   - Ensure the input DataFrame contains the required columns.
   - Raise a `KeyError` if any required columns are missing.

4. **Calculations**:
   - Perform calculations step-by-step, with clear comments if necessary.
   - Use appropriate methods for moving averages (e.g., rolling mean for SMA, exponential weighted mean for EMA).

5. **Output**:
   - Return a DataFrame containing the new indicator columns.
   - Ensure all DataFrame column names are in lowercase.
   - Limit the output values to two decimal places using `.round(2)`.

6. **Example Calls**:
   - Include example calls in the docstring, showing how to use the function.
   - Demonstrate how to add the new columns to the original DataFrame.

### Example Refactored Function:

#### Heikin Ashi (HA) with Optional Pre and Post Smoothing:

```python
def heikin_ashi(df, pre_smoothing_period=None, post_smoothing_period=None):
    """
    Heikin Ashi (HA) with Optional Pre and Post Smoothing

    Heikin Ashi is a type of price chart that shares some characteristics with candlestick charts but differs due to the values used to plot them. 
    This modified version allows for optional smoothing of the original data before the Heikin Ashi calculation and/or smoothing of the Heikin Ashi values themselves, 
    aiming to provide a more refined and smoother representation of price action, making it easier to identify the trend.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'open', 'high', 'low', and 'close'.
    - pre_smoothing_period (int, optional): Period for EMA pre-smoothing of the original data. If provided, original price bars are smoothed before Heikin Ashi calculations.
    - post_smoothing_period (int, optional): Period for EMA post-smoothing of Heikin Ashi values. If provided, Heikin Ashi values are smoothed post calculations.

    Call with:
        ha_df = bta.heikin_ashi(df)
        df['ha_close'] = ha_df['ha_close']
        df['ha_open'] = ha_df['ha_open']
        df['ha_high'] = ha_df['ha_high']
        df['ha_low'] = ha_df['ha_low']

    Returns:
    - pd.DataFrame: DataFrame with 'ha_open', 'ha_high', 'ha_low', and 'ha_close' columns.
    """
    df_copy = df.copy()

    # Ensure the DataFrame contains the required columns
    required_columns = ['open', 'high', 'low', 'close']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"DataFrame must contain '{col}' column")

    # If pre-smoothing is required
    if pre_smoothing_period:
        df_copy['open'] = ema(df_copy, 'open', pre_smoothing_period)
        df_copy['close'] = ema(df_copy, 'close', pre_smoothing_period)
        df_copy['high'] = ema(df_copy, 'high', pre_smoothing_period)
        df_copy['low'] = ema(df_copy, 'low', pre_smoothing_period)

    # Regular Heikin Ashi calculations
    df_copy['ha_close'] = (df_copy['open'] + df_copy['high'] +
                           df_copy['low'] + df_copy['close']) / 4
    df_copy.reset_index(inplace=True)
    ha_open = [(df_copy['open'][0] + df_copy['close'][0]) / 2]
    [ha_open.append((ha_open[i] + df_copy['ha_close'].values[i]) / 2)
     for i in range(0, len(df_copy) - 1)]
    df_copy['ha_open'] = ha_open
    df_copy.set_index('index', inplace=True)
    df_copy['ha_high'] = df_copy[['ha_open', 'ha_close', 'high']].max(axis=1)
    df_copy['ha_low'] = df_copy[['ha_open', 'ha_close', 'low']].min(axis=1)

    # If post-smoothing is required
    if post_smoothing_period:
        df_copy['ha_open'] = ema(df_copy, 'ha_open', post_smoothing_period)
        df_copy['ha_high'] = ema(df_copy, 'ha_high', post_smoothing_period)
        df_copy['ha_low'] = ema(df_copy, 'ha_low', post_smoothing_period)
        df_copy['ha_close'] = ema(df_copy, 'ha_close', post_smoothing_period)

    # Limit to two decimal places
    df_copy['ha_open'] = df_copy['ha_open'].round(2)
    df_copy['ha_high'] = df_copy['ha_high'].round(2)
    df_copy['ha_low'] = df_copy['ha_low'].round(2)
    df_copy['ha_close'] = df_copy['ha_close'].round(2)

    return df_copy[['ha_open', 'ha_high', 'ha_low', 'ha_close']]
```

#### Awesome Oscillator (AO):

```python
def awesome_oscillator(df, window1=5, window2=34, fillna=False):
    """
    Awesome Oscillator (AO)

    The Awesome Oscillator is a momentum indicator used to measure market momentum.
    It is calculated by subtracting a 34-period simple moving average (SMA) of the
    median price from a 5-period SMA of the median price.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain columns: 'high' and 'low'.
    - window1 (int, optional): Short period. Default is 5.
    - window2 (int, optional): Long period. Default is 34.
    - fillna (bool, optional): If True, fill nan values with 0. Default is False.

    Call with:
        df['ao'] = bta.awesome_oscillator(df)

    Returns:
    - pd.DataFrame: DataFrame with 'ao' column.
    """
    df_copy = df.copy()

    median_price = 0.5 * (df['high'] + df['low'])
    min_periods_s = 0 if fillna else window1
    min_periods_l = 0 if fillna else window2
    df_copy['ao'] = (
        median_price.rolling(window1, min_periods=min_periods_s).mean()
        - median_price.rolling(window2, min_periods=min_periods_l).mean()
    )
    if fillna:
        df_copy['ao'] = df_copy['ao'].fillna(0)

    df_copy['ao'] = df_copy['ao'].round(2)
    return df_copy[['ao']]
```

#### Chande Momentum Oscillator (CMO):

```python
def chande_momentum_oscillator(df, length=14):
    """
    Chande Momentum Oscillator (CMO)

    The Chande Momentum Oscillator (CMO) is a technical momentum indicator developed by Tushar Chande. 
    It measures the amount that an asset's price has changed over a specified period of time.

    Parameters:
    - df (pandas.DataFrame): Input DataFrame which should contain the 'close' column.
    - length (int): Length for the CMO calculation. Default is 14.

    Call with:
        df['cmo'] = bta.chande_momentum_oscillator(df)

    For Signal line:
        df['cmo_signal'] = df['cmo'].rolling(window=10).mean().round(2)  # Using SMA for signal

    Returns:
    - pd.DataFrame: DataFrame with 'cmo' column.
    """
    df_copy = df.copy()

    mom = df['close'].diff()
    pos_mom = mom.where(mom > 0, 0)
    neg_mom = -mom.where(mom < 0, 0)
    sm1 = pos_mom.rolling(window=length).sum()
    sm2 = neg_mom.rolling(window=length).sum()
    df_copy['cmo'] = 100 * (sm1 - sm2) / (sm1 + sm2)

    df_copy['cmo'] = df_copy['cmo'].round(2)
    return df_copy[['cmo']]
```

### General Refactoring Steps:

1. **Rename Functions and Columns to Lowercase**:
   - Ensure function names and DataFrame columns are in lowercase.

2. **Add Detailed Descriptions**:
   - Add a brief description of the indicator's purpose at the start of the docstring.
   - Include parameters

, usage examples, and return types in the docstring.

3. **Ensure Consistent Output Format**:
   - Ensure that all functions return a DataFrame with the new indicator columns.
   - Limit numeric output to two decimal places using `.round(2)`.

By following these steps and examples, you can ensure that all functions are refactored consistently, making it easier to maintain and understand the code in the future.

---

Feel free to adjust the prompt and instructions as needed for your specific requirements.

