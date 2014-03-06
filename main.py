import pygame
import random
import math

#--- Global constants ---
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

SCREEN_WIDTH  = 700
SCREEN_HEIGHT = 500

# --- Classes ---


class Player(pygame.sprite.Sprite):
    """ This class represents the player. """

    angle = 1
    speed = 3

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.baseImage = pygame.image.load("ship.tga")
        self.rect = self.baseImage.get_rect()
        self.rect.x,self.rect.y = (SCREEN_WIDTH/2 - 90),(SCREEN_HEIGHT/2 - 90)

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
        self.image,self.rect = rot_center(self.baseImage, self.rect, self.angle)


class Lazer(pygame.sprite.Sprite):
    speed = 5

    def __init__(self, angle, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("lazer.tga")
        self.rect = pygame.rect.Rect(center,self.image.get_size())
        self.speedx =  self.speed*math.cos(math.radians(angle+90))
        self.speedy = -self.speed*math.sin(math.radians(angle+90))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

class Asteroid(pygame.sprite.Sprite):

    def __init__(self,pos,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        if size == 0:
            self.baseImage = pygame.image.load("asteroid0.tga")
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
            self.baseImage = pygame.image.load("asteroid10.tga")
        if size == 2:
            self.baseImage = pygame.image.load("asteroid11.tga")
        if size == 3:
            self.baseImage = pygame.image.load("asteroid20.tga")
        if size == 4:
            self.baseImage = pygame.image.load("asteroid21.tga")
        if size == 1 or size == 2 or size == 3 or size == 4:
            self.center = pos
            self.angle = random.randrange(0,360)
        self.rect = pygame.rect.Rect(self.center,self.baseImage.get_size())
        if size == 0:
            self.angle = random.randrange(80,120)/100*math.degrees(math.atan2(self.rect.center[0]-pos[0], self.rect.center[1]-pos[1]))
        self.speed = random.triangular(1.0, 4.0)
        self.speedx =  self.speed*math.cos(math.radians(self.angle+90))
        self.speedy = -self.speed*math.sin(math.radians(self.angle+90))
        self.rotaSpeed = random.randrange(0,7)
        self.angle = random.randrange(0,360)

    def update(self):
        self.angle += self.rotaSpeed
        self.image,self.rect = rot_center(self.baseImage, self.rect, self.angle)
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


class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    allSprites = None
    enemies = None
    lazers = None
    player = None
    
    # Other data    
    game_over = False
    # score = 0
    
    def __init__(self):
        # self.score = 0
        self.game_over = False
        self.allSprites = pygame.sprite.Group()
        self.lazers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        self.player = Player()
        self.allSprites.add(self.player)

        for i in range(10):
            self.asteroid = Asteroid(self.player.rect.center,0)
            self.allSprites.add(self.asteroid)
            self.enemies.add(self.asteroid)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.lazer = self.fire()
                self.allSprites.add(self.lazer)
                self.lazers.add(self.lazer)
                if self.game_over:
                    self.__init__()
        key = pygame.key.get_pressed()
        if key[pygame.K_r]:
            self.__init__()


        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            for lazer in self.lazers:

                # See if it hit a block
                enemyHits = pygame.sprite.spritecollide(lazer, self.enemies, True)
                # For each block hisst, remove the bullet and add to the score
                for enemy in enemyHits:
                    self.lazers.remove(lazer)
                    self.allSprites.remove(lazer)
                    if enemy.size == 0:
                        self.asteroid = Asteroid(enemy.rect.center,1)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                        self.asteroid = Asteroid(enemy.rect.center,2)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                    elif enemy.size == 1 or enemy.size == 2:
                        self.asteroid = Asteroid(enemy.rect.center,3)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)
                        self.asteroid = Asteroid(enemy.rect.center,4)
                        self.allSprites.add(self.asteroid)
                        self.enemies.add(self.asteroid)                       

            # playerHits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            # print(playerHits, not playerHits)
            # if playerHits:
            #     self.allSprites.remove(self.player)
                    
            self.allSprites.update()
            
                
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(BLACK)
        
        self.allSprites.draw(screen)
            
        pygame.display.flip()

    def fire(self):
        self.lazer = Lazer(self.player.angle, self.player.rect.center)
        return self.lazer

def rot_center(image, rect, angle):
        """rotate an image while keeping its center"""
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image,rot_rect
    
        
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
