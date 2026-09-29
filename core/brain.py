import requests
import json
import re

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

class JarvisBrain:
    def __init__(self, model_name="jarvis"):
        self.model_name = model_name

    def _tr_lower(self, text: str):
        return text.replace("I", "ı").replace("İ", "i").lower()

    def process_command(self, user_text: str):
        """Kullanıcının metnini analiz edip eylem mi yoksa sohbet/oyun tavsiyesi mi olduğuna karar verir."""
        import string
        import re
        
        clean_text = self._tr_lower(user_text).strip()
        # Noktalama işaretlerini temizle (virgül vb. komutları bozmasın diye)
        for p in string.punctuation:
            clean_text = clean_text.replace(p, "")

        # 1. Hizli kural tabanli filtreler (Zero Latency Eylemler)
        if any(w in clean_text for w in ["yaz", "yazdır", "yazar mısın"]) and not any(w in clean_text for w in ["ekranda", "oyunda", "burada", "ne var", "görüyorsun"]):
            text_to_type = re.sub(r'(?i)\b(yaz|yazdır|yazar mısın)\b', '', user_text).strip()
            # Başındaki noktalama veya gereksiz boşlukları temizle
            text_to_type = text_to_type.strip(".,;:?! ")
            if text_to_type:
                return {"type": "action", "skill": "system", "action": "type_text", "text": text_to_type}

        if any(w in clean_text for w in ["sesi kıs", "sesi azalt", "sesi düsür"]):
            return {"type": "action", "skill": "system", "action": "volume_down"}
        
        if any(w in clean_text for w in ["sesi aç", "sesi yükselt", "sesi artır", "sesi fulle", "sesi fülle", "yüze çıkar", "yüz yap", "maximuma çıkar"]):
            return {"type": "action", "skill": "system", "action": "volume_up"}
        
        if any(w in clean_text for w in ["sesi kapat", "sustur", "mute"]):
            return {"type": "action", "skill": "system", "action": "mute"}
        
        if any(w in clean_text for w in ["sesi geri aç", "unmute", "sesi ver"]):
            return {"type": "action", "skill": "system", "action": "unmute"}

        if any(w in clean_text for w in ["masaüstünü göster", "pencereleri küçült", "pencereleri kapat"]):
            return {"type": "action", "skill": "system", "action": "minimize_all"}

        if any(w in clean_text for w in ["müzik kapat", "müziği kapat", "şarkıyı kapat", "şarkı kapat", "winamp kapat", "müziği durdur"]):
            return {"type": "action", "skill": "winamp", "action": "close_music"}

        if any(w in clean_text for w in ["film", "video", "filmi aç", "videoyu aç"]):
            # Extract video query
            words_to_remove = ["filmini", "filmi", "aç", "videoyu", "video", "oynat", "başlat", "izle", "film"]
            query = clean_text
            for w in words_to_remove:
                query = query.replace(w, "")
            query = query.strip()
            return {"type": "action", "skill": "media", "action": "play_video", "query": query}

        if any(w in clean_text for w in ["şarkı", "müzik", "playlist", "çal", "winamp"]):
            mood = clean_text.replace("şarkı çal", "").replace("müzik çal", "").replace("playlist yap", "").replace("winamp", "").strip()
            return {"type": "action", "skill": "winamp", "action": "play_music", "mood": mood or "general"}
            
        if any(w in clean_text for w in ["ekranda", "ekranımda", "görüyorsun", "oyunda", "burada ne yapmam", "ne var", "şu an ne"]):
            return {"type": "action", "skill": "vision", "action": "analyze_screen", "query": user_text}

        # 2. Oyun Tavsiyesi / Sohbet / Strateji (Yerel LLM'e Gönder)
        return {"type": "chat", "prompt": user_text}

    def ask_llm(self, prompt: str) -> str:
        """Yerel Ollama modeline sorgu gönderir ve yanıt alır."""
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }
        try:
            resp = requests.post(OLLAMA_URL, json=payload, timeout=60)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("response", "Kafam biraz karıştı patron, tekrar söyler misin?")
            else:
                return f"Hata aldım patron: {resp.text}"
        except Exception as e:
            return f"Yerel beynime ulaşılamadı: {str(e)}"

if __name__ == "__main__":
    brain = JarvisBrain()
    res = brain.process_command("dövüş oyunu için hızlı şarkılar çal")
    print("Test intent:", res)
