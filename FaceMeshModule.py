import cv2
import numpy
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self, static_image_mode=False,
                       max_num_faces=1,
                       refine_landmarks=False,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.min_tracking_confidence = min_tracking_confidence
        self.min_detection_confidence = min_detection_confidence
        self.refine_landmarks = refine_landmarks
        self. max_num_faces = max_num_faces
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh()
        self.drawSpec =self.mpDraw.DrawingSpec(thickness=1,circle_radius=1)
    def findFaceMesh(self,img,draw= True):
        imRGB =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = self.faceMesh.process(imRGB)
        faces = []
        if results.multi_face_landmarks:

            for facelsm in results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, facelsm, self.mpFaceMesh.FACEMESH_CONTOURS,
                                      self.drawSpec,self.drawSpec)
                face = []
                for id, lm in enumerate(facelsm.landmark):
                    iw, ih, ic = img.shape
                    x, y = int(lm.x*ih), int(lm.y*iw)
                    cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.3, (255, 0, 0),1)
                    face.append([id,x,y])
                faces.append(face)
        return img, faces


def main():
    cap = cv2.VideoCapture(0)  # video link
    pTime = 0
    detector = FaceMeshDetector()
    while True:
        success, old_img = cap.read()
        img = cv2.flip(old_img, 1)
        img, faces = detector.findFaceMesh(img)
        if len(faces) != 0:
            print(faces)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord("q"):
            break
if __name__ == "__main__":
    main()