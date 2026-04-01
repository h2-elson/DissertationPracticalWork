#imports
import subprocess
import datetime

#Log file path
LOG_FILE = "patch_management_log.txt"

def log_event(message):
    #Log message with timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def check_windows_updates():
    #Check for windows updates using powershell commands
    try:
        command = ["powershell", "-Command", "Get-WindowsUpdate"]
        result = subprocess.run(command, capture_output=True, text=True)
        log_event("Checked for updates successfully.")
        log_event(result.stdout)
        return True
    except Exception as e:
        log_event(f"Error checking for updates: {e}")
        return False

def install_windows_updates():
    #Install windows update (simulated)
    try:
        log_event("Simulating installation of updates")
        subprocess.run(["powershell", "-Command", "Install-WindowsUpdate -AcceptAll -IgnoreReboot"])
        log_event("All updates applied succesfully (simulated).")
        return True
    except Exception as e:
        log_event(f"Error installing updates: {e}")
        return False
    
def main():
    log_event("--- Patch Managment Module Started! ---")
    updates_checked = check_windows_updates()
    if updates_checked:
        install_windows_updates()
    log_event("--- Patch Management Module Finished ---\n")

if __name__ == "__main__":
    main()