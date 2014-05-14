import pygame
import player
import enemies
import audio
import menu
import eztext
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, RED, GREEN, GREY, BLACK, WHITE)

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
                self.rect.x += 1
            self.rect.x -= 3
        if self.rect.x > 1000:
            self.rect.x = -1500
        if self.rect.y > 1000:
            self.rect.y = -1500
        if self.rect.x < -3000:
            self.rect.x = -1500
        if self.rect.y < -3000:
            self.rect.y = -1500

class TextOverlay(pygame.sprite.Sprite):
    def __init__(self,string,color,size=70):
        pygame.sprite.Sprite.__init__(self)
        self.baseImage = pygame.Surface(pygame.display.get_surface().get_size(), flags=pygame.SRCALPHA)
        self.baseImage.fill((0,0,0,100))
        pygame.display.get_surface().blit(self.baseImage,(0,0))
        self.image = self.baseImage.copy()
        self.font = pygame.font.Font('image/langdon.otf', size)
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

class LevelChangeOverlay(TextOverlay):
    def __init__(self, level, game):
        TextOverlay.__init__(self, "level " + str(level), GREEN)
        self.level = level
        self.tutorial = [TextOverlay("wasd to move", GREEN, 50),\
                         TextOverlay("use the mouse to aim", GREEN, 50),\
                         TextOverlay("press the left mouse button to shoot", GREEN, 50),\
                         TextOverlay("esc to pause", GREEN, 50),\
                         TextOverlay("then hit q to exit to the main", GREEN, 50),\
                         TextOverlay("press r to restart", GREEN, 50), \
                         TextOverlay("press k next time to skip the tutorial", RED, 50)]
        self.fight = TextOverlay("fight", RED)
        self.game = game
        self.frameNum = 0

    def draw(self,screen):
        if not self.game.paused:
            self.frameNum += 1
        if self.level == 1:
            if self.frameNum < 840:
                self.tutorial[int(self.frameNum/120)].draw(screen)
            else:
                self.frameNum = 0
                self.level = 0
        else:
            if self.frameNum < 70:
                screen.blit(self.image,self.screenRect)
            elif self.frameNum < 100:
                screen.blit(self.baseImage,self.screenRect)
            elif self.frameNum < 140:
                self.fight.draw(screen)
            elif self.frameNum < 180:
                self.game.startLevel()
                self.game.levelChange = False
                self.frameNum = 0

    def update(self, level):
        TextOverlay.__init__(self, "level " + str(level), GREEN)

    def skipTutorial(self):
        self.frameNum = 0
        self.level = 0


class ScoreDisplay(pygame.sprite.Sprite):
    def __init__(self, score):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font('image/muzarela.ttf', 40)
        self.text = self.font.render(str(score), True, WHITE)
        self.rect = self.text.get_rect()
        self.rect.right = SCREEN_WIDTH

    def update(self, score):
        self.text = self.font.render(str(score), True, WHITE)
        self.rect = self.text.get_rect()
        self.rect.right = SCREEN_WIDTH
        

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
    
    def __init__(self, mainMenu, bg, lastInput=""):
        self.score = 0
        self.paused = False
        self.gameOver = False
        self.written = True
        self.allSprites = pygame.sprite.Group()
        self.lazers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = player.Player()
        self.allSprites.add(self.player)
        self.background = bg
        self.lives = LivesDisplay(self.player.lives)
        self.pauseScreen = TextOverlay("paused", GREY)
        self.gameOverScreen = TextOverlay("game over", RED)
        self.victory = False
        self.levelChange = True
        self.asteroids = 1
        self.level = 1
        self.levelChangeOverlay = LevelChangeOverlay(self.level, self)
        self.scoreDisplay = ScoreDisplay(self.score)
        self.mainMenu = mainMenu
        self.audio = audio.Sounds()
        self.input = eztext.Input(x=330,y=320,font=self.scoreDisplay.font,color=WHITE,prompt="name: ")
        self.input.value = lastInput

    def startLevel(self):
        self.allSprites.empty()
        self.enemies.empty()
        self.lazers.empty()
        self.allSprites.add(self.player)
        self.level += 1
        self.asteroids += 3
        for i in range(self.asteroids):
            self.asteroid = enemies.Asteroid(self.player.rect.center,0)
            self.allSprites.add(self.asteroid)
            self.enemies.add(self.asteroid)
        self.levelChangeOverlay.update(self.level)


    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """


        events = pygame.event.get()
        if self.gameOver: self.input.update(events)
        for event in events:
            if not (self.gameOver or self.paused) and event.type == pygame.MOUSEBUTTONDOWN:
                self.audio.shootSound()
                self.lazer = self.player.fire()
                self.allSprites.add(self.lazer)
                self.lazers.add(self.lazer)
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE and not (self.gameOver or self.victory):
                if self.paused:
                    self.paused = False
                else:
                    self.paused = True
                    self.pauseScreen.resetCounter()
            if self.paused and event.type == pygame.KEYUP and event.key == pygame.K_q:
                self.mainMenu.run()
                self.__init__(self.mainMenu, self.background, self.input.value)
            if event.type == pygame.KEYUP and event.key == pygame.K_r and not self.gameOver:
                self.__init__(self.mainMenu, self.background, self.input.value)
            if self.gameOver and event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                if self.score > self.mainMenu.hsTable.getLowest():
                    self.mainMenu.hsTable.submitScore(self.input.value,self.score)
                else:
                    self.mainMenu.hsTable.noHS()
                self.mainMenu.hsTable.run()
                self.__init__(self.mainMenu, self.background, self.input.value)
            if self.levelChange and event.type == pygame.KEYUP and event.key == pygame.K_k:
                self.levelChangeOverlay.skipTutorial()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not (self.gameOver or self.paused):
            for lazer in self.lazers:

                # See if it hit a block
                enemyHits = pygame.sprite.spritecollide(lazer, self.enemies, True, pygame.sprite.collide_circle)
                # For each block hisst, remove the bullet and add to the score
                for enemy in enemyHits:
                    self.lazers.remove(lazer)
                    self.allSprites.remove(lazer)
                    if enemy.size == 0:
                        self.score += 25
                        self.asteroid = enemies.Asteroid(enemy.rect.center,1)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                        self.asteroid = enemies.Asteroid(enemy.rect.center,2)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                    elif enemy.size == 1 or enemy.size == 2:
                        self.score += 50
                        self.asteroid = enemies.Asteroid(enemy.rect.center,3)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                        self.asteroid = enemies.Asteroid(enemy.rect.center,4)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                    elif enemy.size == 3 or enemy.size == 4:
                        self.score += 75
                    

            # see's if the player collides with the astriod
            playerHit = pygame.sprite.spritecollide(self.player, self.enemies,True, pygame.sprite.collide_mask)
            # checks if list is empty 
            if playerHit:
                self.audio.deathSound()
                self.player.lives -= 1
                self.lives.updateLives(self.player.lives)
                if self.player.lives <= 0:
                # if so removes self.player from the list
                    self.gameOver = True
                    self.allSprites.remove(self.player)

            if not self.enemies and not self.gameOver:
                self.levelChange = True

            self.scoreDisplay.update(self.score)
            self.background.update()
            self.lives.update()
            self.allSprites.update()
            
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.blit(self.background.image,self.background.rect)
        screen.blit(self.lives.image,self.lives.rect)
        screen.blit(self.scoreDisplay.text,self.scoreDisplay.rect)
        self.allSprites.draw(screen)
        if self.gameOver:
            self.gameOverScreen.draw(screen)
            if self.score > self.mainMenu.hsTable.getLowest(): self.input.draw(screen)
        if self.victory:
            self.winScreen.draw(screen)
        if self.levelChange:
            self.levelChangeOverlay.draw(screen)
        if self.paused:
            self.pauseScreen.draw(screen)
        pygame.display.update()

