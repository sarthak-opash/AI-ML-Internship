
import os
import csv
from datetime import datetime

CSV_FILE = "Attendence/attendance.csv"

def calculate_total_time(start_time, end_time):
    if end_time == "None":
        return "None"
    fmt = "%H:%M:%S"
    t1 = datetime.strptime(start_time, fmt)
    t2 = datetime.strptime(end_time, fmt)
    return str(t2 - t1)

def mark_attendance(emp_id, emp_name):
    today = datetime.now().strftime("%d-%m-%y")
    time_in = datetime.now().strftime("%H:%M:%S")
    time_out = datetime.now().strftime("%H:%M:%S")
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    header = ["Emp_ID", "Name", "Date", "In", "Out", "Total Time"]
    rows = [] 
    
    if os.path.isfile(CSV_FILE):
        with open(CSV_FILE, "r", newline="") as f:
            reader = list(csv.reader(f))
            rows = reader[1:] if reader else []

    found = False
    for row in rows:
        if len(row) >= 3 and str(row[0]) == str(emp_id) and row[2] == today:
            found = True
            if row[4] == "None":
                row[4] = time_out
                row[5] = calculate_total_time(row[3], row[4])
            elif row[4] == time_out:
                st.warning(f"Attendance already marked for {emp_name} today")
            break

    if not found:
        rows.append([emp_id, emp_name, today, time_in, "None", "None"])

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

    print(f"Attendance Marked for {emp_name}")
