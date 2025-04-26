import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ".", ",", "/"]
]

def drawAll(img, buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        # Draw black filled rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), thickness=-1)
        # Draw white text centered
        font = cv2.FONT_HERSHEY_PLAIN
        font_scale = 3  # Smaller text
        font_thickness = 3
        text_size = cv2.getTextSize(button.text, font, font_scale, font_thickness)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(img, button.text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

    return img

class Button:
    def __init__(self, pos, text, size=[60, 60]):  # Smaller button size
        self.pos = pos
        self.text = text
        self.size = size


buttonList=[]

for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

clicked = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    lmList = []

    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 landmark points
        bbox = hand["bbox"]  # Bounding box info
        center = hand["center"]  # Center of hand
        handType = hand["type"]  # Left or Right hand
    img = drawAll(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size


            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                # Highlight button green when finger is on it
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 240, 0), thickness=-1)

                # Redraw the text after highlighting
                font = cv2.FONT_HERSHEY_PLAIN
                font_scale = 3
                font_thickness = 3
                text_size = cv2.getTextSize(button.text, font, font_scale, font_thickness)[0]
                text_x = x + (w - text_size[0]) // 2
                text_y = y + (h + text_size[1]) // 2
                cv2.putText(img, button.text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

                l, _, _ = detector.findDistance(lmList[8][:2], lmList[12][:2], img)

                # If fingers are close together, register a click
                if l < 40:
                    clicked = True
                    pyautogui.write(button.text)
                    print(button.text)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), thickness=-1)
                    font = cv2.FONT_HERSHEY_PLAIN
                    font_scale = 3
                    font_thickness = 3
                    text_size = cv2.getTextSize(button.text, font, font_scale, font_thickness)[0]
                    text_x = x + (w - text_size[0]) // 2
                    text_y = y + (h + text_size[1]) // 2
                    cv2.putText(img, button.text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)

                if l > 40:
                    clicked = False


    cv2.imshow("image", img)
    cv2.waitKey(1)