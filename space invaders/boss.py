import pygame
import os
import random
import threading
from laser import Laser
from ship import Ship

clock = pygame.time.Clock()
WIDTH, HEIGHT = 800, 750

main_path = os.path.dirname(os.path.realpath(__file__))

def absolute_path(path: str) -> str:
    return os.path.join(main_path, path)

#  Load images
BOSS1_SPACESHIP = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(absolute_path(os.path.join("images",  "boss1.png"))), 180), (150,150))           
YELLOW_LASER = pygame.image.load(absolute_path(os.path.join("images",  "pixel_laser_yellow.png")))


class Boss(Ship, threading.Thread):
    def __init__(self, x:int, y:int, layer:pygame.Surface, health=50):
        super().__init__(x, y, health)
        threading.Thread.__init__(self)
        self.bounced = 0
        self.not_collision = True
        self.ship_img =  BOSS1_SPACESHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.layer = layer
        self.max_health = health

        self.vel_y = 4.0
        self.vel_x = random.randrange(0.0, 10.0)
    
    def check_border(self):
        if  self.x < 0 or  (self.x + self.ship_img.get_width()) > WIDTH:
            self.vel_x *= -1.0
            self.bounced += 1 

        if  self.y < 0 or  (self.y + self.ship_img.get_height()) > HEIGHT - 150:
            self.vel_y *= -1.0
            self.bounced += 1
    
    def run(self):
        #self.bounced < 10 and
        while ( self.health > 0):# to odbijanie zostawilam bo to na razie jedyny sposob jaki mamy na organiczne usuwanie watkow ze statkami xd 
            # trzba tu bedzie zaimplementowac zycie statkow w whileu
            # a i jakos niszczyc watki jak sie wyjdzie z gry, bo aktualnie jak przedwczesnie sie zakonczy gre to te watki sb nadal dzialaja w tle dopoki pamiec im sie nie skoczy
            clock.tick(60)
            self.move()

            
            self.layer.fill((255,255,0)) # czyscimy layer danego bossa kolorem ktory zostal zdefiniowany jako przezroczysty przez colorkey
            self.draw(self.layer) # rysujemy statek bossa na czystym layerze

            # te mutexy na przyszlosc zostawilam okomentowane, idk xd

            # mutex.acquire()
            # try:
            #     self.layer.fill((255,255,0))
            #     super().draw(self.layer)
                
                # pygame.draw.rect(WIN, (0,0,0), (old_x,  old_y, self.ship_img.get_width(), self.ship_img.get_height()))
            # finally:
            #     mutex.release()

        # mutex.acquire()
        # try:
        self.layer.fill((255,255,0)) # ostatnie wyczyszczenie layera, tak zeby wrak statku nie zostawal na ekranie jak sie watek skonczy
        # finally:
        #     mutex.release()
        self.layer = None
        self.join
        
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def move(self):
        self.check_border()
        self.x  += self.vel_x
        self.y += self.vel_y

    def shoot(self):
        if(random.randrange(0, 100) > 90):
            if self.cool_down_counter == 0:
                laser = Laser(self.x - 20, self.y, self.laser_img)
                self.lasers.append(laser)
                self.cool_down_counter = 1

