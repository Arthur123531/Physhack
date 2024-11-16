import pygame
import math
import numpy as np
from  random import randint



# Window dimensions
WIDTH, HEIGHT = 1040, 680

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

M_EARTH = 5.972e24
M_ASTEROID = 1e12
G = 6.67430e-11
speed_cap = 2


class Body:
    def __init__(self, x:int|None = None, y:int|None = None, vx:float|None = None, vy:float|None = None, mass:float|None = None, color:str|tuple[int]|None = None, body_type:str = "asteroid", type_props = {}):
        if x is not None:
            self.x = x
        elif body_type == "asteroid":
            self.x = randint(0, WIDTH)
        else:
            self.x = WIDTH//2
        if y is not None:
            self.y = y
        elif body_type == "asteroid":
            self.y = randint(0, WIDTH)
        else:
            self.y = WIDTH//2
        if vx is not None:
            self.vx = vx
        else:
            self.vx = 0
        if vy is not None:
            self.vy = vy
        else:
            self.vy = 0
        if mass is not None:
            self.mass = mass
        elif body_type == "asteroid":
            self.mass = M_ASTEROID
        elif body_type == "planet":
            self.mass = M_EARTH
        if color is not None:
            self.color = color
        else:
            self.color = BLUE
        self.trail = [(self.x, self.y)]
        self.body_type = body_type
        #if self.body_type == "asteroid":
            #self.visible = type_props["visible"]

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Initial conditions (scaled down)
    EARTH = Body(body_type="planet")
    body1 = Body(color = RED)
    body2 = Body(WIDTH // 2 - 10, HEIGHT // 2 + 10, 0, 0, 1, GREEN)
    body3 = Body(WIDTH // 2 + 10, HEIGHT // 2 - 10, 0, 0, 1, BLUE)
    body4 = Body(WIDTH // 2 + 10, HEIGHT // 2 + 10, 0, 0, 1, BLACK)
    body5 = Body(WIDTH // 2 + 20, HEIGHT // 2 + 00, 0, 0, 1, ORANGE)
    body6 = Body(WIDTH // 2 - 20, HEIGHT // 2 - 00, 0, 0, 1, PINK)
    body7 = Body(WIDTH // 2 + 00, HEIGHT // 2 + 20, 0, 0, 1, PURPLE)
    body8 = Body(WIDTH // 2 - 00, HEIGHT // 2 - 20, 0, 0, 1, YELLOW)

    bodies = [EARTH, body1]

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
            pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), 5)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
