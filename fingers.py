import cv2
import mediapipe as mp
import math
class HandDetector():
    def __init__(self, maxHands=1):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, raised_rightukaz, draw=True):
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

                # Проверка состояния каждого пальца
                move_x = 0
                move_y = 0

                # Для змейки
                if finger_tip_coordinates[0] * 10 < finger_tip_coordinates[1] * 10:
                    if abs(finger_tip_coordinates[1] * 100 - finger_tip_coordinates[0] * 100) > abs(finger_tip_coordinates[2] * 100 - finger_tip_coordinates[3] * 100):
                        move_y = 0
                        move_x = 1
                elif finger_tip_coordinates[0] * 10 > finger_tip_coordinates[1] * 10:
                    if abs(finger_tip_coordinates[1] * 100 - finger_tip_coordinates[0] * 100) > abs(finger_tip_coordinates[2] * 100 - finger_tip_coordinates[3] * 100):
                        move_y = 0
                        move_x = -1
                else: pass
                if finger_tip_coordinates[2] * 10 < finger_tip_coordinates[3] * 10:
                    if abs(finger_tip_coordinates[1] * 100 - finger_tip_coordinates[0] * 100) < abs(finger_tip_coordinates[2] * 100 - finger_tip_coordinates[3] * 100):
                        move_y = -1
                        move_x = 0
                elif finger_tip_coordinates[2] * 10 > finger_tip_coordinates[3] * 10:
                    if abs(finger_tip_coordinates[1] * 100 - finger_tip_coordinates[0] * 100) < abs(finger_tip_coordinates[2] * 100 - finger_tip_coordinates[3] * 100):
                        move_y =1
                        move_x = 0
                else: pass
                raised_rightukaz = [move_x, move_y]
        return img, raised_rightukaz

