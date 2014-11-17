# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
#ship_info = ImageInfo([135, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack 	= simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def turn(self, direction):
        self.angle_vel = direction
        
    def move(self, thrust):
        self.thrust = thrust
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
        #print self.thrust
    def shoot(self):
        global missle_group       
        base_missle_speed = 6
        forward = angle_to_vector(self.angle)
        vel = [0, 0]
        vel[0] = self.vel[0] + forward[0] * base_missle_speed
        vel[1] = self.vel[1] + forward[1] * base_missle_speed

        pos = [0, 0]
        pos[0] = self.pos[0] + (self.radius * forward[0])
        pos[1] = self.pos[1] + (self.radius * forward[1])
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound)
        missle_group.add(a_missile)
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + 90, self.image_center[1]] , self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Friction update
        c = 0.015
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
        
        # Screen wrapping
           
        if self.pos[1] <= self.radius or self.pos[1] >= HEIGHT:
            self.pos[1] = self.pos[1] % HEIGHT
                      
        if self.pos[0] <= 0 or self.pos[0] >= WIDTH:
            self.pos[0] = self.pos[0] % WIDTH
            
        # Thrusting forward      
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * 0.1
            self.vel[1] += forward[1] * 0.1
        self.angle += self.angle_vel
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collide(self, other_object):
        distance = dist(self.pos, other_object.get_position())
        
        if distance > self.radius + other_object.get_radius():
            return False
        elif distance < self.radius + other_object.get_radius():
            return True
   
    def draw(self, canvas):
        if self.animated:
            explosion_index = self.age % 24
            canvas.draw_image(self.image, [self.image_center[0] + explosion_index * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.age += 1
        # Screen wrapping
           
        if self.pos[1] <= self.radius or self.pos[1] >= HEIGHT:
            self.pos[1] = self.pos[1] % HEIGHT
                      
        if self.pos[0] <= 0 or self.pos[0] >= WIDTH:
            self.pos[0] = self.pos[0] % WIDTH
            
        self.angle += self.angle_vel
        
        # check lifespan
        if self.age < self.lifespan:
            return False
        else:
            return True

           
def draw(canvas):
    global time, score, lives, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    #a_rock.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missle_group, canvas)
    process_sprite_group(explosion_group, canvas)
    #a_missile.draw(canvas)
    
    # draw score
    canvas.draw_text("Score: %d"%score, (10, 50), 50, 'white')
    canvas.draw_text("Lives: %d"%lives, (620, 50), 50, 'white')
    # update ship and sprites
    my_ship.update()
    #a_rock.update()
#    a_missile.update()
    # check for collisions rock vs ship
    if group_collide(rock_group, my_ship):
        lives -= 1
    score += group_group_collide(missle_group, rock_group)
    #score += score_add
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    if lives == 0:
        restart()
            
# helper function for drawing groups
def process_sprite_group(group, canvas):
    for elem in set(group):
        elem.draw(canvas)
        is_old = elem.update()
        if is_old:
            group.remove(elem)
          
# helper function for group collisions
def group_collide(group, other_object):
    global explosion_group
    for elem in set(group):
        if elem.collide(other_object):
            an_explosion = Sprite(elem.get_position(), [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(an_explosion)
            group.remove(elem)
            return True
    else:
        return False

def group_group_collide(group1, group2):
    score_add = 0
    for elem in set(group1):
        if group_collide(group2, elem):
            group1.remove(elem)
            score_add += 1
    return score_add

def score_to_range():
    global score
    if score < 10:
        return 1
    elif score >= 10 and score < 20:
        return 2
    elif score >= 20:
        return 4
    else:
        return 5

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, started, my_ship, score
    rang = score_to_range()
    if len(rock_group) < 11 and started:
        vel = [0, 0]
        vel[0] = random.randrange(-(rang), rang + 1)
        vel[1] = random.randrange(-(rang), rang + 1)
    
        x = random.randrange(0, 800)
        y = random.randrange(0, 600) 

        ang = (random.randrange(-5, 11) * 0.01)
      
        a_rock = Sprite([x, y], vel, 0, ang, asteroid_image, asteroid_info)
        distance = dist(my_ship.get_position(), a_rock.get_position())
        if distance > 100:
            rock_group.add(a_rock)
        
    else:
        return
    
def restart():
    global rock_group, started
    started = False
    for elem in set(rock_group):
        rock_group.discard(elem)
# key handlers
def on_keydown(key):
    global my_ship
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn(-0.1)
        
    if key == simplegui.KEY_MAP['right']:
        my_ship.turn(0.1)
        
    if key == simplegui.KEY_MAP['up']:
        my_ship.move(True)
        
    if key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
    
def on_keyup(key):
    global my_ship
    if key == simplegui.KEY_MAP['left']:
        my_ship.turn(0)
    
    if key == simplegui.KEY_MAP['right']:
        my_ship.turn(0)
        
    if key == simplegui.KEY_MAP['up']:
        my_ship.move(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    lives = 3
    score = 0
    soundtrack.rewind()
    soundtrack.play()
    if (not started) and inwidth and inheight:
        started = True

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [4, 4], 0, -0.05, asteroid_image, asteroid_info)
rock_group = set([])
missle_group = set([])
explosion_group = set([])
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(on_keydown)
frame.set_keyup_handler(on_keyup)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
