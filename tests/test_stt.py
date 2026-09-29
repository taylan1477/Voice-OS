from faster_whisper import WhisperModel
import time
import os

print("[Jarvis Ear] Faster-Whisper modeli CUDA uzerinde baslatiliyor...")
start_time = time.time()

# Use CPU with int8 on 16-thread i5-13500H (lightning fast, leaves GPU 100% free for LLM and games)
model = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=8)
load_time = time.time() - start_time
print(f"[Jarvis Ear] Model CUDA'ya basariyla yuklendi ({load_time:.2f} saniye).")

audio_file = "jarvis_intro.mp3"
if os.path.exists(audio_file):
    print(f"[Jarvis Ear] '{audio_file}' dosyasi dinleniyor ve cozumleniyor...")
    transcribe_start = time.time()
    segments, info = model.transcribe(audio_file, language="tr", beam_size=5)
    
    print(f"[Jarvis Ear] Algilanan dil: {info.language} (Olasilik: {info.language_probability:.2f})")
    for segment in segments:
        print(f"[Jarvis Duydu ({segment.start:.1f}s - {segment.end:.1f}s)]: {segment.text}")
    
    total_time = time.time() - transcribe_start
    print(f"[Jarvis Ear] Cozumleme suresi: {total_time:.2f} saniye. Test basarili!")
else:
    print(f"Hata: {audio_file} bulunamadi.")
