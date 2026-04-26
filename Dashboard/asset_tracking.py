#Imports
import platform
import socket
import csv
import datetime
import subprocess

#Log and asset files
LOG_FILE = "asset_tracking_log.txt"
ASSET_FILE = "asset_registry.csv"

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def get_system_info():
    #System information gathering
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    os_info = platform.platform()
    return hostname, ip_address, os_info

def get_installed_software():
    #Uses powershell to list installed software on Windows
    try: 
        command = [
            "powershell",
            "-Command",
            "Get-ItemProperty HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\* | Select-Object DisplayName"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        software_list = result.stdout.split("\n")
        cleaned = [s.strip() for s in software_list if s.strip()]
        return "; ".join(cleaned)
    except Exception as e:
        log_event(f"Error retriveing software list: {e}")
        return "Error retrieving software"

def write_to_csv(hostname, ip, os_info, software):
    rows = []
    updated = False

    # Read existing records if file exists
    try:
        with open(ASSET_FILE, "r", newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
    except FileNotFoundError:
        rows = [["Hostname", "IP Address", "OS", "Installed Software"]]

    # Check if hostname already exists and update it
    for i in range(1, len(rows)):
        if rows[i][0] == hostname:
            rows[i] = [hostname, ip, os_info, software]
            updated = True
            log_event(f"Updated existing asset entry for {hostname}")
            break

    # If not found, append new device
    if not updated:
        rows.append([hostname, ip, os_info, software])
        log_event(f"Added new asset entry for {hostname}")

    # Write everything back to CSV
    with open(ASSET_FILE, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
        
def main():
    log_event("---Asset Tracking Module Started ---")
    hostname, ip , os_info = get_system_info()
    software = get_installed_software()
    write_to_csv(hostname, ip, os_info, software)
    log_event(f"Asset recorded: {hostname} | {ip}")
    log_event("---Asset Tracking Module Finished---\n")

if __name__ == "__main__":
    main()   
