import pygame
import random
import math
import helper
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT)


class Asteroid(pygame.sprite.Sprite):
    """ This class represents the Asteroid. """
    def __init__(self,pos,size):
        """ Called every time a new asteroid is made """
        pygame.sprite.Sprite.__init__(self)
        """Tests made depending the parent size in order to create the smaller asteroids"""
        self.size = size
        if size == 0:
            self.baseImage = pygame.image.load("image/asteroid0.tga")
            self.where = random.randrange(1,5)
            if self.where == 1:
                self.center = [random.randrange(-300,0),random.randrange(-300,SCREEN_HEIGHT+300)]
            elif self.where == 2:
                self.center = [random.randrange(SCREEN_WIDTH,SCREEN_WIDTH+300),random.randrange(-300,SCREEN_HEIGHT+300)]
            elif self.where == 3:
                self.center = [random.randrange(-300,SCREEN_WIDTH+300),random.randrange(-300,0)]
            elif self.where == 4:
                self.center = [random.randrange(SCREEN_HEIGHT,SCREEN_HEIGHT+300),random.randrange(-300,SCREEN_HEIGHT+300)]
        if size == 1:
            """ changes images depending on size """
            self.baseImage = pygame.image.load("image/asteroid10.tga")
        if size == 2:
            self.baseImage = pygame.image.load("image/asteroid11.tga")
        if size == 3:
            self.baseImage = pygame.image.load("image/asteroid20.tga")
        if size == 4:
            self.baseImage = pygame.image.load("image/asteroid21.tga")
        if size == 1 or size == 2 or size == 3 or size == 4:
            """ Creates a random angle for the image to be turned """
            self.center = pos
            self.angle = random.randrange(0,360)
        self.rect = pygame.rect.Rect(self.center,self.baseImage.get_size())
        if size == 0:
            """ Creates the speed and and angle if it is the biggest size as this has not been done before"""
            self.angle = random.randrange(80,120)/100*math.degrees(math.atan2(self.rect.center[0]-pos[0], self.rect.center[1]-pos[1]))
        self.speed = random.triangular(1.0, 4.0)
        self.speedx =  self.speed*math.cos(math.radians(self.angle+90))
        self.speedy = -self.speed*math.sin(math.radians(self.angle+90))
        self.rotaSpeed = random.randrange(0,7)
        self.angle = random.randrange(0,360)
        self.image = self.baseImage.copy()
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        """ Keeps track of rotation and speed to maintain movement """
        self.angle += self.rotaSpeed
        self.image,self.rect = helper.rot_center(self.baseImage, self.rect, self.angle)
        """ Checks if the asteroid is out of bound of the screen , if so moves it to the other side"""
        if self.rect.left>SCREEN_WIDTH:
            self.rect.right=0
        if self.rect.top>SCREEN_HEIGHT:
            self.rect.bottom=0
        if self.rect.right<0:
            self.rect.left=SCREEN_WIDTH
        if self.rect.bottom<0:
            self.rect.top=SCREEN_HEIGHT
        self.rect.x += self.speedx
        self.rect.y += self.speedy