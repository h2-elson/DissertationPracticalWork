import sys
import tkinter as tk
from tkinter import scrolledtext, filedialog
import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#Default run scripts
def run_script(script_name, args=None):
    output_box.delete(1.0, tk.END)

    command = ["python", os.path.join(BASE_DIR, script_name)]
    if args:
        command.extend(args)

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate()
    output_box.insert(tk.END, stdout)
    if stderr:
        output_box.insert(tk.END, "\nERROR:\n" + stderr)


#Run asset registry (create csv and output)
def show_asset_registry():
    run_script("asset_tracking.py")
    csv_path = os.path.join(BASE_DIR, "asset_registry.csv")

    if os.path.exists(csv_path):
        output_box.insert(tk.END, "\n\n=== Asset Registry ===\n\n")
        with open(csv_path) as f:
            for line in f:
                output_box.insert(tk.END, line)


#Access control (open csv)
def run_access_control():
    file_path = filedialog.askopenfilename(
        title="Select users CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    if file_path:
        run_script("access_control.py", [file_path])

#Run malware monitoring (open folder to monitor)
def run_malware_monitor():
    folder = filedialog.askdirectory(title="Select Folder to Scan")

    if not folder:
        return

    script_path = os.path.abspath("malware_monitoring.py")

    result = subprocess.run(
        ["python", script_path, folder],
        capture_output=True,
        text=True
    )

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, result.stdout)
    output_box.insert(tk.END, result.stderr)

    output_box.insert(tk.END, "\n✔ Malware scan completed\n")

#create incident log, (output log)
def show_incident_log():
    run_script("incident_logging.py")
    csv_path = os.path.join(BASE_DIR, "central_incident_log.csv")

    if os.path.exists(csv_path):
        output_box.insert(tk.END, "\n\n=== Central Incident Log ===\n\n")
        with open(csv_path) as f:
            for line in f:
                output_box.insert(tk.END, line)

def create_backup_bat(source, destination):
    script_path = os.path.abspath("backup_automation.py")
    bat_path = os.path.join(BASE_DIR, "run_backup_task.bat")

    python_exe = sys.executable

    with open(bat_path, "w") as f:
        f.write(f'"{python_exe}" "{script_path}" "{source}" "{destination}"\n')

    return bat_path

#Backup automation (select folder, select backup destination)
def run_backup_automation():
    source = filedialog.askdirectory(title="Select Source Folder")
    if not source:
        return

    destination = filedialog.askdirectory(title="Select Destination Folder")
    if not destination:
        return

    script_path = os.path.abspath("backup_automation.py")

    python_exe = sys.executable

    task_name = "SME_Backup_Automation"

    command = [
    "schtasks",
    "/create",
    "/sc", "daily",
    "/tn", task_name,
    "/tr", f'cmd /c cd /d "{BASE_DIR}" && "{sys.executable}" backup_automation.py "{source}" "{destination}"',
    "/st", "02:00",
    "/f"
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    run_command = ["schtasks", "/run", "/tn", task_name]
    run_result = subprocess.run(run_command, capture_output=True, text=True)

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "STDOUT:\n" + result.stdout + "\n\n")
    output_box.insert(tk.END, "STDERR:\n" + result.stderr + "\n\n")

    output_box.insert(tk.END, "=== Immediate Execution ===\n")
    output_box.insert(tk.END, run_result.stdout + "\n" + run_result.stderr + "\n")

    if result.returncode == 0:
        output_box.insert(tk.END, "✔ Task created successfully\n")
    else:
        output_box.insert(tk.END, "❌ Task creation failed\n")

#Patch management 
def run_patch_management():
    command = (
        "powershell -Command "
        "\"Start-Process powershell -Verb RunAs -ArgumentList "
        "'-ExecutionPolicy Bypass -Command Install-WindowsUpdate -AcceptAll -IgnoreReboot'\""
    )

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, result.stdout)
    output_box.insert(tk.END, result.stderr)

window = tk.Tk()
window.title("SME Cybersecurity Dashboard")
window.geometry("850x600")
window.configure(bg="#f4f6f8")

title = tk.Label(
    window,
    text="SME Cybersecurity Dashboard",
    font=("Segoe UI", 22, "bold"),
    bg="#f4f6f8",
    fg="#2c3e50"
)
title.pack(pady=15)

subtitle = tk.Label(
    window,
    text="Practical Security Controls for Small & Medium Enterprises",
    font=("Segoe UI", 11),
    bg="#f4f6f8",
    fg="#555"
)
subtitle.pack(pady=5)


#Buttons

button_frame = tk.Frame(window, bg="#f4f6f8")
button_frame.pack(pady=15)

button_style = {
    "font": ("Segoe UI", 11),
    "width": 30,
    "height": 2,
    "bg": "#3498db",
    "fg": "white",
    "bd": 0,
    "activebackground": "#2980b9"
}

tk.Button(button_frame, text="Asset Tracking", command=show_asset_registry, **button_style).grid(row=0, column=0, padx=10, pady=8)
tk.Button(button_frame, text="Access Control Audit", command=run_access_control, **button_style).grid(row=1, column=0, padx=10, pady=8)
tk.Button(button_frame, text="Malware Monitoring", command=run_malware_monitor, **button_style).grid(row=2, column=0, padx=10, pady=8)
tk.Button(button_frame, text="Incident Logging Report", command=show_incident_log, **button_style).grid(row=3, column=0, padx=10, pady=8)
tk.Button(button_frame, text="Backup Automation", command=run_backup_automation, **button_style).grid(row=4, column=0, padx=10, pady=8)
tk.Button(button_frame, text="Patch Management", command=run_patch_management, **button_style).grid(row=5, column=0, padx=10, pady=8)


#Output

output_box = scrolledtext.ScrolledText(
    window,
    width=150,
    height=30,
    font=("Consolas", 10),
    bg="#ffffff",
    fg="#2c3e50",
    borderwidth=1
)
output_box.pack(pady=20, padx=20)

window.mainloop()