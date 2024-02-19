# Import External Scripts # 
import conversion as con
import distanceCalc as dc
import wavCollection as wc
import figureCreate as fc

# Import Python Libraries #
import numpy as np

# FIELD VARIABLES # 
FS = 44100 # AVG number of samples obtained per second (Sample Rate)
TOTAL_SPREAD = 13.716 # Total Spread of Phased Array from Mic 1 -> Mic N
MIC_COUNT = 3 # Total Number of Microphones 
SCALAR = TOTAL_SPREAD / (MIC_COUNT - 1) # Scalar Multiple For Equidistant Microphones

code = 1302

SYS_ADJ_DIST = 7.625 # Adjacent Distance from Left Most Microphone
SYS_OPP_DIST = 6.858 #Opposite Distance from Left Most Microphone

FORLOOPARR = np.arange(MIC_COUNT) #Looping Array for Mics

# Calculate Mic Distances # 
Mic_Distance_Target = np.zeros(MIC_COUNT, dtype=float)
Mic_Distance_Target = dc.calcDistance(TOTAL_SPREAD, MIC_COUNT, SYS_OPP_DIST, SYS_ADJ_DIST)

print("Mic Distances to Target : " + str(Mic_Distance_Target) + "\n")

minDis, minIndex = np.min(Mic_Distance_Target), np.argmin(Mic_Distance_Target)
maxDis, maxIndex = np.max(Mic_Distance_Target), np.argmax(Mic_Distance_Target)

print("Max Distance / Mic : " + str(maxDis) + "/ " + str(maxIndex) + "\n")

# Calculate Mic Total Sample Values #
Mic_Sample_Delay = np.zeros(MIC_COUNT, dtype=float)
Mic_Sample_Delay = dc.calcSample(Mic_Distance_Target, FS, maxIndex)

print("Mic Sample Delays : " + str(Mic_Sample_Delay) + "\n")

# Process the Sound from Wav to CSV and store in numpy array

mic_Signal_Cells = [np.array([]) for _ in range(MIC_COUNT)]

for mic in FORLOOPARR: 
    file_path = "../MICRECORD/" + str(code) + "/INDIV/Mic" + str(mic + 1) + "_" + str(code) + ".wav" 
    mic_Signal_Cells[mic] = con.convertWavCSV(file_path, FS)
    print("Working")

fc.multiFigure(mic_Signal_Cells, code)

maxSignalArrLengths = np.zeros(MIC_COUNT, dtype=int)

for mic in FORLOOPARR:
    if (mic != maxIndex):
        print(str(mic + 1) + "len preappend - " + str(len(mic_Signal_Cells[mic])))

        mic_Signal_Cells[mic] = np.append(np.zeros(int(Mic_Sample_Delay[mic])), mic_Signal_Cells[mic])
        
        maxSignalArrLengths[mic] = len(mic_Signal_Cells[mic])

    print(str(mic + 1) + "len postappend - " + str(len(mic_Signal_Cells[mic])) + "\n")

maxSize = np.max(maxSignalArrLengths)

print ("Maximum Size : " + str(maxSize) + "\n\n")

for mic in FORLOOPARR:
    print("Pre-zero : " + str(len(mic_Signal_Cells[mic])))
    mic_Signal_Cells[mic] = np.append(mic_Signal_Cells[mic], np.zeros(int(maxSize - len(mic_Signal_Cells[mic]))))
    print("Post-zero : " + str(len(mic_Signal_Cells[mic])))

micSumSignal = np.zeros(int(maxSize))
for finalSummationMic in FORLOOPARR:
    micSumSignal = micSumSignal + mic_Signal_Cells[int(finalSummationMic)]

fc.summationFigure(micSumSignal, code)

# Create Mic Signal Folder # 
# folderPath = "../MICRECORD/" + code + "/SUM_" + code + "/"
folderPath = "../MICRECORD/" + str(code) + "/SUM/FinalAudio_" + str(code) + ".wav"
con.convertCSVWav(folderPath, micSumSignal, FS)
