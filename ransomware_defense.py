import os
import time
import psutil
import logging
import auto_isolation
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 📌 Configure logging
logging.basicConfig(filename="ransomware_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

# 📌 Suspicious process names
SUSPICIOUS_PROCESSES = ["wannacry.exe", "locky.exe", "bad_ransomware.exe", "notpetya.exe"]

# 📌 Folder to monitor for file changes
WATCHED_DIRECTORY = "C:\\Users\\rpmit\\Desktop\\ransomware_defense"

# 🔥 CUSTOM ASCII BANNER
ASCII_BANNER = """
     _______ _______  ______ _______ _____ __   _ _______ _______  _____   ______
        |    |______ |_____/ |  |  |   |   | \  | |_____|    |    |     | |_____/
        |    |______ |    \_ |  |  | __|__ |  \_| |     |    |    |_____| |    \_

"""
def monitor_processes():
    """ Continuously scans for suspicious processes and terminates them. """
    print("\n🔍 Monitoring processes for ransomware threats...")
    print("\n[Press 'B' to go back to the menu]\n")
    
    while True:
        user_input = input("").strip().lower()
        if user_input == "b":
            print("\n🔙 Returning to main menu...\n")
            break

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_name = proc.info['name'].lower()
                if process_name in SUSPICIOUS_PROCESSES:
                    print(f"\n🚨 Detected Suspicious Process: {process_name} (PID: {proc.pid})")
                    proc.kill()
                    print(f"✅ Process {process_name} terminated!")

                    # 🛑 Trigger Auto-Isolation Immediately
                    print("\n⚠️ Initiating Network Isolation!")
                    logging.info(f"Suspicious process {process_name} detected and terminated. Network isolated.")
                    auto_isolation.isolate_network()
                    return
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        time.sleep(2)

class RansomwareMonitor(FileSystemEventHandler):
    """ Watches for file modifications indicating ransomware activity. """
    
    def on_modified(self, event):
        if not event.is_directory:
            print(f"\n🚨 File Modified: {event.src_path}")
            logging.info(f"File modification detected: {event.src_path}")
            
            # 🚨 Auto-Isolation Trigger
            print("⚠️ Possible ransomware detected! Isolating system...")
            auto_isolation.isolate_network()
            return

def monitor_files():
    """ Watches a folder for suspicious file modifications. """
    print(f"\n📂 Monitoring {WATCHED_DIRECTORY} for unauthorized file changes...")
    print("\n[Press 'B' to go back to the menu]\n")

    observer = Observer()
    event_handler = RansomwareMonitor()
    observer.schedule(event_handler, WATCHED_DIRECTORY, recursive=True)
    observer.start()

    while True:
        user_input = input("").strip().lower()
        if user_input == "b":
            print("\n🔙 Returning to main menu...\n")
            observer.stop()
            break
        
    observer.join()

def main():
    print(ASCII_BANNER)  # Show Custom ASCII Banner
    while True:
        print("""
        🔥 Ransomware Defense Toolkit 🔥
        ---------------------------------
        1️⃣ Monitor File Changes
        2️⃣ Monitor & Kill Suspicious Processes
        3️⃣ Auto-Isolate System
        4️⃣ Restore Network
        5️⃣ Exit
        """)

        choice = input("🔹 Select an option: ").strip()
        
        if choice == "1":
            monitor_files()

        elif choice == "2":
            monitor_processes()

        elif choice == "3":
            print("\n🚀 Auto-Isolation Mode Activated...\n")
            auto_isolation.isolate_network()

        elif choice == "4":
            print("\n🔄 Restoring Network...\n")
            auto_isolation.restore_network()

        elif choice == "5":
            print("👋 Hasta la vista, baby!")
            break

        else:
            print("⚠️ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
