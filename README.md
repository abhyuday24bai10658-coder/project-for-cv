# 📸 Smart Attendance System Using Face Recognition

A computer vision project that automatically marks attendance by recognizing faces through a webcam — no manual roll calls needed.

---

## 🔍 What It Does

- Registers faces of people (students / employees) using their webcam photo
- Detects and recognizes faces in real time using the laptop camera
- Automatically marks attendance in a CSV file with name, date, and time
- Prevents duplicate entries — each person is marked only once per day
- Lets you view attendance records filtered by date or name

---

## 📁 Project Structure

```
attendance-system/
│
├── known_faces/          ← Put registered face photos here
│   └── Alice.jpg         ← Automatically saved by register.py
│
├── register.py           ← Step 1: Register a new person's face
├── attendance.py         ← Step 2: Run real-time attendance
├── view_attendance.py    ← Step 3: View attendance records
│
├── attendance.csv        ← Auto-generated attendance log
├── requirements.txt      ← Python dependencies
└── README.md             ← This file
```

---

## ⚙️ Installation

### 1. Make sure you have Python 3.8+ installed
Download from: https://www.python.org/downloads/

### 2. Install required libraries
Open your terminal/command prompt and run:
```bash
pip install cmake
pip install dlib
pip install face_recognition
pip install opencv-python
```

> ⚠️ `dlib` requires Visual Studio Build Tools on Windows. See [dlib install guide](http://dlib.net/compile.html) if you face issues.

---

## 🚀 How to Use

### Step 1 — Register a Person
```bash
python register.py
```
- A webcam window opens
- Enter the person's name when prompted
- Press **SPACE** to capture and save the photo
- Repeat for each person

### Step 2 — Run Attendance
```bash
python attendance.py
```
- The webcam opens and starts recognizing faces
- A green box appears around recognized faces with a ✓ checkmark
- Attendance is saved automatically to `attendance.csv`
- Press **Q** to stop

### Step 3 — View Attendance
```bash
# See all records
python view_attendance.py

# See only today's attendance
python view_attendance.py --today

# See records for a specific person
python view_attendance.py --name Alice
```

---

## 📊 Sample Output (attendance.csv)

| Name  | Date       | Time     | Status  |
|-------|------------|----------|---------|
| Alice | 2025-06-10 | 09:05:32 | Present |
| Bob   | 2025-06-10 | 09:07:15 | Present |
| Alice | 2025-06-11 | 08:58:44 | Present |

---

## 💡 How It Works (Technical Overview)

1. **Face Registration** — Captures a photo and saves it to `known_faces/`
2. **Encoding** — `face_recognition` converts each photo into a 128-point numerical "fingerprint"
3. **Real-time Detection** — OpenCV reads webcam frames; `face_recognition` locates faces in each frame
4. **Matching** — The system compares detected face encodings with stored encodings using Euclidean distance
5. **Attendance Logging** — On a match below the confidence threshold, the name + timestamp is written to CSV

---

## 🔧 Configuration

In `attendance.py`, you can change:
```python
CONFIDENCE_THRESHOLD = 0.55  # Lower = stricter matching (default: 0.55)
```

---

## 📦 Dependencies

| Library | Purpose |
|---------|---------|
| `opencv-python` | Webcam access & drawing bounding boxes |
| `face_recognition` | Face detection and recognition |
| `dlib` | Backend for face_recognition |
| `cmake` | Required to build dlib |

---

## 👤 Author

Created as a BYOP (Build Your Own Project) submission.  
Course: Computer Vision  
Platform: VITyarthi
