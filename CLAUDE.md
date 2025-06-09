# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bamboo-TA is a Python library for technical analysis indicators designed for algorithmic trading. It provides a comprehensive collection of TA indicators organized into modular categories: candles, cycles, momentum, performance, statistics, trend, utility, volatility, and volume. The library is complementary to pandas-ta, ta-lib, and qtpylib.

## Architecture

### Core Structure
- **Main module**: `bamboo_ta/bamboo_ta.py` - Contains generic `test_indicator()` function and imports all indicators
- **Category modules**: Each category (momentum, trend, etc.) has its own directory with `__init__.py` that exports indicators
- **Individual indicators**: Each indicator is self-contained in its own file with no external dependencies
- **Data format**: Expects pandas DataFrame with columns: 'date', 'open', 'high', 'low', 'close', 'volume'

### Indicator Requirements
Each indicator file must contain:
1. Self-contained function with no external dependencies (if an indicator needs ATR, it calculates it internally)
2. Detailed docstring following exact format with Name, Description, More info, Parameters, Call with, Returns sections
3. `test()` function that uses `test_indicator()` from bamboo_ta.py
4. Main block that calls `test()` if run directly

### Code Standards
- Follow PEP8 (snake_case for functions/variables) 
- Include detailed comments explaining calculations
- Functions return DataFrames with specific column names
- Error handling for missing columns/invalid parameters
- No deletion of comments unless no longer needed

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

## Dependencies
- pandas >= 2.2.3
- numpy >= 1.26.4  
- ta, pandas_ta, scipy (for compatibility)