# Bamboo TA Indicators Module

## Volume

Provides volume-based indicators.

### Indicators

- **OBV_Oscillator**: On Balance Volume Oscillator.
- **Usage**:
    ```python
    obv_osc = OBV_Oscillator(df, n1=10, n2=21)
    df['OBV_Oscillator'] = obv_osc['OBV_Oscillator']
    ```