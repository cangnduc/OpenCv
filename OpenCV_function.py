import cv2
import numpy as np

import time



#translate the image by value of x and y
def translateImg(img, x,y):
    transMate = np.float32([[1,0,x],[0,1,y]])
    demension = (img.shape[1], img.shape[0])
    return cv2.warpAffine(img, transMate, demension)
# rotate the image
def rotateImg(img, angle, rotationPoint = None):
    (height, width) = img.shape[0:2]
    if rotationPoint == None:
        rotationPoint = (height//2,width//2)
    rotMate = cv2.getRotationMatrix2D(rotationPoint,angle,1.0)
    demension = (width,height)
    return cv2.warpAffine(img, rotMate,demension)


def displayVideo():
    cap = cv2.VideoCapture(0)  # video link
    pTime = 0
    while True:
        success, old_img = cap.read()
        img = cv2.flip(old_img, 1)
        
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord("q"):
            break

img2 = cv2.imread("shape.png")
gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(3,3),cv2.BORDER_DEFAULT)

canny_gray = cv2.Canny(gray,200,100)
canny_blur = cv2.Canny(blur,200,100)
cv2.imshow("canny_gray",canny_gray)
cv2.imshow("canny_blur",canny_blur)
contours, hierarchies = cv2.findContours(canny_gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
print(len(contours))

cv2.waitKey(0)

