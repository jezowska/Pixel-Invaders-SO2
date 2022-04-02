from multiprocessing.connection import wait
import pygame
import os
import random
from player import Player
from enemy import Enemy
from boss import Boss
from funcs import collide
pygame.font.init()
pygame.init()

main_font = pygame.font.SysFont("Bauhaus 93", 50)
lost_font = pygame.font.SysFont("Bauhaus 93", 60)
title_font = pygame.font.SysFont("Bauhaus 93", 50)

def absolute_path(path: str) -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

WIDTH, HEIGHT = 800, 750
BG = pygame.transform.scale(pygame.image.load(absolute_path(os.path.join("images",  "background.png"))), (WIDTH, HEIGHT))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Invaders")

clock = pygame.time.Clock()

abort = 0


def game_run():
    run = True
    FPS = 60
    lost = False
    lost_count = 0

    level = 0
    enemies = []
    wave_length = 5
    enemy_vel = 3
    player_laser_vel = 15
    enemy_laser_vel = 8

    player = Player(300, 630)

    # bosses with their own layers
    bosses = []
    layers = []

    def redraw_window():
        WIN.blit(BG, (0 ,0))

        # updating level and points labels
        level_label = main_font.render(f"Level: {level}", 1, (255 ,255, 255))
        points_label = main_font.render(f"points: {player.points}", 1, (255 ,255, 255))

        WIN.blit(level_label, (WIDTH - 10 - level_label.get_width(), 10))
        WIN.blit(points_label, (10, 10))

        # updating enemy position
        for enemy in enemies:
            enemy.draw(WIN)

        # updating player position
        player.draw(WIN)

        # if player has lost - game over
        if lost == True:
            lost_label = lost_font.render("Game over", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        # blitting bosses' layers onto the main window
        for layer in layers:
            WIN.blit(layer, (0,0))

        # updating main window
        pygame.display.update()

    while run:
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
            if len(bosses) == 0:
                level += 1
                wave_length += 2
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500 -(500 * level), -100), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)
                # creating bosses and their layers
                for i in range(3):
                    # transparent layers on which bosses are going to be shown
                    layer = pygame.Surface((WIDTH,HEIGHT))
                    layer.set_colorkey((255,255,0))
                    layers.append(layer)

                    # creating a boss, assigning it its layer and starting its thread
                    boss = Boss(random.randrange(100, WIDTH - 200),random.randrange(0, HEIGHT - 300),layer)
                    print("boss: " + str(boss))
                    bosses.append(boss)
                    boss.start()


            # quitting the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    abort = 1
                    for boss in bosses:
                        boss.health = 0
                        boss.join()
                        
                    wait(1)   
                    pygame.quit()

            # keys 
            keys = pygame.key.get_pressed()
            player.move(keys)
            if keys[pygame.K_ESCAPE]:
                for boss in bosses:
                    boss.join()

            # moving enemies amd checking collisions
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

            for boss in bosses:
                if collide(boss, player):
                    boss.health -= 10
                    player.health -= 1
                    player.x = 300
                    player.y = 600

            for boss in bosses:
                if boss.health <= 0:
                    bosses.remove(boss)
                    
            player.move_lasers(-player_laser_vel, enemies, bosses)

def main():

    game_run()
    pygame.quit()

if __name__ == "__main__":
    main()