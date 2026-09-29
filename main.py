import sys
import os
import time
import threading
import winsound
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(__file__))

from core.voice_engine import VoiceEngine
from core.brain import JarvisBrain
from skills.winamp_skill import WinampSkill
from skills.media_skill import MediaSkill
from skills.system_skill import SystemSkill
from skills.vision_skill import VisionSkill
import queue

SERVER_PORT = 8765
command_queue = queue.Queue()

class JarvisAssistant:
    def __init__(self):
        print("="*60)
        print("          ⚡ J.A.R.V.I.S. 100% LOCAL VOICE OS ⚡")
        print("="*60)
        
        self.voice = VoiceEngine()
        self.brain = JarvisBrain()
        self.winamp = WinampSkill()
        self.media = MediaSkill()
        self.system = SystemSkill()
        self.vision = VisionSkill()
        self.is_busy = False
        
        print("\n[Jarvis] Tüm modüller hazır ve göreve hazır!")
        self.voice.speak("Selam kralım!")

    def execute_intent(self, intent: dict):
        """Çözümlenen niyete göre uygun beceriyi çalıştırır."""
        if intent["type"] == "action":
            skill = intent.get("skill")
            action = intent.get("action")

            if skill == "system":
                if action == "volume_down":
                    _, msg = self.system.volume_down()
                    self.voice.speak(msg)
                elif action == "volume_up":
                    _, msg = self.system.volume_up()
                    self.voice.speak(msg)
                elif action == "mute":
                    _, msg = self.system.mute()
                    self.voice.speak(msg)
                elif action == "unmute":
                    _, msg = self.system.unmute()
                    self.voice.speak(msg)
                elif action == "minimize_all":
                    _, msg = self.system.minimize_all_windows()
                    self.voice.speak(msg)
                elif action == "type_text":
                    text = intent.get("text", "")
                    _, msg = self.system.type_text(text)
                    self.voice.speak(msg)

            elif skill == "media":
                query = intent.get("query", "")
                _, msg = self.media.find_and_play_video(query)
                self.voice.speak(msg)

            elif skill == "winamp":
                if action == "close_music":
                    _, msg = self.winamp.close_music()
                    self.voice.speak(msg)
                else:
                    mood = intent.get("mood", "")
                    _, msg = self.winamp.create_playlist_and_play(mood_keywords=mood)
                    self.voice.speak(msg)

            elif skill == "vision":
                query = intent.get("query", "Ekranda ne var?")
                print(f"[Jarvis Ekranı İnceliyor...]")
                _, msg = self.vision.analyze_screen(query)
                self.voice.speak(msg)

        elif intent["type"] == "chat":
            prompt = intent.get("prompt")
            print(f"[Jarvis Düşünüyor...]: {prompt}")
            reply = self.brain.ask_llm(prompt)
            self.voice.speak(reply)

    def listen_and_execute(self, duration=4):
        """Tetiklendiğinde bip sesiyle 4 saniye dinler ve işlemi gerçekleştirir."""
        if self.is_busy:
            print("[Jarvis] Zaten bir işlem yürütülüyor...")
            return
            
        self.is_busy = True
        try:
            # Başlama bipi (yüksek ton)
            try:
                winsound.Beep(1200, 150)
            except Exception:
                pass
            
            audio_path = self.voice.record_microphone(duration=duration)
            
            # Bitiş bipi (alçak ton)
            try:
                winsound.Beep(800, 150)
            except Exception:
                pass
                
            transcription = self.voice.transcribe(audio_path)
            
            if not transcription:
                print("[Jarvis]: Bir ses algılanamadı.")
                self.voice.speak("Seni duyamadım patron.")
            else:
                print(f"[Siz]: {transcription}")
                intent = self.brain.process_command(transcription)
                self.execute_intent(intent)
        finally:
            self.is_busy = False

    def start_background_daemon(self):
        """AHK kısayolları için arka plan HTTP dinleyicisini başlatır."""
        assistant = self
        
        class TriggerHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/listen":
                    # İşlemi hemen kuyruğa al (bağlantı kopsa bile çalışsın)
                    command_queue.put({"source": "ahk"})
                    
                    try:
                        self.send_response(200)
                        self.send_header("Content-type", "application/json")
                        self.end_headers()
                        self.wfile.write(b'{"status": "listening"}')
                    except Exception:
                        pass
                elif self.path == "/ping":
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'{"status": "ready"}')
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                pass  # Suppress HTTP access logs

        server = HTTPServer(("127.0.0.1", SERVER_PORT), TriggerHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        print(f"[Daemon] AHK Kısayol Dinleyicisi aktif (Port: {SERVER_PORT})")

    def run(self):
        """Hem AHK arka plan dinleyicisini hem de konsol döngüsünü çalıştırır."""
        self.start_background_daemon()
        
        print("\n" + "-"*60)
        print("KULLANIM KILAVUZU:")
        print("1. [Ctrl + A + F] veya [Ctrl + Alt + F] tuşuna basın (AHK üzerinden).")
        print("2. Veya konsolda [ENTER]'a basıp doğrudan konuşun.")
        print("3. Veya doğrudan metin yazıp [ENTER]'a basın.")
        print("4. Çıkmak için 'q' yazın.")
        print("-"*60 + "\n")

        import msvcrt
        import sys

        def cli_loop():
            print("\n[Dinleniyor... Konuşmak için AHK (Ctrl+A+F) kullanın veya konsoldayken ENTER'a basın]")
            line = ""
            while True:
                if msvcrt.kbhit():
                    char = msvcrt.getwch()
                    if char in ('\r', '\n'):
                        command_queue.put({"source": "cli", "cmd": line.strip()})
                        if line.strip().lower() in ["q", "exit", "quit"]:
                            break
                        line = ""
                    elif char == '\x08': # Backspace
                        line = line[:-1]
                        sys.stdout.write('\b \b')
                        sys.stdout.flush()
                    else:
                        line += char
                        sys.stdout.write(char)
                        sys.stdout.flush()
                else:
                    time.sleep(0.05)
        
        threading.Thread(target=cli_loop, daemon=True).start()

        # Ana Event Loop
        while True:
            try:
                # Kuyruktan tetikleme bekle
                item = command_queue.get()
                
                if item["source"] == "ahk":
                    self.listen_and_execute(duration=4)
                elif item["source"] == "cli":
                    cmd = item["cmd"]
                    if cmd.lower() in ["q", "exit", "quit"]:
                        self.voice.speak("Görüşürüz Kaptan, sistemleri kapatıyorum.")
                        break
                    elif cmd == "":
                        self.listen_and_execute(duration=4)
                    else:
                        intent = self.brain.process_command(cmd)
                        self.execute_intent(intent)
            except KeyboardInterrupt:
                print("\n[Jarvis] Kapatılıyor...")
                break
            except Exception as e:
                print(f"[Hata]: {e}")

if __name__ == "__main__":
    jarvis = JarvisAssistant()
    jarvis.run()
