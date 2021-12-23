import cv2
import numpy
import mediapipe as mp
import time
pTime = 0
cap = cv2.VideoCapture(0)
mpFaceDetection = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
FaceDetection = mpFaceDetection.FaceDetection()
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = FaceDetection.process(imRGB)
    if results.detections:
        for id, detection in enumerate(results.detections):
            #mpDraw.draw_detection(img,detection)
            bboxC = detection.location_data.relative_bounding_box
            Score = str(int(detection.score[0]*100)) + "%" #dection percentage

            ih, iw, ic = img.shape
            bbox = int(bboxC.xmin * iw),int(bboxC.ymin * ih),\
                   int(bboxC.width * iw),int(bboxC.height * ih) #(x,y,w,h)
            cv2.rectangle(img,bbox,(255,255,0),2)
            cv2.putText(img, Score, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,40),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) == ord("q"):
        break