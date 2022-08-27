import time
import pygame
import random
import math

pygame.init()

HEIGHT, WIDTH = 600, 800
FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fireworks")

COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 165, 0),
    (255, 255, 255),
    (230, 230, 255),
    (255, 192, 203)
]


class Projectiles:
    HEIGHT, WIDTH = 7, 7
    ALPHA_DECREMENT = 4.2

    def __init__(self, x, y, x_val, y_val, color):
        self.x = x
        self.y = y
        self.y_val = y_val
        self.x_val = x_val
        self.color = color
        self.exist = True
        self.move_dist = 0
        self.max_move_dist = 400 # random.randrange(45, 200)
        self.alpha = 255

    def move(self):
        #if self.move_dist < self.max_move_dist:
        self.move_dist += math.sqrt((self.y_val) ** 2 + (self.x_val) ** 2)
        self.x += self.x_val
        self.y += self.y_val
        self.alpha = max(0, self.alpha - self.ALPHA_DECREMENT)
        #else:
        if self.x >= WIDTH or self.x < 0 or self.y >= HEIGHT or self.y < 0 or self.alpha == 0:
            self.exist = False

    def draw(self):
        if self.exist:
            self.draw_rect_alpha(self.color + (self.alpha,), (self.x, self.y, self.WIDTH, self.HEIGHT))
            #pygame.draw.rect(win, self.color, (self.x, self.y, self.WIDTH, self.HEIGHT))

    def draw_rect_alpha(self, color, rect):
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        win.blit(shape_surf, rect)


class Firework:
    RADIUS = 12.5

    def __init__(self, x, y, color, explode_height, y_val=-5):
        self.x = x
        self.y = y
        self.color = color
        self.y_val = y_val
        self.explode_height = explode_height
        self.projectiles = []
        self.exploded = False

    def draw(self):
        if not self.exploded:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)
        for projectile in self.projectiles:
            projectile.draw()


    def create_circular_projectiles(self, num_of_projectiles):
        angle_dif = math.pi*2/num_of_projectiles
        current_angle = 0
        vel = random.randrange(3, 6)
        for _ in range(num_of_projectiles):
            x_vel = math.sin(current_angle)*vel
            y_vel = math.cos(current_angle)*vel
            color = random.choice(COLORS)
            self.projectiles.append(Projectiles(self.x, self.y, x_vel, y_vel, color))
            current_angle += angle_dif

    def create_random_projectiles(self, num_of_projectiles):
        for _ in range(num_of_projectiles):
            y_val = random.choice([num for num in range(-5, 6) if num != 0])
            x_val = random.choice([num for num in range(-5, 6) if num != 0])
            color = random.choice(COLORS)
            self.projectiles.append(Projectiles(self.x, self.y, x_val, y_val, color))



    def explode(self):
        self.exploded = True
        num_of_projectiles = random.randrange(15, 50)
        num2 = random.randrange(0, 7)
        if num2 < 5:
            self.create_random_projectiles(num_of_projectiles)
        else:
            self.create_circular_projectiles(num_of_projectiles)




    def move(self):
        if self.y + self.y_val > self.explode_height:
            self.y += self.y_val
        elif not self.exploded:
            self.y = self.explode_height
            self.explode()


class Launcher:
    WIDTH = 25
    HEIGHT = 30
    COLOR = "grey"

    def __init__(self, x, y, frequency):
        self.x = x
        self.y = y
        self.frequency = frequency
        self.start_time = time.time()
        self.fireworks = []

    def draw(self):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT))

        for firework in self.fireworks:
            firework.draw()

    def lunch(self):
        color = random.choice(COLORS)
        explode_height = random.randrange(40, 350)
        firework = Firework(self.x + self.WIDTH / 2, self.y, color, explode_height, -5)
        self.fireworks.append(firework)

    def loop(self):
        current_time = time.time()
        time_elapsed = current_time - self.start_time
        if time_elapsed * 1000 > self.frequency:
            self.start_time = current_time
            self.lunch()

        for firework in self.fireworks:
            firework.move()
            if firework.exploded:
                if len(firework.projectiles) == 0:
                    self.fireworks.remove(firework)
                else:
                    for projectile in firework.projectiles:
                        projectile.move()
                        if not projectile.exist:
                            firework.projectiles.remove(projectile)


def draw(launchers):
    win.fill("black")
    for launcher in launchers:
        launcher.draw()
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    run = True
    launchers = [Launcher(WIDTH / 6, HEIGHT - Launcher.HEIGHT, random.randrange(1000, 10000)),
                 Launcher(WIDTH * 2 / 6, HEIGHT - Launcher.HEIGHT, random.randrange(1000, 10000)),
                 Launcher(WIDTH * 3 / 6, HEIGHT - Launcher.HEIGHT, random.randrange(1000, 10000)),
                 Launcher(WIDTH * 4 / 6, HEIGHT - Launcher.HEIGHT, random.randrange(1000, 10000)),
                 Launcher(WIDTH * 5 / 6, HEIGHT - Launcher.HEIGHT, random.randrange(1000, 10000))]
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(launchers)
        for launcher in launchers:
            launcher.loop()
    pygame.quit()


if __name__ == '__main__':
    main()
