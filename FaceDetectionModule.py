import cv2
import numpy
import mediapipe as mp
import time
class FaceDetector():
    def __init__(self,minDetection = 0.5):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.minDetection = minDetection
        self.FaceDetection = self.mpFaceDetection.FaceDetection(self.minDetection)

    def findFaces(self,img,draw = True):
        imRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.FaceDetection.process(imRGB)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                    #mpDraw.draw_detection(img,detection)
                bboxC = detection.location_data.relative_bounding_box
                Score = str(int(detection.score[0]*100)) + "%" #dection percentage
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw),int(bboxC.ymin * ih),\
                       int(bboxC.width * iw),int(bboxC.height * ih) #(x,y,w,h)
                detectionPercentage = detection.score[0] * 100
                bboxs.append([id,bbox,detectionPercentage])
                if draw:
                    self.fancyDraw(img,bbox)
                    cv2.putText(img, Score, (bbox[0], bbox[1]-10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
        return bboxs, img
    def fancyDraw(self,img, bbox,l=30,t=3,rt= 1):
        x,y,w,h = bbox
        x1,y1 =x + w, y+h
        cv2.rectangle(img, bbox, (255, 255, 0), rt)
        # TOP LEFT X,Y
        cv2.line(img,(x,y),(x+l,y),(255,255,0),t)
        cv2.line(img, (x, y), (x , y+l), (255, 255, 0), t)
        # TOP RIGHT X1,Y
        cv2.line(img, (x1, y), (x1 - l, y), (255, 255, 0), t)
        cv2.line(img, (x1, y), (x1, y + l), (255, 255, 0), t)
        # BOTTOM LEFT X,Y1
        cv2.line(img, (x, y1), (x + l, y1), (255, 255, 0), t) #ngang
        cv2.line(img, (x, y1), (x, y1 - l), (255, 255, 0), t) # collum
        # BOTTOM RIGHT X1,Y1
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 255, 0), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 255, 0), t)
        return img


def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detector = FaceDetector()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        bboxs, img = detector.findFaces(img,draw = True)
        if len(bboxs) != 0:
            print(bboxs[0])
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord("q"):
            break
if __name__ == "__main__":
    main()