import pandas as pd
import numpy as np

def noise_filter(closestArray, sumArray):
    df = pd.DataFrame({'closest': closestArray,
          'summation': sumArray})
    corr = df['closest'].corr(df['summation'])
    return corr

array_size = 44100 * 100
array1 = np.random.rand(array_size)
array2 = np.random.rand(array_size)

print(noise_filter(array1, array2))
