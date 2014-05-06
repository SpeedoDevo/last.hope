import pygame

def startBackgroundMusic():
    pygame.mixer.Sound("sound/background.ogg").play(-1)
def stopBackgroundMusic():
    print("stop");
    pygame.mixer.music.stop()
class Sounds(object):
    def __init__(self):
        pygame.mixer.set_num_channels(1000)
        self.death = pygame.mixer.Sound("sound/death.ogg")
        self.shoot = pygame.mixer.Sound("sound/shoot2.wav")
        self.shoot.set_volume(0.5)

    def deathSound(self):
        self.death.play()

    def shootSound(self):
        self.shoot.play()

