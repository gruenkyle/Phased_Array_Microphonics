import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import queue
import os


duration = 10
SAMRATE = 44100  # Sample rate
MIC_COUNT = 1  # Adjust based on your setup
CODE = "test_recording"

output_dir = f"../MICRECORD/{CODE}/INDIV/"
os.makedirs(output_dir, exist_ok=True)

audio_queue = queue.Queue()


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


#def audio_callback(indata, outdata, frames, time, status):
#    """Handles both recording and playback."""
#    if status:
#        print(f"Stream error: {status}")
#    outdata[:] = indata  # Play back the recorded input in real time

def audio_callback(indata, frames, time, status):
    """This function is called in real time when new audio data is available."""
    if status:
        print(f"Stream error: {status}")
    audio_queue.put(indata.copy())  # Store audio data for later saving
    sd.play(indata)  # Live playback of input audio

def recordAudio():
    device_idx = deviceIndex()
    if device_idx is None:
        return
    
    sd.default.device = device_idx

    print(f"Recording {MIC_COUNT} channels live for {duration} seconds...")

    # Open input-output stream
    with sd.Stream(
        samplerate=SAMRATE,
        channels=MIC_COUNT,
        dtype='int16',
        callback=audio_callback
    ):
        sd.sleep(duration * 1000)  # Keep the script running while streaming

    print("Recording complete! Saving audio...")

    # Save recorded audio from queue
    recorded_audio = []
    while not audio_queue.empty():
        recorded_audio.append(audio_queue.get())

    # Convert list to numpy array
    audio_data = np.concatenate(recorded_audio, axis=0)

    # Save individual channels
    for channel in range(MIC_COUNT):
        channel_data = audio_data[:, channel]
        filename = f"{output_dir}/Mic{channel + 1}_{CODE}.wav"
        write(filename, SAMRATE, channel_data)
        print(f"Channel {channel + 1} saved to {filename}")

recordAudio()