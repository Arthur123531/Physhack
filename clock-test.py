import pygame

pygame.init()

running = True

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()


timer_font = pygame.font.SysFont("Arial", 32)
counter =  10
text = timer_font.render(str(counter), True, (0,0,0))

timer_event = pygame.USEREVENT +1
pygame.time.set_timer(timer_event, 1000)




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event:
            counter -= 1
            text = timer_font.render(str(counter), True, (0, 0, 0))

            if counter == 0:
                pygame.time.set_timer(timer_event, 0)


    screen.fill((255, 255, 255))
    screen.blit(text, (400, 300))
    pygame.display.flip()
    clock.tick(60)





pygame.quit()