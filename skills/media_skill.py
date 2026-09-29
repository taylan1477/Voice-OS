import os
import subprocess
from pathlib import Path

VIDEO_EXTENSIONS = {".mkv", ".mp4", ".avi", ".mov", ".flv", ".wmv"}

class MediaSkill:
    def __init__(self):
        self.search_dirs = [
            os.path.expanduser(r"~\Desktop"),
            os.path.expanduser(r"~\Downloads"),
            os.path.expanduser(r"~\Videos"),
            r"C:\Users\taycore\Desktop\Prospecting\to watch"
        ]

    def find_and_play_video(self, query=None):
        """Masaüstü veya İndirilenler klasöründeki videoları bulur ve oynatır."""
        candidates = []
        
        for search_dir in self.search_dirs:
            if not os.path.exists(search_dir):
                continue
            for root, _, files in os.walk(search_dir):
                for file in files:
                    ext = Path(file).suffix.lower()
                    if ext in VIDEO_EXTENSIONS:
                        full_path = os.path.join(root, file)
                        try:
                            mtime = os.path.getmtime(full_path)
                            candidates.append({
                                "path": full_path,
                                "name": file,
                                "stem": Path(file).stem.lower(),
                                "mtime": mtime
                            })
                        except Exception:
                            pass
                # Don't recurse too deep in Desktop/Downloads
                if root != search_dir:
                    break

        if not candidates:
            return False, "Masaüstünde veya İndirilenler klasöründe herhangi bir video veya film bulunamadı patron."

        # Sort by modification time (most recent first)
        candidates.sort(key=lambda x: x["mtime"], reverse=True)

        import re
        def normalize(text):
            return re.sub(r'[^a-z0-9]', '', text.lower())
            
        target = None
        if query:
            q = query.lower()
            # 1. Exact match attempt
            for c in candidates:
                if q in c["stem"]:
                    target = c
                    break
            
            # 2. Fuzzy match attempt
            if not target:
                query_words = set(q.split())
                for c in candidates:
                    norm_stem = normalize(c["stem"])
                    if any(normalize(w) in norm_stem for w in query_words if len(normalize(w)) > 3):
                        target = c
                        break

        # Fallback to the latest video
        if not target:
            target = candidates[0]

        print(f"[MediaSkill] Video baslatiliyor: {target['path']}")
        
        # Open with default Windows video player
        os.startfile(target["path"])
        return True, f"'{target['name']}' filmini başlattım patron, iyi seyirler!"

if __name__ == "__main__":
    skill = MediaSkill()
    print("MediaSkill test hazır.")
