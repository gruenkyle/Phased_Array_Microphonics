import pandas as pd
import numpy as np


def noise_filter(closest_array, sum_array, window_size=40):

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

guh = noise_filter(array1, array2)
print("size of noise filter 2: ", len(guh))
