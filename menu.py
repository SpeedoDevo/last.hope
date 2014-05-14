import pygame
import sys
import control
import highscore
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, GREY, BLACK, WHITE)


class Menu(pygame.sprite.Sprite):
    def __init__(self, screen, clock):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font('image/langdon.otf', 40)
        self.options = ["start game", "highscores", "quit"]
        self.pos = 0
        self.bg = control.Background()
        self.hsTable = highscore.ScoreTable(screen, clock, self.bg)
        self.logo = pygame.image.load("image/logo.tga")
        self.logoRect = self.logo.get_rect()
        self.logoRect.center = (SCREEN_WIDTH/2,125)

    def draw(self,screen):
        self.bg.update()
        screen.blit(self.bg.image,self.bg.rect)
        screen.blit(self.logo,self.logoRect)
        for i in range(len(self.options)):
            if i == self.pos:
                color = WHITE
            else:
                color = GREY
            self.text = self.font.render(self.options[i], True, color)
            self.textrect = self.text.get_rect()
            self.textrect.center = (SCREEN_WIDTH/2,(250+i*45))
            self.screen.blit(self.text,self.textrect)
        pygame.display.update()


    def update(self):
        self.pos %= 3
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_s or event.key == pygame.K_DOWN):
                self.pos += 1
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_w or event.key == pygame.K_UP):
                self.pos -= 1
            if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                return self.pos
            return -1

    def run(self):
        while 1:
            self.clock.tick(70)
            self.draw(self.screen)
            selection = self.update()
            if selection == 0:
                return
            elif selection == 1:
                self.hsTable.run()
            elif selection == 2:
                pygame.quit()
                sys.exit(0)
