# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bamboo-TA is a Python library for technical analysis indicators designed for algorithmic trading. It provides a comprehensive collection of TA indicators organized into modular categories: candles, cycles, momentum, performance, statistics, trend, utility, volatility, and volume. The library is complementary to pandas-ta, ta-lib, and qtpylib.

You can find more information about this project and instructions in @PROJECT_INSTRUCTIONS.md

## Core Architecture Philosophy

### Self-Sustained Indicator Design
**Critical Principle**: Each indicator must be completely self-contained with ZERO external dependencies to other indicators within the library. This is the fundamental architectural requirement that differentiates Bamboo-TA from other TA libraries.

**Key Design Rules**:
- If an indicator needs ATR, it calculates ATR internally within the same function
- No imports from other indicator modules within the library
- No shared utility functions between indicators (each implements its own calculations)
- Each indicator file is an isolated, executable unit

## Architecture

### Core Structure
- **Main module**: `bamboo_ta/bamboo_ta.py` - Contains generic `test_indicator()` function and imports all indicators
- **Category modules**: Each category (momentum, trend, etc.) has its own directory with `__init__.py` that exports indicators  
- **Individual indicators**: Each indicator is self-contained in its own file with no external dependencies
- **Data format**: Expects pandas DataFrame with columns: 'date', 'open', 'high', 'low', 'close', 'volume'

### Self-Contained Architecture Deep Dive

**Indicator Independence Examples**:
```python
# WRONG: This would create a dependency
from bamboo_ta.volatility import average_true_range

def some_indicator(df):
    atr = average_true_range(df)  # External dependency - NOT ALLOWED

# CORRECT: Calculate ATR internally
def some_indicator(df):
    # Calculate True Range internally
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=14).mean()  # ATR calculated here
```

**Module Import Structure**:
- Only pandas and numpy are imported directly
- Each category's `__init__.py` imports from individual indicator files
- Main `bamboo_ta.py` imports from all category modules
- No cross-indicator imports within the library

### Indicator Requirements
Each indicator file must contain:
1. **Self-contained function** with no external dependencies (if an indicator needs ATR, it calculates it internally)
2. **Detailed docstring** following exact format with Name, Description, More info, Parameters, Call with, Returns sections
3. **`test()` function** that uses `test_indicator()` from bamboo_ta.py
4. **Main block** that calls `test()` if run directly
5. **DataFrame copy pattern** - always work on `df.copy()` to avoid modifying original data

### Code Standards & Formatting Requirements
- Follow PEP8 (snake_case for functions/variables)
- Include detailed comments explaining calculations
- Functions return DataFrames with specific column names
- Error handling for missing columns/invalid parameters
- No deletion of comments unless no longer needed
- **Critical**: Never break the self-contained design principle

## Common Development Commands

### Testing
```bash
# Test specific indicator
python test_indicators.py [indicator_name] [timeframe]
python test_indicators.py relative_strength_index 1d

# Test all indicators
python test_all_indicators.py

# Test individual indicator file directly
python -m bamboo_ta.momentum.relative_strength_index
```

### Package Building
```bash
# Build package
python3 setup.py sdist bdist_wheel

# Install locally for testing
pip install .

# Check package before upload
twine check dist/*

# Upload to test PyPI
twine upload -r testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

### Test Data
- Located in `data/` directory
- Available timeframes: 1d, 4h, 1h, 30m, 15m, 12h, 8h, 5m
- Format: BTC_USDT-{timeframe}.json
- Contains OHLCV data for BTC/USDT pair

## Key Files

- `bamboo_ta/bamboo_ta.py` - Main module with test_indicator function
- `test_indicators.py` - CLI tool for testing individual indicators  
- `test_all_indicators.py` - Tests all indicators in the library
- `setup.py` - Package configuration (version 0.9.4)
- `.cursorrules` - Contains detailed coding standards and examples
- `requirements.txt` - Dependencies: ta, numpy, pandas, pandas_ta, scipy

## Self-Contained Implementation Patterns

### Mandatory Self-Contained Calculations
When an indicator needs common calculations (ATR, EMA, SMA, etc.), they must be implemented within the indicator function itself:

```python
def indicator_requiring_atr(df: pd.DataFrame, atr_period: int = 14) -> pd.DataFrame:
    df_copy = df.copy()
    
    # Self-contained ATR calculation (do NOT import from volatility module)
    high_low = df_copy['high'] - df_copy['low']
    high_close = abs(df_copy['high'] - df_copy['close'].shift())
    low_close = abs(df_copy['low'] - df_copy['close'].shift())
    
    true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = true_range.rolling(window=atr_period).mean()
    
    # Use ATR in main calculation
    df_copy['result'] = df_copy['close'] / atr  # Example usage
    
    return df_copy[['result']]
```

### Complex Self-Contained Examples
For indicators requiring multiple sub-calculations:

```python
def complex_indicator(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    df_copy = df.copy()
    
    # Internal EMA calculation (don't import from trend module)
    def calculate_ema(series, span):
        return series.ewm(span=span, adjust=False).mean()
    
    # Internal SMA calculation
    def calculate_sma(series, window):
        return series.rolling(window=window).mean()
    
    # Internal Bollinger Bands calculation (don't import from volatility)
    sma = calculate_sma(df_copy['close'], period)
    std = df_copy['close'].rolling(window=period).std()
    bb_upper = sma + (2 * std)
    bb_lower = sma - (2 * std)
    
    # Main indicator logic using self-calculated components
    df_copy['complex_result'] = (df_copy['close'] - bb_lower) / (bb_upper - bb_lower)
    
    return df_copy[['complex_result']]
```

## Development Patterns

### Indicator Function Structure
```python
def indicator_name(df: pd.DataFrame, column: str = "close", period: int = 14) -> pd.DataFrame:
    """Brief description"""
    df_copy = df.copy()
    # Calculations here
    return df_copy[['result_column']]

# Full docstring with exact format
indicator_name.__doc__ = """
Name:
    Indicator Name

Description:
    Detailed description

More info:
    URL reference

Parameters:
    - df (pandas.DataFrame): Input DataFrame
    - column (str): Column to use
    - period (int): Period for calculation

Call with:
    df['result'] = bta.indicator_name(df)['result_column']

Returns:
    pd.DataFrame: DataFrame with result columns
"""

def test():
    """Test function using generic test_indicator"""
    try:
        from bamboo_ta.bamboo_ta import test_indicator
        test_indicator(indicator_name)
    except ImportError:
        print("Error: Could not import test_indicator")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    test()
```

### Usage Patterns
```python
import bamboo_ta as bta

# Single indicator
df['rsi'] = bta.relative_strength_index(df, 'close', 14)['rsi']

# Multi-column result
bb_result = bta.bollinger_bands(df, 'close', 20, 2)
df['bb_upper'] = bb_result['upper']
df['bb_middle'] = bb_result['middle'] 
df['bb_lower'] = bb_result['lower']
```

## Independence Validation
When developing indicators, verify self-containment by:

1. **Import Check**: Only pandas/numpy imports allowed at indicator level
2. **Function Check**: No calls to other bamboo_ta indicator functions
3. **Test Independence**: Each indicator file should run standalone with `python -m bamboo_ta.category.indicator_name`
4. **Dependency Analysis**: Use `grep -r "from bamboo_ta" bamboo_ta/category/` to ensure no internal imports

## Common Violations to Avoid

**❌ NEVER DO THIS**:
```python
# Importing from other bamboo_ta modules
from bamboo_ta.volatility import average_true_range
from bamboo_ta.trend import simple_moving_average

# Using shared utility functions
from bamboo_ta.utils import calculate_something

# Calling other indicators
def my_indicator(df):
    atr_result = average_true_range(df)  # VIOLATION!
```

**✅ ALWAYS DO THIS**:
```python
# Self-contained with internal calculations
def my_indicator(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    
    # Calculate everything needed internally
    # (ATR, SMA, EMA, etc.)
    
    return df_copy[['result_column']]
```

## Dependencies
- pandas >= 2.2.3
- numpy >= 1.26.4  
- ta, pandas_ta, scipy (for compatibility)
