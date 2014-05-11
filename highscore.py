import pygame
import sys
import collections
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, GREY, BLACK, WHITE)

class ScoreTable(pygame.sprite.Sprite):
    def __init__(self, screen, clock, bg):
        pygame.sprite.Sprite.__init__(self)
        self.titleFont = pygame.font.Font('image/langdon.otf', 50)
        self.title = self.titleFont.render("highscores", True, GREY)
        self.titleRect = self.title.get_rect()
        self.titleRect.center = (SCREEN_WIDTH/2,50)
        self.scoreFont = pygame.font.Font('image/muzarela.ttf', 30)
        # self.names = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n"]
        # self.scores = [9 , 8 , 7 , 6 , 5 , 4 , 3 , 2 , 1 , 0 , 0 , 0 , 0 , 0 ]
        # self.hs = {"names": self.names, "scores": self.scores}
        self.h = {13:"a", 12:"b", 11:"c", 10:"d", 9:"e", 8:"f", 7:"g", 6:"h", 5:"i", 4:"j", 3:"k", 2:"l", 1:"m"}
        self.hs = collections.OrderedDict(sorted(self.h.items(), key=lambda t: t[0], reverse=True))
        self.clock = clock
        self.screen = screen
        self.bg = bg

    def draw(self,screen):
        self.bg.update()
        screen.blit(self.bg.image,self.bg.rect)
        screen.blit(self.title,self.titleRect)
        for i in range(len(self.hs)):
            self.text = self.scoreFont.render(str(i+1) + ". " + str(list(self.hs.items())[i][1]) + ": " + str(list(self.hs.items())[i][0]), True, WHITE)
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

# def getLowest