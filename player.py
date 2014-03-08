import pygame
import math
import helper
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT)

class Player(pygame.sprite.Sprite):
    """ This class represents the player. """
    angle = 1
    speed = 3

    def __init__(self):
        self.lives = 3
        pygame.sprite.Sprite.__init__(self)
        self.baseImage = pygame.image.load("image/ship.tga")
        self.rect = self.baseImage.get_rect()
        self.rect.x,self.rect.y = (SCREEN_WIDTH/2 - 90),(SCREEN_HEIGHT/2 - 90)
        self.image = self.baseImage.copy()

    def update(self):
        """ Update the player location. """
        key = pygame.key.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        if key[pygame.K_s] and self.rect.center[1] < SCREEN_HEIGHT: # down key
            self.rect.y += self.speed # move down
        if key[pygame.K_w] and self.rect.center[1] > 0: # up key
            self.rect.y -= self.speed # move up
        if key[pygame.K_d] and self.rect.center[0] < SCREEN_WIDTH: # right key
            self.rect.x += self.speed # move right
        if key[pygame.K_a] and self.rect.center[0] > 0: # left key
            self.rect.x -= self.speed # move left

        self.angle = math.degrees(math.atan2(self.rect.center[0]-mousePosition[0], self.rect.center[1]-mousePosition[1]))
        self.image,self.rect = helper.rot_center(self.baseImage, self.rect, self.angle)

    def fire(self):
        return Lazer(self.angle, self.rect.center)


class Lazer(pygame.sprite.Sprite):
    speed = 5

    def __init__(self, angle, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("image/lazer.tga")
        self.rect = pygame.rect.Rect(center,self.image.get_size())
        self.speedx =  self.speed*math.cos(math.radians(angle+90))
        self.speedy = -self.speed*math.sin(math.radians(angle+90))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if not (-100 < self.rect.x or self.rect.x < SCREEN_WIDTH):
            self.kill()
        if not (-100 < self.rect.y or self.rect.y < SCREEN_HEIGHT):
            self.kill()
