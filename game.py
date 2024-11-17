from game_states import *

pygame.init()

state_font = pygame.font.SysFont("Arial", 32)

app = Control()
state_dict = {
    'start': Start(),
    'game': Game(),
    'win': Win(),
    'game_over': Game_Over(),
    'tutorial' : Tutorial()
}
app.setup_states(state_dict, 'start')
app.main_game_loop()
pygame.quit()