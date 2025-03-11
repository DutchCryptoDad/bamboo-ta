# -*- coding: utf-8 -*-
# symmetric_triangle.py

import pandas as pd
import numpy as np
import math


def symmetric_triangle(
    n: int = 4,
    weighted: bool = False
) -> pd.DataFrame:
    """Symmetric Triangle Indicator"""
    # Input validation
    if not isinstance(n, int) or n < 2:
        raise ValueError("n must be an integer greater than or equal to 2")
    
    # Ensure n is positive    
    n = int(abs(n))
    
    # Calculate the symmetric triangle
    triangle = None
    if n == 2:
        triangle = [1, 1]
    elif n > 2:
        if n % 2 == 0:  # Even n
            front = [i + 1 for i in range(0, math.floor(n / 2))]
            triangle = front + front[::-1]
        else:  # Odd n
            front = [i + 1 for i in range(0, math.floor(0.5 * (n + 1)))]
            triangle = front.copy()
            front.pop()
            triangle += front[::-1]
    
    # Convert to numpy array for consistency
    triangle = np.array(triangle)
    
    # Prepare result
    result = pd.DataFrame()
    
    # Return weighted version if requested
    if weighted:
        triangle_sum = np.sum(triangle)
        triangle_weights = triangle / triangle_sum
        result["symtri_weights"] = triangle_weights
    else:
        result["symtri"] = triangle
    
    return result


symmetric_triangle.__doc__ = """
Name:
    Symmetric Triangle

Description:
    Generates a symmetric triangular array of values, optionally weighted.
    
    The Symmetric Triangle is an array where values increase from both ends towards
    the middle. For even values of n, the middle two values are equal. For odd values
    of n, there is a single peak in the middle.
    
    Examples:
    - n=4: [1, 2, 2, 1]
    - n=5: [1, 2, 3, 2, 1]
    
    These triangular arrays are frequently used as weighting schemes in technical
    indicators like weighted moving averages, where you want to place more emphasis
    on the middle values and less on the ends.

More info:
    This is a common structure used in various technical analysis weighting schemes.

Parameters:
    - n (int): The size of the array to generate. Must be greater than or equal to 2. Default is 4.
    - weighted (bool): If True, returns each value divided by the sum of all values,
      making the weights sum to 1. Default is False.

Call with:
    # Get raw symmetric triangle
    df_tri = bta.symmetric_triangle(n=4)
    
    # Get weighted values
    df_weighted = bta.symmetric_triangle(n=4, weighted=True)

Returns:
    pd.DataFrame: DataFrame with a single column containing the requested values:
    - 'symtri': Raw symmetric triangle values
    - 'symtri_weights': Weighted values if weighted=True
"""


def test():
    """
    Test function for the symmetric_triangle indicator.
    
    This function tests the symmetric_triangle function with various parameters
    and displays the results to the console.
    
    Returns:
        None: Displays the results to the console
    """
    try:
        # Create test cases
        print("Symmetric Triangle n=4:")
        print(symmetric_triangle(n=4))
        
        print("\nSymmetric Triangle n=4 (weighted):")
        print(symmetric_triangle(n=4, weighted=True))
        
        print("\nSymmetric Triangle n=5:")
        print(symmetric_triangle(n=5))
        
        print("\nSymmetric Triangle n=5 (weighted):")
        print(symmetric_triangle(n=5, weighted=True))
        
    except Exception as e:
        print(f"Error during testing: {e}")

# Execute the test if this file is run directly
if __name__ == "__main__":
    test() 