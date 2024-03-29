#######################################
#
#      Phased Array Microphonics
# Figure Creation Script for Microphone 
# inputs as well as extra summation graphs 
#       or system setup diagrams
#
#       Author : Kyle Gruen Yumna Rizvi
#       Date : 02/27/2024
#
#######################################

# Imports # 
import numpy as np
import matplotlib.pyplot as mpl
import random
import database as db


##############
# Creates and saves matplot figure of all audio channel waves
#
# mic_signal_cells(numpy array) = data values of each microphone input
# code(int) = numerical code for current recording / storage
#
# file_output <- matplot figure 
##############
def multiFigure(mic_signal_cells, code):
    # Create storage filepath to store new figure #
    filePath = "../MICRECORD/" + str(code) + "/FIGS/multi_" + str(code) + ".png"
    FORLOOPARR = np.arange(len(mic_signal_cells))

    # Create Figure Object #
    mpl.figure()
    mpl.figure(figsize=(10, 6))
 
    # Plot each microphone data on subplot #
    for mic in FORLOOPARR:
        mpl.subplot(len(mic_signal_cells), 1, mic + 1)
        mpl.plot(mic_signal_cells[mic])   

    # Save figure to filepath above #
    mpl.tight_layout()
    mpl.savefig(filePath)

##############
# Creates and saves summation figure showing wave analysis on summation wave
#
# micSummationArray(numpy array) = data values of summed audio file
# code(int) = numerical code for current recording / storage
#
# file_output <- matplot figure 
##############
def summationFigure(micSummationArray, code):
    # Create File Path #
    filePath = "../MICRECORD/" + str(code) + "/FIGS/FinalSummation_" + str(code) + ".png"

    # Create Figure and Plot #
    mpl.figure()
    mpl.figure(figsize=(10, 6))
    mpl.plot(micSummationArray)

    # Save to file path above #
    mpl.tight_layout()
    mpl.savefig(filePath)

##############
# Creates and saves overlapping figure of closest array on top of summation 
#
# micSummationArray(numpy array) = data values of summed audio file
# closestArray(numpy array) = closest microphone data values
# code(int) = numerical code for current recording / storage
#
# file_output <- matplot figure 
##############
def overlappingFigure(micSummationArray, closestArray, code):
    # Create File Path for Storage #
    filePath = "../MICRECORD/" + str(code) + "/FIGS/Overlap_" + str(code) + ".png"

    # Create figure object and plot mic summation behind closest array #
    mpl.figure()
    mpl.figure(figsize=(10, 6))
    mpl.plot(micSummationArray, label="Summation", color="Blue")
    mpl.plot(closestArray, label="Closest", color="black")

    # Save figure to file path above #
    mpl.tight_layout()
    mpl.savefig(filePath)



def generateDiagram(code):
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
    microphone_emoji = '\U0001F399'  # Unicode for studio microphone emoji
    #diagram.plot(Target Sound)
    mpl.scatter(x, y_coordinates, label = 'Microphones', marker = microphone_emoji)
    mpl.scatter(sysInfo['SOD'], sysInfo['SAD'], label = 'Target Sound')
    # Set y-axis limits
    mpl.xlabel('Total Spread'+ str(total_spread))
    mpl.ylabel('')
    mpl.title('Diagram of Mics')
    mpl.legend(loc='upper right')
    mpl.savefig(filepath)
    mpl.close('all')
