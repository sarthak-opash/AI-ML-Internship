
import csv
import os
from datetime import datetime

CSV_FILE = "Attendence/attendance.csv"


def mark_attendance(emp_id, emp_name):
    today = datetime.now().strftime("%d-%m-%y")
    time_now = datetime.now().strftime("%H:%M:%S")
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    rows = []
    header = ["Emp_ID", "Name", "Date", "In", "Out", "Total Time"]
    found = False

    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "r", newline="") as f:
            reader = list(csv.reader(f))
            if reader:
                rows = reader[1:]

    for row in rows:
        if len(row) >= 3 and str(row[0]) == str(emp_id) and row[2] == today:
            found = True
            if row[4] == "-":
                row[4] = time_now
                row[5] = calculate_total_time(row[3], row[4])
            break

    if not found:
        rows.append([emp_id, emp_name, today, time_now, "-", "-"])

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Attendance Marked for {emp_name}")


def calculate_total_time(start_time, end_time):
    if end_time == "-":
        return "-"

    fmt = "%H:%M:%S"
    t1 = datetime.strptime(start_time, fmt)
    t2 = datetime.strptime(end_time, fmt)
    diff = t2 - t1
    return str(diff)