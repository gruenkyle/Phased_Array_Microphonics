#######################################
#
#      Phased Array Microphonics
# Microphone Distance Calculations Script
#       With Sample Rate Calculations
#
#       Author : Kyle Gruen
#       Date : 02/27/2024
#
#######################################

# Imports #
import numpy as np

# Field Variables #
SPEED_SOUND = 343

##############
# Calculate Distances to target sound of every microphone in Phased Array System
# The total distances are stored in meters
#
# TOTAL_SPREAD(int) = Total spread of array system
# MIC_COUNT(int) = Number of Microphones in Array 
# SOD(float) = Distance on Opposite Side to Target in relation to left most microphone (Mic_0)
# SAD(float) = Distance on Adjacent Side to Target in relation to left most microphone (Mic_0)
#
# return -> numpy array of hypotenous distances to target 
##############
def calcDistance(TOTAL_SPREAD, MIC_COUNT, SOD, SAD):

    # Create Arrays for Storage / Iteration #
    FORLOOPARR = np.arange(MIC_COUNT, dtype=int)
    MIC_DISTANCES_TO_START = np.zeros(MIC_COUNT, dtype=float)
    MIC_DISTANCES_TO_TARGET = np.zeros(MIC_COUNT, dtype=float)

    # Calculate equidistant scalar multiple for distances between microphones #
    SCALAR = TOTAL_SPREAD / (MIC_COUNT - 1)
    for index in FORLOOPARR:
        MIC_DISTANCES_TO_START[index] = ((SCALAR * index))
    MIC_DISTANCES_TO_START[0] = 0

    # Calculate and store opposite distances of microphone to target sound # 
    for index in FORLOOPARR:
        if(MIC_DISTANCES_TO_START[index] > SOD):
            MIC_DISTANCES_TO_TARGET[index] = SOD - MIC_DISTANCES_TO_START[index]
        elif (MIC_DISTANCES_TO_START[index] < SOD):
            MIC_DISTANCES_TO_TARGET[index] = abs(SOD - MIC_DISTANCES_TO_START[index])
    MIC_DISTANCES_TO_TARGET = abs(MIC_DISTANCES_TO_TARGET)

    # Find hypotenous distances of each microphone in relation to target sound #
    for index in FORLOOPARR:
        MIC_DISTANCES_TO_TARGET[index] = ((MIC_DISTANCES_TO_TARGET[index])**2 + SAD**2)**(1/2)

    # Return numpy array with all hypotenous distances to target sound in meters #
    return MIC_DISTANCES_TO_TARGET

##############
# Calculate the Sample Rate necessary to Append Delay on CSV File 
# 
# Distances_To_Target(numpy array) = Numpy Array of Distances to Target Sound
# FS(int) = Sample Rate Data is Recorded At
# MAX_INDEX(int) = ArgMax of Distance Array for Furthest Microphone to Target
#
# return -> numpy array of sample rates necessary for delay append
##############
def calcSample(Distances_To_Target, FS, MAX_INDEX):
    # Create Arrays for Storage and Iteration #
    MIC_COUNT = len(Distances_To_Target)
    FORLOOPARR = np.arange(MIC_COUNT, dtype=int)
    delayTarget = np.zeros(MIC_COUNT, dtype=float)
    sampleDelayTarget = np.zeros(MIC_COUNT, dtype=float)
    totalDelayTarget = np.zeros(MIC_COUNT, dtype=float)

    # Calculate how many samples each microphone will append to allign with furthest #
    for mic in FORLOOPARR:
        delayTarget[mic] = (Distances_To_Target[mic] / SPEED_SOUND)
        sampleDelayTarget[mic] = np.round(delayTarget[mic] * FS)
        totalDelayTarget[mic] = np.round(sampleDelayTarget[MAX_INDEX] - sampleDelayTarget[mic])

    # Return Total Delay Sample Values for All Microphones in Numpy Array #
    totalDelayTarget = abs(totalDelayTarget)
    return totalDelayTarget
