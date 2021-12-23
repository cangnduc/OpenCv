import cv2
import mediapipe as mp
import time


class PoseDetector():
    def __init__(self, static_image_mode=False,
                 model_complexity=1,
                 smooth_landmarks=True,
                 enable_segmentation=False,
                 smooth_segmentation=True,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.mode = static_image_mode
        self.complex = model_complexity
        self.smooth = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complex, self.smooth,
                                     self.enable_segmentation, self.smooth_segmentation, self.min_detection_confidence
                                     , self.min_tracking_confidence)
        self.drawPose = mp.solutions.drawing_utils

    def findPose(self, img, draw=True):
        imRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imRGB)

        if self.results.pose_landmarks:
            if draw:
                self.drawPose.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

    def getPosition(self, img, draw=True):
        if self.results.pose_landmarks:
            lmlist = []
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)
        return lmlist


def main():
    pTime = 0
    cap = cv2.VideoCapture(0)  # ("video Link")
    detector = PoseDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img2 = detector.findPose(img)
        lmlist = detector.getPosition(img, draw= False)
        cv2.circle(img, (lmlist[0][1], lmlist[0][2]), 6, (255, 0, 255), cv2.FILLED)
        print(lmlist)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (30, 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord("q"):
            break


if __name__ == "__main__":
    main()
