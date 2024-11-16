import pygame
import math

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

G = 10000


class Body:
    def __init__(self, x, y, vx, vy, mass, color):
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
        self.vx += ax
        self.vy += ay

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
    body1 = Body(WIDTH // 2, HEIGHT // 2, 1, 0, 100, RED)
    body2 = Body(WIDTH // 2 + 50, HEIGHT // 2, 0, 1, 100, GREEN)
    body3 = Body(WIDTH // 2 + 25, HEIGHT // 2 + 43.30127, 1, 1, 100, BLUE)

    bodies = [body1, body2, body3]

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
