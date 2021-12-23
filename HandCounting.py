import cv2
import numpy
import mediapipe as mp
import time
import numpy as np
import handdection_module as hdt
import os
import requests
import imutils

# url = "http://192.168.1.9:8080/shot.jpg"q
wcam, hcam = 1280, 720
cap = cv2.VideoCapture(0)  # video link
pTime = 0
cap.set(3, wcam)
cap.set(4, hcam)
folderPath = "Assets"
myList = os.listdir(folderPath)
overlaylist = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlaylist.append(image)
detector = hdt.HandDetector(detectionCon=0.9)
tipids = [4, 8, 12, 16, 20]
while True:
    success, old_img = cap.read()
    img = cv2.flip(old_img, 1)
    # using phone as camera
    # img_resp = requests.get(url)
    # img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)
    # img = cv2.imdecode(img_arr, -1)
    # img = imutils.resize(img, width=1280, height=720)

    img = detector.findHands(img)
    lmlist = detector.findHandsPosition(img, draw=False)
    if len(lmlist) != 0:
        # print(lmlist[0][0])q

        fingers = []
        if lmlist[0][0] == 0:
            if lmlist[tipids[0]][2] > lmlist[tipids[0] - 1][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        for id in range(1, 5):
            if lmlist[0][0] == 0:
                if lmlist[tipids[id]][3] < lmlist[tipids[id] - 1][3]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        print(sum(fingers), fingers)
        totalfingers = sum(fingers)
        h, w, c = overlaylist[0].shape
        img[0:h, 0:w] = overlaylist[totalfingers - 1]
        cv2.rectangle(img, (20, 225), (160, 425), (255, 0, 255), cv2.FILLED)
        cv2.putText(img,str(totalfingers),(45,375),cv2.FONT_HERSHEY_TRIPLEX,5,(255,255,255),3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):
        break
