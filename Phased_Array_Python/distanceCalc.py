import numpy as np

SPEED_SOUND = 343

def calcDistance(TS, MC, SOD, SAD):
    FORLOOPARR = np.arange(MC, dtype=int)

    MIC_DISTANCES_TO_START = np.zeros(MC, dtype=float)
    MIC_DISTANCES_TO_TARGET = np.zeros(MC, dtype=float)

    SCALAR = TS / (MC - 1)

    for index in FORLOOPARR:
        MIC_DISTANCES_TO_START[index] = ((SCALAR * index))

    MIC_DISTANCES_TO_START[0] = 0

    for index in FORLOOPARR:
        if(MIC_DISTANCES_TO_START[index] > SOD):
            MIC_DISTANCES_TO_TARGET[index] = SOD - MIC_DISTANCES_TO_START[index]
        elif (MIC_DISTANCES_TO_START[index] < SOD):
            MIC_DISTANCES_TO_TARGET[index] = abs(SOD - MIC_DISTANCES_TO_START[index])

    MIC_DISTANCES_TO_TARGET = abs(MIC_DISTANCES_TO_TARGET)

    for index in FORLOOPARR:
        MIC_DISTANCES_TO_TARGET[index] = ((MIC_DISTANCES_TO_TARGET[index])**2 + SAD**2)**(1/2)

    return MIC_DISTANCES_TO_TARGET


def calcSample(MD, FS, MI):
    MC = len(MD)
    FORLOOPARR = np.arange(MC, dtype=int)

    delayTarget = np.zeros(MC, dtype=float)
    sampleDelayTarget = np.zeros(MC, dtype=float)
    totalDelayTarget = np.zeros(MC, dtype=float)

    for mic in FORLOOPARR:
        delayTarget[mic] = (MD[mic] / SPEED_SOUND)
        sampleDelayTarget[mic] = np.round(delayTarget[mic] * FS)
        totalDelayTarget[mic] = np.round(sampleDelayTarget[MI] - sampleDelayTarget[mic])

    totalDelayTarget = abs(totalDelayTarget)
    return totalDelayTarget
