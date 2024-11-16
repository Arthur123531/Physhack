import pygame
import random

class Star:
    def __init__(self, width, height):
        self.radius = random.randint(1,2)
        self.color = (255,255,255)
        self.pos_x = random.randint(0,width)
        self.pos_y = random.randint(0, height)
        self.decrease = True 
    
    def show(self, screen):
        t = random.randint(0,100)

        if t == 1 or t ==0:
            if self.decrease and self.radius >1 :
                self.radius -=1
                self.decrease = False 
            else:
                self.radius += 1
                self.decrease = True 

        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), self.radius)

