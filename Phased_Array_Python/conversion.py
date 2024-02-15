import numpy as np
import pandas as pd
import sys, os, os.path
from scipy.io import wavfile

def convertWavCSV(file_path, FS):
    if file_path[-3:] != 'wav':
        print("Wrong File Type")
        sys.exit()

    samrate, data = wavfile.read('../MICRECORD/' + file_path)
    wavData = pd.DataFrame(data)

    if len(wavData.columns) == 2:
        print('Stereo File not Compatible, Mono Recording Only')
        sys.exit()

    if samrate != FS:
        print('Incorrect Sample Rate Applied')
        sys.exit()
    
    wavData.columns = ['M']
    convertedCSV = wavData['M'].to_numpy()

    return convertedCSV
    
