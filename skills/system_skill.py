import ctypes
from pycaw.pycaw import AudioUtilities

class SystemSkill:
    def __init__(self):
        pass

    def _get_volume_interface(self):
        devices = AudioUtilities.GetSpeakers()
        return devices.EndpointVolume

    def set_volume(self, level_percent: int):
        """0 ile 100 arasında ses seviyesini ayarlar."""
        try:
            volume = self._get_volume_interface()
            # level_percent to scalar (0.0 to 1.0)
            scalar = max(0.0, min(1.0, level_percent / 100.0))
            volume.SetMasterVolumeLevelScalar(scalar, None)
            return True, f"Sesi yüzde {level_percent} yaptım patron."
        except Exception as e:
            return False, f"Ses ayarlanamadı: {str(e)}"

    def volume_up(self, step=10):
        try:
            volume = self._get_volume_interface()
            current = volume.GetMasterVolumeLevelScalar() * 100
            new_vol = min(100, int(current + step))
            return self.set_volume(new_vol)
        except Exception as e:
            return False, str(e)

    def volume_down(self, step=10):
        try:
            volume = self._get_volume_interface()
            current = volume.GetMasterVolumeLevelScalar() * 100
            new_vol = max(0, int(current - step))
            return self.set_volume(new_vol)
        except Exception as e:
            return False, str(e)

    def mute(self):
        try:
            volume = self._get_volume_interface()
            volume.SetMute(1, None)
            return True, "Sesi tamamen kapattım patron."
        except Exception as e:
            return False, str(e)

    def unmute(self):
        try:
            volume = self._get_volume_interface()
            volume.SetMute(0, None)
            return True, "Sesi açtım patron."
        except Exception as e:
            return False, str(e)

    def minimize_all_windows(self):
        """Tüm pencereleri küçültüp masaüstünü gösterir (Win + D)."""
        # 0x20 is VK_SPACE, but Shell.Application is cleaner
        try:
            ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0) # Win down
            ctypes.windll.user32.keybd_event(0x44, 0, 0, 0) # D down
            ctypes.windll.user32.keybd_event(0x44, 0, 2, 0) # D up
            ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0) # Win up
            return True, "Masaüstünü gösteriyorum patron."
        except Exception as e:
            return False, str(e)

    def type_text(self, text: str):
        """Verilen metni panoya kopyalar ve klavye ile (Ctrl+V) yapıştırır."""
        try:
            import pyperclip
            import pyautogui
            import time
            pyperclip.copy(text)
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
            return True, "Yazıldı, patron."
        except Exception as e:
            return False, f"Metni yazarken hata oluştu: {e}"

if __name__ == "__main__":
    skill = SystemSkill()
    print("SystemSkill hazır.")
