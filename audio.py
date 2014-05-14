import pygame

# load and play background music indefinitely
def startBackgroundMusic():
    pygame.mixer.Sound("sound/background.ogg").play(-1)

# stop background music
def stopBackgroundMusic():
    pygame.mixer.music.stop()

# class for playing sounds
class Sounds(object):
    def __init__(self):
        # load sounds
        pygame.mixer.set_num_channels(1000)
        self.death = pygame.mixer.Sound("sound/death.ogg")
        self.shoot = pygame.mixer.Sound("sound/shoot2.wav")
        self.shoot.set_volume(0.5)

    # fns for playing sounds
    def deathSound(self):
        self.death.play()

    def shootSound(self):
        self.shoot.play()

