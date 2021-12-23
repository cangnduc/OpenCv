import cv2
import numpy as np

from StackImages import stackImages

def getcontours(img):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

path = "shape.png"
img = cv2.imread(path)

imgBlank = np.zeros_like(img)
imGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imBlur = cv2.GaussianBlur(imGray, (7, 7), 1)
imCanny = cv2.Canny(imBlur, 50, 50)

imgStack = stackImages(0.6, ([[img, imGray, imBlur],
                       [imCanny, imgBlank, imgBlank]]))

cv2.imshow("images", imgStack)

cv2.waitKey(0)
