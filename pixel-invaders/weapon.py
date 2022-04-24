import pygame
from funcs import collide

class Weapon:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # drawing weapon on the screen
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # moving weapon 
    def move(self, vel):
        self.y += vel

    # checking if weapon is behind the screen
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    # checking for collision between weapon
    def collision(self, obj):
        return collide(obj, self)