# imports
import os
import shutil
import datetime
import sys

LOG_FILE = "backup_log.txt"


def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


def backup_files(source_folder, backup_folder):
    if not os.path.exists(source_folder):
        log_event(f"Source folder does not exist: {source_folder}")
        return

    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
        log_event(f"Created backup folder: {backup_folder}")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    destination = os.path.join(backup_folder, f"backup_{timestamp}")

    try:
        shutil.copytree(source_folder, destination)
        log_event(f"Backup completed successfully to: {destination}")
    except Exception as e:
        log_event(f"Error during backup: {e}")


def main(source_folder, backup_folder):
    log_event("=== Backup Automation Module Started ===")
    backup_files(source_folder, backup_folder)
    log_event("=== Backup Automation Module Finished ===\n")


# Accept paths from dashboard
if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Source and backup folders not provided.")