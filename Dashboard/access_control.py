#imports
import datetime
import csv
import os

LOG_FILE = "access_control_log.txt"
USER_FILE = "users.csv"  # Sample CSV with users: username,last_login,password_strength

# Password policy settings
MIN_PASSWORD_LENGTH = 8
REQUIRE_NUMERIC = True

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def evaluate_password_strength(password):
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    if REQUIRE_NUMERIC and not any(char.isdigit() for char in password):
        return False
    return True

def enforce_access_controls():
    if not os.path.exists(USER_FILE):
        log_event(f"User file {USER_FILE} not found. Creating sample file.")
        with open(USER_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "last_login", "password"])
            writer.writerow(["alice", "2026-03-25", "pass123"])  # weak
            writer.writerow(["bob", "2026-03-28", "StrongPass1"])  # strong

    updated_users = []
    with open(USER_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row["username"]
            password = row["password"]
            strong = evaluate_password_strength(password)
            if strong:
                log_event(f"Password for {username} meets policy.")
            else:
                log_event(f"Password for {username} FAILED policy. Action required.")
            updated_users.append(row)
    # Optionally: could disable users who fail policies here
    return updated_users

def main():
    log_event("=== Access Control Module Started ===")
    enforce_access_controls()
    log_event("=== Access Control Module Finished ===\n")

if __name__ == "__main__":
    main()