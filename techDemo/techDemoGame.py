import pygame
from techDemoObject import Mole
from techDemoMain import PygameGame
from techDemoObject import Ground
from techDemoScene import Scene
import random


#colors
grass = (200,200,19)
startGround = (210,105,30)
ground = (63,11,11)
sun = (255,252,127)
sunS = (255,252,157)
fontColor = (255,255,255)



class Game(PygameGame):
    def init(self):
        #creates the mole and ground sprite groups (for collisions)
        Mole.init()
        self.moleGroup = pygame.sprite.Group(Mole("Fuzzy",self.width*.25, self.height*.32))
        self.groundGroup = pygame.sprite.Group()
        #creates the board
        for i in range(self.width//20):
            for j in range(self.height//20-20):
                r = random.randint(123, 153)
                g = random.randint(53, 83)
                b = random.randint(9, 33)
                self.groundGroup.add(Ground(50,50,100*i, self.height*.45+100*j, (r,g,b)))
        #to create start/game screen
        self.mode = "start"
        #rectangle to help draw the text
        self.board = pygame.Rect(0, 0, self.width, self.height)
        
        #to time sun/ added to by timer fired
        self.count = 0
        
        #sunX and sunY
        self.sx = self.count
        self.sy = 1
            
    def drawSun(self, screen):
            #sun moves
            
            #when the sun goes off screen
            if(self.sx>self.width+self.width//2 or self.sy>self.height):
                self.sx = 0
                self.sy = 1

            #draws the two layered circles that make the sun
            pygame.draw.circle(screen, sun, (self.sx,self.sy),85) 
            pygame.draw.circle(screen, sunS, (self.sx,self.sy),75) 

    def timerFired(self, dt):
        #for the sun
        self.count+=1
        self.sx +=7
        self.sy += int(self.sy**.2)
        
        #redraws the mole\ground during the game
        if(self.mode == "game"):
            self.moleGroup.update(self.isKeyPressed, self.width, self.height, self.groundGroup)
            self.groundGroup.update(self.width, self.height)
            
            
    def drawStart(self, screen):
        
            self.drawSun(screen)
            #draws ground for start screen (light brown)
            pygame.draw.rect(screen, startGround, (0, self.height//4+125, self.width, self.height*.75))
            self.rect = pygame.Rect(self.width//2, self.height*.8,
                                    100, 100)
                                    
            #fonts
            pygame.font.init()
            f = pygame.font.SysFont("cooperblack", 35)
            f2 = pygame.font.SysFont("cooperblack", 80)
            t1_size = f.size("Click anywhere to start playing!")
            t2_size = f2.size("MOLES")
            t1 = f.render("Click anywhere to start playing!", False, fontColor)
            t2 = f2.render("MOLES", False, fontColor)
            #locations fonts should be placed at
            screen.blit(t1, (self.width/2 - t1_size[0]/2,self.height/2))
            screen.blit(t2, (self.width/2 - t2_size[0]/2,self.height*.25))
            
            #draws the mole next to the title
            self.moleGroup.draw(screen)
            
            #draws grass
            pygame.draw.rect(screen, grass, (0, self.height//2-110, self.width, self.height//64))
        
    def drawGame(self, screen):
        
            self.drawSun(screen)
            
            #draws behind the ground sprites to make it look like mole is under ground (dark brown)
            pygame.draw.rect(screen, ground, (0, self.height//4+125, self.width, self.height*.75))
            
    
            self.rect = pygame.Rect(self.width//2, self.height*.8,
                                    100, 100)
                                    
            #draws player mole/grass
            self.moleGroup.draw(screen)
            self.groundGroup.draw(screen)
            pygame.draw.rect(screen, grass, (0, self.height//2-110, self.width, self.height//64))

    def redrawAll(self, screen):
        #looks at mode and decides what to draw
        if(self.mode == "game"):
            self.drawGame(screen)
            
        elif(self.mode == "start"):
            self.drawStart(screen)
            
            
Game(1200, 900).run()