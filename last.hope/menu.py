''''

@font: from http://www.dafont.com/coders-crux.font
      more about license you can find in data/coders-crux/license.txt
'''

import pygame
import main
from pygame.locals import *

if not pygame.display.get_init():
    pygame.display.init()

if not pygame.font.get_init():
    pygame.font.init()

def Startmenu():
    print("FFS2");
    class Menu: 
        print("yoooo");    
        lista = []
        pola = []
        fontSize = 50
      
        font_path = 'data/coders_crux/coders_crux.ttf'
        font = pygame.font.Font
        dest_surface = pygame.Surface
        ilosc_pol = 0
        fontBackGroundColour = (51,51,51)   
        fontColour =  (255, 255, 153)
        textHighlight = (192,192,192)
        pos_mark = 0
        posMenu = (0,0)
        menu_width = 0
        menu_height = 0

        class Pole:
            tekst = ''
            pole = pygame.Surface
            pole_rect = pygame.Rect
            mark_rect = pygame.Rect

        def move_menu(self, top, left):
            self.posMenu = (top,left) 

        def set_colors(self, text, selection, background):
            self.fontBackGroundColour = background
            self.fontColour =  text
            self.textHighlight = selection
            
        def set_fontsize(self,font_size):
            self.fontSize = font_size
            
        def set_font(self, path):
            self.font_path = path
            
        def get_position(self):
            return self.pos_mark
        
        def init(self, lista, dest_surface):
            self.lista = lista
            self.dest_surface = dest_surface
            self.ilosc_pol = len(self.lista)
            self.stworz_strukture()      
            pygame.mixer.init()
            pygame.mixer.set_num_channels(1000)
            self.move = pygame.mixer.Sound("sound/select.wav")
            self.enter = pygame.mixer.Sound("sound/death.ogg")
            
        def draw(self,przesun=0):
            if przesun:
                self.pos_mark += przesun 
                if self.pos_mark == -1:
                    self.pos_mark = self.ilosc_pol - 1
                self.pos_mark %= self.ilosc_pol
            menu = pygame.Surface((self.menu_width, self.menu_height))
            menu.fill(self.fontBackGroundColour)
            mark_rect = self.pola[self.pos_mark].mark_rect
            pygame.draw.rect(menu,self.textHighlight,mark_rect)

            for i in range(self.ilosc_pol):
                menu.blit(self.pola[i].pole,self.pola[i].pole_rect)
            self.dest_surface.blit(menu,self.posMenu)
            return self.pos_mark

        def stworz_strukture(self):
            time = 0
            self.menu_height = 0
            self.font = pygame.font.Font(self.font_path, self.fontSize)
            for i in range(self.ilosc_pol):
                self.pola.append(self.Pole())
                self.pola[i].tekst = self.lista[i]
                self.pola[i].pole = self.font.render(self.pola[i].tekst, 1, self.fontColour)

                self.pola[i].pole_rect = self.pola[i].pole.get_rect()
                time = int(self.fontSize * 0.2)

                height = self.pola[i].pole_rect.height
                self.pola[i].pole_rect.left = time
                self.pola[i].pole_rect.top = time+(time*2+height)*i

                width = self.pola[i].pole_rect.width+time*2
                height = self.pola[i].pole_rect.height+time*2            
                left = self.pola[i].pole_rect.left-time
                top = self.pola[i].pole_rect.top-time

                self.pola[i].mark_rect = (left,top ,width, height)
                if width > self.menu_width:
                        self.menu_width = width
                self.menu_height += height
            x = self.dest_surface.get_rect().centerx - self.menu_width / 2
            y = self.dest_surface.get_rect().centery - self.menu_height / 2
            mx, my = self.posMenu
            self.posMenu = (x+mx, y+my) 
            
  
    __name__= "__main__"
    if __name__ == "__main__":
        import sys
        surface = pygame.display.set_mode((854,480)) #0,6671875 and 0,(6) of HD resoultion
        surface.fill((51,51,51))
        menu = Menu()#necessary

        logo = pygame.image.load('Logo.png')
        surface.blit(logo, (230, 30))
        menu.init(['Start','Tutorial','Leader Board','Quit'], surface)#necessary
      
        menu.draw()#necessary
        
        pygame.key.set_repeat(199,69)#(delay,interval)
        pygame.display.update()
        while 1:
            for event in pygame.event.get():
                
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        menu.draw(-1) #here is the Menu class function
                        menu.move.play()
                    if event.key == K_DOWN:
                        menu.draw(1) #here is the Menu class function
                        menu.move.play()
                    if event.key == K_RETURN:
                        menu.enter.play()
                        if menu.get_position() == 3:#here is the Menu class function  
                            pygame.display.quit()
                            sys.exit()
                        if menu.get_position() == 0:#Starts game
                            game = main.main()
                         
                            pygame.display.quit()
                            sys.exit()
                    if event.key == K_ESCAPE:
                        menu.enter.play()
                        pygame.display.quit()
                        sys.exit()
                    pygame.display.update()
                elif event.type == QUIT:
                    pygame.display.quit()
                    sys.exit()
            pygame.time.wait(8)
if __name__ == "__main__":
    Startmenu()           
