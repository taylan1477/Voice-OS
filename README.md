# Voice OS (J.A.R.V.I.S.) ⚡🎙️

%100 Yerel, Çevrimdışı (Offline), Sansürsüz ve Otonom Windows Sesli Kontrol İşletim Sistemi Ajanı.

İnternet bağlantısına ihtiyaç duymadan, doğrudan yerel GPU ve CPU üzerinde çalışan yapay zeka modelleriyle Windows'u kontrol eder, oyunlarda ekrana bakıp tavsiye verir, müzik/film arşivinizi yönetir ve klavyenizi kullanarak ekrana yazı yazar.

---

## 🌟 Öne Çıkan Yetenekler

- **🔒 %100 Yerel ve Güvenli:** Verileriniz asla buluta gitmez. Ollama (`qwen2.5:7b` ve `llava:7b`) ile tamamen cihazınızda çalışır.
- **🎙️ Hibrit Ses Motoru (Ear & Mouth):**
  - **Kulak (STT):** `faster-whisper` (Small model, INT8 CPU optimized).
  - **Ağız (TTS):** İnternet varken kristal netliğinde `edge-tts` (AhmetNeural), internet kesildiğinde anında yerel Windows SAPI5 (`pyttsx3`) motoruna otomatik geçiş.
- **👁️ Görsel Analiz (Dual-AI Vision):** Ekranda ne olduğunu inceleyip (oyun arayüzü, masaüstü, logo vb.) tek bir doğal Türkçe cümleyle açıklar.
- **🎮 Gamepad & Klavye Kısayolları:**
  - `Ctrl + A + F` veya `Ctrl + Alt + F` ile anında dinleme.
  - Gamepad üzerindeki `Joy9` (Select/Share) tuşuyla tek tıkla tetikleme.
  - Jarvis kapalıyken kısayola basıldığında PowerShell'i açıp kendini otomatik başlatma.
- **🎵 Akıllı Winamp & Medya Yönetimi:** 
  - 1600+ MP3'lük yerel arşivi indeksler, ruh haline veya sanatçıya göre anında playlist oluşturup çalar.
  - "Müziği kapat" dendiğinde anında kapatır.
  - "Spiderman filmini aç" gibi komutlarda arşivdeki filmleri isim benzerliklerine göre bulup oynatır.
- **⌨️ Klavye Yazı Yazdırma (Typewriter):** Mouse ile herhangi bir text alanına tıkladıktan sonra *"Merhaba dünya yaz"* dediğinizde ışık hızında metni ekrana yazar.
- **🔊 Windows Sistem Kontrolü:** Ses açma, kısma, sessize alma (mute/unmute), tüm pencereleri küçültme (Win+D).

---

## 🛠️ Kurulum ve Gereksinimler

### 1. Sistem Gereksinimleri
- Windows 10 / 11
- Python 3.10+
- [AutoHotkey v2](https://www.autohotkey.com/v2/)
- [Ollama for Windows](https://ollama.com/)

### 2. Gerekli Python Paketleri
```bash
pip install sounddevice numpy faster-whisper edge-tts pygame pyttsx3 pycaw pyautogui pyperclip mutagen requests
```

### 3. Yerel Modellerin Hazırlanması
```bash
# Ollama modellerini indirin
ollama pull qwen2.5:7b
ollama pull llava:7b

# Özel Jarvis kişiliğini oluşturun
ollama create jarvis -f Modelfile
```

---

## 🚀 Çalıştırma

1. `jarvis_hotkey.ahk` dosyasına çift tıklayarak arka plan kısayol dinleyicisini başlatın.
2. Konsoldan doğrudan başlatmak için:
```powershell
python main.py
```
3. Klavyeden **`Ctrl + A + F`** tuşuna veya Gamepad'den **`Joy9`** tuşuna basarak Jarvis'e sesli emir verin!
