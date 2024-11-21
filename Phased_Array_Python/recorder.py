import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

# Parameters
sample_rate = 44100  # Hz (adjust as needed)
duration = 10        # Duration in seconds
channels = 4         # Number of channels for UMC404HD
device_index = 3  # Set this to the index of your UMC404HD (use sd.query_devices() to find it)

# List available devices (optional, helpful for debugging)
print("Available audio devices:")
print(sd.query_devices())

# Set the desired device (if known, replace `None` with the UMC404HD index)
sd.default.device = device_index

print(f"Recording {channels} channels for {duration} seconds...")
audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=channels, dtype='int16')
sd.wait()  # Wait for the recording to finish
print("Recording complete!")

# Save each channel to a separate WAV file
for channel in range(channels):
    channel_data = audio_data[:, channel]
    filename = f"channel_{channel + 1}.wav"
    write(filename, sample_rate, channel_data)
    print(f"Channel {channel + 1} saved to {filename}")