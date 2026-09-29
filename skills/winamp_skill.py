import os
import json
import subprocess
from pathlib import Path
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

MUSIC_DIR = r"C:\Users\taycore\Music"
WINAMP_EXE = r"C:\Program Files (x86)\Winamp\winamp.exe"
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "music_index.json")

class WinampSkill:
    def __init__(self, music_dir=MUSIC_DIR, winamp_path=WINAMP_EXE):
        self.music_dir = music_dir
        self.winamp_path = winamp_path
        self.library = []
        self.load_or_build_index()

    def build_index(self):
        """1600+ MP3 dosyasini tarayip ID3 etiketlerini cikarir."""
        print(f"[WinampSkill] '{self.music_dir}' taraniyor...")
        songs = []
        
        for root, _, files in os.walk(self.music_dir):
            for file in files:
                if file.lower().endswith(".mp3"):
                    full_path = os.path.join(root, file)
                    title = Path(file).stem
                    artist = "Unknown"
                    genre = "Unknown"
                    
                    try:
                        audio = MP3(full_path, ID3=EasyID3)
                        if "title" in audio:
                            title = audio["title"][0]
                        if "artist" in audio:
                            artist = audio["artist"][0]
                        if "genre" in audio:
                            genre = audio["genre"][0]
                    except Exception:
                        pass
                    
                    songs.append({
                        "path": full_path,
                        "filename": file,
                        "title": title,
                        "artist": artist,
                        "genre": genre
                    })
        
        self.library = songs
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(songs, f, ensure_ascii=False, indent=2)
        print(f"[WinampSkill] Toplam {len(songs)} sarki indekslendi ve kaydedildi.")
        return songs

    def load_or_build_index(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    self.library = json.load(f)
                    print(f"[WinampSkill] Onbellekten {len(self.library)} sarki yuklendi.")
                    return
            except Exception:
                pass
        self.build_index()

    def create_playlist_and_play(self, mood_keywords=None, count=30, playlist_name="jarvis_playlist.m3u"):
        """Istenen moda uygun sarkilardan M3U playlisti olusturup Winamp'ta acar."""
        if not self.library:
            self.build_index()

        selected_songs = []
        
        if mood_keywords:
            if isinstance(mood_keywords, str):
                keywords = [k.strip().lower() for k in mood_keywords.split(",")]
            else:
                keywords = [k.lower() for k in mood_keywords]
                
            # Filter matches
            for song in self.library:
                search_space = f"{song['title']} {song['artist']} {song['genre']} {song['filename']}".lower()
                if any(kw in search_space for kw in keywords):
                    selected_songs.append(song)
        
        # If not enough matches or no keyword, pick random sample from library
        import random
        if len(selected_songs) < count:
            remaining = [s for s in self.library if s not in selected_songs]
            random.shuffle(remaining)
            selected_songs.extend(remaining[:count - len(selected_songs)])
        else:
            selected_songs = selected_songs[:count]

        # Write .m3u playlist
        playlist_path = os.path.join(self.music_dir, playlist_name)
        with open(playlist_path, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for song in selected_songs:
                f.write(f"#EXTINF:-1,{song['artist']} - {song['title']}\n")
                f.write(f"{song['path']}\n")
                
        print(f"[WinampSkill] {len(selected_songs)} sarkilik playlist hazirlandi: {playlist_path}")
        
        # Launch Winamp
        if os.path.exists(self.winamp_path):
            subprocess.Popen([self.winamp_path, playlist_path])
            return True, f"{len(selected_songs)} parçalık çalma listesi hazırlandı ve Winamp'ta başlatıldı patron!"
        else:
            # Fallback to default player
            os.startfile(playlist_path)
            return True, f"{len(selected_songs)} parçalık çalma listesi başlatıldı!"

    def close_music(self):
        try:
            subprocess.run(["taskkill", "/IM", "winamp.exe", "/F"], capture_output=True)
            return True, "Müziği kapattım patron."
        except Exception as e:
            return False, "Winamp kapatılamadı."

if __name__ == "__main__":
    skill = WinampSkill()
    print("Test: Indeksleme basarili.")
