from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

print("🚀 File Monitor is Running... Watching for ransomware activity.")

ransomware_extensions = [".encrypted", ".locked", ".wnry", ".locky", ".cry"]

class RansomwareDetector(FileSystemEventHandler):
    def on_moved(self, event):
        """Detects file renames, checking for ransomware extensions."""
        if event.is_directory:
            return
        for ext in ransomware_extensions:
            if event.dest_path.endswith(ext):  # Check the new filename
                print(f"🔍 File Changed: {event.src_path} → {event.dest_path}")
                print(f"⚠️ WARNING: Potential ransomware activity detected!")

watcher = Observer()
handler = RansomwareDetector()
watcher.schedule(handler, path="C:\\Users\\rpmit\\Desktop\\ransomware_defense", recursive=True)

watcher.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    watcher.stop()
watcher.join()
