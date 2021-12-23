import cv2
import numpy
import mediapipe as mp
import time

cap = cv2.VideoCapture(0) #video link
pTime = 0
mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawSpec =mpDraw.DrawingSpec(thickness=1,circle_radius=1)
while True:
    success, old_img = cap.read()
    img = cv2.flip(old_img, 1)
    imRGB =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imRGB)
    if results.multi_face_landmarks:
        for facelsm in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, facelsm, mpFaceMesh.FACEMESH_CONTOURS,
                                  drawSpec,drawSpec)
            for id, lm in enumerate(facelsm.landmark):
                iw, ih, ic = img.shape
                x, y = int(lm.x*ih), int(lm.y*iw)
                cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
                #print(id,x,y)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) == ord("q"):
        break


