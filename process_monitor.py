import psutil
import time
import auto_isolation

suspicious_processes = ["wannacry.exe", "notpetya.exe", "locky.exe", "ransomware.exe"]
LOG_FILE = "ransomware_log.txt"

def log_event(message):
    """Log activity to a file."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{message}\n")

def check_processes():
    """Check running processes for ransomware activity."""
    for process in psutil.process_iter(attrs=["pid", "name"]):
        try:
            process_name = process.info["name"].lower()
            if process_name in suspicious_processes:
                pid = process.info["pid"]
                alert_message = f"🚨 Ransomware process detected: {process_name} (PID: {pid})"
                print(alert_message)
                log_event(alert_message)

                psutil.Process(pid).terminate()
                termination_message = f"✅ Terminated: {process_name} (PID: {pid})"
                print(termination_message)
                log_event(termination_message)

                auto_isolation.isolate_network()
                log_event("🚨 Network Isolated due to ransomware detection.")

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
