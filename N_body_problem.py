import pygame, sys 
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


G = 6.6743e-11
speed_cap = 2



class Body:
    def __init__(self, x, y, vx, vy, mass, color, radius, body_type, type_props = {}):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = color
        self.radius = radius 
        self.trail = [(x, y)]

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.trail.append((self.x, self.y))

    def apply_force(self, fx, fy):
        ax = fx / self.mass
        ay = fy / self.mass
        if (ax**2+ay**2)**.5 < 1e-1:
            self.vx += ax
            self.vy += ay
        if self.vx**2+self.vy**2 > speed_cap**2:
            self.vx /= (self.vx**2+self.vy**2)**.5
            self.vy /= (self.vx**2+self.vy**2)**.5
            self.vx *= speed_cap
            self.vy *= speed_cap

def calculate_force(body1, body2):
    dx = body2.x - body1.x
    dy = body2.y - body1.y
    dist = math.sqrt(dx*dx + dy*dy)
    if dist > 0:
        force = G * body1.mass * body2.mass / (dist * dist)
        angle = math.atan2(dy, dx)
        fx = force * math.cos(angle)
        fy = force * math.sin(angle)
        return fx, fy
    else:
        return 0, 0



  
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
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Initial conditions (scaled down)
    earth = Body(WIDTH // 2 - 10, HEIGHT // 2 - 10, 0, 0, EARTH_MASS, RED, 25, '')
    body2 = Body(WIDTH// 2, HEIGHT//2 -55, 0.0005, 0.0005, 1, GREEN, 5,'')
    body3 = Body(WIDTH // 2 + 10, HEIGHT // 2 - 10, 1, 1, 1, BLUE,5,'')
    body4 = Body(WIDTH // 2 + 10, HEIGHT // 2 + 10, 0, 0, 1, BLACK,5,'')
    body5 = Body(WIDTH // 2 + 20, HEIGHT // 2 + 00, 0, 0, 1, ORANGE,5,'')
    body6 = Body(WIDTH // 2 - 20, HEIGHT // 2 - 00, 0, 0, 1, PINK,5,'')
    body7 = Body(WIDTH // 2 + 00, HEIGHT // 2 + 20, 0, 0, 1, PURPLE,5,'')
    body8 = Body(WIDTH // 2 - 00, HEIGHT // 2 - 20, 0, 0, 1, YELLOW,5,'')

    bodies = [earth, body2]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)

        for i, body in enumerate(bodies):
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
            for k in range(max(0, len(body.trail) - 500), len(body.trail)):
                pygame.draw.circle(screen, body.color, (int(body.trail[k][0]), int(body.trail[k][1])), 2)

            # Draw body
            pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), body.radius)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main_menu()
    #main()
