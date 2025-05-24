import cv2
import pickle
import cvzone
import numpy as np
from datetime import datetime
import time
import pygame
import csv
import os

# Initialize pygame mixer
pygame.mixer.init()

# Load video feed
cap = cv2.VideoCapture('carPark.mp4')

# Load saved positions
with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height = 107, 48
prev_states = [None] * len(posList)
last_check_time = time.time()

# Setup CSV files
free_log_file = 'free_slots_log.csv'
summary_log_file = 'slot_summary_log.csv'

# Create and write headers if not exist
if not os.path.exists(free_log_file):
    with open(free_log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Slot ID', 'Time'])

if not os.path.exists(summary_log_file):
    with open(summary_log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp', 'Total Slots', 'Occupied Slots'])

def checkParkingSpace(imgPro, img):
    current_states = []
    free_slots = 0

    for idx, pos in enumerate(posList):
        x, y = pos
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        is_free = count < 900
        current_states.append(is_free)
        if is_free:
            free_slots += 1

        # Drawing
        color = (0, 255, 0) if is_free else (0, 0, 255)
        thickness = 5 if is_free else 2
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, f'{idx}', (x + 2, y + 2), scale=0.8, thickness=1, offset=1, colorR=color)

    total_slots = len(posList)
    cvzone.putTextRect(img, f'Free: {free_slots}/{total_slots}', (20, 20),
                       scale=2, thickness=3, offset=10, colorR=(0, 200, 0))

    return current_states, free_slots

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) >= cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        break

    # Preprocessing
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    current_time = time.time()
    if current_time - last_check_time >= 2:
        current_states, free_slots = checkParkingSpace(imgDilate, img)
        total_slots = len(posList)
        occupied_slots = total_slots - free_slots

        # Save summary of counts to CSV
        with open(summary_log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_slots, occupied_slots])

        for idx, (prev, curr) in enumerate(zip(prev_states, current_states)):
            if prev is not None and prev != curr:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if curr:  # Slot became FREE
                    print(f"Slot {idx} is now FREE at {timestamp}")

                    # Play sound
                    try:
                        pygame.mixer.music.load("slot_free.mp3")
                        pygame.mixer.music.play()
                    except Exception as e:
                        print(f"Sound error: {e}")

                    # Log to CSV
                    with open(free_log_file, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([idx, timestamp])

        prev_states = current_states
        last_check_time = current_time
    else:
        checkParkingSpace(imgDilate, img)

    # Overlay current datetime
    cv2.putText(img, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                (10, img.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow("Parking Detection", img)
    key = cv2.waitKey(10)

    if key == ord('s'):
        filename = f'snapshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        cv2.imwrite(filename, img)
        print(f"Snapshot saved as {filename}")

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
