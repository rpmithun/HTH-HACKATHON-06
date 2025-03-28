from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class TestHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"🔍 File Modified: {event.src_path}")

path = "C:\\Users\\rpmit\\Desktop\\ransomware_defense"

observer = Observer()
event_handler = TestHandler()
observer.schedule(event_handler, path=path, recursive=True)
observer.start()

print(f"🚀 Watching {path} for changes...")

try:
    while True:
        time.sleep(2)
except KeyboardInterrupt:
    observer.stop()
observer.join()

