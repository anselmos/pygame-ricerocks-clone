import pygame, spritesheet, os.path
from pygame.locals import *

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

# helper function for loading images
# define the current path
main_dir = os.path.split(os.path.abspath(__file__))[0]
def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'art', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()
	
def load_sound(file):
    file = os.path.join(main_dir, 'audio', file)
    sound = pygame.mixer.Sound(file)
    return sound


def main():
	# Init everything
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption('Rice Rocks')
	
	# Load the sounds
	soundtrack = load_sound('music.ogg')
	missile_sound = load_sound('shoot.wav')
	ship_thrust_sound = load_sound('thrust.wav')
	explosion_sound = load_sound('explode.wav')
	
	# Draw the background
	background = load_image('nebula_blue.f2014.png')
	screen.blit(background, (0,0))
	pygame.display.flip()
	
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