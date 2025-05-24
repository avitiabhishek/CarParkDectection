import cv2
import pickle

width, height = 107, 48

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    elif events == cv2.EVENT_RBUTTONDOWN:
        min_distance = float('inf')
        closest_index = -1
        for i, pos in enumerate(posList):
            x1, y1 = pos
            center_x = x1 + width // 2
            center_y = y1 + height // 2
            distance = ((x - center_x)**2 + (y - center_y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest_index = i
        # Remove if close enough (within 50 pixels)
        if min_distance < 50 and closest_index != -1:
            posList.pop(closest_index)

while True:
    img = cv2.imread('carParkImg.png').copy()
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    cv2.imshow("Mark Parking Slots", img)
    cv2.setMouseCallback("Mark Parking Slots", mouseClick)

    key = cv2.waitKey(1)
    if key == ord('s'):
        with open('CarParkPos', 'wb') as f:
            pickle.dump(posList, f)
        print("Positions saved.")
    elif key == 27:  # ESC
        break

cv2.destroyAllWindows()
