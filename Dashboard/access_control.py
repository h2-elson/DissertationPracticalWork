# imports
import datetime
import csv
import os
import sys

LOG_FILE = "access_control_log.txt"

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


def enforce_access_controls(user_file):
    if not os.path.exists(user_file):
        log_event(f"User file {user_file} not found.")
        return

    log_event(f"Checking users from: {user_file}\n")

    with open(user_file, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            username = row["username"]
            password = row["password"]

            strong = evaluate_password_strength(password)

            if strong:
                log_event(f"Password for '{username}' meets policy.")
            else:
                log_event(f"Password for '{username}' FAILED policy. Action required.")


def main(user_file):
    log_event("=== Access Control Module Started ===")
    enforce_access_controls(user_file)
    log_event("=== Access Control Module Finished ===\n")


# Allows file path to be passed from the dashboard GUI
if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("No user CSV file provided.")