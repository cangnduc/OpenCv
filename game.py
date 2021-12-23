import pygame
pygame.init() 
width , height = 600, 600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("dwad")
run = True
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			#sys.exit(0)

	win.fill((255,255,0))

	