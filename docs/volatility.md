# Bamboo TA Indicators Module

## Volatility

Volatility indicators.

### Indicators

- **BollingerBands**: Calculates Bollinger Bands (upper, middle, lower bands).
- **Usage**: 
    ```python
    bb_result = BollingerBands(df, "close", 21, 2, 0)
    df['bb_upper'] = bb_result['BB_upper']
    df['bb_middle'] = bb_result['BB_middle']
    df['bb_lower'] = bb_result['BB_lower']
    ```
- **TR**: True Range (TR) calculation.
- **Usage**: 
    ```python
    tr = TR(df)
    ```
