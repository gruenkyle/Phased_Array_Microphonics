import os
import sys

def recNum():
    directories = next(os.walk('../MICRECORD'))[1]
    print(directories)
    print(len(directories))
    
    if (len(directories) == 0):
        return -1
    
    index = 0
    for dir in directories:
        directories[index] = int(dir[0:-6])
        index += 1
        
    return max(directories)
    
    

def genDir(RECORDNUM, MIC_COUNT, SOURCES, TYPE, NOISE):
    
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
        case "BACKGROUND":
            NOISENUM = "5"
        case "VOICE":
            NOISENUM = "3"
        case "TONE":
            NOISENUM = "1"
        case "NONE":
            NOISENUM = "0"
        
    pathdir = "../RECORDING/" + str(RECORDNUM) + MIC_COUNT + SOURCES + TYPENUM + NOISENUM
    
    exist = os.path.isdir(pathdir)
    if (exist):
        print("ALREADY EXISTS")
    else:
        print("Creating Directories...")
        os.mkdir(pathdir)
        os.mkdir(pathdir + "/FIGS")
        os.mkdir(pathdir + "/INDIV")
        os.mkdir(pathdir + "/SUM")
        
    print(pathdir)

def main():
    recordingNum = recNum() + 1
    
    MIC_COUNT = sys.argv[1]
    SOURCES = sys.argv[2]
    TYPE = sys.argv[3]
    NOISE = sys.argv[4]
    
    genDir(recordingNum, MIC_COUNT, SOURCES, TYPE, NOISE)

if __name__=='__main__':
    main()