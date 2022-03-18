import threading
import pygame
import pygame.math
import random

WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Invaders")

mutex = threading.Lock()

clock = pygame.time.Clock()


class Ball(threading.Thread):
    COLORS = {
        "blue" : "blue",
        "red": "red", 
        "green" : "green",
        "pink" : "pink",
        "orange" : "orange" 
    }

    def __init__(self) -> None:
        self.layer = pygame.surface.Surface((WIDTH, HEIGHT))
        self.vec = pygame.math.Vector2()
        self.vec.y  = random.randrange(0.0, float(HEIGHT))
        self.vec.x = random.randrange(0.0, float(WIDTH))
        self.vel_y = 4.0
        self.vel_x = random.randrange(0.0, 10.0)
        self.color = random.choice(list(self.COLORS))
        self.bounced = 0

    def __init__(self, color) -> None:
        threading.Thread.__init__(self)
        self.layer = pygame.Surface((WIDTH, HEIGHT))
        self.vec = pygame.math.Vector2()
        self.vec.y  = random.randrange(0.0, float(HEIGHT))
        self.vec.x = random.randrange(0.0, float(WIDTH))
        self.vel_y = 4.0
        self.vel_x = random.randrange(0.0, 10.0)
        self.color = color
        self.bounced = 0
        
    def run(self):
        while self.bounced < 10:
        #while True:
            clock.tick(60)
            self.move()

            mutex.acquire()
            try:
                #self.layer.fill((0,0,0,0))
                WIN.fill((0,0,0))
                pygame.draw.rect(WIN, self.color, (self.vec.x,  self.vec.y, 20, 20), 2)
                #WIN.blit(self.layer,(0,0))
                pygame.display.update((self.vec.x-10, self.vec.y-10, 40, 40))
            finally:
                mutex.release()

    def move(self):
        self.check_border()
        self.vec.x  += self.vel_x
        self.vec.y += self.vel_y
    
    def check_border(self):
        if  self.vec.x < 0 or  self.vec.x > WIDTH:
            self.vel_x *= -1.0
            self.bounced += 1 

        if  self.vec.y < 0 or  self.vec.y > HEIGHT:
            self.vel_y *= -1.0
            self.bounced += 1



def main():
    
    run = True
    
    WIN.fill((0,0,0,0))
    
    pygame.display.update()
    ball = Ball("red")
    ball2 = Ball("blue")
    ball3 = Ball("green")
    ball.start()
    ball2.start()
    ball3.start()
    #t1 = threading.Thread(target=ball.draw(WIN, clock))
    #t2 = threading.Thread(target=ball2.draw(WIN, clock))
    #t1.start()
    #t2.start()

    
   
    def refresh():
        
        #ball.move()
        #ball.draw(WIN, clock, mutex())
        #ball2.move()
        #ball2.draw(WIN, clock, mutex())
        pygame.display.update()

    while run:
        clock.tick(60)
        #refresh()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
        


if __name__ == "__main__":
    main() 