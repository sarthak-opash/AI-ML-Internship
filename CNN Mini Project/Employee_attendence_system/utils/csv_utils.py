import csv
import os
from datetime import datetime

CSV_FILE = "Attendence/attendance.csv"


def mark_attendance(emp_id, emp_name):
    today = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")

    file_exists = os.path.isfile(CSV_FILE)

    # Check duplicate for same day
    if file_exists:
        with open(CSV_FILE, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and str(row[0]) == str(emp_id) and row[2] == today:
                    print(f"Attendance already marked for {emp_name} today.")
                    return

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["Emp_ID", "Name", "Date", "Time"])

        writer.writerow([emp_id, emp_name, today, time_now])

    print(f"Attendance Marked for {emp_name}")