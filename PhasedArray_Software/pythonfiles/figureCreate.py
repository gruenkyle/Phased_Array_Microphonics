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


##############
# Creates and saves matplot figure of all audio channel waves
#
# mic_signal_cells(numpy array) = data values of each microphone input
# code(int) = numerical code for current recording / storage
#
# file_output <- matplot figure 
##############
def multiFigure(mic_signal_cells, sysInfo):
    # Create storage filepath to store new figure #
    filePath = "../MICRECORD/" + str(sysInfo['CODE'].iloc[0])  + "/FIGS/multi_" + str(sysInfo['CODE'].iloc[0])  + ".png"
    FORLOOPARR = np.arange(len(mic_signal_cells))

    # Create Figure Object #
    mpl.figure()
    mpl.figure(figsize=(10, 6))
 
    # Plot each microphone data on subplot #
    for mic in FORLOOPARR:
        mpl.subplot(len(mic_signal_cells), 1, mic + 1)
        mpl.plot(mic_signal_cells[mic], color='brown')   
        mpl.grid(True, linestyle='--', color='gray', alpha=0.5)
        # Change background color to beige #
        mpl.gca().set_facecolor('#F5F5DC')  # Hex code for beige
        mpl.xlabel('Number of Samples')
        mpl.ylabel('Amplitude')

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
def summationFigure(micSummationArray, sysInfo):
    # Create File Path #
    filePath = "../MICRECORD/" + str(sysInfo['CODE'].iloc[0])  + "/FIGS/FinalSummation_" + str(sysInfo['CODE'].iloc[0])  + ".png"

    # Create Figure and Plot #
    mpl.figure()
    mpl.figure(figsize=(10, 6))
    mpl.plot(micSummationArray, color='brown')
    mpl.xlabel('Number of Samples')
    mpl.ylabel('Amplitude')

    #yumna added:
    # Add grid lines to the plot #
    mpl.grid(True, linestyle='--', color='gray', alpha=0.5)
    # Change background color to beige #
    mpl.gca().set_facecolor('#F5F5DC')  # Hex code for beige

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
def overlappingFigure(micSummationArray, closestArray, sysInfo):
    # Create File Path for Storage #
    filePath = "../MICRECORD/" + str(sysInfo['CODE'].iloc[0])  + "/FIGS/Overlap_" + str(sysInfo['CODE'].iloc[0])  + ".png"

    # Create figure object and plot mic summation behind closest array #
    mpl.figure()
    mpl.figure(figsize=(10, 6))
    mpl.plot(micSummationArray, label="Summation", color="brown")
    mpl.plot(closestArray, label="Closest", color="black")
    mpl.xlabel('Number of Samples')
    mpl.ylabel('Amplitude')

    #yumna added:
    # Add grid lines to the plot #
    mpl.grid(True, linestyle='--', color='gray', alpha=0.5)
    # Change background color to beige #
    mpl.gca().set_facecolor('#F5F5DC')  # Hex code for beige

    # Save figure to file path above #
    mpl.tight_layout()
    mpl.savefig(filePath)

##############
# Creates and saves figure of the scalar, spread, and optimal amount of microphones
# generateDiagram(code) = gets data from filepath for diagram
# code(int) = numerical code for current recording / storage
#
# file_output <- matplot figure 
##############
def generateDiagram(sysInfo):
    # Create File Path #
    filepath = "../MICRECORD/"+ str(sysInfo['CODE'].iloc[0]) + "/FIGS/" + str(sysInfo['CODE'].iloc[0])  + "_Diagram.png"
    mpl.figure()
    
    # Initialize variables
    mic_value = sysInfo['MIC_COUNT'].iloc[0]  
    total_spread = sysInfo['TOTALSPREAD'].iloc[0]  
    SCALAR = total_spread/ (mic_value - 1)
    x = [i*SCALAR for i in range(mic_value)]
    y = np.zeros(mic_value, dtype=int)
    #MIC_EMOJI = '\U0001F399'  

    #yumna added:
    # Add grid lines to the plot #
    mpl.grid(True, linestyle='--', color='gray', alpha=0.5)
    # Change background color to beige #
    mpl.gca().set_facecolor('#F5F5DC')  # Hex code for beige
    
    # Plot mic values with respect to spread
    mpl.scatter(x, y, label = 'Microphones', marker = "2", s=350)
    mpl.scatter(sysInfo['SOD'], sysInfo['SAD'], label = 'Target Sound', s=50)
    SAD = str(sysInfo['SAD'].iloc[0])
    SOD = str(sysInfo['SOD'].iloc[0])

    mpl.xlabel('Adjacent Distance to Target: ' + SAD)
    mpl.ylabel('Opposite Distance to Target: ' + SOD)

    mpl.ylim(-1, 15)
    mpl.title('Diagram of System - ' + str(sysInfo['CODE'].iloc[0]) + '\nTotal Spread'+ ' ' + str(total_spread) + ' : in Meters')
    mpl.legend(loc='upper right')
    mpl.savefig(filepath)
    mpl.close('all')
