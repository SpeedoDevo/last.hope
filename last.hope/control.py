import pygame
import player
import enemies
import audio
import menu
import sys
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
    enemies = 2
    lazers = None
    player = None
    
    # Other data    
    gameOver = False
    score = 0
    
    def __init__(self):

        self.written = True
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
        self.gameOverScreen = TextOverlay("game over, your score:" + str(Game.score), RED)
        self.winScreen = TextOverlay("victory, your score:" + str(Game.score), GREEN)
        Game.scoreshow = TextOverlay("score", GREY)
        self.victory = False
        self.audio = audio.Sounds()


        for i in range(Game.enemies):
            self.asteroid = enemies.Asteroid(self.player.rect.center,0)
            self.allSprites.add(self.asteroid)
            self.enemies.add(self.asteroid)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
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

                        
            if event.type == pygame.KEYUP and event.key == pygame.K_q:
               if self.gameOver or self.victory:
                  game = menu.Startmenu()
                  audio.stopBackgroundMusic()
                  pygame.display.quit()
                  sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                if self.gameOver:
                    Game.enemies = 2
                    Game.score = 0
                elif self.victory == False:
                    Game.score = Game.score - 750
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
                enemyHits = pygame.sprite.spritecollide(lazer, self.enemies, True, pygame.sprite.collide_circle)
                # For each block hisst, remove the bullet and add to the score
                for enemy in enemyHits:
                    self.lazers.remove(lazer)
                    self.allSprites.remove(lazer)
                    if enemy.size == 0:
                        Game.score = Game.score + 25
                        
                        self.asteroid = enemies.Asteroid(enemy.rect.center,1)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                        self.asteroid = enemies.Asteroid(enemy.rect.center,2)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                    elif enemy.size == 1 or enemy.size == 2:
                        Game.score = Game.score + 50
                      
                        self.asteroid = enemies.Asteroid(enemy.rect.center,3)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                        self.asteroid = enemies.Asteroid(enemy.rect.center,4)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)                      
                    elif enemy.size == 3 or enemy.size == 4:
                        Game.score = Game.score + 75
                        
            # see's if the player collides with the astriod
            playerHit = pygame.sprite.spritecollide(self.player, self.enemies,True, pygame.sprite.collide_mask)
            # checks if list is empty 
            if playerHit:
                self.audio.deathSound()
                self.player.lives -= 1
                Game.score = Game.score - 1000
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
        self.gameOverScreen = TextOverlay("game over, your score:" + str(Game.score), RED)
        self.winScreen = TextOverlay("victory, you rock ! ", GREEN)
        screen.blit(self.background.image,self.background.rect)
        screen.blit(self.lives.image,self.lives.rect)
        self.allSprites.draw(screen)
        myfont = pygame.font.SysFont('image/langdon.otf', 30)
        contLabel = myfont.render("Press R to continue or Q to quit ", 1, (GREY))
		
        scoreLabel = myfont.render("Score: " + str(Game.score), 1, (GREY))
        screen.blit(scoreLabel, (10,30))
        levelLable = myfont.render("Level: " + str(Game.enemies - 1 ), 1, (GREY))
        screen.blit(levelLable, (10,50))
        if self.paused:
            self.pauseScreen.draw(screen)
        if self.gameOver:
            if self.written:
                
                file = open( "Scores.txt", "r" )
                array = []
                for line in file:
                    array.append(int(line))
                file.close()   
                print(array);
                array2 = [0,0,0,0,0,Game.score]
                for x in range(0,5):
                    print(x);
                    array2[x] = array[x]
                array2.sort(reverse = True)
                print(array2);
                file = open( "Scores.txt", "w" )
                file.write(str(array2[0]) + "\n" + str(array2[1]) + "\n" + str(array2[2]) + "\n" + str(array2[3]) + "\n" + str(array2[4]) + "\n")
                file.close()
                self.written = False
            self.gameOverScreen.draw(screen)
            screen.blit(contLabel, (300,400))
        if self.victory:
            if self.written:
                Game.enemies = Game.enemies + 1
                self.written = False
            self.winScreen.draw(screen)
            screen.blit(contLabel, (300,400))
        pygame.display.flip()

