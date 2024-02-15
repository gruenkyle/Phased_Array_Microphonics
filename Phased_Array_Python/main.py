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
Mic_Distance_Target = np.zeros(MIC_COUNT, dtype=float)
Mic_Distance_Target = dc.calcDistance(TOTAL_SPREAD, MIC_COUNT, SYS_OPP_DIST, SYS_ADJ_DIST)

minDis,minIndex = np.min(Mic_Distance_Target), np.argmin(Mic_Distance_Target)
maxDis, maxIndex = np.max(Mic_Distance_Target), np.argmax(Mic_Distance_Target)

# Calculate Mic Total Sample Values #
Mic_Sample_Value = np.zeros(MIC_COUNT, dtype=float)
Mic_Sample_Value = dc.calcSample(Mic_Distance_Target, FS, maxIndex)

# Process the Sound from Wav to CSV and store in numpy array

micSignalCells = [np.array([]) for _ in range(MIC_COUNT)]

for mic in FORLOOPARR: 
    #file_path = "../MICRECORD/" + code + "/INDIV/mic_" + mic + "_" + code + ".wav" 
    #micSignalCells[mic] = con.convertWavCSV(file_path)
    print("Mic Counted")

maxSignalArrLengths = np.zeros(MIC_COUNT, dtype=int)

for mic in FORLOOPARR:
    if (mic != maxIndex):
        micSignalCells[mic] = np.append(np.zeros(int(totalSampleDelay[mic])), micSignalCells[mic])
        maxSignalArrLengths[mic] = len(micSignalCells[mic])

maxSize = np.max(maxSignalArrLengths)

for mic in FORLOOPARR:
    micSignalCells[mic] = np.append(micSignalCells[mic], np.zeros(int(maxSize - maxSignalArrLengths[mic])))
    print(len(micSignalCells[mic]))

micSumSignal = np.zeros(int(maxSize))
for finalSummationMic in FORLOOPARR:
    micSumSignal = micSumSignal + micSignalCells[int(finalSummationMic)]

# Create Mic Signal Folder # 
# folderPath = "../MICRECORD/" + code + "/SUM/"
    
# con.folderCreate(folderPath)
# con.convertCSVWav(filePath, micSumSignal)
    
