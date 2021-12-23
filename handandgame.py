import cv2
import mediapipe as mp
import time
import numpy as np
import pygame
import os
width , height  = 600, 600
Win = pygame.display.set_mode((width,height))
pygame.init()
white = (255,255,255)
cap = cv2.VideoCapture(0)
cTime = 0
pTime = 0
fps = 30
mpHands = mp.solutions.hands
hands = mpHands.Hands( )
mpDraw = mp.solutions.drawing_utils
run = True
clock = pygame.time.Clock()
# red_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
# YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
# yellow_spaceship =pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(55,40))
def draw_window(cx,cy):
	Win.fill(white)
	
	Win.blit(yellow_spaceship,(cx,cy))
	pygame.display.update()
	

def findxy():
	
	if result.multi_hand_landmarks:
		for handLms in result.multi_hand_landmarks:
			for id, lm in enumerate(handLms.landmark):
				h,w,c = img.shape
				cx, cy = int(lm.x*w), int(lm.y*h)
				if id ==4:
					cv2.circle(img,(cx,cy), 15, (255,0,255),3)
					
				mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
				return cx, cy


	

	
	
	
while True:
	success, img = cap.read()
	imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	result = hands.process(imgRGB)
	clock.tick(fps)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	
	if findxy():
		try:
			x,y =findxy()
			draw_window(x,y)
		except:
			pass

	
	cv2.imshow("Image", img)
	