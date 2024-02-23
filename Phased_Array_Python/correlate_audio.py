import pandas as pd
import numpy as np

def noise_filter(closestArray, sumArray):
    

    # Set window size
    window_size = 40

    # Create Pandas DataFrame for the arrays
    df = pd.DataFrame({'closest': closestArray, 'sum': sumArray})

    # Initialize an empty list to store correlations
    correlations = []

    # Iterate over the arrays with a sliding window using Pandas rolling window function
    for window in df.rolling(window_size):
        # Skip the first (window_size - 1) correlations since they are not calculated due to rolling window
        if len(window) == window_size:
            correlations.append(window['closest'].corr(window['sum']))

    # Convert the list of correlations to a NumPy array
    correlations_array = np.array(correlations)

    # Print the correlations array
    print("Correlations array:", correlations_array)

# Assuming you have two arrays array1 and array2 with 44100 entries each
# Generate random arrays for demonstration purposes
array_size = 44100
array1 = np.random.rand(array_size)
array2 = np.random.rand(array_size)

noise_filter(array1, array2)