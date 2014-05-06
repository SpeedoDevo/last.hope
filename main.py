import pygame
import control
import audio
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT)

      
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
    game = control.Game()
    audio.startBackgroundMusic()
    # Main game loop
    while not done:
        
        # print("prcss " + str(pygame.time.get_ticks()))
        # Process events (keystrokes, mouse clicks, etc)
        done = game.process_events()
        
        # print("logic " + str(pygame.time.get_ticks()))
        # Update object positions, check for collisions
        game.run_logic()
        
        # print("frame " + str(pygame.time.get_ticks()))
        # Draw the current frame
        game.display_frame(screen)
        
        # print("fps   " + str(clock.get_fps()))
        # Pause for the next frame
        clock.tick_busy_loop(70)
        
    # Close window and exit    
    pygame.quit()

# Call the main function, start up the game
if __name__ == "__main__":
    main()
