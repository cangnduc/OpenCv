import cv2
import numpy
import mediapipe as mp
import time
class PoseDetector():
	def __init__(self,static_image_mode=False,
					   model_complexity=1,
					   smooth_landmarks=True,
					   enable_segmentation=False,
					   smooth_segmentation=True,
					   min_detection_confidence=0.5,
					   min_tracking_confidence=0.5):
		self.mode = static_image_mode
		self.complex =model_complexity
		self.smooth =smooth_landmarks
		self.segenable = enable_segmentation
		self.smooth_segmentation =smooth_segmentation
		self.min_detection_confidence = min_detection_confidence
		self. min_tracking_confidence = min_tracking_confidence
		self.mpPose = mp.solutions.pose
		self.pose = self.mpPose.Pose()
		self.drawPose = mp.solutions.drawing_utils
	def findPose(self,img, draw = True):
		imRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.pose.process(imRGB)
		if self.results.pose_landmarks:
			if draw:
				self.drawPose.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
	def findPosePosition(self,img, draw = True):
		if self.results.pose_landmarks:
			lmlist = []
			for id, lm in enumerate(self.results.pose_landmarks.landmark):
				h, w, c = img.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				lmlist.append([id, cx, cy])
				if draw:
					cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)

		return lmlist
class HandDetector():
	def __init__(self, mode = False, maxHand =2, detectionCon =0.5, trackCon = 0.5):
		self.mode = mode
		self.maxHands = maxHand
		self.detectionCon = detectionCon
		self.trackCon = trackCon
		self.mpHands = mp.solutions.hands
		self.hands = self.mpHands.Hands(self.mode,self.maxHands,
										self.detectionCon,self.trackCon
										)
		self.mpdraw = mp.solutions.drawing_utils

	def findHands(self, img, draw = True):
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)
		if self.results.multi_hand_landmarks:
			#print(len(results.multi_hand_landmarks)) // number of hands
			for handlms in self.results.multi_hand_landmarks:
				if draw:
					self.mpdraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
		return img

	def findHandsPosition(self, img, handNo=0,draw=True):
		lmList = []
		imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		self.results = self.hands.process(imgRGB)
		if self.results.multi_hand_landmarks:

			#myHand = self.results.multi_hand_landmarks[handNo] # chon 1 hand de lay gia tri
			for num, myHand in enumerate(self.results.multi_hand_landmarks): #lay het hands
				for id, lm in enumerate(myHand.landmark):
					h, w, c, = img.shape
					cx, cy, = int(lm.x * w), int(lm.y * h)
					lmList.append([num,id,cx,cy])
					if draw:
						cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

		return lmList

def main():
	cap = cv2.VideoCapture(0)
	pTime = 0
	dector = PoseDetector()
	hand_det = HandDetector()
	while True:
		success, old_img = cap.read()
		img = cv2.flip(old_img, 1)
		img = hand_det.findHands(img)
		#img2 = dector.findPose(img)
		#PoseP =dector.findPosePosition(img)
		HandP = hand_det.findHandsPosition(img,draw = False)
		print(HandP)

		cTime = time.time()
		fps = 1 / (cTime - pTime)
		pTime = cTime

		cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

		cv2.imshow("Image", img)
		if cv2.waitKey(1) == ord("q"):
			break
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()