import pygame
import math
import numpy as np
from  random import randint



# Window dimensions
WIDTH, HEIGHT = 1040, 680
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

#Constants
M_EARTH = 5.972e24
M_ASTEROID = 1e12
R_EARTH = 6371e3
Scaling = R_EARTH/25
G = 6.67430e-11
speed_cap = 2




class Body:
    def __init__(self, x:int|None = None, y:int|None = None, vx:float|None = None, vy:float|None = None, mass:float|None = None, radius:int|None = None, color:str|tuple[int]|None = None, body_type:str = "asteroid", type_props = {}):
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
        if radius is not None:
            self.radius = radius
        elif body_type == "planet":
            self.radius = 25
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
        #if self.body_type == "asteroid":
            #self.visible = type_props["visible"]

    def update_position(self):
        self.x += self.vx
        self.x -= EARTH.vx
        self.y += self.vy
        self.trail.append((self.x, self.y))

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
    dx = (body2.x - body1.x)*Scaling
    dy = (body2.y - body1.y)*Scaling
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


class State(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.prev_state = None

class Start(State):
    def __init__(self):
        super().__init__()
        self.next = 'game'

    def cleanup(self):
        print('Cleaning Start state')

    def startup(self):
        self.state_text = state_font.render('Start', True, (0, 0, 0))

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.state_text, (0, 0))

class Game(State):
    def __init__(self):
        super().__init__()
        self.next = 'win'

    def cleanup(self):
        print('Cleaning Game state')

    def startup(self):
        # self.state_text = state_font.render('Gaming', True, (255, 255, 255))

        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        self.timer_counter = 10  # Change to whatever time we give

        self.timer_font = pygame.font.SysFont('Arial', 30)
        self.timer_text = self.timer_font.render('Timer: ' + str(self.timer_counter), True, BLACK)

        self.bodies = [EARTH]
        for i in range(5):
            self.bodies.append(Body(body_type="asteroid"))

    def get_event(self, event):
        if event.type == self.timer_event:
            self.timer_counter -= 1
            self.timer_text = self.timer_font.render('Timer: ' + str(self.timer_counter), True, BLACK)
            if self.timer_counter == 0:
                pygame.time.set_timer(self.timer_event, 0)
                self.done = True


    def update(self, screen, dt):

        for i, body in enumerate(self.bodies):
            for j in range(len(self.bodies)):
                if i != j:
                    fx, fy = calculate_force(body, self.bodies[j])
                    body.apply_force(fx, fy)

            body.update_position()

        self.draw(screen)

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for i, body in enumerate(self.bodies):
            for k in range(max(0, len(body.trail) - 500), len(body.trail)):
                pygame.draw.circle(screen, body.color, (int(body.trail[k][0]), int(body.trail[k][1])), 2)

            pygame.draw.circle(screen, body.color, (int(body.x), int(body.y)), body.radius)

        screen.blit(self.timer_text, (0, 0))


class Win(State):
    def __init__(self):
        super().__init__()
        self.next = 'start'

    def cleanup(self):
        print('Cleaning Win state')

    def startup(self):
        self.state_text = state_font.render('Win', True, (0, 0, 0))

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.state_text, (0, 0))

# Object that runs the game loop and control the switching of states
class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(self.size)
        self.clock = pygame.time.Clock()

    # Setup the initial state before running main game loop
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup()

    # Switch to the next state, dictated by the current state .next field
    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous

    # Loop over the events and give each to the current game state so it can process it
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            self.state.get_event(event)

    # Update each loop to check if states need to switch + update graphics depending on state
    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, dt)

    # main game loop
    def main_game_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.fps) / 1000.0
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()
            self.clock.tick(60)

pygame.init()

state_font = pygame.font.SysFont("Arial", 32)

settings = {
    'size': (1040, 680),
    'fps': 60
}

app = Control(**settings)
state_dict = {
    'start': Start(),
    'game': Game(),
    'win': Win()
}
app.setup_states(state_dict, 'start')
app.main_game_loop()
pygame.quit()