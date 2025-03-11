# -*- coding: utf-8 -*-
# pascals_triangle.py

import pandas as pd
import numpy as np
from functools import reduce
from operator import mul


def pascals_triangle(
    n: int = 4,
    weighted: bool = False,
    inverse: bool = False
) -> pd.DataFrame:
    """Pascal's Triangle Indicator"""
    # Input validation
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    
    # Function to calculate combinations (n choose r)
    def combination(n, r):
        # Ensure n and r are non-negative
        n = int(abs(n))
        r = int(abs(r))
        
        # Special case
        if r > n:
            return 0
            
        # Optimization: compute nCr = nC(n-r) if r > n/2
        r = min(r, n - r)
        
        if r == 0:
            return 1
            
        # Calculate nCr using multiplicative formula
        numerator = reduce(mul, range(n, n - r, -1), 1)
        denominator = reduce(mul, range(1, r + 1), 1)
        return numerator // denominator
    
    # Calculate Pascal's Triangle values for row n
    triangle = np.array([combination(n=n, r=i) for i in range(0, n + 1)])
    
    # Calculate sum for weighted version
    triangle_sum = np.sum(triangle)
    
    # Calculate weights
    triangle_weights = triangle / triangle_sum
    
    # Calculate inverse weights
    inverse_weights = 1 - triangle_weights
    
    # Prepare result
    result = pd.DataFrame()
    
    # Return appropriate array based on parameters
    if weighted and inverse:
        result["pascal_inverse_weights"] = inverse_weights
    elif weighted:
        result["pascal_weights"] = triangle_weights
    else:
        result["pascal"] = triangle
    
    return result


pascals_triangle.__doc__ = """
Name:
    Pascal's Triangle

Description:
    Generates a row of Pascal's Triangle, optionally weighted or inverse weighted.
    
    Pascal's Triangle is a triangular array of binomial coefficients, where each number
    is the sum of the two numbers directly above it. It has numerous applications in
    mathematics, particularly in combinatorics, probability, and algebra.
    
    This implementation can generate:
    1. The raw values of a specific row of Pascal's Triangle
    2. A weighted version where each value is divided by the sum of all values in the row
    3. An inverse weighted version (1 - weighted value)

More info:
    https://en.wikipedia.org/wiki/Pascal%27s_triangle

Parameters:
    - n (int): The row of Pascal's Triangle to generate (0-indexed). Default is 4.
    - weighted (bool): If True, returns each value divided by the sum of all values. Default is False.
    - inverse (bool): If True and weighted is True, returns 1 minus the weighted values. Default is False.

Call with:
    # Get raw Pascal's Triangle row
    df_pascal = bta.pascals_triangle(n=4)
    
    # Get weighted values
    df_weighted = bta.pascals_triangle(n=4, weighted=True)
    
    # Get inverse weighted values
    df_inverse = bta.pascals_triangle(n=4, weighted=True, inverse=True)

Returns:
    pd.DataFrame: DataFrame with a single column containing the requested values:
    - 'pascal': Raw Pascal's Triangle values
    - 'pascal_weights': Weighted values if weighted=True
    - 'pascal_inverse_weights': Inverse weighted values if weighted=True and inverse=True
"""


def test():
    """
    Test function for the pascals_triangle indicator.
    
    This function tests the pascals_triangle function with various parameters
    and displays the results to the console.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create test cases
        print("Pascal's Triangle Row 4:")
        print(pascals_triangle(n=4))
        
        print("\nPascal's Triangle Row 4 (weighted):")
        print(pascals_triangle(n=4, weighted=True))
        
        print("\nPascal's Triangle Row 4 (inverse weighted):")
        print(pascals_triangle(n=4, weighted=True, inverse=True))
        
        print("\nPascal's Triangle Row 8:")
        print(pascals_triangle(n=8))
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 