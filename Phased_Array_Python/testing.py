import numpy as np
import database as db
import matplotlib.pyplot as mpl

code = 10321801


filepath = "../MicRECORD/"+ str(code) +"/FIGS/" + str(code) + "_Diagram.png"
sysInfo = db.getInformation(code)
mpl.figure()
#spread/mic# = scalar
mic_value = sysInfo['MIC_COUNT'].iloc[0]  # replace with actual value of #mic through database
total_spread = sysInfo['TOTALSPREAD'].iloc[0]  # replace with actual value of total spread through database
#scalar = sysInfo.scalar
v = total_spread/ (mic_value - 1)
x = [i*v for i in range(mic_value)]
y_coordinates = np.zeros(mic_value, dtype=int)
mpl.ylim(-1, 15)
#diagram.plot(Target Sound)
mpl.scatter(x, y_coordinates)
mpl.scatter(sysInfo['SOD'], sysInfo['SAD'])
# Set y-axis limits
mpl.xlabel('Total Spread'+ str(total_spread))
mpl.ylabel('')
mpl.title('Diagram of Mics')
mpl.savefig(filepath)