import numpy as np
import matplotlib.pyplot as mpl

def multiFigure(mic_signal_cells, code):
    filePath = "../MICRECORD/" + str(code) + "/FIGS/multi_" + str(code) + ".png"
    FORLOOPARR = np.arange(len(mic_signal_cells))

    mpl.figure()
    for mic in FORLOOPARR:
        mpl.subplot(len(mic_signal_cells[mic]), mic_signal_cells[mic], mic)

    mpl.tight_layout()
    mpl.savefig(filePath)
    mpl.show()

