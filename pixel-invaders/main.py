import pygame
import os
import random
import threading
from player import Player
from enemy import Enemy
from boss import Boss
from funcs import collide
from funcs import absolute_path

pygame.font.init()
pygame.init()

main_font = pygame.font.SysFont("Bauhaus 93", 50)
lost_font = pygame.font.SysFont("Bauhaus 93", 60)
title_font = pygame.font.SysFont("Bauhaus 93", 50)

WIDTH, HEIGHT = 800, 750
BG = pygame.transform.scale(pygame.image.load(absolute_path(os.path.join("images", "background.png"))), (WIDTH, HEIGHT))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Invaders")
mutex = threading.Lock()
clock = pygame.time.Clock()


def game_run():
    run = True
    FPS = 120

    lost = False
    lost_count = 0
    level = 0
    bosses_count = 3
    enemies = []
    enemy_vel = 3
    player_weapon_vel = 15
    enemy_weapon_vel = 8
    immunity = 0

    temp = 1

    # creating a player
    player = Player(300, 630)

    # bosses with their own layers
    bosses = []
    layers = []

    def redraw_window():
        WIN.blit(BG, (0, 0))

        # updating level and points labels
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        points_label = main_font.render(f"points: {player.points}", 1, (255, 255, 255))

        WIN.blit(level_label, (WIDTH - 10 - level_label.get_width(), 10))
        WIN.blit(points_label, (10, 10))

        # updating enemy position
        for enemy in enemies:
            enemy.draw(WIN)

        # updating player position
        player.draw(WIN)

        # if player has lost - game over
        if lost:
            lost_label = lost_font.render("Game over", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

        # blitting bosses' layers onto the main window
        for layer in layers:
            WIN.blit(layer, (0, 0))

        # updating main window
        pygame.display.update()

    # main game loop
    while run:
        clock.tick(FPS)
        redraw_window()

        # decrementing the remaining immunity frames counter
        if immunity > 0:
            immunity -= 1

        # lost screen
        if player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            # joining boss threads
            for boss in bosses:
                boss.health = 0
                boss.join()

            if lost_count > FPS * 5:
                run = False
            else:
                continue

        # beginning the next wave and spawning bosses
        if len(bosses) == 0:
            level += 1

            # incrementing the amount of bosses every 5 levels
            if level % 5 == 0:
                bosses_count += 1

            # creating bosses and their layers
            for i in range(bosses_count):
                # transparent layers on which bosses are going to be shown
                layer = pygame.Surface((WIDTH, HEIGHT))
                layer.set_colorkey((255, 255, 0))
                layers.append(layer)

                # creating a boss, assigning it its layer and starting its thread
                boss = Boss(random.randrange(100, WIDTH - 200), random.randrange(0, HEIGHT - 300), layer)
                print("boss " + str(temp) + "\t" + str(boss))

                temp += 1

                bosses.append(boss)
                boss.start()

            print()

        # spawning enemies at random time intervals
        if random.randrange(1, 20 * FPS) <= level * 5:
            enemy = Enemy(random.randrange(50, WIDTH - 100), -100, random.choice(["red", "blue", "green"]))
            enemies.append(enemy)

        # quitting the game and joining bosses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                for boss in bosses:
                    boss.health = 0
                    boss.join()

                pygame.quit()

        # checking pressed keys and checking if player has to move or shoot
        keys = pygame.key.get_pressed()
        player.move(keys)
        #if keys[pygame.K_ESCAPE]:
        #   for boss in bosses:
        #       boss.health = 0
        #       boss.join()

        # moving enemies and checking collisions
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_weapons(enemy_weapon_vel, player)

            if random.randrange(0, 2 * FPS) == 1:
                enemy.shoot()

            # checking for collision between player and enemy
            if collide(enemy, player) and immunity == 0:
                player.health -= 10
                enemies.remove(enemy)
                immunity = FPS / 2

            # deleting the enemy if it's behind the border
            elif enemy.y + enemy.get_height() > HEIGHT:
                enemies.remove(enemy)

        # checking for collision between player and bosses
        for boss in bosses:
            if collide(boss, player) and immunity == 0:
                boss.health -= 25
                player.health -= 25
                immunity = FPS / 2

        # if boss' health is 0 or less - removing boss
        for boss in bosses:
            if boss.health <= 0:
                index = bosses.index(boss)
                boss.join()
                bosses.remove(boss)
                layers.remove(layers[index])

        # moving player weapon and checking for collision with player's weapon
        mutex.acquire()
        try:
            player.move_weapons(-player_weapon_vel, enemies, bosses)
        finally:
            mutex.release()


def main():
    game_run()
    pygame.quit()


if __name__ == "__main__":
    main()
