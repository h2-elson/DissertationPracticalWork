#imports
import os
import shutil
import datetime

LOG_FILE = "backup_log.txt"
SOURCE_FOLDER = "\\Users\\Harry\\DissertationPracticalWork\\test\\critical_files"
BACKUP_FOLDER = "\\Users\\Harry\\DissertationPracticalWork\\test\\backup_files"

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def ensure_folders():
    for folder in [SOURCE_FOLDER, BACKUP_FOLDER]:
        if not os.path.exists(folder):
            os.makedirs(folder)
            log_event(f"Created folder: {folder}")

def backup_files():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")
    try:
        shutil.copytree(SOURCE_FOLDER, destination)
        log_event(f"Backup completed successfully to {destination}")
        return True
    except Exception as e:
        log_event(f"Error during backup: {e}")
        return False

def main():
    log_event("=== Backup Automation Module Started ===")
    ensure_folders()
    backup_files()
    log_event("=== Backup Automation Module Finished ===\n")

if __name__ == "__main__":
    main()