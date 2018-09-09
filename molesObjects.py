#from tutorial
import pygame
import math
import time
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
        if(isinstance(self, Ground) or isinstance(self, WormBlock)):
            self.rect = pygame.Rect(self.x - self.width, self.y - self.height,
                                    2 * self.width, 2 * self.height)
        else:
            w, h = self.image.get_size()
            self.width, self.height = w, h
            #the objects hitbox
            self.rect = pygame.Rect(self.x - w*.75, self.y - h/2,
                                     w*1.1, h*1.1)

    def update(self, screenWidth, screenHeight):
        self.updateRect()
        if(isinstance(self, Ground)):
            pass
        else:# wrap around, and update the rectangle again
            if self.rect.left > screenWidth:
                self.x -= self.speed
            elif self.rect.right < 0:
                self.x += self.speed
            if self.rect.top > screenHeight:
                self.y -= self.speed
            elif self.rect.bottom < 0:
                self.y += self.speed
            self.updateRect()

class Mole(GameObject):

    @staticmethod
    def init():
        #draws the mole/loads mole image
        Mole.moleImage =  pygame.transform.scale(
        pygame.image.load('Images\moleRetry.png').convert_alpha(),(60,75))
        #Mole.moleImage = pygame.Surface((80, 120))  
        #Mole.moleImage = Mole.moleImage.convert_alpha()


    def __init__(self, PID, x, y):
        super(Mole, self).__init__(x, y, Mole.moleImage, 49)
        
        #for mole movement
        self.speed = 12
        self.gravity = 4
        
        #for sockets
        self.PID = PID
        
        #mole hitbox
        self.rect = pygame.Rect(x, y,
                        2 * x, 2 * y)
                        
        #for health bar
        self.health = 100
        self.morehealth = 0
        
        #for stamina bar
        self.stamina = 100
        self.staminaRemove = .2
        
        #for block trade and inventory
        self.score = 0
        self.worms = 0
        self.bucks = 0
        self.grubs = 0
        self.bossBlocks = 0
        
        #for trading menu
        self.trade = False
        
        #for upgrade menu
        self.upgrade = False
        
        #for pause menu
        self.pause = False
        
        #for boss fighy
        self.boss = False
        
        #for upgrades
        self.digspeed = .3
                                
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
            if(by>=self.y-self.height*2):
                return True
        return False

    def update(self, keysDown, screenWidth, screenHeight, ground):
        w, h = self.image.get_size()
        
        
        if(keysDown(pygame.K_ESCAPE)):
            if(self.trade):
                self.trade = False
                self.x= screenWidth//2
            if(self.upgrade):
                self.upgrade = False
                self.x = screenWidth*.9
        
        if(keysDown(pygame.K_p)):
            self.pause = not self.pause
            time.sleep(.1)
    
        if not self.pause and not self.trade and not self.upgrade:
            if keysDown(pygame.K_LEFT):
                self.x -=self.speed//2
                
                if(self.isGroundCollision(ground) and self.y>screenHeight*.4):
                    for block in ground:
                        if(self.hitsLeftWall(block)):
                            #plays sound
                            
                            self.specialCheck(block)
                            self.stamina-=self.staminaRemove*2
                            block.kill()
                            time.sleep(self.digspeed)
                        
            if keysDown(pygame.K_RIGHT):
                self.x +=self.speed//2
                
                #for digging. this checks if the block is hitting the right wall
                if(self.isGroundCollision(ground) and self.y>screenHeight*.4):
                    for block in ground:
                        if(self.hitsRightWall(block)):
                            
                            self.specialCheck(block)
                            self.stamina-=self.staminaRemove*2
                            block.kill()
                            time.sleep(self.digspeed)
        
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
                            self.specialCheck(block)
                            self.stamina-=self.staminaRemove*2
                            block.kill()
                            time.sleep(self.digspeed)
    
        
            
        super(Mole, self).update(screenWidth, screenHeight)

        if not (self.isGroundCollision(ground)):
            self.y+=self.gravity//2
    
    def isGroundCollision(self, ground):
    #checks for collisions
        return pygame.sprite.spritecollide(self, ground, False)
            
    def changePID(self, PID):
    #for sockets
            self.PID = PID
            
    def getHealth(self):
    #health check for health bar
        return self.health
        
    def getLoc(self):
        return self.x, self.y
        
    def specialCheck(self, block):
        if(type(block) == WormBlock):
            self.score +=10
            self.worms +=1
            
        elif(type(block) == HazardBlock):
            self.health-=50
            
        elif(type(block) == GrubBlock):
            self.score+=50
            self.grubs +=1
        elif(type(block) == BossBlock):
            self.score+=10000
            self.bossBlocks = 1

    def addHealth(self):
        if(self.health<100+self.morehealth):
            self.health+=1
    def addStamina(self):
        if(self.stamina<100):
            self.stamina+=1
    
    def getTrade(self):
        return self.trade
        
class Wolf(GameObject):

    @staticmethod
    def init():
        #draws the mole/loads mole image
        Wolf.wolfImage =  pygame.transform.scale(
        pygame.image.load('Images\wolf.png').convert_alpha(),(120,60))


    def __init__(self, PID, x, y):
        super(Wolf, self).__init__(x, y, Wolf.wolfImage, 30)
        
        #for mole movement
        self.speed = 12
        #for sockets
        self.PID = PID
        
        #mole hitbox
        self.rect = pygame.Rect(x, y,
                        2 * x, 2 * y)
                        
        #for health bar
        self.health = 1000
        
    def update(self, screenWidth, screenHeight, mole):
        
        w, h = self.image.get_size()
        
        self.x+=self.speed
        yPattern = random.randint(-10,10)
        self.y+=yPattern
        
        if(self.x>screenWidth-w):
            self.speed=-self.speed
        elif(self.x<0+w):
            self.speed=-self.speed
            
        if(self.y<screenHeight*.05):
            self.y+=1
        elif(self.y>screenHeight*.3):
            self.y-=1
            
        if(self.isMoleCollision(mole)):
            for hero in mole:
                if(hero.y<self.y):
                    self.health-=10
                else:
                    hero.health-=10
    
        
            
        super(Wolf, self).update(screenWidth, screenHeight)
        
    def isMoleCollision(self, mole):
    #checks for collisions
        return pygame.sprite.spritecollide(self, mole, False)
            

            
class Ground(GameObject):
    
    def __init__(self,  width, height, x, y,color):
        #first send the new ground object to the sprite superclass
        
        self.x, self.y = x, y
        self.width = width
        self.height = height
        self.speed = 20

        self.rect = pygame.Rect(x - self.width, y - self.height,
                                2 * self.width, 2 * self.height)
        
        #a surface is needed to draw the ground on
        self.image = pygame.Surface((2*self.width,  2*self.height))  
        self.image = self.image.convert_alpha()
        
        self.image.fill(color)
        
        super(Ground, self).__init__(x, y, self.image, self.width*2)
        
    def getRect(self):  # GET REKT
        self.rect = pygame.Rect(self.x - self.width, self.y - self.height,
                                2 * self.width, 2 * self.height)
                                
    def update(self, screenWidth, screenHeight, sx, sy):
        if(sx>0 or sx<0):
            self.x-=sx
        if(sy>0 or sy<0):
            self.y-=sy
        
        super(Ground, self).update(screenWidth, screenHeight)
        
                                
    def getXandY(self):
    #for dig function
        return self.x,self.y,self.width,self.height
    
    def __repr__(self):
    #for debugging
        return str("y"+str(self.y)+"  x:" + str(self.x))
        
class WormBlock(Ground):
    
    def __init__(self, width, height, x, y, color):
        wormColor = (255,200,200)
        super(WormBlock, self).__init__(width, height, x, y,color)
        
        self.wormNum = 20
        
        x = self.width//5
        y = self.height//5
        
                      
        for i in range(self.wormNum):
            locY =  random.randint(0, self.height-x)
            locX =  random.randint(10, self.width-y)
            coord1 = (locX+x*i, locY+y*i)
            coord2 = (locX+x*i+20, locY+y*i)
            pygame.draw.line(self.image, wormColor,coord1, coord2, 8)
            
class GrubBlock(Ground):
    
    def __init__(self, width, height, x, y, color):
        grubColor = (245,245,220)
        super(GrubBlock, self).__init__(width, height, x, y,color)
        
        self.grubNum = random.randint(5, 10)
                                
                                
        for i in range(self.grubNum):
            locY =  random.randint(20, self.height*2-20)
            locX =  random.randint(10, self.width*2-20)
            radius = random.randint(2, 5)
            pygame.draw.circle(self.image, grubColor,(locX,locY), radius)
        
class HazardBlock(Ground):
    
    def __init__(self, width, height, x, y, color):
        hazardColor = (255,100,100)
        super(HazardBlock, self).__init__(width, height, x, y,hazardColor)
        
class BossBlock(Ground):
    
    def __init__(self, width, height, x, y, color):
        hazardColor = (0,0,0)
        super(BossBlock, self).__init__(width, height, x, y,hazardColor)
        
        
        
    