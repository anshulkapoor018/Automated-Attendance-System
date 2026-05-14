import base64
import csv
import os
import re
import time
from pathlib import Path

import cv2
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS

import attendance_Generator
from face_recognition_system.detectors import FaceDetector
import face_recognition_system.operations as op


ROOT = Path(__file__).resolve().parent
PEOPLE_FOLDER = ROOT / "face_recognition_system" / "people"
RAW_ATTENDANCE = ROOT / "a.csv"
GENERATED_ATTENDANCE = ROOT / "b.csv"
FACE_CASCADE = ROOT / "haarcascade_frontalface_default.xml"
RECOGNITION_THRESHOLD = 100

app = Flask(__name__)
CORS(app)


def safe_student_id(value):
    value = value.strip()
    if not value:
        raise ValueError("Student ID is required")
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", value)
    if safe != value:
        raise ValueError("Use only letters, numbers, dashes, and underscores")
    return safe


def decode_image(data_url):
    if not data_url:
        raise ValueError("Missing image")
    if "," in data_url:
        data_url = data_url.split(",", 1)[1]
    image_bytes = base64.b64decode(data_url)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("Could not decode image")
    return frame


def face_images_from_frame(frame):
    detector = FaceDetector(str(FACE_CASCADE))
    faces_coord = detector.detect(frame, False)
    if len(faces_coord) == 0:
        return [], []
    faces_img = op.cut_face_rectangle(frame, faces_coord)
    faces_img = op.normalize_intensity(faces_img)
    faces_img = op.resize(faces_img)
    return faces_coord, faces_img


def list_students():
    PEOPLE_FOLDER.mkdir(parents=True, exist_ok=True)
    students = []
    for path in sorted(PEOPLE_FOLDER.iterdir()):
        if path.is_dir():
            image_count = len([item for item in path.iterdir() if item.suffix.lower() in {".jpg", ".jpeg", ".png"}])
            students.append({"id": path.name, "imageCount": image_count})
    return students


def load_training_data():
    images = []
    labels = []
    label_names = {}

    for index, student in enumerate(list_students()):
        label_names[index] = student["id"]
        student_folder = PEOPLE_FOLDER / student["id"]
        for image_path in sorted(student_folder.iterdir()):
            if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                continue
            image = cv2.imread(str(image_path), 0)
            if image is not None:
                images.append(image)
                labels.append(index)

    if not images:
        raise RuntimeError("No enrolled face images found")
    return images, np.array(labels), label_names


def append_attendance(student_id):
    new_file = not RAW_ATTENDANCE.exists() or RAW_ATTENDANCE.stat().st_size == 0
    with RAW_ATTENDANCE.open("a", newline="") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(time.strftime("%d/%m/%Y").split())
        writer.writerow([student_id])


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "students": list_students()})


@app.get("/api/students")
def students():
    return jsonify({"students": list_students()})


@app.post("/api/enroll")
def enroll():
    payload = request.get_json(force=True)
    student_id = safe_student_id(payload.get("studentId", ""))
    frame = decode_image(payload.get("image", ""))
    faces_coord, faces_img = face_images_from_frame(frame)
    if len(faces_img) != 1:
        return jsonify({"ok": False, "message": "Show exactly one face to enroll"}), 400

    student_folder = PEOPLE_FOLDER / student_id
    student_folder.mkdir(parents=True, exist_ok=True)
    next_index = len(list(student_folder.glob("*.jpg"))) + 1
    image_path = student_folder / ("%s.jpg" % next_index)
    cv2.imwrite(str(image_path), faces_img[0])

    return jsonify({
        "ok": True,
        "student": {"id": student_id, "imageCount": next_index},
        "faces": len(faces_coord),
        "message": "Saved sample %s for %s" % (next_index, student_id),
    })


@app.post("/api/recognize")
def recognize():
    frame = decode_image(request.get_json(force=True).get("image", ""))
    faces_coord, faces_img = face_images_from_frame(frame)
    if len(faces_img) == 0:
        return jsonify({"ok": False, "message": "No face detected"}), 400

    images, labels, label_names = load_training_data()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(images, labels)

    results = []
    for face_img in faces_img:
        label, confidence = recognizer.predict(face_img)
        student_id = label_names.get(label)
        matched = confidence < RECOGNITION_THRESHOLD
        if matched and student_id:
            append_attendance(student_id)
        results.append({
            "studentId": student_id if matched else None,
            "confidence": round(float(confidence), 2),
            "matched": matched,
        })

    return jsonify({"ok": True, "results": results})


@app.post("/api/generate-attendance")
def generate_attendance():
    if not RAW_ATTENDANCE.exists():
        return jsonify({"ok": False, "message": "No raw attendance file found"}), 400
    attendance_Generator.convert()
    return jsonify({"ok": True, "attendance": read_attendance(GENERATED_ATTENDANCE)})


@app.get("/api/attendance")
def attendance():
    path = GENERATED_ATTENDANCE if GENERATED_ATTENDANCE.exists() else RAW_ATTENDANCE
    return jsonify({"attendance": read_attendance(path)})


def read_attendance(path):
    if not path.exists():
        return []
    with path.open("r", newline="") as file:
        return [row for row in csv.reader(file) if row]


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
