import tkinter as tk

import wave

import threading

import pyaudio


# tkinter: A built-in Python library for creating graphical user interfaces (GUIs).

# pyaudio: A library that provides bindings for PortAudio, which allows audio input and output.

# wave: A module for reading and writing WAVE files.

# threading: A module to run multiple threads allowing the GUI to remain responsive during recording.

 

# Set the recording parameters

FORMAT = pyaudio.paInt16  # Audio format

CHANNELS = 2               # Number of audio channels

RATE = 44100               # Sample rate in Hertz

CHUNK = 1024               # Chunk size

duration = 10              # Duration of the recording in seconds

audio_file_path = "output2.wav"  # File to save the audio





#indicates whether audio is already recording

class AudioRecorder: 
    """ Audio Recorder object """
    def __init__(self):

        self.is_recording = False

        self.frames = []

#records audio

    def record_audio(self):

        self.frames = []  # Clear previous frames

        self.is_recording = True

         

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,

                        channels=CHANNELS,

                        rate=RATE,

                        input=True,

                        frames_per_buffer=CHUNK)

  

        print("Recording started...")

         

        for _ in range(0, int(RATE / CHUNK * duration)):

            data = stream.read(CHUNK)

            self.frames.append(data)

  

        print("Recording finished.")

        stream.stop_stream()

        stream.close()

        p.terminate()

        self.is_recording = False

 #saves audio

    def save_audio(self):

        if self.frames:

            with wave.open(audio_file_path, 'wb') as wf:

                wf.setnchannels(CHANNELS)

                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))

                wf.setframerate(RATE)

                wf.writeframes(b''.join(self.frames))

            print(f"Audio saved to {audio_file_path}")

  

def start_recording(recorder):

    threading.Thread(target=recorder.record_audio).start()

  

def save_recording(recorder):

    recorder.save_audio()

 #buttons 

def on_record_button_click(recorder):

    if not recorder.is_recording:

        start_recording(recorder)

    else:

        print("Recording is already in progress.")

  

def on_save_button_click(recorder):

    save_recording(recorder)

  

def main():

    #Create the audio recorder

    recorder = AudioRecorder()

  

    #Set up the GUI

    root = tk.Tk()

    root.title("Audio Recorder")

  

    record_button = tk.Button(root, text="Record", command=lambda: on_record_button_click(recorder))

    record_button.pack(pady=10)

  

    save_button = tk.Button(root, text="Save", command=lambda: on_save_button_click(recorder))

    save_button.pack(pady=10)

  

    root.mainloop()

  

if __name__ == "__main__":

    main()
