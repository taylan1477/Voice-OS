import base64
import requests
import pyautogui
import os
from io import BytesIO

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

class VisionSkill:
    def __init__(self, model_name="llava"):
        self.model_name = model_name

    def analyze_screen(self, query: str) -> tuple[bool, str]:
        """Ekran görüntüsü alır ve vizyon modeli ile analiz eder."""
        try:
            # Ekran görüntüsü al ve diske kaydet (debug için)
            screenshot = pyautogui.screenshot()
            screenshot.save("last_vision.jpg", format="JPEG")
            
            # Bellekte kaydet ve base64'e çevir
            buffered = BytesIO()
            screenshot.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
            
            payload = {
                "model": self.model_name,
                "prompt": f"Briefly describe what is happening on this computer screen in one short English sentence. If there is a large logo, text, or specific program visible, mention its name exactly.",
                "images": [img_str],
                "stream": False
            }
            
            resp = requests.post(OLLAMA_URL, json=payload, timeout=90)
            if resp.status_code == 200:
                eng_desc = resp.json().get("response", "")
                
                # Çeviri için Jarvis'i (Qwen) kullan
                trans_payload = {
                    "model": "jarvis",
                    "prompt": f"Şu İngilizce ekran betimlemesini bağlama en uygun kelimeleri seçerek (örneğin cover kelimesini kapı değil kapak olarak), çok doğal ve profesyonel bir Türkçe ile tek cümle halinde çevir. Ekstra hiçbir yorum yapma: '{eng_desc}'",
                    "stream": False
                }
                t_resp = requests.post(OLLAMA_URL, json=trans_payload, timeout=60)
                if t_resp.status_code == 200:
                    reply = t_resp.json().get("response", "Ekranı analiz edemedim.")
                    return True, reply
                else:
                    return False, "Çeviri merkezimde sorun var."
            else:
                return False, f"Görme merkezimde bir sorun var: {resp.text}"
                
        except Exception as e:
            return False, f"Ekranına bakamadım Kaptan: {str(e)}"
