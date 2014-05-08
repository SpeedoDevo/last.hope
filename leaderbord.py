import pygame
import sys
import control
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, GREY, BLACK, WHITE)


class Menu(pygame.sprite.Sprite):

    def __init__(self, screen, clock):
        pygame.display.set_caption("LAST HOPE -SCOREs-")
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font('image/langdon.otf', 50)
        self.options = ["menu","quit"]
        self.screenRect = (0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        self.pos = 0
        self.bg = control.Background()
        self.file = open( "Scores.txt", "r" )
        self.array = []
        for line in self.file:
            self.array.append(int(line))
        self.file.close()   
    def draw(self,screen):
        self.bg.update()
        screen.blit(self.bg.image,self.bg.rect)
        for i in range(len(self.options)):
            colorScore = GREY
            if i == self.pos:
                color = WHITE
            else:
                color = GREY
            self.text = self.font.render(self.options[i], True, color)
            self.textrect = self.text.get_rect()
            self.textrect.center = (SCREEN_WIDTH/2,(200+i*45))
            self.screen.blit(self.text,self.textrect) 
        for i in range(0,5):
            self.score1 = self.font.render("--" + str(self.array[i]) + "--", True, colorScore)
            self.score1rect = self.score1.get_rect()
            self.score1rect.center = (SCREEN_WIDTH/2,(350+i*45))
            self.screen.blit(self.score1,self.score1rect)        

        # screen.blit(self.image,self.screenRect)
        pygame.display.update()


    def update(self):
        self.pos %= 2
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.pos += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                self.pos -= 1
            if event.type == pygame.MOUSEBUTTONDOWN:
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
                pygame.quit()
                sys.exit(0)
