import pygame
import time
import os
import random
import threading
from player import Player
from enemy import Enemy
from laser import Laser
from boss import Boss
from collide import collide

pygame.font.init()


WIDTH, HEIGHT = 800, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Hooters")

main_path = os.path.dirname(os.path.realpath(__file__))

def absolute_path(path: str) -> str:
    return os.path.join(main_path, path)

clock = pygame.time.Clock()

RED_SPACESHIP = pygame.transform.rotate(pygame.image.load(absolute_path(os.path.join("assets",  "purple.png"))), 180)




#  Background
BG = pygame.transform.scale(pygame.image.load(absolute_path(os.path.join("assets",  "background.png"))), (WIDTH, HEIGHT))


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

    # listy z bossami i ich layerami. na razie kazdy boss ma swoj osobny layer, potem mozna to zmergeowac ale do tego potrzebne by byly mutexy
    bosses = []
    layers = []
    for i in range(5):
        # nieprzezroczysty layer w ktorych ustawiany jest colorkey - kazdy pixel na tej powierzchni ktory bedzie mial ten kolor nie zostanie zblitowany na glowne okno gry
        layer = pygame.Surface((WIDTH,HEIGHT))
        layer.set_colorkey((255,255,0))
        layers.append(layer)

        # tworzymy obiekty bossow, przekazujemy im layery przez referencje, dodajemy je do listy i zaczynamy ich watki
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

        # dla kazdego bossowego layera w liscie blitujemy go na glowne okno
        for layer in layers:
            WIN.blit(layer, (0,0))

        # jednorazowo updateujemy zawartosc glownego okna, nigdzie w watkach nie updateujemy jakis fragmentow ekranu czy cos
        pygame.display.update()

    while run:
        clock.tick(120)
        redraw_window()


        #  lost screen
        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue


        #  spawning enemies
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500 -(500 * level), -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)


        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


        # keys
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x - player_vel > 0: #  left
            player.x -= player_vel
        
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH: #  right
            player.x += player_vel

        if keys[pygame.K_UP] and player.y - player_vel > 0: #  up
            player.y -= player_vel

        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT: #  down
            player.y += player_vel

        if keys[pygame.K_z]:
            player.shoot()


        #  enemies
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(enemy_laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                player.x = 300
                player.y = 630
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


if __name__ == "__main__":
    main_menu()