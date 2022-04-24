import time

from weapon import Weapon

WIDTH, HEIGHT = 800, 750


class Ship:
    COOLDOWN = 15

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.weapon_img = None
        self.weapons = []
        self.cool_down_counter = 0

    # drawing ship on the screen
    def draw(self, window):
        try:
            window.blit(self.ship_img, (self.x, self.y))
        except:
            time.sleep((0.1))
            window.blit(self.ship_img, (-self.x, -self.y))

        for weapon in self.weapons:
            weapon.draw(window)

    # moving weapons, checking for collision or weapon's being offscreen
    def move_weapons(self, vel, obj):
        self.cooldown()
        for weapon in self.weapons:
            weapon.move(vel)
            if weapon.off_screen(HEIGHT):
                self.weapons.remove(weapon)
            elif weapon.collision(obj):
                obj.health -= 10
                self.weapons.remove(weapon)

    # prevent spamming weapon
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # shooting a weapon
    def shoot(self):
        if self.cool_down_counter == 0:
            weapon = Weapon(self.x, self.y, self.weapon_img)
            self.weapons.append(weapon)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
