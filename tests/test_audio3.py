from pycaw.pycaw import AudioUtilities

try:
    devices = AudioUtilities.GetSpeakers()
    vol = devices.EndpointVolume
    print(dir(vol))
    print("Mute:", vol.GetMute())
    print("Scalar:", vol.GetMasterVolumeLevelScalar())
except Exception as e:
    import traceback
    traceback.print_exc()
