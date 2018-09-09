#from tutorial
import pygame
import math
import time

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
        #the objects hitbox
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

    @staticmethod
    def init():
        #draws the mole/loads mole image
        Mole.moleImage =  pygame.transform.scale(
        pygame.image.load('Images\moleRetry.png').convert_alpha(),(50,65))
        #Mole.moleImage = pygame.Surface((80, 120))  
        Mole.moleImage = Mole.moleImage.convert_alpha()


    def __init__(self, PID, x, y):
        super(Mole, self).__init__(x, y, Mole.moleImage, 30)
        
        #for mole movement
        self.speed = 20
        self.gravity = 9
        
        #for sockets
        self.PID = PID
        
        #mole hitbox
        self.rect = pygame.Rect(x, y,
                        2 * x, 2 * y)
                        
        #for health bar
        self.health = 100
                                
    def hitsLeftWall(self, block):
        #checks if the mole is colliding with a ground object to its left
        bx, by,w,h = block.getXandY()
        if(bx+w < self.x):  
            if(by-h<self.y and by+h>self.y): 
                if(pygame.sprite.collide_rect(block, self)):
                    return True
        return False
    
    def hitsRightWall(self, block):
        #checks if the mole is colliding with a ground object to its right
        bx, by, w, h = block.getXandY()
        if(bx-w > self.x):  
            if(by-h<self.y and by+h>self.y): 
                if(pygame.sprite.collide_rect(block, self)):
                    return True
        return False
    
    def hitsGround(self, block):
        #checks if mole is colliding with a ground object on the bottom
        bx, by,w,h = block.getXandY()
        if(by > self.y and pygame.sprite.collide_rect(block, self)):
            return True
        return False
        
    def hitsCiel(self, block):
        #checks if mole is hitting a ground object above
        bx, by,w,h = block.getXandY()
        if(by <= self.y+self.height and pygame.sprite.collide_rect(block, self)):
            if(by>=self.y-self.height):
                return True
        return False

    def update(self, keysDown, screenWidth, screenHeight, ground):
        
        if keysDown(pygame.K_LEFT):
            self.x -=self.speed//2
            
            
            if(self.isGroundCollision(ground) and self.y>screenHeight*.4):
                for block in ground:
                    if(self.hitsLeftWall(block)):
                        block.kill()
                        self.x +=self.speed//2
                        print("left")
                    
        if keysDown(pygame.K_RIGHT):
            self.x +=self.speed//2
            
            #for digging. this checks if the block is hitting the right wall
            if(self.isGroundCollision(ground) and self.y>screenHeight*.4):
                for block in ground:
                    if(self.hitsRightWall(block)):
                        block.kill()
                        print("right")

        if keysDown(pygame.K_UP):
            self.y -=self.speed
            
            #stops mole from leaving the map
            if(self.y<0):
                self.y+=self.speed
                
            #stops mole from flying through ground objects
            if(self.isGroundCollision(ground)):
                for block in ground:
                    if(self.hitsCiel(block)):
                        self.y+=self.speed

        if keysDown(pygame.K_DOWN):
            self.y +=self.speed
                
            #for digging down
            if(self.isGroundCollision(ground) and self.y>screenHeight*.4):
                for block in ground:
                    if(self.hitsGround(block)):
                        block.kill()
                        print("down loop")
                        
            
                
        super(Mole, self).update(screenWidth, screenHeight)
        
        #for gravity
        if not (self.isGroundCollision(ground)):
            self.y+=self.gravity
        
    def isGroundCollision(self, ground):
    #checks for collisions
        return pygame.sprite.spritecollide(self, ground, False)
            
    def changePID(self, PID):
            self.PID = PID

class Ground(pygame.sprite.Sprite):
    
    #this function will draw the goals
    def __init__(self,  width, height, x, y,color):
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
        
        self.image.fill(color)
        
    def getRect(self):  # GET REKT
        self.rect = pygame.Rect(self.x - self.width, self.y - self.height,
                                2 * self.width, 2 * self.height)
                                
    def update(self, screenWidth, screenHeight):
        super(Ground, self).update(screenWidth, screenHeight)
        
                                
    def getXandY(self):
    #for dig function
        return self.x,self.y,self.width,self.height
    
    def __repr__(self):
    #for debugging
        return str("y"+str(self.y)+"  x:" + str(self.x))
