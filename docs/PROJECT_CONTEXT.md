# VOICE OS (J.A.R.V.I.S.) - PROJE DÖKÜMANTASYONU & BAĞLAM (CONTEXT) ⚡🎙️

Bu döküman, **Voice OS** projesinin donanım yapılandırmasını, mimarisini, kazanılan tecrübeleri, çözülen kritik bug'ları ve gelecek yol haritasını içerir. Yeni açılacak Antigravity konuşmasında bu dosyayı referans alarak sıfır kayıpla devam edilecektir.

---

## 🎯 Projenin Amacı ve Felsefesi
Voice OS; kullanıcının kendi donanımı üzerinde (HP Victus 16 - i5-13500H, RTX 4060 8GB VRAM, 32GB RAM), **%100 yerel, internetsiz (offline), takip edilemez, sansürsüz ve sıfır gecikmeli (zero-latency)** çalışan bir Windows Sesli İşletim Sistemi Kokpitidir.

- **GitHub Reposu:** `https://github.com/taylan1477/Voice-OS`
- **Yerel Klasör:** `C:\Projeler\HelperTools\Voice-OS`

---

## 🏛️ Mimari Bileşenler ve Akış

```
[Gamepad (Joy9) / Klavye (Ctrl+A+F)]
             │
             ▼
   [jarvis_hotkey.ahk] ────(HTTP GET :8765/listen)────► [main.py (BaseHTTPRequestHandler)]
                                                                    │ (Thread-Safe Queue)
                                                                    ▼
                                                          [main.py (Main Thread Event Loop)]
                                                                    │
                                   ┌────────────────────────────────┴──────────────────────────────┐
                                   ▼                                                               ▼
                     [core/voice_engine.py]                                              [core/brain.py]
                   (Faster-Whisper STT / INT8)                                      (Türkçe Karakter & Regex Router)
                                   │                                                               │
                                   ▼                                                               ▼
                      Metin: "Spiderman filmini aç"                                    Intent: {"skill": "media", ...}
                                   │                                                               │
                                   └────────────────────────────────┬──────────────────────────────┘
                                                                    ▼
                                                       [skills/*_skill.py]
                                               (Winamp, Media, System, Vision)
                                                                    │
                                                                    ▼
                                                     [core/voice_engine.py]
                                              (Hibrit: Edge-TTS / SAPI5 pyttsx3)
```

### 1. `main.py` (Orchestrator)
- **Thread Mimarisi:** Windows'ta `sounddevice` ve ses kayıt motorunun kilitlenmemesi için tüm ses dinleme ve skill çalıştırma işlemleri **ana iş parçacığında (Main Thread)** kuyruktan (`queue.Queue`) beslenir.
- **Konsol Girişi:** Klasik `input()` fonksiyonunun Windows konsol I/O kilitlenmesine yol açması sorunu `msvcrt.kbhit()` kullanılarak tamamen çözülmüştür.
- **HTTP Daemon (Port: 8765):** AHK kısayolundan gelen `/listen` isteklerini karşılar.

### 2. `core/voice_engine.py` (Ear & Mouth)
- **Kulak (STT):** `faster-whisper` `small` modelini INT8 CPU optimizasyonu (8 thread) ile sıfır gecikmeyle çalıştırır.
- **Ağız (TTS):** **Hibrit Ses Motoru**. Önce internet üzerinden Microsoft'un doğal sesi olan `edge-tts` (`tr-TR-AhmetNeural`) dener; internet kesildiğinde ise anında yerel Windows SAPI5 (`pyttsx3`) ses motoruna otomatik geçiş yapar.

### 3. `core/brain.py` (Intent Router & Local LLM)
- **Türkçe Karakter Normalizasyonu:** Python'ın yerleşik `.lower()` fonksiyonunun Türkçedeki büyük "İ" harfini "i̇" (noktalı i) yapıp kelime eşleşmelerini bozması sorunu `_tr_lower()` fonksiyonu ile çözüldü.
- **Noktalama Temizliği:** Cümle sonundaki veya ortasındaki virgül, nokta gibi işaretler temizlenerek kural tabanlı eylemlere (`system`, `media`, `winamp`, `vision`) yönlendirilir.
- **Ollama LLM Entegrasyonu:** Eylem dışı genel sohbet, oyun danışmanlığı veya strateji soruları yerel `http://127.0.0.1:11434/api/generate` üzerinden `jarvis` modeline (Qwen 2.5 7B) gönderilir.

### 4. `Modelfile` (Kişilik Kuralları)
- Hitap: Sadece **Kaptan** veya **Patron**.
- Uzunluk: En fazla **1-2 cümle**.
- **Asla "Yes Man" Değil:** Bilmediği veya yapamayacağı bir şeyi uydurmaz (hayal kurmaz), doğrudan *"Bilmiyorum patron"* der.
- **Asla Proaktif Değil:** Kullanıcı komut vermediği sürece arka planda kendi kendine konuşmaz veya işlem başlatmaz.
- Model sıcaklığı: `temperature 0.3` (halüsinasyonu minimuma indirmek için analitik ayarlandı).

### 5. Yetenekler (`skills/`)
- `system_skill.py`: `pycaw` ile Windows master ses seviyesi (volume up/down/mute/unmute), Win+D masaüstü minimizer, `pyperclip` + `pyautogui` ile textfield'lara klavyeyle yazı yazma (`type_text`).
- `winamp_skill.py`: `C:\Users\taycore\Music` klasöründeki 1625 MP3'ü indeksler, ruh haline göre m3u listesi oluşturur, Winamp'ı başlatır ve kapatır (`close_music`).
- `media_skill.py`: `C:\Users\taycore\Desktop\Prospecting\to watch` klasöründeki filmleri (`Spider-Man (2002).mp4`, `Matango.mp4` vb.) arar. Dosya ismindeki parantez, yıl, tire gibi karakterleri temizleyen **Fuzzy Matching** ile hatasız açar.
- `vision_skill.py`: Ekranda ne olduğunu analiz eder. **Çift Yapay Zeka (Dual-AI)** prensibiyle çalışır: `pyautogui` ile ekran görüntüsü alır (`last_vision.jpg` debug dosyası kaydeder), önce `llava:7b`'ye İngilizce betimletir, ardından `jarvis` (Qwen) ile doğal ve akıcı bir Türkçe tek cümleye çevirtir.

### 6. `jarvis_hotkey.ahk` (AutoHotkey v2)
- Kısayollar: `Ctrl + A + F`, `Ctrl + Alt + F` veya Gamepad **`Joy9`** (Select/Share tuşu).
- **Auto-Launcher:** Eğer Jarvis (`main.py`) açık değilken kısayola basılırsa, hata vermek yerine PowerShell penceresi açıp `C:\Projeler\HelperTools\Voice-OS` dizininde Jarvis'i otomatik başlatır.

---

## 🧠 Gelecek Yol Haritası (Smart Plan)
1. **Faz 1: LLM Tabanlı JSON Intent Router (Sıradaki Adım)**
   - Kural tabanlı `if any(w in text)` kontrolleri yerine, LLM'in doğal dili anlayıp `{ "intent": "play_movie", "target": "spiderman" }` gibi yapılandırılmış JSON çıktısı vermesini sağlamak.
2. **Faz 2: Gelişmiş GUI & Uygulama Otonomisi**
   - Sadece film/müzik değil, *"Discord'u aç"*, *"Steam'i başlat"* gibi dinamik uygulama yöneticisi.
3. **Faz 3: Oturum Bağlamı (Contextual Memory)**
   - *"Sesi aç"* dedikten hemen sonra *"Biraz daha"* denildiğinde önceki eylemi hatırlayan kısa süreli bellek.
