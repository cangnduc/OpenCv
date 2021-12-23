import cv2
import numpy
import mediapipe as mp
import time
import handdection_module as hdt

cap = cv2.VideoCapture(0)  # video link
pTime = 0

while True:
    success, old_img = cap.read()
    img = cv2.flip(old_img, 1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):
        break


