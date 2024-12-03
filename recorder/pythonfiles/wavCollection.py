import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

duration = 10

def deviceIndex():
    target_name = "IN 1-4 (BEHRINGER UMC 404HD 192"
    target_host_api = "MME"

    for idx, device in enumerate(sd.query_devices()):
        host_api_name = sd.query_hostapis()[device['hostapi']]['name']
        if target_name in device['name'] and target_host_api in host_api_name:
            print(f"Target device found: Index {idx} -> {device['name']} ({host_api_name})")
            break
    else:
        print("Target device not found.")

    return idx

def recordAudio(CODE, SAMRATE, MIC_COUNT):
    sd.default.device = deviceIndex()
    
    print(f"Recording {MIC_COUNT} channels for {duration} seconds...")
    audio_data = sd.rec(int(SAMRATE * duration), samplerate=SAMRATE, channels=MIC_COUNT, dtype='int16')
    sd.wait()
    print("Recording complete!")
    
    for channel in range(MIC_COUNT):
        channel_data = audio_data[:, channel]
        filename = f"../MICRECORD/{CODE}/INDIV/Mic{channel + 1}_{CODE}.wav"
        write(filename, SAMRATE, channel_data)
        print(f"Channel {channel + 1} saved to {filename}")