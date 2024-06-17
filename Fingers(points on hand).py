import cv2
import mediapipe as mp

camera = cv2.VideoCapture(0)


class HandDetector():
    def __init__(self, maxHands=2):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_landmarks, self.mpHands.HAND_CONNECTIONS)
                '''for i, landmark in enumerate(hand_landmarks.landmark):
                    x, y, z = int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0]), int(landmark.z * 100)
                    if i == 8:
                        print(f'Point {i}: ({x}, {y}, {z})')'''
        return img

detector = HandDetector()

while camera.isOpened():
    suc, img = camera.read()
    if not suc:
        break
    img = detector.findHands(img)
    cv2.imshow("IMG", img)
    if cv2.waitKey(1) == 27:
        break