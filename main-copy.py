from N_body_problem import *

def main_menu():  # main menu screen
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.blit(BG, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(50).render('PLANET LAND', True, '#b68f40')
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, 100))

        play_button = Button(image=pygame.image.load('Play Rect.png'), pos=(WIDTH // 2, 250),
                             text_input='PLAY', font=get_font(75), base_color='#d7fcd4', hovering_color='White')
        quit_button = Button(image=pygame.image.load('Quit Rect.png'), pos=(WIDTH // 2, 450),
                             text_input='QUIT', font=get_font(75), base_color='#d7fcd4', hovering_color='White')

        screen.blit(menu_text, menu_rect)

        for button in [play_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.quit()
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    main()
                if quit_button.checkForInput(menu_mouse_pos):
                    running = False
                    # pygame.quit()

        # pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


###########################################################################


# game loop
def main():
    pygame.init()
    pygame.display.set_icon(EARTH_SPRITE.convert_alpha())
    clock = pygame.time.Clock()

    # Timer initialization
    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)
    timer_counter = 1000  # Change to whatever time we give

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
                    timer_text = timer_font.render('You survived !', True, BLACK)

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
                    EARTH.mass += 5e24
                    if len(bodies) == 1:
                        bodies.append(Body(body_type="asteroid"))
                if EARTH.mass > 2e25:
                    pygame.quit()

        # Draw timer
        screen.blit(timer_text, (0, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main_menu()
    # main()
