#from tutorial
import pygame
import math
import random

brown = (139,69,19)


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.baseImage = image.copy()  # non-rotated version of image
        w, h = image.get_size()

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self, screenWidth, screenHeight):
        self.updateRect()
        # wrap around, and update the rectangle again
        if self.rect.left > screenWidth:
            self.x -= screenWidth + self.width
        elif self.rect.right < 0:
            self.x += screenWidth + self.width
        if self.rect.top > screenHeight:
            self.y -= self.speed
        elif self.rect.bottom < 0:
            self.y += screenHeight + self.height
        self.updateRect()

class Mole(GameObject):
    # we only need to load the image once, not for every ship we make!
    #   granted, there's probably only one ship...
    @staticmethod
    def init():
        #Mole.moleImage =  pygame.transform.scale(
        #pygame.image.load('moleRetry.png').convert_alpha(),(80, 120))
        Mole.moleImage = pygame.Surface((20, 40))  
        Mole.moleImage = Mole.moleImage.convert_alpha()
        
        #Mole.moleImage.fill((r,g,b))

    def __init__(self, PID, x, y, color):
        super(Mole, self).__init__(x, y, Mole.moleImage, 30)
        self.speed = 20
        self.gravity = 9
        self.PID = PID
        self.rect = pygame.Rect(x, y,
                                2 * x, 2 * y)
        self.moleImage.fill((color))

    def move(self, dx, dy, screenWidth, screenHeight):
        print("in move with " +self.PID )
        self.x += dx
        self.y += dy
        super(Mole, self).update(screenWidth, screenHeight)

    def teleport(self, x, y):
        self.x = x
        self.y = y
        
    def update(self, keysDown, screenWidth, screenHeight, ground, isMe):
        if(isMe):
            if keysDown(pygame.K_LEFT):
                self.x -=self.speed//2
                msg = "playerMoved %d %d\n" % (-self.speed//2, 0)
    
            if keysDown(pygame.K_RIGHT):
                self.x +=self.speed//2
                msg = "playerMoved %d %d\n" % (self.speed//2, 0)
    
            if keysDown(pygame.K_UP):
                self.y -=self.speed
                msg = "playerMoved %d %d\n" % (0, -self.speed)
    
            if keysDown(pygame.K_DOWN):
                self.y +=self.speed
                if(self.isGroundCollision(ground)):
                    self.y-=self.speed
                
        super(Mole, self).update(screenWidth, screenHeight)
        
        
        if not (self.isGroundCollision(ground)):
            self.y+=self.gravity
        
    def isGroundCollision(self, ground):
        return pygame.sprite.spritecollide(self, ground, False)
            
    def changePID(self, PID):
            self.PID = PID

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
