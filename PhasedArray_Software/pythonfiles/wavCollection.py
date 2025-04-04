import threading
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import queue
import os

# === Configuration ===
duration = 10  # seconds
SAMRATE = 44100  # Sample rate
MIC_COUNT = 2  # Number of input channels (microphones)
OUTPUT_DEVICE_INDEX = 4  # Change this to your speaker index (run the tempCodeRunner.py)
CODE = "test_recording"

#output_dir = f"../MICRECORD/{CODE}/INDIV/"
output_dir = "./output/"
os.makedirs(output_dir, exist_ok=True)

# === Queues for recording and playback ===
record_queue = queue.Queue()
playback_queue = queue.Queue()

# === Find input device index ===
def deviceIndex():
    '''
    Find the input device index (we should make something similar for output index tho)
    '''
    target_name = "Microphone Array (Intel® Smart"
    target_host_api = "MME"

    for idx, device in enumerate(sd.query_devices()):
        host_api_name = sd.query_hostapis()[device['hostapi']]['name']
        if target_name in device['name'] and target_host_api in host_api_name:
            print(f"Target device found: Index {idx} -> {device['name']} ({host_api_name})")
            return idx
    print("Target device not found.")
    return None

# === Input callback ===
def audio_callback(indata, frames, time, status):
    '''
    put the audio in the queues - one to play back and one to record
    '''
    if status:
        print(f"Stream error: {status}")
    record_queue.put(indata.copy())
    playback_queue.put(indata.copy())

# === Playback thread ===
def playback_thread():
    '''
    This thread runs below, it does the actual playback
    '''
    print("Using output device:", sd.query_devices(OUTPUT_DEVICE_INDEX)['name']) #make sure these are headphones to avoid feedback!
    try:
        with sd.OutputStream(
            samplerate=SAMRATE,
            channels=1,
            dtype='float32',
            device=OUTPUT_DEVICE_INDEX
        ) as stream:
            while True:
                data = playback_queue.get()
                if data is None:
                    break
                mono = data[:, 0].astype(np.float32) / 32768.0
                stream.write(mono)
    except Exception as e:
        print(f"Playback error: {e}")

# === Main function ===
def recordAudio():
    '''
    Main function to record audio
    '''
    device_idx = deviceIndex()
    if device_idx is None:
        return

    # Start playback thread
    thread = threading.Thread(target=playback_thread) # this is where the thread starts - it runs in the background
    thread.start()

    print(f"Recording {MIC_COUNT} channels live for {duration} seconds...")

    # take in the audio
    with sd.InputStream(
        samplerate=SAMRATE,
        channels=MIC_COUNT,
        dtype='int16',
        callback=audio_callback,
        device=device_idx
    ):
        sd.sleep(duration * 1000)

    print("Recording complete! Saving audio...")

    # Stop the playback thread
    playback_queue.put(None)
    thread.join()

    # Gather recorded chunks
    recorded_audio = []
    while not record_queue.empty():
        recorded_audio.append(record_queue.get())

    if not recorded_audio:
        print("No audio was recorded.")
        return

    # Concatenate and save
    audio_data = np.concatenate(recorded_audio, axis=0)
    print("Total frames recorded:", audio_data.shape[0])

    # Save individual channels
    for channel in range(MIC_COUNT):
        channel_data = audio_data[:, channel]
        filename = f"{output_dir}/Mic{channel + 1}_{CODE}.wav"
        write(filename, SAMRATE, channel_data)
        print(f"Channel {channel + 1} saved to {filename}")


def test_speaker():
    '''
    Function to test speakers. If you hear a tone, it's working.
    '''
    print("starting....")
    duration = 1
    t = np.linspace(0, duration, int(SAMRATE * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * 440 * t)  # A4 tone
    sd.play(tone, samplerate=SAMRATE, device=OUTPUT_DEVICE_INDEX)
    sd.wait()
    

#test_speaker()
recordAudio()
#print("Output directory:", os.path.abspath(output_dir))

