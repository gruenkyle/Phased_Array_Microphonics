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
Mic_Sample_Delay = np.zeros(MIC_COUNT, dtype=float)
Mic_Sample_Delay = dc.calcSample(Mic_Distance_Target, FS, maxIndex)

# Process the Sound from Wav to CSV and store in numpy array

mic_Signal_Cells = [np.array([]) for _ in range(MIC_COUNT)]

code = 0424

for mic in FORLOOPARR: 
    file_path = code + "/INDIV/mic_" + mic + "_" + code + ".wav" 
    mic_Signal_Cells[mic] = con.convertWavCSV(file_path, FS)
    print("Working")

maxSignalArrLengths = np.zeros(MIC_COUNT, dtype=int)

for mic in FORLOOPARR:
    if (mic != maxIndex):
        mic_Signal_Cells[mic] = np.append(np.zeros(int(Mic_Sample_Delay[mic])), mic_Signal_Cells[mic])
        maxSignalArrLengths[mic] = len(mic_Signal_Cells[mic])

maxSize = np.max(maxSignalArrLengths)

for mic in FORLOOPARR:
    mic_Signal_Cells[mic] = np.append(mic_Signal_Cells[mic], np.zeros(int(maxSize - maxSignalArrLengths[mic])))

micSumSignal = np.zeros(int(maxSize))
for finalSummationMic in FORLOOPARR:
    micSumSignal = micSumSignal + mic_Signal_Cells[int(finalSummationMic)]

# Create Mic Signal Folder # 
# folderPath = "../MICRECORD/" + code + "/SUM_" + code + "/"
    
# con.folderCreate(folderPath)
# con.convertCSVWav(filePath, micSumSignal)
    
