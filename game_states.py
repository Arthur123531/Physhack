import pygame

from N_body_problem import *
from blink_stars import *
from itertools import islice

pygame.display.set_caption('Cosmocrash')
TIME_LIMIT = 100

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range (1, 6):
            img = pygame.image.load(f'images/explosion{num}.png')
            img.convert_alpha()
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_counter = 0

    def update(self):
        explosion_speed = 4
        # update explosion animation
        self.frame_counter += 1

        if self.frame_counter >= explosion_speed and self.index < len(self.images) - 1:
            self.frame_counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.frame_counter >= explosion_speed:
            self.kill()


class State(object):
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.prev_state = None

class Start(State):
    def __init__(self):
        super().__init__()
        self.next = 'tutorial'

    def cleanup(self):
        print('')

    def startup(self):
        self.menu_text = get_font(75).render('COSMOCRASH', True, '#b68f40')
        self.menu_rect = self.menu_text.get_rect(center=(WIDTH // 2, 100))
        self.menu_mouse_pos = pygame.mouse.get_pos()

        #blinking stars 
        self.star_list = [Star(WIDTH, HEIGHT) for _ in range(300)]

        #music
        pygame.mixer.music.load('sounds/space_intro.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(60)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(self.menu_mouse_pos):
                self.done = True
            if self.quit_button.checkForInput(self.menu_mouse_pos):
                self.quit = True


    def update(self, screen, dt):
        self.menu_mouse_pos = pygame.mouse.get_pos()

        self.play_button = Button(image=pygame.image.load('images/Play Rect.png'), pos=(WIDTH // 2, 280),
                                  text_input='PLAY', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        self.quit_button = Button(image=pygame.image.load('images/Quit Rect.png'), pos=(WIDTH // 2, 480),
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

class Tutorial(State):
    def __init__(self):
        super().__init__()
        self.next = 'game'

    def cleanup(self):
        print('')

    def startup(self):
        self.star_list = [Star(WIDTH, HEIGHT) for _ in range(300)]

        self.tuto_text = get_font(75).render('TUTORIAL', True, '#b68f40')
        self.tuto_rect = self.tuto_text.get_rect(center=(WIDTH // 2, 100))

        self.line1 = get_font(15).render('!! WARNING WARNING !!', True, '#FFFFFF')
        self.line1_rect = self.line1.get_rect(center=(WIDTH // 2, 200))
        self.line2 = get_font(15).render('A SHOWER OF ASTEROIDS IS COMING TOWARD PLANET EARTH!', True, '#FFFFFF')
        self.line2_rect = self.line2.get_rect(center=(WIDTH // 2, 250))
        self.line3 = get_font(15).render('FORTUNATLY, BRAND NEW LUNAR INSTALLATIONS LET US', True, '#FFFFFF')
        self.line3_rect = self.line3.get_rect(center=(WIDTH // 2, 300))
        self.line4 = get_font(15).render('CONTROL THE MOON\'s ORBIT TO DEFEND OUR PLANET!', True, '#FFFFFF')
        self.line4_rect = self.line4.get_rect(center=(WIDTH // 2, 350))
        self.line5 = get_font(15).render("USE THE UP KEY TO INCREASE THE MOON'S RADIUS", True, '#FFFFFF')
        self.line5_rect = self.line5.get_rect(center=(WIDTH // 2, 430))
        self.line6 = get_font(15).render("USE THE DOWN KEY TO DECREASE THE MOON'S RADIUS", True, '#FFFFFF')
        self.line6_rect = self.line6.get_rect(center=(WIDTH // 2, 480))
        self.line7 = get_font(15).render("USE THE W KEY TO INCREASE THE MOON'S VELOCITY", True, '#FFFFFF')
        self.line7_rect = self.line7.get_rect(center=(WIDTH // 2, 530))
        self.line8 = get_font(15).render("USE THE S KEY TO DECREASE THE MOON'S VELOCITY", True, '#FFFFFF')
        self.line8_rect = self.line8.get_rect(center=(WIDTH // 2, 580))
        self.line9 = get_font(15).render("PRESS ANY KEY TO CONTINUE!", True, '#b68f40')
        self.line9_rect = self.line9.get_rect(center=(WIDTH // 2, 630))

        #music
        pygame.mixer.music.load('sounds/tuto_sound.mp3')
        pygame.mixer.music.play(-1)

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.done = True

    def update(self, screen, dt):
        self.draw(screen)

    def draw(self, screen):
        screen.blit(BG_DIM, (0, 0))

        for s in self.star_list:
            s.show(screen)

        screen.blit(self.tuto_text, self.tuto_rect)
        screen.blit(self.line1, self.line1_rect)
        screen.blit(self.line2, self.line2_rect)
        screen.blit(self.line3, self.line3_rect)
        screen.blit(self.line4, self.line4_rect)
        screen.blit(self.line5, self.line5_rect)
        screen.blit(self.line6, self.line6_rect)
        screen.blit(self.line7, self.line7_rect)
        screen.blit(self.line8, self.line8_rect)
        screen.blit(self.line9, self.line9_rect)

class Game(State):
    def __init__(self):
        super().__init__()
        self.next = 'win'
        self.distance_change_rate = 0  # Rate at which distance changes
        self.velocity_change_rate = 1  # Rate at which velocity changes
        self.explosion_group = pygame.sprite.Group()

    def cleanup(self):
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
        self.timer_counter = TIME_LIMIT
        self.velocity_change_rate = 1
        self.distance_change_rate = 0
        EARTH.counter = 0
        self.explosion_group = pygame.sprite.Group()

    def predict_orbit(self, moon, earth, steps=300, step_size=1):
        """
        Predict the orbit of the moon around earth for a given number of steps.
        Returns a list of predicted positions.
        """
        # Create copies to simulate movement without affecting actual objects
        sim_moon = SimplifiedBody(
            x=moon.x,
            y=moon.y,
            vx=moon.vx,
            vy=moon.vy,
            mass=moon.mass
        )
        sim_earth = SimplifiedBody(
            x=earth.x,
            y=earth.y,
            vx=earth.vx,
            vy=earth.vy,
            mass=earth.mass
        )
        
        positions = []
        
        for _ in range(steps):
            # Calculate gravitational force
            fx, fy = calculate_force(sim_moon, sim_earth)
            
            # Apply force for this time step
            sim_moon.vx += fx * step_size / sim_moon.mass
            sim_moon.vy += fy * step_size / sim_moon.mass
            
            # Update position
            sim_moon.x += sim_moon.vx * step_size
            sim_moon.y += sim_moon.vy * step_size
            
            # Store position
            positions.append((int(sim_moon.x), int(sim_moon.y)))
            
            # Break if moon would collide with earth
            if (sim_moon.x - sim_earth.x)**2 + (sim_moon.y - sim_earth.y)**2 < (45)**2:
                break
                
        return positions

    def draw_orbit_preview(self, screen):
        """Draw the predicted orbit path as a dotted line"""
        if not hasattr(self, 'orbit_preview') or self.orbit_preview_timer <= 0:
            self.orbit_preview = self.predict_orbit(self.moon, EARTH)
            self.orbit_preview_timer = 5  # Update prediction every 10 frames
        else:
            self.orbit_preview_timer -= 1
        
        # Draw only every 10th point to create dotted line effect
        for pos in islice(self.orbit_preview, 0, None, 10):
            pygame.draw.circle(screen, BLUE, pos, 2)
        
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

        self.orbit_preview_timer = 0
        self.show_preview = True
        
        self.healthbar_font = get_font(15)
        self.healthbar_text = self.healthbar_font.render('Health', True, WHITE)
        
        pygame.draw.rect(screen, (255,0,0), (800,15,220,40))
        pygame.draw.rect(screen, (0,128,0), (800,15,220 - 22*EARTH.counter,40))

        pygame.mixer.music.load('sounds/game_sound.mp3')
        pygame.mixer.music.play(-1)

        self.sound_hit = pygame.mixer.Sound('sounds/hit_sound.mp3')

    def get_event(self, event):
        if event.type == self.timer_event:
            if self.timer_counter % 10 == 0 and self.timer_counter != TIME_LIMIT:
                self.bodies.append(Body(body_type="asteroid"))
            self.timer_counter -= 1
            self.timer_text = self.timer_font.render('Timer: ' + str(self.timer_counter), True, WHITE)
            if self.timer_counter == 0:
                pygame.time.set_timer(self.timer_event, 0)
                self.next = 'win'
                self.done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not event.key == pygame.K_DOWN:
                self.distance_change_rate = 1
            if event.key == pygame.K_DOWN and not event.key == pygame.K_UP:
                self.distance_change_rate = -1
            if event.key == pygame.K_w and not event.key == pygame.K_s:
                self.velocity_change_rate = 1.03
            if event.key == pygame.K_s and not event.key == pygame.K_w:
                self.velocity_change_rate = 0.97

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.distance_change_rate = 0
            if event.key == pygame.K_DOWN:
                self.distance_change_rate = 0
            if event.key == pygame.K_w:
                self.velocity_change_rate = 1
            if event.key == pygame.K_s:
                self.velocity_change_rate = 1

        if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
            self.show_preview = not self.show_preview

    def update(self, screen, dt):

        # Move moon closer to Earth
        dx = self.moon.x - EARTH.x
        dy = self.moon.y - EARTH.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 50:  # Minimum distance to prevent collision
            dx /= distance
            dy /= distance
            self.moon.x += dx * self.distance_change_rate
            self.moon.y += dy * self.distance_change_rate

        # Increase velocity
        current_speed = (self.moon.vx ** 2 + self.moon.vy ** 2) ** 0.5
        if current_speed > 0:
            self.moon.vx *= self.velocity_change_rate
            self.moon.vy *= self.velocity_change_rate
        else:
            # If stationary, give it a small initial velocity
            self.moon.vx = self.velocity_change_rate - 1
            self.moon.vy = self.velocity_change_rate - 1

        for i, body in enumerate(self.bodies):
            for j in range(len(self.bodies)):
                if i != j:
                    fx, fy = calculate_force(body, self.bodies[j])
                    body.apply_force(fx, fy)

            body.update_position()

            # Ensure bodies stay within the screen boundaries
            if body.x < -50 or body.x > WIDTH+50 or body.y < -50 or body.y > WIDTH+50:
                if body == self.moon:
                    self.next =  "game_over"
                    self.done = True
                self.bodies.remove(body)
            if body != EARTH:
                if (body.x-EARTH.x)**2 + (body.y-EARTH.y)**2 < (45)**2:
                    self.bodies.remove(body)
                    self.explosion_group.add(Explosion(body.x, body.y))
                    self.sound_hit.play()
                    

                    if body  == self.moon:
                        self.next = 'game_over'
                        self.done = True
                    EARTH.counter += 1
                    
                    pygame.draw.rect(screen, (255,0,0), (800,15,220,40))
                    pygame.draw.rect(screen, (0,128,0), (800,15,220 - 22*EARTH.counter,40))
        
                    if len(self.bodies) == 1:
                        self.bodies.append(Body(body_type="asteroid"))
                if EARTH.counter >= 10:
                    self.next = 'game_over'
                    self.done = True
            if body.body_type == "asteroid":
                if (body.x-self.moon.x)**2 + (body.y-self.moon.y)**2 < (20)**2:
                    self.bodies.remove(body)
                    self.explosion_group.add(Explosion(body.x, body.y))
                    self.sound_hit.play()
        if not any(body.body_type == "asteroid" for body in self.bodies):
            self.bodies.append(Body(body_type="asteroid"))
        self.draw(screen)
        self.explosion_group.draw(screen)
        self.explosion_group.update()

    def draw(self, screen):
        screen.fill((0, 0, 0)) 

        if self.show_preview:
            self.draw_orbit_preview(screen)

        screen.blit(self.timer_text, (0, 15))
    
        
        preview_text = get_font(20).render(
            'Preview: ON (Tab to toggle)' if self.show_preview else 'Preview: OFF (Tab to toggle)', 
            True, WHITE
            )
        screen.blit(preview_text, (0, 45))
        #blinking stars 
        for s in self.star_list:
            s.show(screen)

        for body in self.bodies:
            body.tail_display()
            body.draw_body()
            
        pygame.draw.rect(screen, (255,0,0), (800,15,220,40))
        pygame.draw.rect(screen, (0,128,0), (800,15,220 - 22*EARTH.counter,40))
        screen.blit(self.healthbar_text, (925,60))
            

class Win(State):
    def __init__(self):
        super().__init__()
        self.next = 'game'

    def cleanup(self):
        print('Cleaning Win state')
    
    def startup(self):
        self.menu_text = get_font(50).render('YOU WIN !', True, '#7aeaff')
        self.menu_rect = self.menu_text.get_rect(center=(WIDTH // 2, 100))
        self.menu_mouse_pos = pygame.mouse.get_pos()
        self.star_list = [Star(WIDTH, HEIGHT) for _ in range(300)]
        pygame.mixer.music.load('sounds/win_sound.mp3')
        pygame.mixer.music.play()


    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(self.menu_mouse_pos):
                self.done = True
            if self.quit_button.checkForInput(self.menu_mouse_pos):
                self.quit = True

    def update(self, screen, dt):
        self.menu_mouse_pos = pygame.mouse.get_pos()

        self.play_button = Button(image=pygame.image.load('images/medium_rec.png'), pos=(WIDTH // 2, 280),
                                  text_input='PLAY AGAIN', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        self.quit_button = Button(image=pygame.image.load('images/Quit Rect.png'), pos=(WIDTH // 2, 480),
                                  text_input='QUIT', font=get_font(75), base_color='#d7fcd4', hovering_color='White')

        for button in [self.play_button, self.quit_button]:
            button.changeColor(self.menu_mouse_pos)

        self.draw(screen)

    def draw(self, screen):
        screen.blit(YOUWIN_BG, (0, 0))
        screen.blit(self.menu_text, self.menu_rect)
        for button in [self.play_button, self.quit_button]:
            button.update(screen)
        for s in self.star_list:
            s.show(screen)

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
        self.star_list = [Star(WIDTH, HEIGHT) for _ in range(300)]
        pygame.mixer.music.load('sounds/game_over.mp3')
        pygame.mixer.music.play()

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.checkForInput(self.menu_mouse_pos):
                self.done = True
            if self.quit_button.checkForInput(self.menu_mouse_pos):
                self.quit = True


    def update(self, screen, dt):
        self.menu_mouse_pos = pygame.mouse.get_pos()

        self.play_button = Button(image=pygame.image.load('images/medium_rec.png'), pos=(WIDTH // 2, 250),
                                  text_input='PLAY AGAIN', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        self.quit_button = Button(image=pygame.image.load('images/Quit Rect.png'), pos=(WIDTH // 2, 450),
                                  text_input='QUIT', font=get_font(75), base_color='#d7fcd4', hovering_color='White')

        for button in [self.play_button, self.quit_button]:
            button.changeColor(self.menu_mouse_pos)

        self.draw(screen)

    def draw(self, screen):
        screen.blit(GAME_OVER_BG, (0, 0))
        screen.blit(self.menu_text, self.menu_rect)
        for button in [self.play_button, self.quit_button]:
            button.update(screen)
        for s in self.star_list:
            s.show(screen)

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