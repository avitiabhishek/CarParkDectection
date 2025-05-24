CarParkDectection An AI-powered smart parking solution that detects and tracks free and occupied parking spaces in real-time using computer vision (OpenCV) and video footage. The system also logs parking activity, provides alerts, and supports interactive setup of slot regions.
🧠 Features ✅ Interactive slot marking (click to add, right-click to remove)

🎥 Real-time video analysis using OpenCV

🧠 Adaptive thresholding + filtering for robust detection

📊 Logs:

free_slots.csv: timestamps when slots become free

summary_slots.csv: occupancy summaries with time

🔔 Audio alerts when a slot becomes free

🖼️ Save snapshots of the current state

⏱️ Live timestamp overlay

. ├── carPark.mp4 # Input video of the parking area ├── carParkImg.png # Static image for selecting parking regions ├── CarParkPos # Pickle file containing selected slot positions ├── slot_free.mp3 # Audio notification when a slot becomes free ├── free_slots.csv # Logs: Slot ID and time when it becomes free ├── summary_slots.csv # Logs: Total and occupied slots with timestamps ├── parkingspacepicker.py # Tool to pick/adjust parking slots manually ├── parking_detection.py # Main script for detection and monitoring ├── README.md # You're here!
