from pycaw.pycaw import AudioUtilities

devices = AudioUtilities.GetSpeakers()
print("dir(devices):", dir(devices))
