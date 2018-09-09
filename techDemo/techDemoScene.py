import pygame

class Scene():
    def __init__(self, w , h, mode="start", paused=False):
        self.w = w
        self.h = h
        self.mode = mode
        self.paused = paused
        self.board = pygame.Rect(0, 0, self.w, self.h)
        
    def draw(self, screen, scores=[0,0]):
        if self.paused == True and self.mode == "game": self.drawPaused(screen)
        else:	
            if self.mode == "start": self.drawStart(screen)
            elif self.mode == "game": self.drawGame(screen, scores)
            elif self.mode == "end": self.drawEnd(screen)

    def drawStart(self, screen):
        pygame.font.init()
        f = pygame.font.SysFont('Comic Sans MS', 30)
        t1_size = f.size("Click anywhere to start playing!")
        t1 = f.render("Click anywhere to start playing!", False, (0, 230, 172))
        t2_size = f.size("Press 'p' to pause and 'q' to quit.")
        t2 = f.render("Press 'p' to pause and 'q' to quit.", False, (0, 230, 172))
        pygame.draw.rect(screen, pygame.Color(204, 255, 220), self.board)
        screen.blit(t1, (self.w/2 - t1_size[0]/2,self.h/2))
        screen.blit(t2, (self.w/2 - t2_size[0]/2,self.h/2 + t1_size[1]))

    def drawGame(self, screen, scores):
        pygame.font.init()
        f = pygame.font.SysFont('Comic Sans MS', 20)
        s_left = f.render("Score: " + str(scores[0]), False, (0, 0, 0))
        r_size = f.size("Score: " + str(scores[1]))
        s_right = f.render("Score: " + str(scores[1]), False, (0, 0, 0))
        left = pygame.Rect(0, 0, self.w/2, self.h)
        right = pygame.Rect(self.w/2, 0, self.w, self.h)
        pygame.draw.rect(screen, pygame.Color(173, 235, 235), left)
        pygame.draw.rect(screen, pygame.Color(255, 153, 153), right)
        screen.blit(s_left, (0,0))
        screen.blit(s_right, (self.w - r_size[0], 0))

    def drawEnd(self, screen):
        pygame.font.init()
        f = pygame.font.SysFont('Comic Sans MS', 30)
        t1_size = f.size("Thanks for playing! Click anywhere to start again!")
        t1 = f.render("Thanks for playing! Click anywhere to start again!", False, (0, 230, 172))
        pygame.draw.rect(screen, pygame.Color(204, 255, 220), self.board)
        screen.blit(t1, (self.w/2 - t1_size[0]/2,self.h/2))

    def drawPaused(self, screen):
        pygame.font.init()
        f = pygame.font.SysFont('Comic Sans MS', 30)
        t1_size = f.size("Press 'p' to unpause.")
        t1 = f.render("Press 'p' to unpause.", False, (0, 230, 172))
        pygame.draw.rect(screen, pygame.Color(204, 255, 220), self.board)
        screen.blit(t1, (self.w/2 - t1_size[0]/2,self.h/2))
