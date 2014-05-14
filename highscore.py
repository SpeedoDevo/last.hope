import pygame
import sys
import collections # for ordered dict
import pickle # for saving and loading highscores
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, GREY, BLACK, WHITE)

# class that shows, saves and loads highscores
class ScoreTable(pygame.sprite.Sprite):
    # passing in bg so that it's never reinitialized
    def __init__(self, screen, clock, bg):
        pygame.sprite.Sprite.__init__(self)
        self.titleFont = pygame.font.Font('image/langdon.otf', 50)
        self.title = self.titleFont.render("highscores", True, GREY)
        self.titleRect = self.title.get_rect()
        # center on top of the screen
        self.titleRect.center = (SCREEN_WIDTH/2,75)
        self.scoreFont = pygame.font.Font('image/muzarela.ttf', 30)
        self.clock = clock
        self.screen = screen
        self.bg = bg
        # last sores the player's last highscore
        self.last = 0
        self.load()

    def draw(self,screen):
        #update then blit bg
        self.bg.update()
        screen.blit(self.bg.image,self.bg.rect)
        screen.blit(self.title,self.titleRect)
        for i in range(len(self.hs)):
            #red color for the user's highscore
            if list(self.hs.items())[i][0] == self.last:
                color = RED
            else:
                color = WHITE
            self.text = self.scoreFont.render(str(i+1) + ". " + str(list(self.hs.items())[i][1]) + ": " + str(list(self.hs.items())[i][0]), True, color)
            self.textrect = self.text.get_rect()
            # position text based on iteration number
            self.textrect.center = (SCREEN_WIDTH/2,(150+i*35))
            self.screen.blit(self.text,self.textrect)
        pygame.display.update()


    def update(self):
        for event in pygame.event.get():
            # let the game quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            # quit from hstable with click or enter
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                return True
            return False

    def run(self):
        while 1:
            # because we are out of the game loop here we need an own ticking
            self.clock.tick(70)
            self.draw(self.screen)
            if self.update(): return

    def getLowest(self):
        # get the lowest score to decide whether it's high enough fot adding in the table
        return min(list(self.hs.keys()))

    def submitScore(self,name,score):
        # delete the last
        self.hs.popitem()
        # add item
        self.hs[score] = name
        # save which was it
        self.last = score
        # reorder list
        self.hs = collections.OrderedDict(sorted(self.hs.items(), reverse=True))
        # save to file
        self.save()

    def noHS(self):
        # remove highlighting if the score wasn't high enough
        self.last = None

    def save(self):
        # pickle highscores into file
        pickle.dump(self.hs, open("hs.dat", "wb"), 2)

    def load(self):
        # load highscores if it already exists
        try:
            self.hs = pickle.load(open("hs.dat", "rb"))
        # create new file if it doesn't
        except:
            temp = {50000:"SpeedoDevo", 40000:"OliGee", 30000:"Jaume", 20000:"Kyle", 10000:"Steve", 9000:"Danielle", 8000:"Phil", 7000:"Mark", 6000:"Hugh", 5000:"Lisa"}
            self.hs = collections.OrderedDict(sorted(temp.items(), reverse=True))
            self.save()