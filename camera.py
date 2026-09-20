import cv2
from ultralytics import YOLO
from urllib.parse import quote
from datetime import datetime
import csv
import os
import time

# Camera settings
# Update this if your router assigns the camera a different local IP.
CAMERA_IP = "192.168.1.2"

# Credentials are requested at runtime and are never stored in this file.
USERNAME = input("Tapo camera username: ")
PASSWORD = input("Tapo camera password: ")

username = quote(USERNAME, safe="")
password = quote(PASSWORD, safe="")

RTSP_URL = (
    f"rtsp://{username}:{password}"
    f"@{CAMERA_IP}:554/stream1"
)

# Event log
EVENT_FILE = "events.csv"

if not os.path.exists(EVENT_FILE):
    with open(EVENT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "event", "duration_seconds"])


def log_event(event, duration=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(EVENT_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, event, duration])

    print(f"[{timestamp}] {event}")


print("Loading AI model...")
model = YOLO("yolo11n.pt")

print("Connecting to Tapo C200...")
cap = cv2.VideoCapture(RTSP_URL)

if not cap.isOpened():
    print("Could not connect to camera.")
    exit()

print("Connected!")
print("AI monitoring started.")
print("Press Q in the camera window to stop.")

person_present = False
person_entered_at = None
last_person_seen = None
LEAVE_DELAY = 5

while True:
    success, frame = cap.read()

    if not success:
        print("Lost camera stream.")
        break

    results = model(frame, verbose=False)
    person_detected = False

    for box in results[0].boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = model.names[class_id]

        if class_name == "person" and confidence > 0.50:
            person_detected = True
            last_person_seen = time.time()

    if person_detected and not person_present:
        person_present = True
        person_entered_at = time.time()
        log_event("PERSON ENTERED")

    if person_present and last_person_seen is not None:
        seconds_since_seen = time.time() - last_person_seen

        if seconds_since_seen > LEAVE_DELAY:
            person_present = False
            duration = int(time.time() - person_entered_at)
            log_event("PERSON LEFT", duration)
            person_entered_at = None
            last_person_seen = None

    annotated = results[0].plot()
    status = "PERSON PRESENT" if person_present else "ROOM EMPTY"

    cv2.putText(
        annotated,
        status,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2,
    )

    cv2.imshow("Tapo C200 - AI Monitor", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Monitoring stopped.")
