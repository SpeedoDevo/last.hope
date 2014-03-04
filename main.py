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
        self.baseImage = pygame.image.load("ship.png").convert()
        self.rect = self.baseImage.get_rect()
        self.rect.x,self.rect.y = (SCREEN_WIDTH/2 - 90),(SCREEN_HEIGHT/2 - 90)
        self.baseImage.set_colorkey(BLACK)

    def update(self):
        """ Update the player location. """
        key = pygame.key.get_pressed()
        mousePosition = pygame.mouse.get_pos()
        # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_s] and self.rect.center[1] < SCREEN_HEIGHT:# down key
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
        self.angle = angle
        self.speedx =  self.speed*math.cos(math.radians(self.angle+90))
        self.speedy = -self.speed*math.sin(math.radians(self.angle+90))



    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

    # def draw(self, screen):
        
        

class Game(object):
    """ This class represents an instance of the game. If we need to
        reset the game we'd just need to create a new instance of this
        class. """

    all_sprites_list = None
    player = None
    
    # Other data    
    game_over = False
    # score = 0
    
    def __init__(self):
        # self.score = 0
        self.game_over = False
        self.all_sprites_list = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites_list.add(self.player)

    def process_events(self):
        """ Process all of the events. Return a "True" if we need
            to close the window. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.all_sprites_list.add(self.fire())
                if self.game_over:
                    self.__init__()

        return False

    def run_logic(self):
        """
        This method is run each time through the frame. It
        updates positions and checks for collisions.
        """
        if not self.game_over:
            # Move all the sprites
            self.all_sprites_list.update()
            
                
    def display_frame(self, screen):
        """ Display everything to the screen for the game. """
        screen.fill(WHITE)
        
        self.all_sprites_list.draw(screen)
            
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
