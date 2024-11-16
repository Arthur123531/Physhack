from N_body_problem import *
from blink_stars import *

TIME_LIMIT = 1000

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
        print('')

    def startup(self):
        self.menu_text = get_font(75).render('COSMOCRASH', True, '#b68f40')
        self.menu_rect = self.menu_text.get_rect(center=(WIDTH // 2, 100))
        self.menu_mouse_pos = pygame.mouse.get_pos()

        #blinking stars 
        self.star_list = [Star(WIDTH, HEIGHT) for _ in range(300)]

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(self.menu_mouse_pos):
                self.done = True
            if self.quit_button.checkForInput(self.menu_mouse_pos):
                self.quit = True


    def update(self, screen, dt):
        self.menu_mouse_pos = pygame.mouse.get_pos()

        self.play_button = Button(image=pygame.image.load('Play Rect.png'), pos=(WIDTH // 2, 280),
                             text_input='PLAY', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        self.quit_button = Button(image=pygame.image.load('Quit Rect.png'), pos=(WIDTH // 2, 480),
                             text_input='QUIT', font=get_font(75), base_color='#d7fcd4', hovering_color='White')

        for button in [self.play_button, self.quit_button]:
            button.changeColor(self.menu_mouse_pos)

        self.draw(screen)

    def draw(self, screen):
        screen.blit(BG, (0, 0))
        screen.blit(self.menu_text, self.menu_rect)
        for button in [self.play_button, self.quit_button]:
            button.update(screen)

        #blinking stars 
        for s in self.star_list:
            s.show(screen)

class Game(State):
    def __init__(self):
        super().__init__()
        self.next = 'win'
        self.distance_change_rate = 3  # Rate at which distance changes
        self.velocity_change_rate = 0.1  # Rate at which velocity changes

    def cleanup(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
        self.timer_counter = TIME_LIMIT
        EARTH.counter = 0

    def startup(self):
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)
        self.timer_counter = TIME_LIMIT

        self.timer_font = get_font(25)
        self.timer_text = self.timer_font.render('Timer: ' + str(self.timer_counter), True, WHITE)

        self.bodies = [EARTH, Body(body_type="moon")]
        self.moon = self.bodies[1]  # Store reference to moon for easier access

        #blinking stars 
        self.star_list = [Star(WIDTH, HEIGHT) for _ in range(300)]

    def get_event(self, event):
        if event.type == self.timer_event:
            if self.timer_counter % 10 == 0:
                self.bodies.append(Body(body_type="asteroid"))
            self.timer_counter -= 1
            self.timer_text = self.timer_font.render('Timer: ' + str(self.timer_counter), True, WHITE)
            if self.timer_counter == 0:
                pygame.time.set_timer(self.timer_event, 0)
                self.done = True

        # Handle keyboard controls for the moon
        keys = pygame.key.get_pressed()
        
        # Adjust moon's distance from Earth
        if keys[pygame.K_UP]:
            # Move moon away from Earth
            dx = self.moon.x - EARTH.x
            dy = self.moon.y - EARTH.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                # Normalize direction vector
                dx /= distance
                dy /= distance
                # Move moon outward along this vector
                self.moon.x += dx * self.distance_change_rate
                self.moon.y += dy * self.distance_change_rate
        
        if keys[pygame.K_DOWN]:
            # Move moon closer to Earth
            dx = self.moon.x - EARTH.x
            dy = self.moon.y - EARTH.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 50:  # Minimum distance to prevent collision
                dx /= distance
                dy /= distance
                self.moon.x -= dx * self.distance_change_rate
                self.moon.y -= dy * self.distance_change_rate

        # Adjust moon's velocity
        if keys[pygame.K_w]:
            # Increase velocity
            current_speed = (self.moon.vx**2 + self.moon.vy**2)**0.5
            if current_speed > 0:
                speed_multiplier = 1 + self.velocity_change_rate
                self.moon.vx *= speed_multiplier
                self.moon.vy *= speed_multiplier
            else:
                # If stationary, give it a small initial velocity
                self.moon.vx = self.velocity_change_rate
                self.moon.vy = self.velocity_change_rate

        if keys[pygame.K_s]:
            # Decrease velocity
            current_speed = (self.moon.vx**2 + self.moon.vy**2)**0.5
            if current_speed > 0:
                speed_multiplier = 1 - self.velocity_change_rate
                self.moon.vx *= speed_multiplier
                self.moon.vy *= speed_multiplier

    def update(self, screen, dt):
        for i, body in enumerate(self.bodies):
            collisions = 0
            for j in range(len(self.bodies)):
                if i != j:
                    fx, fy = calculate_force(body, self.bodies[j])
                    body.apply_force(fx, fy)

            body.update_position()

            # Ensure bodies stay within the screen boundaries
            if body.x < 0 or body.x > WIDTH:
                body.vx *= -1
            if body.y < 0 or body.y > HEIGHT:
                body.vy *= -1
            
            if body != EARTH:
                if (body.x-EARTH.x)**2 + (body.y-EARTH.y)**2 < (45)**2:
                    self.bodies.remove(body)
                    if body  == self.moon:
                        self.next = 'game_over'
                        self.done = True
                    EARTH.counter += 1
                    if len(self.bodies) == 1:
                        self.bodies.append(Body(body_type="asteroid"))
                if EARTH.counter > 10:
                    self.next = 'game_over'
                    self.done = True
            elif body != self.moon:
                if (body.x-self.moon.x)**2 + (body.y-self.moon.y)**2 < (20)**2:
                    self.bodies.remove(body)

        self.draw(screen)

    def draw(self, screen):
        screen.fill((0, 0, 0)) 

        screen.blit(self.timer_text, (0, 15))

        #blinking stars 
        for s in self.star_list:
            s.show(screen)

        for body in self.bodies:
            body.tail_display()
            body.draw_body()
            

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

class Game_Over(State):
    def __init__(self):
        super().__init__()
        self.next = 'game'

    def cleanup(self):
        print('Cleaning game over state')

    def startup(self):
        self.menu_text = get_font(50).render('GAME OVER', True, '#b68f40')
        self.menu_rect = self.menu_text.get_rect(center=(WIDTH // 2, 100))
        self.menu_mouse_pos = pygame.mouse.get_pos()

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(self.menu_mouse_pos):
                self.done = True
            if self.quit_button.checkForInput(self.menu_mouse_pos):
                self.quit = True


    def update(self, screen, dt):
        self.menu_mouse_pos = pygame.mouse.get_pos()

        self.play_button = Button(image=pygame.image.load('medium_rec.png'), pos=(WIDTH // 2, 250),
                             text_input='PLAY AGAIN', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        self.quit_button = Button(image=pygame.image.load('Quit Rect.png'), pos=(WIDTH // 2, 450),
                             text_input='QUIT', font=get_font(75), base_color='#d7fcd4', hovering_color='White')

        for button in [self.play_button, self.quit_button]:
            button.changeColor(self.menu_mouse_pos)

        self.draw(screen)

    def draw(self, screen):
        screen.blit(BG, (0, 0))
        screen.blit(self.menu_text, self.menu_rect)
        for button in [self.play_button, self.quit_button]:
            button.update(screen)

# Object that runs the game loop and control the switching of states
class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
            delta_time = self.clock.tick(60) / 1000.0
            self.event_loop()
            self.update(delta_time)
            pygame.display.update()


pygame.init()

state_font = pygame.font.SysFont("Arial", 32)

app = Control()
state_dict = {
    'start': Start(),
    'game': Game(),
    'win': Win(),
    'game_over': Game_Over()
}
app.setup_states(state_dict, 'start')
app.main_game_loop()
pygame.quit()
