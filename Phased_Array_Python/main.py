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

# Import External Scripts # 
import conversion as con
import distanceCalc as dc
import figureCreate as fc
import database as db

# Import Python Libraries #
import numpy as np

# FIELD VARIABLES # 
code = 10321802 # Unique Code Identification #

recordingInformation = db.getInformation(code) # Gather information about recording code 

FS = recordingInformation['SAMRATE'].iloc[0] # AVG number of samples obtained per second (Sample Rate)
TOTAL_SPREAD = recordingInformation['TOTALSPREAD'].iloc[0] # Total Spread of Phased Array from Mic 1 -> Mic N
MIC_COUNT = recordingInformation['MIC_COUNT'].iloc[0] # Total Number of Microphones 

SCALAR = TOTAL_SPREAD / (MIC_COUNT - 1) # Scalar Multiple For Equidistant Microphones

SYS_ADJ_DIST = recordingInformation['SAD'].iloc[0] # Adjacent Distance to Target from Left Most Microphone
SYS_OPP_DIST = recordingInformation['SOD'].iloc[0] # Opposite Distance to Target from Left Most Microphone

FORLOOPARR = np.arange(MIC_COUNT) # Iteration Array For Number of Microphones

# Calculate Mic Distances to Target Values # 
Mic_Distance_Target = np.zeros(MIC_COUNT, dtype=float)
Mic_Distance_Target = dc.calcDistance(TOTAL_SPREAD, MIC_COUNT, SYS_OPP_DIST, SYS_ADJ_DIST)
print("Mic Distances to Target : " + str(Mic_Distance_Target) + "\n")

# Find ArgMin/Max and Min/Max of Distance Values # 
minDis, minIndex = np.min(Mic_Distance_Target), np.argmin(Mic_Distance_Target)
maxDis, maxIndex = np.max(Mic_Distance_Target), np.argmax(Mic_Distance_Target)
print("Max Distance / Mic : " + str(maxDis) + "/ " + str(maxIndex) + "\n")

# Calculate How Many Samples Need to be Appended to Each Microphone Array #
Mic_Sample_Delay = np.zeros(MIC_COUNT, dtype=float)
Mic_Sample_Delay = dc.calcSample(Mic_Distance_Target, FS, maxIndex)
print("Mic Sample Delays : " + str(Mic_Sample_Delay) + "\n")

# Create NumPy Array of Arrays to store microphone data #
mic_Signal_Cells = [np.array([]) for _ in range(MIC_COUNT)]

# Convert Wav Files into CSV Data and Store in mic_Signal_Cells #
for mic in FORLOOPARR: 
    file_path = "../MICRECORD/" + str(code) + "/INDIV/Mic" + str(mic + 1) + "_" + str(code) + ".wav" 
    mic_Signal_Cells[mic] = con.convertWavCSV(file_path, FS)

# Generate Figure Displaying all Microphone Waves on MatPlot #
fc.multiFigure(mic_Signal_Cells, code)

# Create Storage Array for Maximum lengths of each audio file #
maxSignalArrLengths = np.zeros(MIC_COUNT, dtype=int)

# Loop over each microphone and append samples to start of array for system phasing #
for mic in FORLOOPARR:
    if (mic != maxIndex):

        mic_Signal_Cells[mic] = np.append(np.zeros(int(Mic_Sample_Delay[mic])), mic_Signal_Cells[mic])
        
        maxSignalArrLengths[mic] = len(mic_Signal_Cells[mic])

maxSize = np.max(maxSignalArrLengths)

# Reallign all arrays to have equivalent sizes #
for mic in FORLOOPARR:
    #print("Pre-zero : " + str(len(mic_Signal_Cells[mic])) + " for Mic #" + mic)
    mic_Signal_Cells[mic] = np.append(mic_Signal_Cells[mic], np.zeros(int(maxSize - len(mic_Signal_Cells[mic]))))
    #print("Post-zero : " + str(len(mic_Signal_Cells[mic])) + " for Mic #" + mic)

# Sum all audio signals into one large array #
micSumSignal = np.zeros(int(maxSize))
for finalSummationMic in FORLOOPARR:
    micSumSignal = micSumSignal + mic_Signal_Cells[int(finalSummationMic)]

# Create Summation Figure and Overlapping Figure #
fc.summationFigure(micSumSignal, code)
fc.overlappingFigure(micSumSignal, mic_Signal_Cells[minIndex], code)

# Create Mic Signal Folder and Store Converted Summation CSV to Wav # 
folderPath = "../MICRECORD/" + str(code) + "/SUM/FinalAudio_" + str(code) + ".wav"
con.convertCSVWav(folderPath, micSumSignal, FS)
