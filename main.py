import pygame
from pygame.locals import *

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

def main():
	# Init everything
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Rice Rocks')

	# Init game objects
	clock = pygame.time.Clock()

	# Game loop
	while 1:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == QUIT:
				return
		pygame.display.flip()
print ("If you can see this, then PyGame was succesfully imported")


if __name__ == '__main__': main()