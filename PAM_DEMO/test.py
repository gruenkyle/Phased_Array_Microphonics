#######################################
#
#      Phased Array Microphonics
# Main Phased Array Algorithm Script 
# Combines all other Scripts to output summation 
# file for Phased Alteration and Graphs
#
#   Authors : Kyle Gruen, Ibrahim Shabini
#           Date : 02/27/2024
#
#######################################

# # Import External Scripts # 
# import conversion as con
# import distanceCalc as dc
import figureCreate as fc
# import database as db
# import wavCollection as wc

# Import Python Libraries #
import numpy as np
import pandas as pd
import sys

def initializeDir():
    print("testing")

def main():
    
    # wc.recordAudio()
    
    data = {
        'CODE': [str(sys.argv[1])],
        'SAD': [float(sys.argv[2])], 
        'SOD': [float(sys.argv[3])],
        'SAMRATE': [int(sys.argv[4])],
        'MIC_COUNT': [int(sys.argv[5])], 
        'TOTALSPREAD': [float(sys.argv[6])]
    }
    recordingInformation = pd.DataFrame(data)
    
        
    FS = recordingInformation['SAMRATE'].iloc[0] # AVG number of samples obtained per second (Sample Rate)
    TOTAL_SPREAD = recordingInformation['TOTALSPREAD'].iloc[0] # Total Spread of Phased Array from Mic 1 -> Mic N
    MIC_COUNT = recordingInformation['MIC_COUNT'].iloc[0] # Total Number of Microphones 
    
    SCALAR = TOTAL_SPREAD / (MIC_COUNT - 1) # Scalar Multiple For Equidistant Microphones
    
    SYS_ADJ_DIST = recordingInformation['SAD'].iloc[0] # Adjacent Distance to Target from Left Most Microphone
    SYS_OPP_DIST = recordingInformation['SOD'].iloc[0] # Opposite Distance to Target from Left Most Microphone

    FORLOOPARR = np.arange(MIC_COUNT) # Iteration Array For Number of Microphones

    print([FS, TOTAL_SPREAD, MIC_COUNT, SCALAR, SYS_ADJ_DIST, SYS_OPP_DIST, FORLOOPARR])
    
if __name__=='__main__':
    main()