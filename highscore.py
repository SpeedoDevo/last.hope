import pygame
import sys
import collections
import pickle
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, GREY, BLACK, WHITE)

class ScoreTable(pygame.sprite.Sprite):
    def __init__(self, screen, clock, bg):
        pygame.sprite.Sprite.__init__(self)
        self.titleFont = pygame.font.Font('image/langdon.otf', 50)
        self.title = self.titleFont.render("highscores", True, GREY)
        self.titleRect = self.title.get_rect()
        self.titleRect.center = (SCREEN_WIDTH/2,50)
        self.scoreFont = pygame.font.Font('image/muzarela.ttf', 30)
        self.clock = clock
        self.screen = screen
        self.bg = bg
        self.last = 0
        self.load()

    def draw(self,screen):
        self.bg.update()
        screen.blit(self.bg.image,self.bg.rect)
        screen.blit(self.title,self.titleRect)
        for i in range(len(self.hs)):
            if list(self.hs.items())[i][0] == self.last:
                color = RED
            else:
                color = WHITE
            self.text = self.scoreFont.render(str(i+1) + ". " + str(list(self.hs.items())[i][1]) + ": " + str(list(self.hs.items())[i][0]), True, color)
            self.textrect = self.text.get_rect()
            self.textrect.center = (SCREEN_WIDTH/2,(100+i*35))
            self.screen.blit(self.text,self.textrect)
        pygame.display.update()


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
            return False

    def run(self):
        while 1:
            self.clock.tick(70)
            self.draw(self.screen)
            if self.update(): return

    def getLowest(self):
        return min(list(self.hs.keys()))

    def submitScore(self,name,score):
        self.hs.popitem()
        self.hs[score] = name
        self.last = score
        self.hs = collections.OrderedDict(sorted(self.hs.items(), reverse=True))
        self.save()

    def save(self):
        pickle.dump(self.hs, open("hs.dat", "wb"), 2)

    def load(self):
        try:
            self.hs = pickle.load(open("hs.dat", "rb"))
        except:
            temp = {50000:"SpeedoDevo", 40000:"OliGee", 30000:"Jaume", 20000:"Kyle", 10000:"Steve", 9000:"Danielle", 8000:"Phil", 7000:"Mark", 6000:"Hugh", 5000:"Matt", 4000:"Lisa", 3000:"Todd", 2000:"Ryan"}
            self.hs = collections.OrderedDict(sorted(temp.items(), reverse=True))
            self.save()