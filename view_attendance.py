"""
view_attendance.py — View and filter attendance records.

Usage:
    python view_attendance.py              # Show all records
    python view_attendance.py --today      # Show today's records only
    python view_attendance.py --name Alice # Show records for a specific person
"""

import csv
import os
import argparse
from datetime import datetime


ATTENDANCE_FILE = "attendance.csv"


def view_records(filter_today=False, filter_name=None):
    if not os.path.exists(ATTENDANCE_FILE):
        print("No attendance file found. Run attendance.py first.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    rows = []

    with open(ATTENDANCE_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if filter_today and row["Date"] != today:
                continue
            if filter_name and row["Name"].lower() != filter_name.lower():
                continue
            rows.append(row)

    if not rows:
        print("No records found for the given filter.")
        return

    # Print table
    print(f"\n{'Name':<20} {'Date':<12} {'Time':<10} {'Status'}")
    print("-" * 55)
    for row in rows:
        print(f"{row['Name']:<20} {row['Date']:<12} {row['Time']:<10} {row['Status']}")

    print(f"\nTotal records: {len(rows)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="View attendance records")
    parser.add_argument("--today", action="store_true", help="Show today's records only")
    parser.add_argument("--name", type=str, help="Filter by person name")
    args = parser.parse_args()

    view_records(filter_today=args.today, filter_name=args.name)
