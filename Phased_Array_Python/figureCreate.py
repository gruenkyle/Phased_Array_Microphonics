import numpy as np
import matplotlib.pyplot as mpl

def multiFigure(mic_signal_cells, code):
    filePath = "../MICRECORD/" + str(code) + "/FIGS/multi_" + str(code) + ".png"
    FORLOOPARR = np.arange(len(mic_signal_cells))

    mpl.figure()
    mpl.figure(figsize=(10, 6))

    for mic in FORLOOPARR:
        mpl.subplot(len(mic_signal_cells), 1, mic + 1)
        mpl.plot(mic_signal_cells[mic])   

    mpl.tight_layout()
    mpl.savefig(filePath)

def summationFigure(micSummationArray, code):
    filePath = "../MICRECORD/" + str(code) + "/FIGS/FinalSummation_" + str(code) + ".png"
    mpl.figure()
    mpl.figure(figsize=(10, 6))
    mpl.plot(micSummationArray)

    mpl.tight_layout()
    mpl.savefig(filePath)

