#import
import os
import datetime
import csv

# Paths to all module logs
MODULE_LOGS = [
    "patch_management_log.txt",
    "asset_tracking_log.txt",
    "malware_monitor_log.txt",
    "backup_log.txt",
    "access_control_log.txt"
]

CENTRAL_LOG_CSV = "central_incident_log.csv"

def read_module_logs():
    incidents = []
    for log_file in MODULE_LOGS:
        if not os.path.exists(log_file):
            continue
        with open(log_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:  # skip empty lines
                    incidents.append((datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                      os.path.basename(log_file),
                                      line))
    return incidents

def write_central_log(incidents):
    file_exists = os.path.exists(CENTRAL_LOG_CSV)
    with open(CENTRAL_LOG_CSV, "a", newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Timestamp", "Module", "Message"])
        for incident in incidents:
            writer.writerow(incident)

def main():
    incidents = read_module_logs()
    write_central_log(incidents)
    print(f"Aggregated {len(incidents)} log entries into {CENTRAL_LOG_CSV}")

if __name__ == "__main__":
    main()