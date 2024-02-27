#######################################
#
#      Phased Array Microphonics
# Script to Analyze and Return Data Base Values
#       given specific code number 
#
#          Author : Kyle Gruen
#          Date : 02/27/2024
#
#######################################

# Import Python Libraries #
import numpy as np
import sys, os, os.path
import pandas as pd

# Get Data Base # 
filePathDB = "../MICRECORD/RecordingDatabase.txt"
database = pd.read_csv(filePathDB)

def getInformation(code):
    # Find Row in dataframe that correlates to the code given #
    return information

print(getInformation(1034112000))