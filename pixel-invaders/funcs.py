import pygame
import os

# function which determines whether two objects have collided with eachother based on their collision masks
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# getting absolute path, so the program is able to run regardless of location
def absolute_path(path: str) -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
