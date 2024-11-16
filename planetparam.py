import pygame
import random
import numpy as np
from N_body_problem import Body
"""
    left to do 
    - change by how much the mass increases when asteroid hits 
    - change by how much the radius increases when asteroid hits 
    """
pygame.init()

window = pygame.display.set_mode((1040,680))
running = True
r = 25 

planet_skin = pygame.image.load('images.jpg')

def spawn_asteroid(): 
    angle = random.randrange(1,360)
    angle_rad = np.radians(angle)
    
    if 1 <= angle < 45:
        x = 340 * np.tan(angle_rad) + 520
        y = 0
    elif 45 <= angle < 90:
        x = 1040
        y = 340 - 520 * np.tan(np.pi / 2 - angle_rad)
    elif 90 <= angle < 135:
        x = 1040
        y = 340 + 520 * np.tan(angle_rad - np.pi / 2)
    elif 135 <= angle < 180:
        x = 520 - 340 * np.tan(np.pi - angle_rad)
        y = 680
    elif 180 <= angle < 225:
        x = 520 - 340 * np.tan(angle_rad - np.pi)
        y = 680
    elif 225 <= angle < 270:
        x = 0
        y = 340 + 520 * np.tan(3 * np.pi / 2 - angle_rad)
    elif 270 <= angle < 315:
        x = 0
        y = 340 - 520 * np.tan(angle_rad - 3 * np.pi / 2)
    elif 315 <= angle < 360:
        x = 520 + 340 * np.tan(2 * np.pi - angle_rad)
        y = 0 
    return Body(x, y, 0, 0, 1, 0,  "", body_type="asteroid", type_props={"visible":True})

asteroid1 = spawn_asteroid()
Planet = Body(520,340, 0,0, 5.9722e24, 25, (255,0,0), body_type="planet", type_props={"visible":True})

while running:
    cursor = pygame.mouse.get_pos()
    window.fill((0, 0, 0))
    planet = pygame.draw.circle(window, (0, 0, 255), (520, 340), r)
    
    if asteroid1.visible:
        asteroid = pygame.Rect(asteroid1.x, asteroid1.y, 50, 50)
        pygame.draw.rect(window, (255, 0, 0), asteroid)

        if asteroid1.x < cursor[0]:
            asteroid1.x += 2
        else:
            asteroid1.x -= 2
        
        if asteroid1.y < cursor[1]:
            asteroid1.y += 2
        else:
            asteroid1.y -= 2

        if asteroid.colliderect(planet):
            Planet.mass += 5e29
            r += 2*np.pi*2
            asteroid1.visible = False
    
    if Planet.mass>1.9e30:
        running = False

    if  not asteroid1.visible:
            asteroid1 = spawn_asteroid()
            asteroid1.visible = True
    
    pygame.display.update() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
