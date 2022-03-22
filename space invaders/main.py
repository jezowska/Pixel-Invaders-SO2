import pygame
import time
import os
import random
import threading
pygame.font.init()


WIDTH, HEIGHT = 800, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Hooters")


clock = pygame.time.Clock()


# Load images
RED_SPACESHIP = pygame.transform.rotate(pygame.image.load(os.path.join("assets", "purple.png")), 180)
GREEN_SPACESHIP = pygame.transform.rotate(pygame.image.load(os.path.join("assets", "green.png")), 180)
BLUE_SPACESHIP = pygame.transform.rotate(pygame.image.load(os.path.join("assets", "blue.png")), 180)
BOSS1_SPACESHIP = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(os.path.join("assets", "boss1.png")), 180), (150,150))

# Player ship
PLAYER_SPACESHIP = pygame.transform.scale(pygame.image.load(os.path.join("assets", "player.png")), (80,100))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background.png")), (WIDTH, HEIGHT))


class Ship:
    COOLDOWN = 15

    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SPACESHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, enemies):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for enemy in enemies:
                    if laser.collision(enemy):
                        enemies.remove(enemy)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


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


class Boss(Ship, threading.Thread):
    def __init__(self, x, y, layer, health=1000):
        super().__init__(x, y, health)
        threading.Thread.__init__(self)

        self.bounced = 0

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

        if  self.y < 0 or  (self.y + self.ship_img.get_height()) > HEIGHT:
            self.vel_y *= -1.0
            self.bounced += 1
    
    def run(self):
        while (self.bounced < 10):#to odbijanie zostawilam bo to na razie jedyny sposob jaki mamy na organiczne usuwanie watkow ze statkami xd 
            #trzba tu bedzie zaimplementowac zycie statkow w whileu
            #a i jakos niszczyc watki jak sie wyjdzie z gry, bo aktualnie jak przedwczesnie sie zakonczy gre to te watki sb nadal dzialaja w tle dopoki pamiec im sie nie skoczy
            clock.tick(60)
            self.move()

            
            self.layer.fill((255,255,0))#czyscimy layer danego bossa kolorem ktory zostal zdefiniowany jako przezroczysty przez colorkey
            self.draw(self.layer)#rysujemy statek bossa na czystym layerze

            #te mutexy na przyszlosc zostawilam okomentowane, idk xd

            #mutex.acquire()
            #try:
            #    self.layer.fill((255,255,0))
            #    super().draw(self.layer)
                
                #pygame.draw.rect(WIN, (0,0,0), (old_x,  old_y, self.ship_img.get_width(), self.ship_img.get_height()))
            #finally:
            #    mutex.release()

        #mutex.acquire()
        #try:
        self.layer.fill((255,255,0))#ostatnie wyczyszczenie layera, tak zeby wrak statku nie zostawal na ekranie jak sie watek skonczy
        #finally:
        #    mutex.release()
        
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        #pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def move(self):
        self.check_border()
        self.x  += self.vel_x
        self.y += self.vel_y

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
    
    def collision(self, obj):
        return collide(obj, self)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5

    player_vel = 10
    enemy_vel = 3
    player_laser_vel = 15
    enemy_laser_vel = 8

    player = Player(300, 630)

    #listy z bossami i ich layerami. na razie kazdy boss ma swoj osobny layer, potem mozna to zmergeowac ale do tego potrzebne by byly mutexy
    bosses = []
    layers = []
    for i in range(5):
        #nieprzezroczysty layer w ktorych ustawiany jest colorkey - kazdy pixel na tej powierzchni ktory bedzie mial ten kolor nie zostanie zblitowany na glowne okno gry
        layer = pygame.Surface((WIDTH,HEIGHT))
        layer.set_colorkey((255,255,0))
        layers.append(layer)

        #tworzymy obiekty bossow, przekazujemy im layery przez referencje, dodajemy je do listy i zaczynamy ich watki
        boss = Boss(random.randrange(100, WIDTH - 200),random.randrange(100, HEIGHT - 200),layer)
        bosses.append(boss)
        boss.start()

    lost = False
    lost_count = 0

    

    def redraw_window():
        WIN.blit(BG, (0 ,0))

        level_label = main_font.render(f"Level: {level}", 1, (255 ,255, 255))

        WIN.blit(level_label, (WIDTH - 10 - level_label.get_width(), 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost == True:
            lost_label = lost_font.render("You Lost!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        #dla kazdego bossowego layera w liscie blitujemy go na glowne okno
        for layer in layers:
            WIN.blit(layer, (0,0))

        #jednorazowo updateujemy zawartosc glownego okna, nigdzie w watkach nie updateujemy jakis fragmentow ekranu czy cos
        pygame.display.update()

    while run:
        clock.tick(120)
        redraw_window()


        # lost screen
        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue


        # spawning enemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500 -(500 * level), -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)


        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        #keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - player_vel > 0: # left
            player.x -= player_vel
        
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel

        if keys[pygame.K_UP] and player.y - player_vel > 0: # up
            player.y -= player_vel

        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel

        if keys[pygame.K_z]:
            player.shoot()


        # enemies
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(enemy_laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)


        player.move_lasers(-player_laser_vel, enemies)


def main_menu():
    run = True
    title_font = pygame.font.SysFont("comicsans", 50)
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()

    pygame.quit()

main_menu()
