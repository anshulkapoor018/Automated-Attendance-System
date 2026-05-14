# Automated Attendance System

An old OpenCV/Tkinter attendance project, revived with a modern React web interface and a small Flask API wrapper around the original face-recognition workflow.

## What It Does

- Opens a browser-based camera preview.
- Enrolls students by saving face samples from webcam frames.
- Recognizes enrolled students with OpenCV LBPH face recognition.
- Records attendance into the existing CSV flow.
- Generates a de-duplicated attendance sheet from the raw capture file.

The original Tkinter scripts are still present for reference, but the recommended way to run and iterate on the project is now the React + Flask web app.

## Project Structure

```text
.
├── backend.py                         # Flask API for students, recognition, and attendance
├── Final.py                           # Legacy OpenCV enrollment/recognition helpers, Python 3 compatible
├── attendance_Generator.py            # De-duplicates raw attendance into b.csv
├── face_recognition_system/           # Face detection helpers and enrolled face images
├── web/                               # React/Vite frontend
├── requirements.txt                   # Python dependencies
└── run_web.command                    # Starts backend and frontend together
```

## Setup

From the project root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

cd web
npm install
```

## Run The Web App

From the project root:

```bash
./run_web.command
```

Then open:

```text
http://127.0.0.1:5173/
```

The browser will ask for camera permission. Allow it to use enrollment and attendance capture.

## Web Workflow

1. Click **Start Camera**.
2. Enter a student ID.
3. Click **Capture Enrollment Sample** multiple times for the same student.
4. Click **Take Attendance** to recognize the current camera frame and append attendance.
5. Click **Generate** to create the de-duplicated attendance sheet.

## API

The Flask backend runs on `http://127.0.0.1:5001`.

Useful endpoints:

- `GET /api/health`
- `GET /api/students`
- `POST /api/enroll`
- `POST /api/recognize`
- `GET /api/attendance`
- `POST /api/generate-attendance`

## Notes

- Existing sample data under `face_recognition_system/people/` is reused.
- `a.csv` is the raw attendance file.
- `b.csv` is generated runtime output and is ignored by git.
- The legacy Tkinter app can still be launched with `Main.py`, but the web app is the maintained path for future iteration.
