import os
import sys

def recNum(ID):
    directories = next(os.walk('../MICRECORD'))[1]
    print(directories)
    print(len(directories))
    
    if (len(directories) == 0):
        return 0
    
    index = 0
    found = 0
    
    for dir in directories:
        if (str(dir[-4:len(dir)]) == ID):
            found += 1
            print("found")
        directories[index] = 0
        index += 1
    
    if (found > 0):
        return found + 1
    return 0
    
    

def generate(MIC_COUNT, TYPE, NOISE):
    
    sources = 1
    
    match TYPE:
        case "BACKGROUND":
            TYPENUM = "5"
        case "VOICE":
            TYPENUM = "3"
        case "TONE":
            TYPENUM = "1"
            
    match NOISE:
        case "VOICE + BACKGROUND":
            NOISENUM = "8"
            sources += 2
        case "BACKGROUND":
            NOISENUM = "5"
            sources += 1
        case "VOICE":
            NOISENUM = "3"
            sources += 1
        case "TONE":
            NOISENUM = "1"
            sources += 1
        case "NONE":
            NOISENUM = "0"
            
    ID = str(MIC_COUNT) + str(sources) + TYPENUM + NOISENUM
        
    RECORDNUM = recNum(ID)
    
    pathdir = "../MICRECORD/" + str(RECORDNUM) + ID
    
    exist = os.path.isdir(pathdir)
    if (exist):
        print("ALREADY EXISTS")
    else:
        print("Creating Directories...")
        os.mkdir(pathdir)
        os.mkdir(pathdir + "/FIGS")
        os.mkdir(pathdir + "/INDIV")
        os.mkdir(pathdir + "/SUM")
        
    return (str(RECORDNUM) + str(MIC_COUNT) + str(sources) + TYPENUM + NOISENUM)