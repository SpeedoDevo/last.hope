import pygame
import control
import audio
import menu
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT)

      
def main():
    """ Main program function. """
    # initialize Pygame and set up the window
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("LAST HOPE")
    pygame.mouse.set_visible(True)
    
    done = False
    clock = pygame.time.Clock()
    audio.startBackgroundMusic()
    mainMenu = menu.Menu(screen, clock)
    mainMenu.run()
    game = control.Game(mainMenu, mainMenu.bg)

    # main game loop
    while not done:
        # process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
        
        # update object positions, check for collisions
        game.run_logic()
        
        # draw the current frame
        game.display_frame(screen)
        
        # tick
        clock.tick(70)
        
    # close window and exit
    pygame.quit()

# call the main function, start up the game
if __name__ == "__main__":
    main()
