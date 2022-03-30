import pygame
import os
from laser import Laser
from ship import Ship
from funcs import absolute_path

WIDTH, HEIGHT = 800, 750

PLAYER_SPACESHIP = pygame.transform.scale(pygame.image.load(absolute_path(os.path.join("images",  "player.png"))), (80,100))
YELLOW_LASER = pygame.image.load(absolute_path(os.path.join("images",  "pixel_laser_yellow.png")))


class Player(Ship):
    def __init__(self, x:int, y:int, health=100) -> None:
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACESHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.points = 0
        self.vel = 15

    def move_lasers(self, vel:int, enemies:list, bosses:list):
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
    def draw(self, window:pygame.display) -> None:
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window:pygame.display) -> None:
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def move(self, keys:pygame.key) -> None:
        if keys[pygame.K_LEFT] and self.x - self.vel > 0: #  left
            self.x -= self.vel
        
        if keys[pygame.K_RIGHT] and self.x + self.vel + self.get_width() < WIDTH: #  right
            self.x += self.vel

        if keys[pygame.K_UP] and self.y - self.vel > 0: #  up
            self.y -= self.vel

        if keys[pygame.K_DOWN] and self.y + self.vel + self.get_height() + 15 < HEIGHT: #  down
            self.y += self.vel

        if keys[pygame.K_z]:
            self.shoot()
