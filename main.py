import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

# Initialize webcam
cap = cv2.VideoCapture(0)
cam_width = 1280
cam_height = 720
cap.set(3, cam_width)
cap.set(4, cam_height)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Hand detector
detector = HandDetector(detectionCon=0.8)

# Keyboard layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ".", ",", "/"],
    ["Space", "Delete"]
]

class Button:
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.text = text
        self.size = size

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), thickness=-1)
        font = cv2.FONT_HERSHEY_PLAIN
        font_scale = 3
        font_thickness = 3
        text_size = cv2.getTextSize(button.text, font, font_scale, font_thickness)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, button.text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)
    return img

# Create button list
buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        if key == "Space":
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key, size=[500, 60]))
        elif key == "Delete":
            buttonList.append(Button([100 * j + 50 + 500, 100 * i + 50], key, size=[150, 60]))
        else:
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

prev_hover = None
last_click_time = 0
delay = 8  # seconds

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    lmList = []

    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

    img = drawAll(img, buttonList)

    hoveredButton = None

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                hoveredButton = button

                # Highlight green
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 240, 0), thickness=-1)
                font = cv2.FONT_HERSHEY_PLAIN
                font_scale = 3
                font_thickness = 3
                text_size = cv2.getTextSize(button.text, font, font_scale, font_thickness)[0]
                text_x = x + (w - text_size[0]) // 2
                text_y = y + (h + text_size[1]) // 2
                cv2.putText(img, button.text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

                current_time = time.time()

                if prev_hover != hoveredButton or current_time - last_click_time > delay:
                    # Type key
                    if button.text == "Space":
                        pyautogui.write(" ")
                    elif button.text == "Delete":
                        pyautogui.press("backspace")
                    else:
                        pyautogui.write(button.text)
                    print(f"Typed: {button.text}")

                    # Simulate mouse click at screen position of the button center
                    screen_x = int((x + w / 2) * screen_width / cam_width)
                    screen_y = int((y + h / 2) * screen_height / cam_height)
                    pyautogui.click(screen_x, screen_y)
                    print(f"Clicked at screen position: ({screen_x}, {screen_y})")

                    last_click_time = current_time

                    # Show red flash
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=-1)
                    cv2.putText(img, button.text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

                break

    prev_hover = hoveredButton

    cv2.imshow("image", img)
    cv2.waitKey(1)
