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
                #print(finger_tip_coordinates)
                #Для ninja game
                if finger_tip_coordinates[0] * 10 + 0.3 < finger_tip_coordinates[1] * 10:
                    if abs(finger_tip_coordinates[1] * 100 - finger_tip_coordinates[0] * 100) > finger_tip_coordinates[3] * 100 - finger_tip_coordinates[2] * 100:
                        move_x = 1
                        move_y = 0
                    else:
                        move_x = 1
                        move_y = 1
                elif finger_tip_coordinates[0] * 10 > finger_tip_coordinates[1] * 10 + 0.3:
                    if abs(finger_tip_coordinates[1] * 100 - finger_tip_coordinates[0] * 100) > finger_tip_coordinates[3] * 100 - finger_tip_coordinates[2] * 100:
                        move_x = -1
                        move_y = 0
                    else:
                        move_x = -1
                        move_y = 1
                else:
                    if finger_tip_coordinates[3] * 100 - finger_tip_coordinates[2] * 100 + 0.3 > 0:
                        move_x = 0
                        move_y = 1
                # Для змейки
                '''if finger_tip_coordinates[0] * 10 < finger_tip_coordinates[1] * 10:
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
                        move_y = 1
                        move_x = 0
                else: pass'''
                raised_rightukaz = [move_x, move_y]
                #print(raised_rightukaz)
                '''for i, landmark in enumerate(hand_landmarks.landmark):
                    x, y, z = int(landmark.x * img.shape[1]), int(landmark.y * img.shape[0]), int(landmark.z * 100)
                    if i == 8:
                        print(f'Point {i}: ({x}, {y}, {z})')'''
        return img, raised_rightukaz

'''class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
pt = Point(1, 2)
print(pt.__dict__)'''