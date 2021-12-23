import cv2
import mediapipe as mp
import time
import handdection_module as htd
detector = htd.HandDetector
pTime = 0
cap = cv2.VideoCapture(0) #("video Link")
mpPose = mp.solutions.pose
pose = mpPose.Pose()
drawPose = mp.solutions.drawing_utils

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    imRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = pose.process(imRGB)

    if results.pose_landmarks:
        drawPose.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx,cy), 6, (255,0,255), cv2.FILLED)
            #print(id,lm)
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)),(30,40), cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):
        break
