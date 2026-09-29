import asyncio
import edge_tts
import pygame
import os
import time

VOICE = "tr-TR-AhmetNeural"  # Microsoft's natural Turkish neural male voice
TEXT = "Selam Kaptan! Ben Jarvis. RTX 4060 üzerinde tüm sistemlerim aktif ve emrindeyim."
OUTPUT_FILE = "jarvis_intro.mp3"

async def speak():
    print(f"[Jarvis Voice] Ses dosyasi olusturuluyor: {TEXT}")
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)
    print("[Jarvis Voice] Ses dosyasi hazir, hoparlorden caliniyor...")
    
    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        
    pygame.mixer.quit()
    print("[Jarvis Voice] Tamamlandi.")

if __name__ == "__main__":
    asyncio.run(speak())
