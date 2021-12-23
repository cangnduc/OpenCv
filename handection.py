import cv2
import numpy
import mediapipe as mp
import time
pTime = 0
cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils
while True:
	success, old_img = cap.read()
	img = cv2.flip(old_img, 1)
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	#newimgRGB = cv2.flip(imgRGB,1)

	results = hands.process(imgRGB)
	if results.multi_hand_landmarks:
		#print(len(results.multi_hand_landmarks)) // number of hands
		for handlms in results.multi_hand_landmarks:

			for id, lm in enumerate(handlms.landmark):
				h, w, c, = img.shape
				cx, cy = int(lm.x*w), int(lm.y*h)
				if id == 8:
					cv2.circle(img,(cx,cy),15,(255,0,0),4)
				mpdraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)
				print(cx,cy)
	cTime = time.time()
	fps = 1/(cTime-pTime)
	pTime = cTime

	cv2.putText(img, str(int(fps)),(50,50), cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

	cv2.imshow("Image", img)
	if cv2.waitKey(1) == ord("q"):
		break


cv2.destroyAllWindows()

