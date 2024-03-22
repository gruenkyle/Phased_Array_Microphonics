import pandas as pd
import numpy as np

def noise_filter(closestArray, sumArray, window_size=100):
    
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
    return correlations_array

def noise_filter2(closest_array, sum_array, window_size=40):

    corr = []

    for i in range(closest_array.size // window_size):
        closest_window = closest_array[i:i+window_size]
        sum_window = sum_array[i:i+window_size]
        corr.append(np.corrcoef(closest_window, sum_window, rowvar=False))



   # num_elements = len(closest_array) - window_size + 1
    
    '''# Create a 2D array with rolling windows for both arrays
    rolling_closest = np.lib.stride_tricks.sliding_window_view(closest_array, window_size)
    rolling_sum = np.lib.stride_tricks.sliding_window_view(sum_array, window_size)
    
    # Compute correlations for each window
    correlations = np.corrcoef(rolling_closest, rolling_sum, rowvar=False)'''
    
    # Extract the correlation coefficients between 'closest' and 'sum'

    # print(correlations)
    
    return corr



# Assuming you have two arrays array1 and array2 with 44100 entries each
# Generate random arrays for demonstration purposes
array_size = 44100
array1 = np.random.rand(1000)  # Example data
array2 = np.random.rand(1000)  # Example data



#blah = noise_filter(array1, array2)
#print("size of noise filter 1: ", blah.size)

guh = noise_filter2(array1, array2)
print("size of noise filter 2: ", len(guh))
