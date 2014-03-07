import pygame
import random
import math
import player
import helper
import enemies
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('background.gif')
        self.rect = self.image.get_rect()
        self.rect.x = -1500
        self.rect.y = -1500
        self.frameNum = 0

    def update(self):
        self.frameNum += 1
        if self.frameNum % 3 == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_s]:
                self.rect.y -= 1
            if key[pygame.K_w]:
                self.rect.y += 1
            if key[pygame.K_d]:
                self.rect.x -= 1
            if key[pygame.K_a]:
                self.rect.y += 1
            self.rect.x -= 2
        if self.rect.x > 1000:
            self.rect.x = -1500
        if self.rect.y > 1000:
            self.rect.y = -1500
        if self.rect.x < -3000:
            self.rect.x = -1500
        if self.rect.y < -3000:
            self.rect.y = -1500

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    allSprites = None
    enemies = None
    lazers = None
    player = None
    
    # Other data    
    gameOver = False
    # score = 0
    
    def __init__(self):
        # self.score = 0
        self.paused = False
        self.gameOver = False
        self.allSprites = pygame.sprite.Group()
        self.lazers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = player.Player()
        self.allSprites.add(self.player)
        self.background = Background()

        for i in range(5):
            self.asteroid = enemies.Asteroid(self.player.rect.center,0)
            self.allSprites.add(self.asteroid)
            self.enemies.add(self.asteroid)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                shoot = pygame.mixer.Sound("shoot.ogg")
                pygame.mixer.Sound.play(shoot)
                self.lazer = self.fire()
                self.allSprites.add(self.lazer)
                self.lazers.add(self.lazer)
                if self.gameOver:
                    self.__init__()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            if self.paused == True:
                self.paused = False
            else:
                self.paused = True
        if key[pygame.K_r]:
            self.__init__()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.gameOver:
            for lazer in self.lazers:

                # See if it hit a block
                enemyHits = pygame.sprite.spritecollide(lazer, self.enemies, True)
                # For each block hisst, remove the bullet and add to the score
                for enemy in enemyHits:
                    self.lazers.remove(lazer)
                    self.allSprites.remove(lazer)
                    if enemy.size == 0:
                        self.asteroid = enemies.Asteroid(enemy.rect.center,1)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                        self.asteroid = enemies.Asteroid(enemy.rect.center,2)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                    elif enemy.size == 1 or enemy.size == 2:
                        self.asteroid = enemies.Asteroid(enemy.rect.center,3)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                        self.asteroid = enemies.Asteroid(enemy.rect.center,4)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)                       

            # see's if the player collides with the astriod
            playerhits = pygame.sprite.spritecollide(self.player, self.enemies,True)
            # checks if list is empty 
            if playerhits:
                deathsound = pygame.mixer.Sound("death.ogg")
                pygame.mixer.Sound.play(deathsound)
                self.player.lives -= 1
                print(self.player.lives)
                if self.player.lives < 1:
                # if so removes self.player from the list 
                    self.allSprites.remove(self.player)
                    
            if self.paused:
            # Display some text
                # font = pygame.font.Font(None, 36)
                # text = font.render("paused", 1, (10, 10, 10))
                # textpos = text.get_rect()
                # textpos.centerx = self.background.get_rect().centerx
                # self.background.blit(text, textpos)
                # pygame.time.wait(10)
                pass
            else:
                self.background.update()
                self.allSprites.update()
            
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.blit(self.background.image,self.background.rect)
        self.allSprites.draw(screen)
            
        pygame.display.flip()

    def fire(self):
        self.lazer = player.Lazer(self.player.angle, self.player.rect.center)
        return self.lazer 
        
def main():
    """ Main program function. """
    # Initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("LAST HOPE")
    pygame.mouse.set_visible(True)
    
    # Create our objects and set the data
    done = False
    clock = pygame.time.Clock()
    
    # Create an instance of the Game class
    game = Game()
    backgroundsong = pygame.mixer.Sound("background.ogg")
    pygame.mixer.Sound.play(backgroundsong)
    # Main game loop
    while not done:
        
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
        
        # Update object positions, check for collisions
        game.run_logic()
        
        # Draw the current frame
        game.display_frame(screen)
        
        # Pause for the next frame
        clock.tick(60)
        
    # Close window and exit    
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
