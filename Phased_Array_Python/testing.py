import numpy as np
import database as db
import matplotlib as mpl

code = 1034112000


filepath = "../MicRECORD/"+ code +"/FIGS/" + code + "_Diagram"
sysInfo = db.getInformation(code)
diagram = mpl.figure()
#spread/mic# = scalar
mic_value = sysInfo.MIC_COUNT  # replace with actual value of #mic through database
total_spread = sysInfo.TOTALSPREAD  # replace with actual value of total spread through database
#scalar = sysInfo.scalar
v = sysInfo.TOTALSPREAD/ (sysInfo.Mic_COUNT - 1)
x = [0, i*v for i in range(mic_value)]
y_coordinates = np.zeros(sysInfo.MIC_COUNT, dtype=int)
mpl.ylim(-1, 15)
#diagram.plot(Target Sound)
diagram.plot(x, y_coordinates)
# Set y-axis limits
mpl.xlabel('Total Spread'+ total_spread)
mpl.ylabel('')
mpl.title('Diagram of Mics')
diagram.save(filepath)