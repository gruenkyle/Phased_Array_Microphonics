import threading
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import queue
import os

"""
Things to do:
1. We need to configure this so that it works with multiple mics
    a. Maybe have the user set how many mics they have, but ensure that the output can handle it
2. Have stereo (or anything better) playback - rn it's just mono
3. The beginning of the recording still kind of stutters - it's a non-issue but we should still work on it
4. Have the processing done on it before outputting - might be out of scope tho.
"""

# === Configuration ===
SAMRATE = 44100  # Sample rate
DURATION = 10  # Duration of recording in seconds
CODE = "test_recording"
OUTPUT_DIR = "./output/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Queues for recording and playback ===
record_queue = queue.Queue()
playback_queue = queue.Queue()

# === Choose devices and mic settings ===
def choose_input_device():
    print("\nAvailable input devices:\n")
    for idx, dev in enumerate(sd.query_devices()):
        if dev['max_input_channels'] > 0:
            print(f"{idx}: {dev['name']} - {dev['max_input_channels']} channels")

    device_index = int(input("\nEnter the index of your INPUT device: "))
    max_channels = sd.query_devices(device_index)['max_input_channels']
    mic_count = int(input(f"How many microphones (1 to {max_channels}): "))
    return device_index, mic_count

def choose_output_device():
    print("\nAvailable output devices:\n")
    for idx, dev in enumerate(sd.query_devices()):
        if dev['max_output_channels'] > 0:
            print(f"{idx}: {dev['name']} - {dev['max_output_channels']} channels")

    return int(input("\nEnter the index of your OUTPUT (playback) device: "))

def choose_playback_option(mic_count):
    print("\nPlayback options:")
    for i in range(mic_count):
        print(f"{i}: Listen to Mic {i+1}")
    print(f"{mic_count}: Mix all microphones")
    return int(input("Choose playback option: "))

# === Audio callback function ===
def audio_callback(indata, frames, time, status):
    if status:
        print(f"Stream error: {status}")
    record_queue.put(indata.copy())
    playback_queue.put(indata.copy())

# === Playback thread ===
def playback_thread(output_device_index, mic_count, playback_choice):
    print("Playback thread started...")

    try:
        with sd.OutputStream(
            samplerate=SAMRATE,
            channels=1,
            dtype='float32',
            device=output_device_index
        ) as stream:
            while True:
                data = playback_queue.get()
                if data is None:
                    break

                if playback_choice == mic_count:  # Mix all
                    mono = np.mean(data.astype(np.float32) / 32768.0, axis=1)
                else:  # Specific mic channel
                    mono = data[:, playback_choice].astype(np.float32) / 32768.0

                stream.write(mono)
    except Exception as e:
        print(f"Playback error: {e}")

# === Main function ===
def record_audio():
    input_device_index, mic_count = choose_input_device()
    output_device_index = choose_output_device()
    playback_choice = choose_playback_option(mic_count)

    # Start playback thread
    thread = threading.Thread(target=playback_thread, args=(output_device_index, mic_count, playback_choice))
    thread.start()

    print(f"\nRecording {mic_count} channels for {DURATION} seconds...\n")

    # Start recording
    with sd.InputStream(
        samplerate=SAMRATE,
        channels=mic_count,
        dtype='int16',
        callback=audio_callback,
        device=input_device_index
    ):
        sd.sleep(DURATION * 1000)

    print("\nRecording complete! Saving audio files...")

    # Stop playback thread
    playback_queue.put(None)
    thread.join()

    # Collect recorded audio chunks
    recorded_audio = []
    while not record_queue.empty():
        recorded_audio.append(record_queue.get())

    if not recorded_audio:
        print("No audio recorded.")
        return

    # Concatenate all audio chunks
    audio_data = np.concatenate(recorded_audio, axis=0)
    print(f"Total frames recorded: {audio_data.shape[0]}")

    # Save full multi-channel audio
    full_file = f"{OUTPUT_DIR}/All_Mics_{CODE}.wav"
    write(full_file, SAMRATE, audio_data)
    print(f"Saved all channels to: {full_file}")

    # Save individual mic channels
    for channel in range(mic_count):
        channel_data = audio_data[:, channel]
        filename = f"{OUTPUT_DIR}/Mic{channel + 1}_{CODE}.wav"
        write(filename, SAMRATE, channel_data)
        print(f"Saved Mic {channel + 1} to: {filename}")

    print("\n✅ All done!\n")

# === Optional Speaker Test ===
def test_speaker():
    print("Testing output speaker...")
    duration = 1
    t = np.linspace(0, duration, int(SAMRATE * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * 440 * t)  # A4 tone
    sd.play(tone, samplerate=SAMRATE)
    sd.wait()
    print("Speaker test complete!")

# === Run ===
if __name__ == "__main__":
    record_audio()
    # test_speaker()  # Uncomment to test speaker


