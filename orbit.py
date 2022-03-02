import pygame
import math
import random

pygame.init()

font = pygame.font.SysFont('Fira Code', 30)

screen = pygame.display.set_mode((0, 0))
size = w, h = screen.get_width(), screen.get_height()
pygame.display.set_caption("Orbit Simulator")


class Planet(pygame.sprite.Sprite):

    def __init__(self, x, y, vx, vy, r, g, b, s):
        super().__init__()

        self.vx = vx
        self.vy = vy
        self.color = (r, g, b)
        self.size = s

        self.image = pygame.Surface([s**2, s**2])
        self.image.set_colorkey((255, 255, 255))

        pygame.draw.circle(self.image, self.color, (self.size // 2, self.size // 2), 5)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        d = math.sqrt((h / 2 - self.rect.y) ** 2 + (w / 2 - self.rect.x) ** 2)

        self.vx -= (g * (self.rect.x - w / 2) / d ** 3)
        self.vy -= (g * (self.rect.y - h / 2) / d ** 3)

        self.rect.x += self.vx
        self.rect.y += self.vy


Planets = pygame.sprite.Group()

for i in range(10):
    planet = Planet(w / 2 - random.randint(-300, 300), h / 2 - random.randint(-400, 400), random.randint(-10, 10) / 10,
                    random.randint(-10, 10) / 10, random.randint(0, 255), random.randint(0, 255),
                    random.randint(0, 255), random.randint(3, 5))
    Planets.add(planet)

t = 0
g = 500

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill((50, 50, 75))
    pygame.draw.circle(screen, (255, 255, 0), (w / 2, h / 2), 10)
    Planets.update()
    Planets.draw(screen)

    time = font.render("Time: " + str(t), True, (255, 128, 0))
    textRect3 = time.get_rect()
    textRect3.topright = (w - 10, 10)
    screen.blit(time, textRect3)

    pygame.display.flip()

    clock.tick(120)

    t += 1
