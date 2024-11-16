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


G = 1
speed_cap = 2
arr = np.array([[1,1],[1,1]])
arr.tranpose()


class Body:
    def __init__(self, x, y, vx, vy, mass, color, type, type_props = {}):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.mass = mass
        self.color = color
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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # Initial conditions (scaled down)
    body1 = Body(WIDTH // 2 - 10, HEIGHT // 2 - 10, 0, 0, 1, RED)
    body2 = Body(WIDTH // 2 - 10, HEIGHT // 2 + 10, 0, 0, 1, GREEN)
    body3 = Body(WIDTH // 2 + 10, HEIGHT // 2 - 10, 0, 0, 1, BLUE)
    body4 = Body(WIDTH // 2 + 10, HEIGHT // 2 + 10, 0, 0, 1, BLACK)
    body5 = Body(WIDTH // 2 + 20, HEIGHT // 2 + 00, 0, 0, 1, ORANGE)
    body6 = Body(WIDTH // 2 - 20, HEIGHT // 2 - 00, 0, 0, 1, PINK)
    body7 = Body(WIDTH // 2 + 00, HEIGHT // 2 + 20, 0, 0, 1, PURPLE)
    body8 = Body(WIDTH // 2 - 00, HEIGHT // 2 - 20, 0, 0, 1, YELLOW)

    bodies = [body1, body2, body3, body4, body5, body6, body7, body8]

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
