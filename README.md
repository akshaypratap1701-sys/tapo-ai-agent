# Tapo AI Agent

A local computer-vision prototype for a TP-Link Tapo C200 camera.

## Current V1

- Connects to the Tapo C200 over RTSP
- Runs YOLO11n locally using Ultralytics
- Detects people in the live stream
- Displays `PERSON PRESENT` / `ROOM EMPTY`
- Logs `PERSON ENTERED` and `PERSON LEFT`
- Records timestamps and occupancy duration in `events.csv`
- Uses a 5-second leave delay to reduce false exit events

## Setup

Tested on macOS with a Tapo C200.

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Open `camera.py` and set `CAMERA_IP` to the camera's current local IP address.

Then run:

```bash
python camera.py
```

Enter the Tapo **Camera Account** username and password when prompted. Credentials are URL-encoded before being used in the RTSP URL and are not stored in the source code.

## Camera stream

The prototype uses the C200 high-quality RTSP stream:

```text
rtsp://<username>:<password>@<camera-ip>:554/stream1
```

Do not expose the camera's RTSP port directly to the public internet.

## Event output

Runtime events are written locally to `events.csv`. The file is ignored by Git because it can contain private information about room occupancy.

## Roadmap

The next version can add:

- chatbot over camera state and event history
- snapshots for important events
- natural-language questions such as "When was someone last in the room?"
- vision-model interpretation of activity
- notifications
- ONVIF pan/tilt control
- agentic observe → reason → act loops

## Privacy

Camera credentials, event logs, model weights, virtual environments, and captured media should remain local and are excluded from the repository.
