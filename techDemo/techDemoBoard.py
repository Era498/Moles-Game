import pygame
import math

brown = (139,69,19)

class Ground(pygame.sprite.Sprite):
    
    #this function will draw the goals
    def __init__(self,  width, height, x, y):
        #first send the new goal object to the sprite superclass
        super(Ground, self).__init__()
        
        self.x, self.y = x, y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(x - self.width, y - self.height,
                                2 * self.width, 2 * self.height)
        
        #a surface is needed to place the goal on
        self.image = pygame.Surface((2 * self.width, 2 * self.height))  
        self.image = self.image.convert_alpha()
        #random colors
        
        self.image.fill(brown)
        
    def getRect(self):  # GET REKT
        self.rect = pygame.Rect(self.x - self.width, self.y - self.height,
                                2 * self.width, 2 * self.height)
                                
    def getLocation(self):
        return width, self.height, self.x, self.y
