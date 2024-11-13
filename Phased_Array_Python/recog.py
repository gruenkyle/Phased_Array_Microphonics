import sounddevice as sd

input_devices = sd.query_devices(kind='input')

print(input_devices)