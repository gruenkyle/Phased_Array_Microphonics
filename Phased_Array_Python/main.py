# Import External Scripts # 
import conversion as con
import distanceCalc as dc
import wavCollection as wc

# Import Python Libraries #
import numpy as np

# FIELD VARIABLES # 
FS = 44100 # AVG number of samples obtained per second (Sample Rate)
TOTAL_SPREAD = 10.0 # Total Spread of Phased Array from Mic 1 -> Mic N
MIC_COUNT = 4 # Total Number of Microphones 
SCALAR = TOTAL_SPREAD / (MIC_COUNT - 1) # Scalar Multiple For Equidistant Microphones

SYS_ADJ_DIST = 5 # Adjacent Distance from Left Most Microphone
SYS_OPP_DIST = 7.5 #Opposite Distance from Left Most Microphone

FORLOOPARR = np.arange(MIC_COUNT) #Looping Array for Mics

# Calculate Mic Distances # 
Mic_Distance_Start = np.zeros(MIC_COUNT, dtype=float)

##
#
# for mic in FORLOOPARR:
#   mic[mic]
#
#
#
#