'''
pygamegame.py
created by Lukas Peraza
 for 15-112 F15 Pygame Optional Lecture, 11/11/15
use this code in your term project if you want
- CITE IT
- you can modify it to your liking
  - BUT STILL CITE IT
- you should remove the print calls from any function you aren't using
- you might want to move the pygame.display.flip() to your redrawAll function,
    in case you don't need to update the entire display every frame (then you
    should use pygame.display.update(Rect) instead)
'''
import pygame
from molesObjects import Mole


class PygameGame(object):

    def init(self, mode, x=0, y=0):
        self.x = x
        self.y = y
        self.mode = mode
        

    def mousePressed(self, x, y):
        print(self.mode)
        if self.mode == "start":
            print("in start loop")
            instX = self.width/2-150
            instY =self.height*.75
            boxSizeX = 300
            boxSizeY = 50
            if(x>instX and x<instX+boxSizeX):
                if(y<instY+boxSizeY and y>instY):
                    self.mode = "instruct"
                else: self.mode = "game"
            else: 
                print("change mode")
                self.mode = "game"
                
            
        elif(self.mode == "instruct"):
            self.mode = "start"
            
        elif self.mode == "end" or self.mode == "win":
            print("checking self mode")
            self.mode = "start"
            self.init()
        
        elif self.mode == "game":
            #button size
            boxSizeX = 100
            boxSizeY = 50
            #check for wormPress
            wormX =self.width*.75
            wormY = self.height*.4
            grubY = self.height*.5
            insY = self.height*.6
            
            #this is so the buttons work, it checks if the click is inside 
            #one of the buttons in trade or upgrade
            for mole in self.moleGroup:
                if(mole.trade):
                    if(x>wormX and x<wormX+boxSizeX):
                        if(y<wormY+boxSizeY and y>wormY):
                            if(mole.worms>0):
                                mole.worms-=1
                                mole.bucks+=10
                        elif(y<grubY+boxSizeY and y>grubY):
                            if(mole.grubs>0):
                                mole.grubs-=1
                                mole.bucks+=50
                                
                        elif(y<insY+boxSizeY and y>insY):
                            print("in insect")
                            if(mole.bossBlocks  == 1):
                                mole.trade = False
                                mole.boss-=1
                                mole.staminaRemove = 0
                                mole.boss = True
                                mole.x = 50
                                mole.y = self.height*.2
                                self.mode = "boss"
                                
                #upgrade button check
                elif(mole.upgrade):
                    if(x>wormX and x<wormX+boxSizeX):
                        if(y<wormY+boxSizeY and y>wormY):
                            if(mole.bucks>=50):
                                mole.digspeed*=.75
                                mole.bucks-=50
                        elif(y<grubY+boxSizeY and y>grubY):
                            if(mole.bucks>=100):
                                mole.morehealth += 100
                                mole.health+=100
                                mole.bucks-=100
                        elif(y<insY+boxSizeY and y>insY):
                            print("in insect")
                            if(mole.bucks>=200):
                                mole.staminaRemove /=2
                                mole.bucks-=200
            
        
    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        #273 up, 275 down, 274 left, 276 right
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass
        
    def drawBoard(self, screen):
        screen.fill(self.bgColor)
        

    def redrawAll(self, screen):
        self.moleGroup.draw(screen)

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=1200, height=900, fps=50, title="Moles the Game"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (135, 206, 235)
        pygame.init()

    def run(self):
        
        #plays sound
        pygame.mixer.music.load("sounds\Music.mp3")
        pygame.mixer.music.play(-1)

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            pygame.display.flip()
            self.drawBoard(screen)
            self.redrawAll(screen)
            
        pygame.quit()
