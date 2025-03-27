import psutil
import logging
import time
import os

# 🚀 Set up logging
LOG_FILE = "ransomware_alerts.log"
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

print("🚀 Process Monitor is Running... Watching for ransomware activity.")

# 🚨 Define suspicious ransomware processes
suspicious_processes = [
    "vssadmin.exe",  # Used to delete Windows Shadow Copies
    "wmic.exe",      # Can delete backups
    "cipher.exe",    # Can encrypt/wipe files
    "taskkill.exe",  # Some ransomware kills security software
    "powershell.exe" # If running suspicious scripts
]

def detect_ransomware_processes():
    """Scans running processes and terminates any that match ransomware signatures."""
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            process_name = process.info['name'].lower()
            process_id = process.info['pid']

            if process_name in suspicious_processes:
                print(f"🚨 Ransomware process detected: {process_name} (PID: {process_id})")
                logging.info(f"🚨 Ransomware process detected: {process_name} (PID: {process_id})")
                
                # Kill process
                os.system(f"taskkill /PID {process_id} /F")
                print(f"✅ Terminated: {process_name} (PID: {process_id})")
                logging.info(f"✅ Terminated: {process_name} (PID: {process_id})")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Continuous monitoring loop
try:
    while True:
        detect_ransomware_processes()
        time.sleep(5)  # Adjust scanning frequency
except KeyboardInterrupt:
    print("🛑 Process Monitor Stopped.")
