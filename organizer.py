import os
import time
from pathlib import Path
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Replace with your custom downloads folder path if different
WATCH_DIR = Path.home() / "Downloads"

EXTENSION_MAP = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
    "Installers": [".dmg", ".pkg", ".exe", ".msi", ".deb"],
    "Code": [".py", ".cs", ".js", ".html", ".css", ".json", ".xml"],
    "Media": [".mp3", ".wav", ".mp4", ".mkv", ".avi", ".mov"],
}

class DownloadOrganizerHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Ignore directory modifications
        if event.is_directory:
            return
        
        self.organize_folder()

    def organize_folder(self):
        for item in WATCH_DIR.iterdir():
            if item.is_dir() or item.name.startswith("."):
                continue

            # Ignore incomplete downloads (e.g., .crdownload, .tmp, .part)
            if item.suffix in [".crdownload", ".tmp", ".part"]:
                continue

            destination_folder = self.get_destination_folder(item.suffix.lower())
            
            if destination_folder:
                target_dir = WATCH_DIR / destination_folder
                target_dir.mkdir(exist_ok=True)
                
                target_path = target_dir / item.name
                
                counter = 1
                while target_path.exists():
                    target_path = target_dir / f"{item.stem}_{counter}{item.suffix}"
                    counter += 1

                try:
                    time.sleep(0.5)
                    shutil.move(str(item), str(target_path))
                    print(f"[MOVED] {item.name} -> {destination_folder}/")
                except Exception as e:
                    print(f"[ERROR] Failed to move {item.name}: {e}")

    def get_destination_folder(self, extension):
        for category, extensions in EXTENSION_MAP.items():
            if extension in extensions:
                return category
        return "Other"  # Fallback folder if extension isn't listed

if __name__ == "__main__":
    print(f"Monitoring started for directory: {WATCH_DIR}")
    event_handler = DownloadOrganizerHandler()
    event_handler.organize_folder()

    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nMonitoring stopped.")

    observer.join()