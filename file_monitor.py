import hashlib
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 📂 Path to watch
WATCHED_FOLDER = "C:\\Users\\rpmit\\Desktop\\ransomware_defense"
LOG_FILE = "ransomware_log.txt"

# 🔍 Dictionary to store file hashes
file_hashes = {}

def write_log(message):
    """Write a message to the log file with a timestamp."""
    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def get_file_hash(file_path):
    """Generate SHA-256 hash for a given file."""
    try:
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return None

class RansomwareDetector(FileSystemEventHandler):
    """Detects ransomware activity by monitoring file changes."""

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = event.src_path

        # 🚨 Ignore modifications to the log file and script files
        if os.path.basename(file_path) in [LOG_FILE, "file_monitor.py"]:
            return

        new_hash = get_file_hash(file_path)

        if new_hash:
            if file_path in file_hashes and file_hashes[file_path] != new_hash:
                alert_msg = f"⚠️ WARNING: Potential ransomware activity detected! {file_path}"
                print(alert_msg)
                write_log(alert_msg)

            file_hashes[file_path] = new_hash

    def on_created(self, event):
        if not event.is_directory:
            alert_msg = f"📁 New File Created: {event.src_path}"
            print(alert_msg)
            write_log(alert_msg)
            file_hashes[event.src_path] = get_file_hash(event.src_path)

    def on_moved(self, event):
        """Handles file renaming events."""
        alert_msg = f"🔁 File Renamed: {event.src_path} → {event.dest_path}"
        print(alert_msg)
        write_log(alert_msg)

        # Remove old file hash if exists
        if event.src_path in file_hashes:
            del file_hashes[event.src_path]

        # Add new file hash
        if event.dest_path:
            file_hashes[event.dest_path] = get_file_hash(event.dest_path)

def initialize_hashes():
    """Preload existing file hashes to track changes over time."""
    for root, _, files in os.walk(WATCHED_FOLDER):
        for file in files:
            file_path = os.path.join(root, file)
            file_hashes[file_path] = get_file_hash(file_path)

def start_monitoring():
    """Starts the watchdog file monitoring process."""
    initialize_hashes()
    watcher = Observer()
    handler = RansomwareDetector()
    watcher.schedule(handler, path=WATCHED_FOLDER, recursive=True)
    watcher.start()

    print("🔍 Watchdog is running. Waiting for file changes...")

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("🛑 File monitoring stopped.")
        watcher.stop()
