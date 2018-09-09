import pygame
from molesObjects import Mole
from molesObjects import Wolf
from molesMain import PygameGame
from molesObjects import Ground
from molesObjects import WormBlock
from molesObjects import HazardBlock
from molesObjects import GrubBlock
from molesObjects import BossBlock
import random


#colors
grass = (200,200,19)
startGround = (210,105,30)
ground = (63,11,11)
sun = (255,252,127)
sunS = (255,252,157)
fontColor = (255,255,255)


#outline from tutorial
class Game(PygameGame):
    def init(self):
        #creates the mole and ground sprite groups (for collisions)
        Mole.init()
        self.moleGroup = pygame.sprite.Group(Mole("Fuzzy",self.width*.25, self.height*.3))
        Wolf.init()
        self.wolfGroup = pygame.sprite.Group(Wolf("Angry",self.width*.75, self.height*.3))
        self.groundGroup = pygame.sprite.Group()
        self.drawGround()

        
        
        #to create start/game screen
        self.mode = "start"
        #rectangle to help draw the text
        self.board = pygame.Rect(0, 0, self.width, self.height)
        
        #to time sun/ added to by timer fired
        self.count = 0
        
        #sunX and sunY
        self.sunX = self.count
        self.sunY = 1
        
        #scroll stuff
        self.sx =0
        self.sy=0
        self.sm =self.width//2
        self.smy = self.height*.32
        
    #taken from string notes 
    def readFile(self):
        with open("scores.txt", "rt") as f:
            return f.read()
    
    #taken from string notes
    def writeFile(self,newScore):
        #parse and format string correctly when reading
        
        read = self.readFile()
        
        newContents= ""
        
        readList = read.splitlines()
        
        if(newScore>int(readList[0])):
            newContents+=str(newScore)+"\n"
            newContents+=readList[1]+"\n"
            newContents+=readList[2]+"\n"
            
        elif(newScore>int(readList[1])):
            newContents+=readList[0]+"\n"
            newContents+=str(newScore)+"\n"
            newContents+=readList[2]+"\n"
            
        elif(newScore>int(readList[2])):
            newContents+=readList[0]+"\n"
            newContents+=readList[1]+"\n"
            newContents+=str(newScore)+"\n"
        else:
            newContents+=readList[0]+"\n"
            newContents+=readList[1]+"\n"
            newContents+=readList[2]+"\n"
        
        #splitlines
        #use for loop: for items in list
        with open("scores.txt", "wt") as f:
            f.write(newContents)
            
    def drawGround(self):
        bossBlockCount = 0
        #creates the board
        for i in range(-self.width//40, self.width//40):
            for j in range(self.height//20-20):
                #colors
                r = random.randint(123, 153)
                g = random.randint(53, 83)
                b = random.randint(9, 33)
                
                #now roll for special block
                special = random.randint(0,100)
                #worm block drawing
                if(special < 5 and j>self.height//40-self.height//22):
                    self.groundGroup.add(WormBlock(50,50,100*i, self.height*.45+100*j, (r,g,b)))
                elif(special < 10 and j>self.height//21-self.height//22):
                    self.groundGroup.add(WormBlock(50,50,100*i, self.height*.45+100*j, (r,g,b)))
                #hazard block drawing
                elif(special>=10 and special<11):
                    self.groundGroup.add(HazardBlock(50,50,100*i, self.height*.45+100*j, (r,g,b)))
                elif(special>=10 and special<13 and j>self.height//20-self.height//22):
                    self.groundGroup.add(HazardBlock(50,50,100*i, self.height*.45+100*j, (r,g,b)))
                elif(special>=10 and special<20 and j>self.height//20-self.height//25):
                    self.groundGroup.add(HazardBlock(50,50,100*i, self.height*.45+100*j, (r,g,b)))
                #grub block drawing, at greater depths
                elif(special>=13 and special<20 and j>self.height//20-self.height//22):
                    self.groundGroup.add(GrubBlock(50,50,100*i, self.height*.45+100*j, (r,g,b)))
                elif(j>self.height//18-self.height//21 and bossBlockCount == 0 and i ==0):
                    bossBlockCount+=1
                    self.groundGroup.add(BossBlock(50,50,100*i, self.height*.45+100*j, (r,g,b)))
                else:
                    self.groundGroup.add(Ground(50,50,100*i, self.height*.45+100*j, (r,g,b)))
        
            
    def drawSun(self, screen):
            #sun moves
            
            #when the sun goes off screen
            if(self.sx>self.width+self.width//2 or self.sunY>self.height):
                self.sunX = 0
                self.sunY = 1

            #draws the two layered circles that make the sun
            pygame.draw.circle(screen, sun, (self.sunX-int(self.sx),self.sunY-int(self.sy)),85) 
            pygame.draw.circle(screen, sunS, (self.sunX-int(self.sx),self.sunY-int(self.sy)),75) 
            
    def drawMoonandStars(self, screen):
            #moon moves
            
            #when the moon goes off screen
            if(self.sx>self.width+self.width//2 or self.sunY>self.height):
                self.sunX = 0
                self.sunY = 1

            #draws the two layered circles that make the moon
            pygame.draw.circle(screen, (245,245,220), (self.sunX-int(self.sx),self.sunY-int(self.sy)),85) 
            pygame.draw.circle(screen, (255,222,173), (self.sunX-int(self.sx),self.sunY-int(self.sy)+10),75) 
            
            for i in range(15):
                for j in range(15):
                    pygame.draw.circle(screen, (255,255,102), (80*i, 175*j),5)
                    
            for i in range(15):
                for j in range(15):
                    pygame.draw.circle(screen, (255,255,102), (90*i, 100*j),5)
                    
            
            
            
    def changeScroll(self):
        for mole in self.moleGroup:
            x,y = mole.getLoc()
    #setup guided by sidescroller example
        if(x<self.sx+self.sm):
            self.sx = x-self.sm
           # print("!!!!!!!!!!!x1!!!!!!!!!!!!!")
        elif(x>self.width+self.sx-self.sm):
            self.sx=x-self.width+self.sm
            #print("!!!!!!!!!!!!!!!!!!x2!!!!!!!!!!!!!!!!")
        if(y<self.sy):
             self.sy = y
        elif(y>-self.height+self.sy-self.smy):
            self.sy=y-self.height+self.smy*2

    def timerFired(self, dt):
        #for the sun
        self.count+=1
        if(self.count%100==0):
            self.sunX +=3
            self.sunY += int(self.sunY**.05)
        
        h=self.height
        w = self.width
        ground = self.groundGroup
        mole = self.moleGroup
        
        #redraws the mole\ground during the game
        if(self.mode == "game"):
            tempx = self.sx
            tempy= self.sy
            self.changeScroll()
            self.moleGroup.update(self.isKeyPressed, w, h, ground)
            if(tempx != self.sx):
                self.groundGroup.update(self.width, self.height, self.sx-tempx, 0)
            if(tempy!=self.sy):
                self.groundGroup.update(self.width, self.height, 0, self.sy-tempy)
            for mole in self.moleGroup:
                if not mole.upgrade and not mole.trade and not mole.pause:
                    mole.stamina-=mole.staminaRemove
                if mole.health <= 0 or mole.stamina<=0:
                    self.mode = "end"
                    self.writeFile(mole.score)
                    
        elif(self.mode == "boss"):
            self.moleGroup.update(self.isKeyPressed, w, h, ground)
            self.wolfGroup.update( w, h, mole)
            for mole in self.moleGroup:
                if not mole.upgrade and not mole.trade and not mole.pause:
                    mole.stamina-=mole.staminaRemove
                if mole.health <= 0 or mole.stamina<=0:
                    self.mode = "end"
                    self.writeFile(mole.score)
                for boss in self.wolfGroup:
                    if boss.health<=0:
                        self.wolfGroup.empty()
                        self.mode = "win"
                        mole.score+=10000
                        self.writeFile(mole.score)
                    
            
    def drawStart(self, screen):
            h=self.height
            w = self.width
        
            self.drawSun(screen)
            #draws ground for start screen (light brown)
            pygame.draw.rect(screen, startGround, (0, h//4+125, w, h*.75))
            self.rect = pygame.Rect(self.width//2, self.height*.8,
                                    100, 100)
                                    
            #fonts
            pygame.font.init()
            f = pygame.font.SysFont("cooperblack", 35)
            f2 = pygame.font.SysFont("cooperblack", 80)
            
            
            t1_size = f.size("Click anywhere to start playing!")
            t2_size = f2.size("MOLES")
            t3_size = f.size("Instructions")
            
            t1 = f.render("Click anywhere to start playing!", False, fontColor)
            t3 = f.render("Instructions", False, fontColor)
            t2 = f2.render("MOLES", False, fontColor)
            #locations fonts should be placed at
            screen.blit(t1, (self.width/2 - t1_size[0]/2,self.height/2))
            screen.blit(t2, (self.width/2 - t2_size[0]/2,self.height*.25))
            
            #rectangular button for instructions
            
            pygame.draw.rect(screen, (222,184,135), (self.width/2-150, self.height*.75, 300, 50))
            
            screen.blit(t3, (self.width/2 - t3_size[0]/2,self.height*.75))
            
            #draws the mole next to the title
            self.moleGroup.draw(screen)
            
            #draws grass
            pygame.draw.rect(screen, grass, (0, self.height//2-110, self.width, self.height//64))
            
    def drawClinic(self, screen):
        #right left x y
            lx =100-self.sx
            ly = self.height//8-self.sy
            rx =200
            ry =self.height*.25+12
        
            #draws clinic
            pygame.draw.rect(screen, (255,255,255), (lx,ly,rx,ry))
            
            #draw windows
            for i in range(5):
                for j in range(5):
                    pygame.draw.rect(screen, (176,196,222), (lx+i*40+8,ly+j*40+20,25,25))
                    #draws window shiny stuff
                    pygame.draw.rect(screen, (240,248,255), (lx+i*40+14,ly+j*40+22,5,5))
            
            pygame.font.init()
            cFont = pygame.font.SysFont("comicsansms", 15, True)
            ct_size = cFont.size("Clinic")
            ct = cFont.render("Clinic", False, (255,0,0))
            screen.blit(ct, (200 - ct_size[0]/2-self.sx,self.height/8-self.sy))
    
            self.rect = pygame.Rect(self.width//2, self.height*.8,
                                    100, 100)
                                    
            #adds health
            for mole in self.moleGroup:
                x,y = mole.getLoc()
                if(x>lx and x<lx+rx):
                    if(y<ly+ry and y>ly):
                        mole.addHealth()
                        mole.addStamina()
                                    
    def drawTradeDepot(self, screen):
        #right left x y
            lx =600-self.sx
            ly = self.height//6-self.sy
            rx =400
            ry =self.height*.22
            
            #draws depot main building
            pygame.draw.rect(screen, (245,222,179), (lx,ly,rx,ry))
            pygame.draw.rect(screen, (210,180,140), (lx+100,ly+50,rx//2,ry*.4))
            
            #opens trade menu
            for mole in self.moleGroup:
                x,y = mole.getLoc()
                if(x>lx and x<lx+rx):
                    if(y<ly+ry and y>ly):
                        mole.trade = True
            
            cFont = pygame.font.SysFont("cooperblack", 35, False)#perpetua, stencil
            ct_size = cFont.size("Trader Mole's")
            ct = cFont.render("Trader Mole's", False, (255,255,255))
            screen.blit(ct, (lx+ct_size[0]//3,ly+ct_size[1]*.35))
            
            
                        
    def drawUpgradeShop(self, screen):
    #right left x y
        lx =1100-self.sx
        ly = self.height//6-self.sy
        rx =400
        ry =self.height*.22
        
        #draws shop main building
        pygame.draw.rect(screen, (192,192,192), (lx,ly,rx,ry))
        pygame.draw.rect(screen, (47,79,79), (lx+100,ly+50,rx//2,ry*.4))
        
        #opens upgrade menu
        for mole in self.moleGroup:
            x,y = mole.getLoc()
            if(x>lx and x<lx+rx):
                if(y<ly+ry and y>ly):
                    mole.upgrade = True
                    
        cFont = pygame.font.SysFont("stencil", 35, False)#perpetua, stencil
        ct_size = cFont.size("Gym Rat")
        ct = cFont.render("Gym Rat", False, (255,255,255))
        screen.blit(ct, (lx+ct_size[0]*.85,ly+ct_size[1]//2))
                            
                        
                        
                                    
    def drawScore(self, screen):
            score = 0
            moleBucks =0
            for mole in self.moleGroup:
                score+=mole.score
                moleBucks +=mole.bucks
        
            pygame.font.init()
            cFont = pygame.font.SysFont("arialblack", 20)
            ct_size = cFont.size("Score: "+str(score))
            ct = cFont.render("Score: "+str(score), False, (255,255,255))
            screen.blit(ct, (self.width- ct_size[0]*1.1,self.height*.01))
            #tracks moleBucks total
            mb_size = cFont.size("MoleBucks: "+str(moleBucks))
            mb = cFont.render("MoleBucks: "+str(moleBucks), False, (255,255,255))
            screen.blit(mb, (self.width- mb_size[0]*1.05,self.height*.03))
            
    def drawUpgrade(self, screen):
        
        pygame.draw.rect(screen, (50,50,50), (50, 50, self.width-100, self.height-100))
        pygame.draw.rect(screen, (120,120,120), (120, 120, self.width-240, self.height-240))
        pygame.font.init()
        cFont = pygame.font.SysFont("cooperblack", 45, False)#perpetua, stencil
        ct_size = cFont.size("Gym Rat")
        ct = cFont.render("Gym Rat", False, (255,255,255))
        screen.blit(ct, (self.width//2- ct_size[0]*.5,self.height*.16))
        
        sellFont = pygame.font.SysFont("cooperblack", 35, False)#perpetua, stencil
        sell_size = cFont.size("Pick your upgrade")
        ct = sellFont.render("Pick your upgrade", False, (255,255,255))
        screen.blit(ct, (self.width*.79-sell_size[0]*.5,self.height*.3))

            
        #font for items being sold
        cFont = pygame.font.SysFont("cooperblack", 25, False)#perpetua, stencil
        #draw a spot to sell each special block type
        
        #dig speed
        worm_size = cFont.size("Faster Dig Speed, 50 MoleBucks:" )
        worm = cFont.render("Faster Dig Speed, 50 MoleBucks:", False, (255,255,255))
        screen.blit(worm, (self.width*.28- worm_size[0]*.5,self.height*.4))
        
        #more health
        health_size = cFont.size("Increased Health, 100 MoleBucks:" )
        health = cFont.render("Increased Health, 100 MoleBucks:", False, (255,255,255))
        screen.blit(health, (self.width*.28- health_size[0]*.5,self.height*.5))
        
        #longer stamina time
        health_size = cFont.size("More Stamina, 200 MoleBucks:" )
        health = cFont.render("More Stamina, 200 MoleBucks:", False, (255,255,255))
        screen.blit(health, (self.width*.28- health_size[0]*.5,self.height*.6))
        
        end_size = cFont.size("Press Esc to exit")
        end = cFont.render("Press Esc to exit", False, (255,255,255))
        
        #renders text
        screen.blit(end, (self.width//2- end_size[0]*.5,self.height*.87))
        
        
        #draw buttons to allow the stuff to be sold
        pygame.draw.rect(screen, (50,50,50), (self.width*.75, self.height*.4, 100, 50))
        pygame.draw.rect(screen, (50,50,50), (self.width*.75, self.height*.5, 100, 50))
        pygame.draw.rect(screen, (50,50,50), (self.width*.75, self.height*.6, 100, 50))
        
        
        
    def drawTrade(self, screen):
        
        pygame.draw.rect(screen, (244,164,96), (50, 50, self.width-100, self.height-100))
        pygame.draw.rect(screen, (244,200,96), (120, 120, self.width-240, self.height-240))
        pygame.font.init()
        cFont = pygame.font.SysFont("cooperblack", 45, False)#perpetua, stencil
        ct_size = cFont.size("Trader Mole's")
        ct = cFont.render("Trader Mole's", False, (255,255,255))
        screen.blit(ct, (self.width//2- ct_size[0]*.5,self.height*.16))
        
        sellFont = pygame.font.SysFont("cooperblack", 35, False)#perpetua, stencil
        sell_size = cFont.size("Sell")
        ct = sellFont.render("Sell", False, (255,255,255))
        screen.blit(ct, (self.width*.79-sell_size[0]*.5,self.height*.3))
        
        #see which special blocks the players have
        #first define types of special blocks
        worm = 0
        grub = 0
        boss = 0
        for mole in self.moleGroup:
            worm+=mole.worms
            grub+=mole.grubs
            boss+=mole.bossBlocks
            
        #font for items being sold
        cFont = pygame.font.SysFont("cooperblack", 25, False)#perpetua, stencil
        #draw a spot to sell each special block type
        
        #wormblocks
        worm_size = cFont.size("Worm Blocks: "+ str(worm))
        worm = cFont.render("Worm Blocks: " + str(worm), False, (255,255,255))
        screen.blit(worm, (self.width*.28- worm_size[0]*.5,self.height*.4))
        
        #grubblocks
        worm_size = cFont.size("Grub Blocks: "+ str(grub))
        worm = cFont.render("Grub Blocks: " + str(grub), False, (255,255,255))
        screen.blit(worm, (self.width*.28- worm_size[0]*.5,self.height*.5))
        
        #bossBlocks
        worm_size = cFont.size("Boss Blocks: "+ str(boss))
        worm = cFont.render("Boss Blocks: " + str(boss), False, (255,255,255))
        screen.blit(worm, (self.width*.28- worm_size[0]*.5,self.height*.6))
        
        end_size = cFont.size("Press Esc to exit")
        end = cFont.render("Press Esc to exit", False, (255,255,255))
        
        #renders text
        screen.blit(end, (self.width//2- end_size[0]*.5,self.height*.87))
        
        #draw buttons to allow the stuff to be sold
        pygame.draw.rect(screen, (244,164,96), (self.width*.75, self.height*.4, 100, 50))
        
        pygame.draw.rect(screen, (244,164,96), (self.width*.75, self.height*.5, 100, 50))
        
        pygame.draw.rect(screen, (255,0,0), (self.width*.75, self.height*.6, 100, 50))
        
    def drawEnd(self, screen):
        #draws the game over screen
        
        #draws boxes
        pygame.draw.rect(screen, (255,235,205), (50, 50, self.width-100, self.height-100))
        pygame.draw.rect(screen, (244,164,96), (100, 100, self.width-200, self.height-200))
        
        #draws text
        cFont = pygame.font.SysFont("cooperblack", 45, False)#perpetua, stencil
        ct_size = cFont.size("Game Over")
        ct = cFont.render("Game Over.", False, (255,255,255))
        screen.blit(ct, (self.width//2- ct_size[0]*.5,self.height*.16))
        
        scoreFont = pygame.font.SysFont("cooperblack", 45, False)#perpetua, stencil
        scoreS = self.readFile()
        
        #render "Highscore" text
        score_size = cFont.size("Highscores")
        score = cFont.render("Highscores", False, (255,255,255))
        screen.blit(score, (self.width*.5-score_size[0]//2,self.height*.3))
        
        scoreList = scoreS.splitlines()
        
        score1 = scoreList[0]
        score2 = scoreList[1]
        score3 = scoreList[2]
        
        #render score 1
        score_size = cFont.size("1st:               "+ score1)
        score = cFont.render("1st:               "+ score1, False, (255,255,255))
        screen.blit(score, (self.width*.35,self.height*.4))
        
        #render score 2
        score_size = cFont.size("2nd:               "+score2)
        score = cFont.render("2nd:               "+score2, False, (255,255,255))
        screen.blit(score, (self.width*.35,self.height*.5))
        
        #render score 3
        score_size = cFont.size("3rd:               "+score3)
        score = cFont.render("3rd:               "+score3, False, (255,255,255))
        screen.blit(score, (self.width*.35,self.height*.6))
        
        
        
        end_size = cFont.size("Click anywhere to restart")
        end = cFont.render("Click anywhere to restart", False, (255,255,255))
        
        #renders text
        screen.blit(end, (self.width//2- end_size[0]*.5,self.height*.8))
        
        
    def drawWin(self, screen):
        #draws the win screen
        
        #draws boxes
        pygame.draw.rect(screen, (255,235,205), (50, 50, self.width-100, self.height-100))
        pygame.draw.rect(screen, (244,164,96), (100, 100, self.width-200, self.height-200))
        
        #draws text
        cFont = pygame.font.SysFont("cooperblack", 45, False)#perpetua, stencil
        ct_size = cFont.size("YOU WIN")
        ct = cFont.render("YOU WIN", False, (255,255,255))
        screen.blit(ct, (self.width//2- ct_size[0]*.5,self.height*.16))
        
        scoreFont = pygame.font.SysFont("cooperblack", 45, False)#perpetua, stencil
        scoreS = self.readFile()
        
        #render "Highscore" text
        score_size = cFont.size("Highscores")
        score = cFont.render("Highscores", False, (255,255,255))
        screen.blit(score, (self.width*.5-score_size[0]//2,self.height*.3))
        
        scoreList = scoreS.splitlines()
        
        score1 = scoreList[0]
        score2 = scoreList[1]
        score3 = scoreList[2]
        
        #render score 1
        score_size = cFont.size("1st:               "+ score1)
        score = cFont.render("1st:               "+ score1, False, (255,255,255))
        screen.blit(score, (self.width*.35,self.height*.4))
        
        #render score 2
        score_size = cFont.size("2nd:               "+score2)
        score = cFont.render("2nd:               "+score2, False, (255,255,255))
        screen.blit(score, (self.width*.35,self.height*.5))
        
        #render score 3
        score_size = cFont.size("3rd:               "+score3)
        score = cFont.render("3rd:               "+score3, False, (255,255,255))
        screen.blit(score, (self.width*.35,self.height*.6))
        
        
        
        end_size = cFont.size("Click anywhere to play again!")
        end = cFont.render("Click anywhere to play again!", False, (255,255,255))
        
        #renders text
        screen.blit(end, (self.width//2- end_size[0]*.5,self.height*.8))
        
    def drawPause(self, screen):
        #draws the pause screen
        
        #draws boxes
        pygame.draw.rect(screen, (255,235,205), (50, 50, self.width-100, self.height-100))
        pygame.draw.rect(screen, (244,164,96), (100, 100, self.width-200, self.height-200))
        
        #draws text
        cFont = pygame.font.SysFont("cooperblack", 45, False)#perpetua, stencil
        ct_size = cFont.size("Game Paused")
        ct = cFont.render("Game Paused.", False, (255,255,255))
        screen.blit(ct, (self.width//2- ct_size[0]*.5,self.height*.16))
        end_size = cFont.size("Press P to resume")
        end = cFont.render("Press P to resume", False, (255,255,255))
        
        #renders text
        screen.blit(end, (self.width//2- end_size[0]*.5,self.height*.5))
        
    def drawBossFight(self, screen):
        
        screen.fill((55,0,150))
        
        self.drawScore(screen)
        
        self.drawMoonandStars(screen)
        
        self.groundGroup.empty()
        self.groundGroup.add(Ground(self.width,self.height*.45,0, self.height, startGround))
        
        self.moleGroup.draw(screen)
        
        self.groundGroup.draw(screen)
        
        self.wolfGroup.draw(screen)
        
        self.drawHealth(screen)

        self.drawScore(screen)
        
        self.drawBossHealth(screen)
        
        
    def drawHealth(self, screen):
        #draws health bar
        health =0
        morehealth =0 
        for mole in self.moleGroup:
            health = mole.getHealth()
            morehealth = mole.morehealth
            if(mole.trade):
                self.drawTrade(screen)
            elif(mole.upgrade):
                self.drawUpgrade(screen)
            elif(mole.pause):
                self.drawPause(screen)
        pygame.draw.rect(screen, (255,255,255), (4, 4, 112+morehealth, 32))
        pygame.draw.rect(screen, (255,0,0), (10, 10, mole.health, 20))
        
    def drawBossHealth(self, screen):
        #draws health bar
        health =0
        for boss in self.wolfGroup:
            health = boss.health
        pygame.draw.rect(screen, (255,255,255), (4, 4+self.width//2, 1008, 32))
        pygame.draw.rect(screen, (255,0,0), (10, 10+self.width//2, boss.health, 20))
        
    def drawStamina(self,screen):
        #draws stamina
        stamina =0
        for mole in self.moleGroup:
            stamina = mole.stamina
            color = (255,255-(1500//(stamina+1)),255-(1500//(stamina+1)))
            if(stamina<25):
                warn = pygame.mixer.Sound('sounds\emergency.wav')
                warn.play()
            if(color[1]<0):
                color = (255,0,0)
                
        pygame.draw.rect(screen, color , (4, 44, 112, 32))
        pygame.draw.rect(screen, (0,0,255), (10, 50, stamina, 20))
    
    
        
        
        
    def drawGame(self, screen):

            self.drawSun(screen)
            
            self.drawClinic(screen)
            
            self.drawUpgradeShop(screen)
            
            #draws behind the ground sprites to make it look like mole is under ground (dark brown)
            pygame.draw.rect(screen, ground, (0, self.height//4+125-self.sy, self.width, self.height*2))
            
            #draws player mole/ground
            self.drawTradeDepot(screen)
            self.moleGroup.draw(screen)
            self.groundGroup.draw(screen)
            #draws grass
            pygame.draw.rect(screen, grass, (0, self.height//2-110-self.sy, self.width, self.height//64))
            
            self.drawHealth(screen)
            
            self.drawStamina(screen)
            
            self.drawScore(screen)
            
    def drawInstructions(self,screen):
        #draws boxes
        pygame.draw.rect(screen, (255,235,205), (50, 50, self.width-100, self.height-100))
        pygame.draw.rect(screen, (244,164,96), (100, 100, self.width-200, self.height-200))
        
        #draws text
        cFont = pygame.font.SysFont("cooperblack", 45, False)#perpetua, stencil
        ct_size = cFont.size("Instructions")
        ct = cFont.render("Instructions", False, (255,255,255))
        screen.blit(ct, (self.width//2- ct_size[0]*.5,self.height*.16))
        
        
        textFont = pygame.font.SysFont("cooperblack", 25, False)#perpetua, stencil
        
        text_size = textFont.size("You are a mole who has gained the power of flight. Try to defeat the owl!")
        text = textFont.render("You are a mole who has gained the power of flight. Try to defeat the owl!", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.26))
        
        text_size = textFont.size("Dig by holding down the left, right, and down arrow keys")
        text = textFont.render("Dig by holding down the left, right, and down arrow keys", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.3))
        
        text_size = textFont.size("Collect blocks which contain pink worms or white grubs")
        text = textFont.render("Collect blocks which contain pink worms or white grubs", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.35))
        
        text_size = textFont.size("Avoid hot pink blocks, which damage you")
        text = textFont.render("Avoid hot pink blocks, which damage you", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.4))
        
        text_size = textFont.size("Make sure to watch your stamina(blue). If it runs out, you die")
        text = textFont.render("Make sure to watch your stamina(blue). If it runs out, you die", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.45))
        
        text_size = textFont.size("Go to the Clinic to heal and gain stamina")
        text = textFont.render("Go to the Clinic to heal and gain stamina", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.5))
        
        
        text_size = textFont.size("Sell your blocks at Trader Mole's and buy upgrades at Gym Rat")
        text = textFont.render("Sell your blocks at Trader Mole's and buy upgrades at Gym Rat", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.55))
        
        text_size = textFont.size("After collecting the boss block, which allows you to damage the owl,")
        text = textFont.render("After collecting the boss block, which allows you to damage the owl,", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.6))
        
        text_size = textFont.size("sleep at Trader Moles to go to the final battle!")
        text = textFont.render("sleep at Trader Moles to go to the final battle!", False, (255,255,255))
        #renders text
        screen.blit(text, (self.width*.15,self.height*.65))
        
        
        end_size = cFont.size("Click to go back")
        end = cFont.render("Click to go back", False, (255,255,255))
        #renders text
        screen.blit(end, (self.width//2- end_size[0]*.5,self.height*.8))
        
            

    def redrawAll(self, screen):

        #looks at mode and decides what to draw
        if(self.mode == "game"):
            self.drawGame(screen)
        elif(self.mode == "start"):
            self.drawStart(screen)
        elif(self.mode == "end"):
            self.drawEnd(screen)
        elif(self.mode == "instruct"):
            self.drawInstructions(screen)
        elif(self.mode == "boss"):
            self.drawBossFight(screen)
        elif(self.mode == "win"):
            self.drawWin(screen)
            
            
            
Game(1200, 900).run()