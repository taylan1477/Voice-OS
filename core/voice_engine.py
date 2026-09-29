import os
import time
import asyncio
import pyttsx3
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
import wave
import edge_tts
import pygame

TEMP_AUDIO_IN = "temp_input.wav"
TEMP_AUDIO_OUT = "temp_output.mp3"
VOICE = "tr-TR-AhmetNeural"

class VoiceEngine:
    def __init__(self):
        print("[VoiceEngine] Faster-Whisper (Kulak) yükleniyor...")
        self.stt_model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=8)
        print("[VoiceEngine] Kulak ve Ağız motorları hazır (Hibrit Mod).")

    def speak(self, text: str):
        """Önce bulut (edge-tts) dener, başarısız olursa yerel sese (pyttsx3) geçer."""
        if not text:
            return
        print(f"[Jarvis Söylüyor]: {text}")
        
        async def _synth():
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(TEMP_AUDIO_OUT)

        try:
            # 1. İnternet üzerinden (edge-tts) deneme
            asyncio.run(_synth())
            pygame.mixer.init()
            pygame.mixer.music.load(TEMP_AUDIO_OUT)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
            pygame.mixer.quit()
        except Exception as e:
            print(f"[VoiceEngine] Bulut ses motoru başarısız, yerel sese geçiliyor... ({e})")
            # 2. Hata olursa yerel sese (pyttsx3) geçiş
            try:
                engine = pyttsx3.init()
                engine.setProperty('rate', 150)
                voices = engine.getProperty('voices')
                for voice in voices:
                    if "turkish" in voice.name.lower() or "tr" in getattr(voice, 'languages', []):
                        engine.setProperty('voice', voice.id)
                        break
                engine.say(text)
                engine.runAndWait()
            except Exception as e2:
                print(f"[VoiceEngine Hatası]: Yerel ses de çalışmadı: {e2}")

    def record_microphone(self, duration=5, samplerate=16000):
        """Mikrofondan belirtilen sure boyunca ses kaydeder."""
        print(f"\n[🎤 Jarvis Dinliyor... ({duration} sn konuşun)]")
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        
        with wave.open(TEMP_AUDIO_IN, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
            
        print("[Jarvis Düşünüyor...]")
        return TEMP_AUDIO_IN

    def transcribe(self, audio_path=TEMP_AUDIO_IN):
        """Kaydedilen sesi Turkce metne cevirir."""
        try:
            segments, info = self.stt_model.transcribe(audio_path, language="tr", beam_size=5)
            text = " ".join([seg.text for seg in segments]).strip()
            return text
        except Exception as e:
            print(f"[STT Hatası]: {e}")
            return ""

if __name__ == "__main__":
    v = VoiceEngine()
    v.speak("Sistem testi tamamlandı patron.")
