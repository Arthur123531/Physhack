import pygame
import random
import numpy as np

pygame.init()
window = pygame.display.set_mode((1040,680))

r = 10
running = True

class asteroid: 
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.asteroid_visible = True 
    
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
    return asteroid(x, y)
asteroid1 = spawn_asteroid()
asteroid2 = spawn_asteroid()
asteroid3 = spawn_asteroid()
asteroids=[asteroid1,asteroid2, asteroid3]
while running:
    cursor = pygame.mouse.get_pos()

    window.fill((0, 0, 0))

    planet = pygame.draw.circle(window, (0, 0, 255), (520, 340), r)
    for i in asteroids:
        if i.asteroid_visible:
            asteroid = pygame.Rect(x, y, 50, 50)
            pygame.draw.rect(window, (255, 0, 0), asteroid)

            if x < cursor[0]:
                x += 2
            else:
                x -= 2
            
            if y < cursor[1]:
                y += 2
            else:
                y -= 2

            if asteroid.colliderect(planet):
                r += 20
                asteroid_visible = False

        if  not asteroid_visible:
                x, y = spawn_asteroid()
                asteroid_visible = True
            pygame.display.update() 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

pygame.quit()
