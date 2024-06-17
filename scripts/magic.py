import cv2
import mediapipe as mp
import math
class HandDetector():
    def __init__(self, maxHands=1):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, landmarks, self.mpHands.HAND_CONNECTIONS)
                finger_tip_coordinates = [landmarks.landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP].x,
                                          landmarks.landmark[self.mpHands.HandLandmark.INDEX_FINGER_MCP].x,
                                          landmarks.landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP].y,
                                          landmarks.landmark[self.mpHands.HandLandmark.INDEX_FINGER_MCP].y]

        return img