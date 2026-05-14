import React, { useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "/api";

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const streamRef = useRef(null);
  const [cameraActive, setCameraActive] = useState(false);
  const [studentId, setStudentId] = useState("");
  const [students, setStudents] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [status, setStatus] = useState("Ready");
  const [busy, setBusy] = useState(false);
  const [lastRecognition, setLastRecognition] = useState(null);

  const enrolledSamples = useMemo(
    () => students.reduce((total, student) => total + student.imageCount, 0),
    [students]
  );

  useEffect(() => {
    refreshStudents();
    refreshAttendance();
    return () => stopCamera();
  }, []);

  async function api(path, options = {}) {
    const response = await fetch(`${API}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options
    });
    const data = await response.json();
    if (!response.ok || data.ok === false) {
      throw new Error(data.message || "Request failed");
    }
    return data;
  }

  async function refreshStudents() {
    const data = await api("/students");
    setStudents(data.students);
  }

  async function refreshAttendance() {
    const data = await api("/attendance");
    setAttendance(data.attendance);
  }

  async function startCamera() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 },
        audio: false
      });
      streamRef.current = stream;
      videoRef.current.srcObject = stream;
      setCameraActive(true);
      setStatus("Camera running");
    } catch (error) {
      setStatus(`Camera error: ${error.message}`);
    }
  }

  function stopCamera() {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((track) => track.stop());
      streamRef.current = null;
    }
    setCameraActive(false);
  }

  function captureFrame() {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas || !video.videoWidth) {
      throw new Error("Start the camera before capturing");
    }
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL("image/jpeg", 0.92);
  }

  async function enrollSample() {
    const id = studentId.trim();
    if (!id) {
      setStatus("Enter a student ID before enrolling");
      return;
    }
    setBusy(true);
    try {
      const image = captureFrame();
      const data = await api("/enroll", {
        method: "POST",
        body: JSON.stringify({ studentId: id, image })
      });
      setStatus(data.message);
      await refreshStudents();
    } catch (error) {
      setStatus(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function recognizeFrame() {
    setBusy(true);
    try {
      const image = captureFrame();
      const data = await api("/recognize", {
        method: "POST",
        body: JSON.stringify({ image })
      });
      const result = data.results[0];
      setLastRecognition(result);
      setStatus(
        result?.matched
          ? `Marked ${result.studentId} present (${result.confidence})`
          : "Face was detected but did not match an enrolled student"
      );
      await refreshAttendance();
    } catch (error) {
      setStatus(error.message);
    } finally {
      setBusy(false);
    }
  }

  async function generateAttendance() {
    setBusy(true);
    try {
      const data = await api("/generate-attendance", { method: "POST" });
      setAttendance(data.attendance);
      setStatus("Generated de-duplicated attendance sheet");
    } catch (error) {
      setStatus(error.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="app">
      <section className="topbar">
        <div>
          <p className="eyebrow">Automated Attendance</p>
          <h1>Face Recognition Console</h1>
        </div>
        <div className="status">{status}</div>
      </section>

      <section className="layout">
        <div className="cameraPanel">
          <div className="panelHeader">
            <div>
              <h2>Live Camera</h2>
              <p>Use browser camera capture for enrollment and attendance.</p>
            </div>
            <div className={cameraActive ? "pill good" : "pill"}>{cameraActive ? "Live" : "Idle"}</div>
          </div>
          <div className="videoFrame">
            <video ref={videoRef} autoPlay playsInline muted />
            {!cameraActive && <div className="videoEmpty">Camera preview</div>}
          </div>
          <canvas ref={canvasRef} hidden />
          <div className="toolbar">
            <button onClick={startCamera} disabled={cameraActive}>Start Camera</button>
            <button onClick={stopCamera} disabled={!cameraActive}>Stop Camera</button>
            <button className="primary" onClick={recognizeFrame} disabled={!cameraActive || busy || !students.length}>
              Take Attendance
            </button>
          </div>
        </div>

        <aside className="sidePanel">
          <section className="card">
            <h2>Enroll Student</h2>
            <label>
              Student ID
              <input value={studentId} onChange={(event) => setStudentId(event.target.value)} placeholder="e.g. admin_Anshul" />
            </label>
            <button className="primary" onClick={enrollSample} disabled={!cameraActive || busy}>
              Capture Enrollment Sample
            </button>
            <p className="hint">Capture 10-20 samples per student for better matching.</p>
          </section>

          <section className="stats">
            <div>
              <strong>{students.length}</strong>
              <span>Students</span>
            </div>
            <div>
              <strong>{enrolledSamples}</strong>
              <span>Samples</span>
            </div>
            <div>
              <strong>{Math.max(attendance.length - 1, 0)}</strong>
              <span>Rows</span>
            </div>
          </section>

          <section className="card">
            <div className="cardTitle">
              <h2>Students</h2>
              <button className="ghost" onClick={refreshStudents}>Refresh</button>
            </div>
            <div className="list">
              {students.length ? students.map((student) => (
                <div className="listRow" key={student.id}>
                  <span>{student.id}</span>
                  <small>{student.imageCount} samples</small>
                </div>
              )) : <p className="empty">No students enrolled yet.</p>}
            </div>
          </section>

          <section className="card">
            <div className="cardTitle">
              <h2>Attendance</h2>
              <button className="ghost" onClick={generateAttendance} disabled={busy}>Generate</button>
            </div>
            {lastRecognition && (
              <p className="hint">
                Last: {lastRecognition.matched ? lastRecognition.studentId : "Unknown"} ({lastRecognition.confidence})
              </p>
            )}
            <div className="attendance">
              {attendance.length ? attendance.map((row, index) => (
                <div className="attendanceRow" key={`${row.join("-")}-${index}`}>
                  <span>{index === 0 ? "Date" : "Present"}</span>
                  <strong>{row.join(" ")}</strong>
                </div>
              )) : <p className="empty">No attendance recorded yet.</p>}
            </div>
          </section>
        </aside>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
