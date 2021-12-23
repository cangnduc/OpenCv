import math

import cv2
import numpy as np
import mediapipe as mp
import time
import handdection_module as hdt
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]
print(minVol, maxVol, volRange)
cap = cv2.VideoCapture(0)  # video link
wcam, hcam = 640, 480
cap.set(3, wcam)
cap.set(4, hcam)
pTime = 0
hand_detector = hdt.HandDetector(detectionCon=0.6)
volBar = 400
perc = 0
while True:
    success, old_img = cap.read()
    img = cv2.flip(old_img, 1)
    img = hand_detector.findHands(img)
    lmlist = hand_detector.findHandsPosition(img, draw=False)
    if len(lmlist) != 0:
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [20, 150], [minVol, maxVol])
        # volume.SetMasterVolumeLevel(vol, None)
        volBar = np.interp(length, [20, 150], [400, 150])
        perc = np.interp(length, [20, 150], [0, 100])
    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 255), 2)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 255), cv2.FILLED)
    cv2.putText(img, str(int(perc)), (50, 140), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0),2)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):
        break
