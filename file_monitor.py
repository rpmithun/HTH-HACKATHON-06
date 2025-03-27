from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import psutil
import logging
import shutil

# 🚀 Set up logging
LOG_FILE = "ransomware_alerts.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

print("🚀 File Monitor is Running... Watching for ransomware activity.")

# 🚨 Define suspicious ransomware extensions
ransomware_extensions = [".encrypted", ".locked", ".wnry", ".locky", ".cry"]
suspicious_processes = ["vssadmin.exe", "wmic.exe", "cipher.exe"]  # Known ransomware tools

# 🛡️ Protect critical directories
watched_dir = "C:\\Users\\rpmit\\Desktop\\ransomware_defense"
backup_dir = "C:\\Users\\rpmit\\Desktop\\backup"

# Ensure backup directory exists
if not os.path.exists(backup_dir):
    os.makedirs(backup_dir)

class RansomwareDetector(FileSystemEventHandler):
    def on_moved(self, event):
        """Detects file renames, checking for ransomware extensions."""
        if event.is_directory:
            return

        for ext in ransomware_extensions:
            if event.dest_path.endswith(ext):  # Check if renamed file has ransomware extension
                print(f"🔍 File Changed: {event.src_path} → {event.dest_path}")
                print(f"⚠️ WARNING: Potential ransomware activity detected!")
                
                # Log event
                logging.info(f"⚠️ WARNING: {event.src_path} renamed to {event.dest_path}")

                # 🚨 Kill suspicious processes
                self.terminate_ransomware()

                # 🔄 Restore the original file (if possible)
                self.restore_file(event.src_path)

    def terminate_ransomware(self):
        """Kills processes commonly used by ransomware."""
        for process in psutil.process_iter():
            try:
                if process.name().lower() in suspicious_processes:
                    print(f"🚨 Killing ransomware process: {process.name()}")
                    process.terminate()
                    logging.info(f"🚨 Terminated: {process.name()}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    def restore_file(self, file_path):
        """Restores files from backup if they are modified by ransomware."""
        original_filename = os.path.basename(file_path)
        backup_path = os.path.join(backup_dir, original_filename)

        if os.path.exists(backup_path):
            shutil.copy2(backup_path, file_path)
            print(f"✅ Restored {file_path} from backup.")
            logging.info(f"✅ Restored {file_path} from backup.")
        else:
            print(f"⚠️ No backup found for {file_path}.")
            logging.warning(f"⚠️ No backup found for {file_path}.")

# Start monitoring
watcher = Observer()
handler = RansomwareDetector()
watcher.schedule(handler, path=watched_dir, recursive=True)

watcher.start()

try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    watcher.stop()
watcher.join()
