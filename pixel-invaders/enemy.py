import pygame
import os
from weapon import Weapon
from ship import Ship
from funcs import absolute_path


#loading the textures used for ships and their weapons
RED_WEAPON = pygame.image.load(absolute_path(os.path.join("images",  "pixel_weapon_red.png")))
GREEN_WEAPON = pygame.image.load(absolute_path(os.path.join("images",  "pixel_weapon_green.png")))
BLUE_WEAPON = pygame.image.load(absolute_path(os.path.join("images",  "pixel_weapon_blue.png")))

RED_SPACESHIP = pygame.transform.rotate(pygame.image.load(absolute_path(os.path.join("images",  "purple.png"))), 180)
GREEN_SPACESHIP = pygame.transform.rotate(pygame.image.load(absolute_path(os.path.join("images",  "green.png"))), 180)
BLUE_SPACESHIP = pygame.transform.rotate(pygame.image.load(absolute_path(os.path.join("images",  "blue.png"))), 180)


#Class representing the minor enemies' ships
class Enemy(Ship):

    #color map binding three colors to their respective ship and weapon textures
    COLOR_MAP = {
                "red": (RED_SPACESHIP, RED_WEAPON),
                "green": (GREEN_SPACESHIP, GREEN_WEAPON),
                "blue": (BLUE_SPACESHIP, BLUE_WEAPON)
                }

    #init method calling for the parent's init and setting the appropriate images as its textures
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        cool_down_counter = 0
        self.ship_img, self.weapon_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    #function used for determining the ship's position based on its vertical speed parameter
    def move(self, vel):
        self.y += vel

    #spawns weapon objects at random time intervals
    def shoot(self):
        if self.cool_down_counter == 0:
            weapon = Weapon(self.x - 20, self.y, self.weapon_img)
            self.weapons.append(weapon)
            self.cool_down_counter = 1
