import pygame
import player
import enemies
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, GREY, BLACK)

class Background(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('image/background.gif')
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

class TextOverlay(pygame.sprite.Sprite):
    def __init__(self,string,color):
        pygame.sprite.Sprite.__init__(self)
        self.baseImage = pygame.Surface(pygame.display.get_surface().get_size(), flags=pygame.SRCALPHA)
        self.baseImage.fill((0,0,0,100))
        pygame.display.get_surface().blit(self.baseImage,(0,0))
        self.image = self.baseImage.copy()
        self.font = pygame.font.Font('image/langdon.otf', 70)
        self.text = self.font.render(string, True, color)
        self.textrect = self.text.get_rect()
        self.textrect.center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
        self.image.blit(self.text,self.textrect)
        self.screenRect = (0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
        if string == "paused":
            self.frameNum = 0
            self.isPaused = True
        else:
            self.isPaused = False

    def draw(self,screen):
        if self.isPaused:
            self.frameNum += 1
            if (self.frameNum % 70) < 35:
                screen.blit(self.image,self.screenRect)
            else:
                screen.blit(self.baseImage,self.screenRect)
        else:
            screen.blit(self.image,self.screenRect)

    def resetCounter(self):
        self.frameNum = 0

class LivesDisplay(pygame.sprite.Sprite):

    def __init__(self,lives):
        pygame.sprite.Sprite.__init__(self)
        self.baseImage = pygame.image.load('image/lives.tga')
        self.lives = lives

    def updateLives(self,lives):
        self.lives = lives

    def update(self):
        if self.lives < 0:
            self.lives = 0
        self.image = pygame.Surface((40*self.lives, 30))
        self.image.blit(self.baseImage,(0,0,40*self.lives, 30))
        self.rect = self.image.get_rect()

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
        self.lives = LivesDisplay(self.player.lives)
        self.pauseScreen = TextOverlay("paused", GREY)
        self.gameOverScreen = TextOverlay("game over", RED)
        self.winScreen = TextOverlay("victory", GREEN)
        self.victory = False
        self.shoot = pygame.mixer.Sound("sound/shoot.ogg")
        self.deathSound = pygame.mixer.Sound("sound/death.ogg")


        for i in range(5):
            self.asteroid = enemies.Asteroid(self.player.rect.center,0)
            self.allSprites.add(self.asteroid)
            self.enemies.add(self.asteroid)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if not (self.gameOver or self.paused) and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound.play(self.shoot)
                self.lazer = self.player.fire()
                self.allSprites.add(self.lazer)
                self.lazers.add(self.lazer)
                if self.gameOver:
                    self.__init__()
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                if self.paused:
                    self.paused = False
                else:
                    self.paused = True
                    self.pauseScreen.resetCounter()
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.__init__()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not (self.gameOver or self.paused):
            for lazer in self.lazers:

                # See if it hit a block
                enemyHits = pygame.sprite.spritecollide(lazer, self.enemies, True, pygame.sprite.collide_mask)
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
            playerHit = pygame.sprite.spritecollide(self.player, self.enemies,True, pygame.sprite.collide_mask)
            # checks if list is empty 
            if playerHit:
                pygame.mixer.Sound.play(self.deathSound)
                self.player.lives -= 1
                self.lives.updateLives(self.player.lives)
                if self.player.lives <= 0:
                # if so removes self.player from the list
                    self.gameOver = True
                    self.allSprites.remove(self.player)

            if not self.enemies and not self.gameOver:
                self.victory = True
                    
            self.background.update()
            self.lives.update()
            self.allSprites.update()
            
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.blit(self.background.image,self.background.rect)
        screen.blit(self.lives.image,self.lives.rect)
        self.allSprites.draw(screen)
        if self.paused:
            self.pauseScreen.draw(screen)
        if self.gameOver:
            self.gameOverScreen.draw(screen)
        if self.victory:
            self.winScreen.draw(screen)
        pygame.display.flip()

