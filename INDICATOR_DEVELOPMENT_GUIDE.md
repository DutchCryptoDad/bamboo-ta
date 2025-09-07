# Bamboo-TA Technical Indicator Development Guide

## Table of Contents
1. [Overview](#overview)
2. [Coding Standards](#coding-standards)
3. [Indicator Structure](#indicator-structure)
4. [Documentation Requirements](#documentation-requirements)
5. [Testing Framework](#testing-framework)
6. [Available Indicators](#available-indicators)
7. [Usage Examples](#usage-examples)
8. [Integration with Trading Platforms](#integration-with-trading-platforms)
9. [Best Practices](#best-practices)
10. [Common Patterns](#common-patterns)

## Overview

Bamboo-TA is a comprehensive Python library for technical analysis indicators designed for algorithmic trading. It provides a collection of TA indicators organized into modular categories that complement existing libraries like pandas-ta, ta-lib, and qtpylib.

### Key Design Principles
- **Self-contained indicators**: Each indicator calculates all dependencies internally
- **Consistent API**: Uniform function signatures and return patterns
- **DataFrame-based**: Works with pandas DataFrames containing OHLCV data
- **Modular architecture**: Organized by indicator categories
- **Testing integrated**: Built-in testing framework for validation

## Coding Standards

### File Structure
```
# Standard file header
# -*- coding: utf-8 -*-
# indicator_name.py

import pandas as pd
import numpy as np  # If needed

def indicator_name(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.DataFrame:
    """Brief description"""
    # Implementation
    
# Detailed docstring assignment
indicator_name.__doc__ = """..."""

def test():
    """Test function"""
    # Testing implementation

if __name__ == "__main__":
    test()
```

### Naming Conventions
- **File names**: Use snake_case (e.g., `relative_strength_index.py`)
- **Function names**: Use snake_case (e.g., `relative_strength_index()`)
- **Variable names**: Use snake_case (e.g., `rolling_avg`)
- **Column names**: Use snake_case for output columns (e.g., `rsi`, `bb_upper`)

### Code Style Requirements
- Follow PEP8 standards
- Use type hints for function parameters and return types
- Include detailed comments explaining calculation steps
- Maintain consistent indentation (4 spaces)
- Use meaningful variable names
- Handle edge cases and invalid parameters

### Error Handling
```python
# Check required columns
required_columns = ["open", "high", "low", "close"]
for col in required_columns:
    if col not in df.columns:
        raise KeyError(f"DataFrame must contain '{col}' column")

# Parameter validation
if period <= 0:
    raise ValueError("Period must be positive")
```

## Indicator Structure

### Core Requirements

#### 1. Self-Contained Functions
Each indicator must be completely independent:
```python
def bollinger_bands(df: pd.DataFrame, column: str = "close", period: int = 20, std_dev: float = 2.0) -> pd.DataFrame:
    """Calculate Bollinger Bands"""
    df_copy = df.copy()
    
    # Calculate SMA (not imported - calculated here)
    sma = df_copy[column].rolling(window=period).mean()
    
    # Calculate standard deviation
    rolling_std = df_copy[column].rolling(window=period).std()
    
    # Calculate bands
    df_copy["bb_upper"] = sma + (rolling_std * std_dev)
    df_copy["bb_middle"] = sma
    df_copy["bb_lower"] = sma - (rolling_std * std_dev)
    
    return df_copy[["bb_upper", "bb_middle", "bb_lower"]]
```

#### 2. Consistent Function Signature
```python
def indicator_name(
    df: pd.DataFrame,           # Always first parameter
    column: str = "close",      # Target column (if applicable)
    period: int = 14,          # Primary period parameter
    # ... other parameters with defaults
) -> pd.DataFrame:             # Always returns DataFrame
```

#### 3. DataFrame Copy Pattern
Always work on a copy to avoid modifying the original DataFrame:
```python
def indicator_name(df: pd.DataFrame, ...):
    df_copy = df.copy()
    # Work with df_copy
    return df_copy[["result_column"]]
```

#### 4. Return Format
Always return a DataFrame with only the calculated columns:
```python
# Single column result
return df_copy[["rsi"]]

# Multiple column result
return df_copy[["bb_upper", "bb_middle", "bb_lower"]]
```

## Documentation Requirements

### Docstring Format
Every indicator must follow this exact docstring format:

```python
indicator_name.__doc__ = """
Name:
    Full Indicator Name (ABBREVIATION)

Description:
    Detailed description of what the indicator measures and how it works.
    Include mathematical background and interpretation guidelines.

More info:
    https://www.investopedia.com/terms/x/example.asp

Parameters:
    - df (pandas.DataFrame): Input DataFrame containing OHLCV data.
    - column (str): The column to analyze. Default is 'close'.
    - period (int): The lookback period. Default is 14.
    - other_param (type): Description of parameter. Default is value.

Call with:
    df['rsi'] = bta.relative_strength_index(df)['rsi']
    
    # Or for multiple outputs:
    bb_result = bta.bollinger_bands(df, 'close', 20, 2.0)
    df['bb_upper'] = bb_result['bb_upper']
    df['bb_middle'] = bb_result['bb_middle']
    df['bb_lower'] = bb_result['bb_lower']

Returns:
    pd.DataFrame: DataFrame with 'column_name' containing the indicator values.
"""
```

### Documentation Sections Explained

- **Name**: Official name with common abbreviation
- **Description**: Clear explanation of purpose and calculation method
- **More info**: Link to authoritative source (Investopedia, academic papers)
- **Parameters**: Complete list with types and defaults
- **Call with**: Practical usage examples showing assignment patterns
- **Returns**: Exact description of returned DataFrame structure

## Testing Framework

### Test Function Structure
Every indicator file must include a test function:

```python
def test():
    """
    Test function for the indicator_name indicator.
    
    This function uses the generic test_indicator function from bamboo_ta.py
    to test the indicator_name indicator.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Import the test_indicator function from bamboo_ta
        from bamboo_ta.bamboo_ta import test_indicator
        
        # Test the indicator
        test_indicator(indicator_name)
        
    except ImportError:
        print("Error: Could not import test_indicator from bamboo_ta.bamboo_ta")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    test()
```

### Generic Test Function
The `test_indicator()` function in `bamboo_ta.py` provides standardized testing:
- Loads test data from `data/` directory
- Applies indicator with default parameters
- Displays results in tabular format
- Handles errors gracefully

### Running Tests
```bash
# Test individual indicator
python -m bamboo_ta.momentum.relative_strength_index

# Test with specific timeframe
python test_indicators.py relative_strength_index 4h

# Test all indicators
python test_all_indicators.py
```

## Available Indicators

### Momentum Indicators (48 indicators)
- **Oscillators**: RSI, Stochastic, Williams %R, CCI, ROC
- **MACD Family**: MACD, MACD Leader, MACD Volume
- **Specialized**: Awesome Oscillator, QQE, Wave Trend, Ultimate Oscillator
- **Advanced**: Fisher Transform, Inertia, TTM Squeeze

### Trend Indicators (58 indicators)
- **Moving Averages**: SMA, EMA, WMA, HMA, T3, ALMA, KAMA
- **Channels**: Bollinger Trend, SSL Channels, Price Channel
- **Trend Following**: SuperTrend, Parabolic SAR, UT Bot, PMAX
- **Advanced**: Nadaraya Watson Smoothers, FRAMA Channel

### Volatility Indicators (16 indicators)
- **Bands**: Bollinger Bands, Keltner Channel, Donchian Channel
- **Range Measures**: Average True Range, True Range, Ulcer Index
- **Volatility**: Relative Volatility Index, Mass Index

### Volume Indicators (21 indicators)
- **Volume Flow**: On Balance Volume, Accumulation Distribution, Chaikin Money Flow
- **Volume Oscillators**: Price Volume Oscillator, Volume Weighted Average Price
- **Advanced**: Klinger Volume Oscillator, Time Relative Volume

### Candlestick Patterns (7 indicators)
- **Modified Candles**: Heiken Ashi, Linear Regression Candles
- **Pattern Detection**: Candlestick Patterns, Exhaustion Bars
- **Smoothed Variants**: Smoothed Heiken Ashi

### Utility Functions (57 functions)
- **Mathematical**: Standard Deviation, Z-Score, Linear Regression
- **Trading Utils**: Stop Loss/Take Profit, Pump/Dump Protection
- **Statistical**: Entropy, Kurtosis, Skewness, Quantile
- **Performance**: Returns, Drawdown, Sharpe Ratio

### Cycles (1 indicator)
- **Cycle Analysis**: Even Better Sinewave

## Usage Examples

### Basic Usage Pattern
```python
import bamboo_ta as bta
import pandas as pd

# Load your data (must contain: open, high, low, close, volume)
df = pd.read_csv('your_data.csv')

# Single indicator
df['rsi'] = bta.relative_strength_index(df, 'close', 14)['rsi']

# Multiple outputs
bb_result = bta.bollinger_bands(df, 'close', 20, 2.0)
df['bb_upper'] = bb_result['bb_upper']
df['bb_middle'] = bb_result['bb_middle'] 
df['bb_lower'] = bb_result['bb_lower']
```

### Advanced Usage with Custom Parameters
```python
# RSI with different period and source
df['rsi_21'] = bta.relative_strength_index(df, 'high', 21)['rsi']

# MACD with custom parameters
macd_result = bta.macd(df, 'close', 12, 26, 9)
df['macd'] = macd_result['macd']
df['macd_signal'] = macd_result['macd_signal']
df['macd_histogram'] = macd_result['macd_histogram']

# Bollinger Bands with different standard deviation
bb_tight = bta.bollinger_bands(df, 'close', 20, 1.5)
df['bb_tight_upper'] = bb_tight['bb_upper']
df['bb_tight_lower'] = bb_tight['bb_lower']
```

### Combining Indicators
```python
# Trend + Momentum confirmation
df['ema_50'] = bta.exponential_moving_average(df, 'close', 50)['ema']
df['rsi'] = bta.relative_strength_index(df, 'close', 14)['rsi']

# Multi-timeframe approach (requires resampling)
df_4h = df.resample('4h').agg({
    'open': 'first',
    'high': 'max', 
    'low': 'min',
    'close': 'last',
    'volume': 'sum'
})
df_4h['trend_4h'] = bta.supertrend(df_4h)['supertrend']
```

## Integration with Trading Platforms

### Freqtrade Integration

#### Strategy Implementation
```python
# In your Freqtrade strategy file
import bamboo_ta as bta

class YourStrategy(IStrategy):
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe['rsi'] = bta.relative_strength_index(dataframe, 'close', 14)['rsi']
        
        # Bollinger Bands
        bb_result = bta.bollinger_bands(dataframe, 'close', 20, 2.0)
        dataframe['bb_upper'] = bb_result['bb_upper']
        dataframe['bb_middle'] = bb_result['bb_middle']
        dataframe['bb_lower'] = bb_result['bb_lower']
        
        # MACD
        macd_result = bta.macd(dataframe, 'close', 12, 26, 9)
        dataframe['macd'] = macd_result['macd']
        dataframe['macd_signal'] = macd_result['macd_signal']
        
        return dataframe
    
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (dataframe['rsi'] < 30) &  # Oversold
                (dataframe['close'] < dataframe['bb_lower']) &  # Below BB lower
                (dataframe['macd'] > dataframe['macd_signal'])  # MACD bullish
            ),
            'enter_long'] = 1
        return dataframe
```

#### Requirements.txt Addition
```
bamboo-ta>=0.9.4
```

### Other Platform Integration

#### QuantConnect
```python
import bamboo_ta as bta

class YourAlgorithm(QCAlgorithm):
    def Initialize(self):
        # Setup code
        pass
    
    def OnData(self, data):
        # Convert QC data to pandas DataFrame
        df = self.History(self.symbol, 100, Resolution.Hour)
        df = df.reset_index()
        
        # Apply indicators
        df['rsi'] = bta.relative_strength_index(df, 'close', 14)['rsi']
        
        # Trading logic
        if df['rsi'].iloc[-1] < 30:
            self.SetHoldings(self.symbol, 1.0)
```

#### Backtrader
```python
import bamboo_ta as bta
import backtrader as bt

class YourStrategy(bt.Strategy):
    def __init__(self):
        # Convert backtrader data to pandas
        self.df = pd.DataFrame({
            'open': [x[0] for x in self.data.open.get(size=100)],
            'high': [x[0] for x in self.data.high.get(size=100)],
            'low': [x[0] for x in self.data.low.get(size=100)],
            'close': [x[0] for x in self.data.close.get(size=100)],
            'volume': [x[0] for x in self.data.volume.get(size=100)]
        })
        
        # Calculate indicators
        self.rsi_values = bta.relative_strength_index(self.df, 'close', 14)['rsi']
```

## Best Practices

### Performance Optimization
1. **Minimize DataFrame copies**: Only copy when necessary
2. **Use vectorized operations**: Prefer pandas operations over loops
3. **Avoid chained operations**: Use `.loc[]` for assignments
4. **Cache calculations**: Store intermediate results when reused

### Memory Management
```python
# Good: Minimal memory usage
def efficient_indicator(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df_copy = df[['close']].copy()  # Only copy needed columns
    df_copy['result'] = df_copy['close'].rolling(period).mean()
    return df_copy[['result']]

# Avoid: Copying entire DataFrame unnecessarily
def inefficient_indicator(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    df_copy = df.copy()  # Copies all columns
    # ... calculations
    return df_copy[['result']]
```

### Error Handling Best Practices
```python
def robust_indicator(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.DataFrame:
    # Input validation
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")
    
    if column not in df.columns:
        raise KeyError(f"Column '{column}' not found in DataFrame")
    
    if period <= 0:
        raise ValueError("Period must be positive")
    
    if len(df) < period:
        raise ValueError(f"DataFrame must have at least {period} rows")
    
    # Safe computation with proper handling of edge cases
    df_copy = df.copy()
    result = df_copy[column].rolling(window=period, min_periods=period).mean()
    df_copy['indicator'] = result
    
    return df_copy[['indicator']]
```

## Common Patterns

### Moving Average Pattern
```python
def moving_average_indicator(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.DataFrame:
    df_copy = df.copy()
    
    # Simple Moving Average
    df_copy['sma'] = df_copy[column].rolling(window=period).mean()
    
    # Exponential Moving Average  
    df_copy['ema'] = df_copy[column].ewm(span=period, adjust=False).mean()
    
    # Weighted Moving Average
    weights = np.arange(1, period + 1)
    df_copy['wma'] = df_copy[column].rolling(period).apply(
        lambda x: np.dot(x, weights) / weights.sum(), raw=True
    )
    
    return df_copy[['sma', 'ema', 'wma']]
```

### Oscillator Pattern
```python
def oscillator_indicator(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.DataFrame:
    df_copy = df.copy()
    
    # Calculate price changes
    delta = df_copy[column].diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate moving averages
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    # Calculate oscillator
    rs = avg_gains / avg_losses
    oscillator = 100 - (100 / (1 + rs))
    
    df_copy['oscillator'] = oscillator
    
    return df_copy[['oscillator']]
```

### Multi-Column Output Pattern
```python
def band_indicator(df: pd.DataFrame, column: str = "close", period: int = 20, multiplier: float = 2.0) -> pd.DataFrame:
    df_copy = df.copy()
    
    # Calculate middle line
    middle = df_copy[column].rolling(window=period).mean()
    
    # Calculate standard deviation
    std = df_copy[column].rolling(window=period).std()
    
    # Calculate bands
    df_copy['upper'] = middle + (std * multiplier)
    df_copy['middle'] = middle
    df_copy['lower'] = middle - (std * multiplier)
    
    # Optional: Calculate additional metrics
    df_copy['width'] = (df_copy['upper'] - df_copy['lower']) / df_copy['middle'] * 100
    df_copy['percent_b'] = (df_copy[column] - df_copy['lower']) / (df_copy['upper'] - df_copy['lower'])
    
    return df_copy[['upper', 'middle', 'lower', 'width', 'percent_b']]
```

### Self-Contained Dependency Pattern
```python
def complex_indicator(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.DataFrame:
    """Indicator that needs ATR but calculates it internally"""
    df_copy = df.copy()
    
    # Calculate True Range (needed for ATR)
    high_low = df_copy['high'] - df_copy['low']
    high_close = abs(df_copy['high'] - df_copy['close'].shift())
    low_close = abs(df_copy['low'] - df_copy['close'].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    
    # Calculate ATR (dependency calculated internally)
    atr = true_range.rolling(window=period).mean()
    
    # Use ATR in main calculation
    df_copy['complex_indicator'] = df_copy[column] / atr
    
    return df_copy[['complex_indicator']]
```

---

## Conclusion

This guide provides the foundation for developing high-quality technical indicators for the Bamboo-TA library. Following these standards ensures consistency, reliability, and ease of integration across different trading platforms.

For questions or contributions, refer to the project repository and existing indicator implementations as examples.