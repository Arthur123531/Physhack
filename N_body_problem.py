from itertools import count

import pygame
import math
import numpy as np
from  random import randint
from button import Button


# Window dimensions and more
WIDTH, HEIGHT = 1040, 680
BG = pygame.image.load('galaxy_pixel.png')

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
R_EARTH = 6371e3
Scaling = R_EARTH/25
G = 6.67430e-11
speed_cap = 2

#sprites
EARTH_SPRITE = pygame.image.load('Earth.png')

screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Body:
    def __init__(self, x:int|None = None, y:int|None = None, vx:float|None = None, vy:float|None = None, mass:float|None = None, radius:int|None = None, color:str|tuple[int]|None = None, body_type:str = "asteroid", type_props = {}, sprite = None):
        if x is not None:
            self.x = x
        elif body_type == "asteroid":
            self.x = randint(WIDTH//4, 3*WIDTH//4)
        else:
            self.x = WIDTH//2
        if y is not None:
            self.y = y
        elif body_type == "asteroid":
            self.y = randint(HEIGHT //4, 3*HEIGHT//4)
        else:
            self.y = HEIGHT//2
        if vx is not None:
            self.vx = vx
        elif body_type == "planet":
            self.vx = 0
        else: 
            self.vx = randint(-100, 100)/200
        if vy is not None:
            self.vy = vy
        elif body_type == "planet":
            self.vy = 0
        else: 
            self.vy = randint(-100, 100)/200
        if mass is not None:
            self.mass = mass
        elif body_type == "asteroid":
            self.mass = M_ASTEROID
        elif body_type == "planet":
            self.mass = M_EARTH
        if radius is not None:
            self.radius = radius
        elif body_type == "planet":
            self.radius = 80
        else:
            self.radius = 5
        if color is not None:
            self.color = color
        elif body_type == "planet":
            self.color = BLUE
        else:
            self.color = BLACK
        self.trail = [(self.x, self.y)]
        self.body_type = body_type
        if sprite is not None:
            self.sprite = sprite
        elif body_type == "planet":
            self.sprite = EARTH_SPRITE
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
        if self.body_type == "planet":
            return
        for i in range(max(0, len(self.trail) - 500), len(self.trail)):
                pygame.draw.circle(screen, self.color, (int(self.trail[i][0]), int(self.trail[i][1])), 2)
    
    def update_position(self):
        self.x += self.vx
        self.x -= EARTH.vx
        self.y += self.vy
        self.y -= EARTH.vy
        self.trail.append((self.x, self.y))
        if self.sprite is not None:
            self.scale_and_center_sprite()
        else:
            self.circle = pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def apply_force(self, fx, fy):
        ax = fx / self.mass
        ay = fy / self.mass
        if (ax**2+ay**2)**.5 < 10:
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


   
########################################################################### MAIN MENU    
def main_menu(): #main menu screen 
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True 
    while running:
        screen.blit(BG, (0,0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(50).render('PLANET LAND', True, '#b68f40')
        menu_rect = menu_text.get_rect(center=(WIDTH //2,100))

        play_button = Button(image = pygame.image.load('Play Rect.png'), pos = (WIDTH //2, 250),
                             text_input = 'PLAY', font = get_font(75), base_color = '#d7fcd4', hovering_color = 'White')
        quit_button = Button(image = pygame.image.load('Quit Rect.png'), pos = (WIDTH //2, 450),
                             text_input = 'QUIT', font = get_font(75), base_color = '#d7fcd4', hovering_color = 'White')
        
        screen.blit(menu_text, menu_rect)

        for button in [play_button, quit_button]:
             button.changeColor(menu_mouse_pos)
             button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                  #pygame.quit()
                  running = False 
                  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    main()
                if quit_button.checkForInput(menu_mouse_pos):
                    running = False 
                    #pygame.quit()
                    
        #pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
###########################################################################            
             

#game loop
def main():
    pygame.init()
    pygame.display.set_icon(EARTH_SPRITE.convert_alpha())
    clock = pygame.time.Clock()

    # Timer initialization
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    timer_counter = 1000 # Change to whatever time we give

    timer_font = pygame.font.SysFont('Arial', 30)
    timer_text = timer_font.render('Timer: ' + str(timer_counter), True, BLACK)


    # Initial conditions
    

    bodies = [EARTH]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == timer_event:
                if timer_counter % 10 == 0:
                    bodies.append(Body(body_type="asteroid"))
                timer_counter -= 1
                timer_text = timer_font.render('Timer: ' + str(timer_counter), True, BLACK)
                if timer_counter == 0:
                    pygame.time.set_timer(timer_event, 0)
                    timer_text = timer_font.render('You survived !' , True, BLACK)

        screen.fill(WHITE)

        for i, body in enumerate(bodies):
            collisions = 0
            for j in range(len(bodies)):
                if i != j:
                    fx, fy = calculate_force(body, bodies[j])
                    body.apply_force(fx, fy)

            body.update_position()

            # Ensure bodies stay within the screen boundaries
            if body.x < 0 or body.x > WIDTH:
                body.vx *= -1
            if body.y < 0 or body.y > HEIGHT:
                body.vy *= -1

            # Draw trail
            body.tail_display()


            if body != EARTH:
                if body.circle.colliderect(EARTH.circle):
                    bodies.remove(body)
                    collisions +=1
                    if len(bodies) == 1:
                       bodies.append(Body(body_type="asteroid"))
        if bodies[0].mass > 2e30:
            pygame.quit()
            

        #Draw timer
        screen.blit(timer_text, (0,0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_menu()
    #main()
