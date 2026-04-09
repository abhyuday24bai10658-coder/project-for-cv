"""
attendance.py — Main script for the Smart Attendance System.
Detects and recognizes faces via webcam and marks attendance in a CSV file.

Usage:
    python attendance.py
"""

import cv2
import face_recognition
import os
import csv
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────────
KNOWN_FACES_DIR = "known_faces"       # Folder with registered face photos
ATTENDANCE_FILE = "attendance.csv"    # Output CSV file
CONFIDENCE_THRESHOLD = 0.55           # Lower = stricter matching (0.0 – 1.0)
# ───────────────────────────────────────────────────────────────────────────


def load_known_faces():
    """Load all registered faces from the known_faces folder."""
    known_encodings = []
    known_names = []

    print("[INFO] Loading registered faces...")

    for filename in os.listdir(KNOWN_FACES_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            name = os.path.splitext(filename)[0]  # e.g. "Alice.jpg" → "Alice"
            image_path = os.path.join(KNOWN_FACES_DIR, filename)

            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(name)
                print(f"  ✓ Loaded: {name}")
            else:
                print(f"  ✗ No face found in: {filename} (skipped)")

    print(f"[INFO] {len(known_names)} face(s) loaded.\n")
    return known_encodings, known_names


def mark_attendance(name):
    """Write attendance entry to CSV (only once per session per person)."""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Read existing entries to avoid duplicates in today's session
    existing = set()
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader, None)  # skip header
            for row in reader:
                if len(row) >= 2 and row[1] == date_str:
                    existing.add(row[0])

    if name not in existing:
        with open(ATTENDANCE_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            # Write header if file is new/empty
            if os.stat(ATTENDANCE_FILE).st_size == 0:
                writer.writerow(["Name", "Date", "Time", "Status"])
            writer.writerow([name, date_str, time_str, "Present"])
        print(f"[ATTENDANCE] Marked: {name} at {time_str}")
        return True  # newly marked
    return False  # already marked today


def run_attendance():
    """Open webcam and run real-time face recognition."""

    # Initialise attendance file with header if it doesn't exist
    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["Name", "Date", "Time", "Status"])

    known_encodings, known_names = load_known_faces()

    if not known_names:
        print("[ERROR] No registered faces found. Run register.py first.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open webcam.")
        return

    print("[INFO] Webcam started. Press Q to quit.\n")

    # Track who has been marked in THIS session (for on-screen feedback)
    marked_today = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # ── Face detection (process at half size for speed) ─────────────
        small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small)
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            name = "Unknown"
            color = (0, 0, 255)  # Red for unknown

            if len(distances) > 0:
                best_idx = distances.argmin()
                if distances[best_idx] < CONFIDENCE_THRESHOLD:
                    name = known_names[best_idx]
                    color = (0, 200, 0)  # Green for recognised

                    # Mark attendance
                    newly_marked = mark_attendance(name)
                    if newly_marked:
                        marked_today.add(name)

            # ── Draw box and label (scale back to full size) ─────────────
            top, right, bottom, left = [v * 2 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            label = f"{name}"
            if name in marked_today:
                label += " ✓"

            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # ── HUD ──────────────────────────────────────────────────────────
        cv2.putText(frame, f"Marked today: {len(marked_today)}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, "Press Q to quit", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)

        cv2.imshow("Smart Attendance System", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n[DONE] Attendance saved to: {ATTENDANCE_FILE}")


if __name__ == "__main__":
    run_attendance()
