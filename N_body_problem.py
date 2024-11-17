from itertools import count

import pygame
import math
import numpy as np
import random 
from button import Button
from blink_stars import Star


# Window dimensions and more
WIDTH, HEIGHT = 1040, 680
BG = pygame.image.load('galaxy_pixel.png')
BG_DIM =  pygame.image.load('galaxy_pixel_dim.png')
GAME_OVER_BG = pygame.image.load('GO_BG.png')
GAME_OVER_BG = pygame.transform.scale(GAME_OVER_BG, (1040, 680))
YOUWIN_BG = pygame.image.load('you_win.png')
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
EARTH_MASS = 5.9722 * 10**24

#Constants
M_EARTH = 5.972e24
M_ASTEROID = 1e12
M_MOON = 7.34767309e22
R_EARTH = 6371e3
Scaling = R_EARTH/25
G = 6.67430e-11
speed_cap = 2
acc_cap = 10
MOON_DIST = 384400000/Scaling/10
MOON_MASS = 7.342e23
MOON_VEL = 1022/Scaling*150
#sprites
EARTH_SPRITE = pygame.image.load('Earth2.png')
ASTEROID_SPRITE = pygame.image.load("asteroid2.png")
MOON_SPRITE = pygame.image.load("moon2.png")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

def asteroid_cords_and_speed_generator():
    # Choose a random side of the screen
    side = random.choice(['top', 'bottom', 'left', 'right'])
    
    # Generate position on the chosen side
    if side == 'top':
        x = random.uniform(0, WIDTH)
        y = 0
    elif side == 'bottom':
        x = random.uniform(0, WIDTH)
        y = HEIGHT
    elif side == 'left':
        x = 0
        y = random.uniform(0, HEIGHT)
    else:  # right
        x = WIDTH
        y = random.uniform(0, HEIGHT)
    
    # Calculate velocity components directed towards the center
    center_x, center_y = WIDTH // 2, HEIGHT // 2
    dx = center_x - x
    dy = center_y - y
    
    # Normalize the velocity vector
    speed = np.sqrt(dx**2 + dy**2)
    vx = dx / speed
    vy = dy / speed
    
    # Scale the velocity to a desired speed (adjust as needed)
    desired_speed = 1  # Adjust this value to control the asteroid's speed
    vx *= desired_speed
    vy *= desired_speed
    
    return x, y, vx, vy




class SimplifiedBody:
    """A simplified version of Body class for orbit calculations"""
    def __init__(self, x, y, vx, vy, mass):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass

class Body:
    def __init__(self, x:int|None = None, y:int|None = None, vx:float|None = None, vy:float|None = None, mass:float|None = None, radius:int|None = None, color:str|tuple[int]|None = None, body_type:str = "asteroid", type_props = {}, sprite = None):
        if x is not None:
            self.x = x
        elif body_type == "asteroid":
            pass
        elif body_type == "moon":
            self.x = int(EARTH.x + MOON_DIST)
        else:
            self.x = WIDTH//2
        if y is not None:
            self.y = y
        elif body_type == "asteroid":
            pass
        elif body_type == "moon":
            self.y = EARTH.y 
        else:
            self.y = HEIGHT//2
        if vx is not None:
            self.vx = vx
        elif body_type == "planet":
            self.vx = 0
        elif body_type == "moon":
            self.vx = EARTH.vx
        elif body_type == "asteroid": 
            pass
        if vy is not None:
            self.vy = vy
        elif body_type == "planet":
            self.vy = 0
        elif body_type == "moon":
            self.vy = EARTH.vy+MOON_VEL
        elif body_type == "asteroid": 
            self.x, self.y, self.vx, self.vy = asteroid_cords_and_speed_generator()
        if mass is not None:
            self.mass = mass
        elif body_type == "asteroid":
            self.mass = M_ASTEROID
        elif body_type == "planet":
            self.mass = M_EARTH
        elif body_type == "moon":
            self.mass = MOON_MASS
        if radius is not None:
            self.radius = radius
        elif body_type == "planet":
            self.radius = 80
        elif body_type == "moon":
            self.radius = 50
        else:
            self.radius = 50
        if color is not None:
            self.color = color
        elif body_type == "planet" or body_type == "moon":
            self.color = BLUE
        else:
            self.color = WHITE
        self.trail = [(self.x, self.y)]
        self.body_type = body_type
        self.counter = 0
        if sprite is not None:
            self.sprite = sprite
        elif body_type == "planet":
            self.sprite = EARTH_SPRITE.convert_alpha()
        elif body_type == "asteroid":
            self.sprite = ASTEROID_SPRITE.convert_alpha()
        elif body_type == "moon":
            self.sprite = MOON_SPRITE.convert_alpha()
        else:
            self.sprite = None
        if self.sprite is not None:
            self.scale_and_center_sprite()
        else:
            self.circle = pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        if body_type == "asteroid" and "visible" in type_props.keys():
            self.visible = type_props["visible"]
    def scale_and_center_sprite(self):
        if self.sprite is None:
            return

        # Calculate the scale factor based on the radius
        scale_factor = self.radius / max(self.sprite.get_width(), self.sprite.get_height())

        # Scale the sprite
        self.sprite = pygame.transform.smoothscale(
            self.sprite,
            (int(self.sprite.get_width() * scale_factor),
             int(self.sprite.get_height() * scale_factor))
        )
        # Center the sprite
        self.circle = screen.blit(self.sprite, self.sprite.get_rect(center=(int(self.x), int(self.y))))
    
    def tail_display(self):
        if self!=EARTH:
            for i in range(max(0, len(self.trail) - 500), len(self.trail)):
                pygame.draw.circle(screen, self.color, (int(self.trail[i][0]), int(self.trail[i][1])), 2)
    
    def update_position(self):
        self.x += self.vx
        self.x -= EARTH.vx
        self.y += self.vy
        self.y -= EARTH.vy
        self.trail.append((self.x, self.y))

    def draw_body(self):
        if self.sprite is not None:
            self.scale_and_center_sprite()
        else:
            self.circle = pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_force(self, fx, fy):
        ax = fx / self.mass
        ay = fy / self.mass
        if (ax**2+ay**2)**.5 >= acc_cap:
            ax /= (ax**2+ay**2)**.5
            ay /= (ax**2+ay**2)**.5
            ax *= acc_cap
            ay *= acc_cap
        self.vx += ax
        self.vy += ay
        if self.vx**2+self.vy**2 > speed_cap**2:
            self.vx /= (self.vx**2+self.vy**2)**.5
            self.vy /= (self.vx**2+self.vy**2)**.5
            self.vx *= speed_cap
            self.vy *= speed_cap


def calculate_force(body1, body2):
    dx = (body2.x - body1.x)*Scaling*10
    dy = (body2.y - body1.y)*Scaling*10
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        force = G * body1.mass * body2.mass / (dist * dist)
        angle = math.atan2(dy, dx)
        fx = force * math.cos(angle)
        fy = force * math.sin(angle)
        return fx, fy
    else:
        return 0, 0

#Planet
EARTH = Body(body_type="planet")

  
def get_font(size): 
    #pygame.font.Font("font.ttf", size) NOT WORKING
    pygame.font.init()
    return pygame.font.Font("font.ttf", size)