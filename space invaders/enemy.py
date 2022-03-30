import imp
import pygame
import time
import os
import random
import threading
from laser import Laser
from ship import Ship
from funcs import absolute_path

RED_LASER = pygame.image.load(absolute_path(os.path.join("images",  "pixel_laser_red.png")))
GREEN_LASER = pygame.image.load(absolute_path(os.path.join("images",  "pixel_laser_green.png")))
BLUE_LASER = pygame.image.load(absolute_path(os.path.join("images",  "pixel_laser_blue.png")))

RED_SPACESHIP = pygame.transform.rotate(pygame.image.load(absolute_path(os.path.join("images",  "purple.png"))), 180)
GREEN_SPACESHIP = pygame.transform.rotate(pygame.image.load(absolute_path(os.path.join("images",  "green.png"))), 180)
BLUE_SPACESHIP = pygame.transform.rotate(pygame.image.load(absolute_path(os.path.join("images",  "blue.png"))), 180)

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACESHIP, RED_LASER),
                "green": (GREEN_SPACESHIP, GREEN_LASER),
                "blue": (BLUE_SPACESHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
