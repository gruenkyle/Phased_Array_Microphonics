#######################################
#
#      Phased Array Microphonics
# Conversion between Wav / CSV Script
#
#       Author : Kyle Gruen
#       Date : 02/27/2024
#
#######################################

# Imports #
import numpy as np
import pandas as pd
import sys, os, os.path
from scipy.io import wavfile


##############
# Conversion from Mono Wav to CSV array
#
# file_path(str) : File Path to wav file 
# FS : Sample rate initialized in main method
#
# return -> numpy array of values from wav
##############
def convertWavCSV(file_path, FS):
    
    # ERROR CHECK : File is not Wav File #
    if file_path[-3:] != 'wav':
        print(file_path + " <- Path does not lead to Wav file")
        sys.exit()

    # Store Sample Rate and Data into Pandas DataFrame #
    samrate, data = wavfile.read(file_path)
    wavData = pd.DataFrame(data)

    # ERROR CHECK : WavData must be Mono Recording not Stereo #
    if len(wavData.columns) == 2:
        print('Stereo File not Compatible, Mono Recording Only')
        sys.exit()

    # ERROR CHECK : Passed Sample Rate and Wav Sample rate do not match # 
    if samrate != FS:
        print('Sample Rates Differ : Passed = ' + FS + ' | File Rate = ' + samrate)
        sys.exit()
    
    # Convert from Pandas Array to Numpy Array, then return array #
    wavData.columns = ['M']
    convertedCSV = wavData['M'].to_numpy()

    return convertedCSV

##############
# Conversion from Numpy Array to Wav File
#
# file_path(str) : File Path to output new wav file 
# micData(numpy array) : array to be converted to wav
# FS : Sample rate initialized in main method
#
# return -> numpy array of values from wav
############## 
def convertCSVWav(file_path, micData, FS):
    
    # Convert file to Pandas Data frame to wavfile.write() method 
    df = pd.DataFrame(micData)
    wavfile.write(file_path, FS, df.astype(np.int32).values)

    