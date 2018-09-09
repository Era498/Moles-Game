#############################
# Sockets Client Demo
# by Rohan Varma
# adapted by Kyle Chin
#############################
grass = (200,200,19)
ground = (139,69,19)


import socket
import threading
from queue import Queue

HOST = "127.0.0.1" # put your IP address here if playing on multiple computers
PORT = 50003

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
  server.setblocking(1)
  msg = ""
  command = ""
  while True:
    msg += server.recv(10).decode("UTF-8")
    command = msg.split("\n")
    while (len(command) > 1):
      readyMsg = command[0]
      msg = "\n".join(command[1:])
      serverMsg.put(readyMsg)
      command = msg.split("\n")

# events-example0.py from 15-112 website
# Barebones timer, mouse, and keyboard events

import pygame
from serverObject import Mole
from techDemoMain import PygameGame
from serverObject import Ground
import random

####################################
# customize these functions
####################################


class PygameGame(object):

    def init(self, x=0, y=0):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.x = x
        self.y = y
        Mole.init()
        self.me = Mole("Fuzzy",self.width/2, self.height*.43, (r,g,b))
        self.moleGroup = pygame.sprite.Group(self.me)
        self.groundGroup = pygame.sprite.Group(Ground(self.width, self.height//4, self.width, self.height*.75))
        self.otherStrangers = dict()
        self.otherGroup = pygame.sprite.Group()
        self.server = server
        self.serverMsg = serverMsg
        

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        #273 up, 275 down, 274 left, 276 right
        dx, dy = 0, 0
        msg = ""
    
        # moving
        if keyCode in [273,  275, 274, 276]:
            speed = 5
            if keyCode == 273:
                dy = -speed
            elif keyCode == 274:
                dy = speed
            elif keyCode == 276:
                dx = -speed
            elif keyCode == 275:
                dx = speed
            # move myself
            self.me.move(dx, dy, self.width, self.height)
            # update message to send
            msg = "playerMoved %d %d\n" % (dx, dy)

        # send the message to other players!
        if (msg != ""):
            print ("sending: ", msg,)
            self.server.send(msg.encode())

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        while (serverMsg.qsize() > 0):
            msg = serverMsg.get(False)
            print("msg = " + str(msg))
            try:
                print("received: ", msg, "\n")
                msg = msg.split()
                command = msg[0]
        
                if (command == "myIDis"):
                    myPID = msg[1]
                    self.me.changePID(myPID)
            
                elif (command == "newPlayer"):
                    newPID = msg[1]
                    x = self.width/2
                    y = self.height/2
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    self.otherStrangers[newPID] = Mole(newPID, x, y, (r,g,b))
                    self.otherGroup.add(Mole(newPID, x, y, (r,g,b)))
        
                elif (command == "playerMoved"):
                    PID = msg[1]
                    dx = int(msg[2])
                    dy = int(msg[3])
                    self.otherStrangers[PID].move(dx,dy, self.width, self.height)
                    self.moleGroup.update(self.isKeyPressed, self.width, self.height, self.groundGroup, True)
                    self.otherGroup.update(self.isKeyPressed, self.width, self.height, self.groundGroup, False)

        
            except:
                print("failed")
            serverMsg.task_done()

        
            
    def drawBoard(self, screen):
        screen.fill(self.bgColor)
        

    def redrawAll(self, screen):
        self.moleGroup.draw(screen)
        self.otherGroup.draw(screen)
        self.groundGroup.draw(screen)
        pygame.draw.rect(screen, grass, (0, self.height//2-2, self.width, self.height//64))
        
    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=400, height=300, fps=50, title="Tech Demo"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (135, 206, 235)
        pygame.init()


####################################
# use the run function as-is
####################################
    
    def run(self, width, height, serverMsg=None, server=None):
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
                self.drawBoard(screen)
                self.redrawAll(screen)
                pygame.display.flip()

            pygame.quit()


serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()
game = PygameGame()
game.run(200, 200, serverMsg, server)
