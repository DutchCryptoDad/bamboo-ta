# candles.py

```
Traceback (most recent call last):
  File "test.py", line 27, in <module>
    dynamic_exhaustion = bta.dynamic_exhaustion_bars(df)
  File "/home/dcd/bamboo-ta/bamboo_ta/candles.py", line 158, in dynamic_exhaustion_bars
    maj_qual, min_qual = Calculate_Exhaustion_Candles(df_copy, window, zscore_multi)
NameError: name 'Calculate_Exhaustion_Candles' is not defined
```

Some of these functions below are not defined...

```
    maj_qual, min_qual = calculate_exhaustion_candles(df_copy, window, zscore_multi)
    
    df_copy['maj_qual'] = maj_qual
    df_copy['min_qual'] = min_qual

    maj_len, min_len = calculate_exhaustion_lengths(df_copy)
    
    df_copy['maj_len'] = maj_len
    df_copy['min_len'] = min_len

    df_copy = populate_leledc_major_minor(df_copy, maj_qual, min_qual, maj_len, min_len)
```