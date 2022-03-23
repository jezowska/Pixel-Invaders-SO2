import pygame
import os
from laser import Laser
from ship import Ship

main_path = os.path.dirname(os.path.realpath(__file__))

def absolute_path(path: str) -> str:
    return os.path.join(main_path, path)

WIDTH, HEIGHT = 800, 750

#  Player ship
PLAYER_SPACESHIP = pygame.transform.scale(pygame.image.load(absolute_path(os.path.join("assets",  "player.png"))), (80,100))
#  Lasers
YELLOW_LASER = pygame.image.load(absolute_path(os.path.join("assets",  "pixel_laser_yellow.png")))


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACESHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.points = 0

    def move_lasers(self, vel, enemies, bosses):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for enemy in enemies:
                    if laser.collision(enemy):
                        enemies.remove(enemy)
                        self.points += 100
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                for boss in bosses:
                    if laser.collision(boss):
                        if(boss.health <= 10):
                            self.points += 500
                        boss.health -= 10
                        self.points += 100
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))
