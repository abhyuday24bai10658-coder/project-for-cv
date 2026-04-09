"""
register.py — Add a new person to the attendance system.
Run this once for each person you want to track.

Usage:
    python register.py
"""

import cv2
import os

# Folder where face photos will be saved
KNOWN_FACES_DIR = "known_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)


def register_face():
    name = input("Enter the person's name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    print(f"\n[INFO] Opening webcam. Press SPACE to capture the photo, or Q to quit.")

    cap = cv2.VideoCapture(0)  # 0 = default webcam

    if not cap.isOpened():
        print("[ERROR] Could not open webcam. Make sure it's connected.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to read from webcam.")
            break

        # Show live feed
        display = frame.copy()
        cv2.putText(display, f"Registering: {name}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 200, 0), 2)
        cv2.putText(display, "SPACE = Capture  |  Q = Quit", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1)
        cv2.imshow("Register Face", display)

        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # SPACE to capture
            save_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
            cv2.imwrite(save_path, frame)
            print(f"[SUCCESS] Photo saved as: {save_path}")
            break

        elif key == ord('q') or key == 27:  # Q or ESC to quit
            print("[INFO] Registration cancelled.")
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    register_face()
