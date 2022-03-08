import pygame
import sys
import math
import random


pygame.init()


font = pygame.font.SysFont('Fira Code', 30)


screen = pygame.display.set_mode((0, 0))
size = w, h = screen.get_width(), screen.get_height()
background = pygame.Surface(pygame.Rect(0, 0, w, h).size)

pygame.display.set_caption("Orbit Simulator")
g = 500

planets = []

def start():
    for i in range(30):
        ang = random.uniform(math.radians(0), math.radians(360))
        dist = random.uniform(100, 300)

        speed_angle = random.uniform(math.radians(0), math.radians(360))
        speed = random.uniform(0, 1)
        mass = random.uniform(5, 10)
        planets.append([[w / 2 - math.cos(ang) * dist, h / 2 - math.sin(ang) * dist],
                        [math.cos(speed_angle) * speed, math.sin(speed_angle) * speed],
                        [random.randint(0, 255),
                         random.randint(0, 255),
                         random.randint(0, 255)],
                        mass, mass])

t = 0
start()
Running = True
Paused = False
Debug = True
clock = pygame.time.Clock()

background.fill((50, 50, 50))

while Running:

    firstx = 0
    firsty = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Running = False
            if event.key == pygame.K_SPACE:
                Paused = not Paused
            if event.key == pygame.K_F3:
                Debug = not Debug
            if event.key == pygame.K_c:
                background.fill((50, 50, 50))
            if event.key == pygame.K_BACKSPACE:
                planets.clear()
            if event.key == pygame.K_r:
                planets.clear()
                background.fill((50, 50, 50))
                for i in range(30):
                    ang = random.uniform(math.radians(0), math.radians(360))
                    dist = random.uniform(100, 300)

                    speed_angle = random.uniform(math.radians(0), math.radians(360))
                    speed = random.uniform(0, 1)
                    mass = random.uniform(-10, 10)
                    planets.append([[w / 2 - math.cos(ang) * dist, h / 2 - math.sin(ang) * dist],
                                    [math.cos(speed_angle) * speed, math.sin(speed_angle) * speed],
                                    [random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255)],
                                    mass, mass])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                firstx = pygame.mouse.get_pos()[0]
                firsty = pygame.mouse.get_pos()[1]
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                speed_angle = random.uniform(math.radians(0), math.radians(360))
                speed = random.uniform(0, 1)
                mass = random.uniform(5, 10)
                planets.append([[pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]],
                                [math.cos(speed_angle) * speed, math.sin(speed_angle) * speed],
                                [random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255)],
                                mass, mass])
    screen.blit(background, (0, 0))

    for index, i in enumerate(planets):
        if not Paused:
            sundist = math.sqrt((h / 2 - i[0][1]) ** 2 + (w / 2 - i[0][0]) ** 2)

            tempx = i[0][0]
            tempy = i[0][1]

            if sundist < 20:
                planets.pop(index)
            else:
                i[1][0] -= (g * (i[0][0] - w / 2) / sundist ** 3)
                i[1][1] -= (g * (i[0][1] - h / 2) / sundist ** 3)

                for s in planets:
                    dr = math.sqrt((s[0][1] - i[0][1]) ** 2 + (s[0][0] - i[0][0]) ** 2)

                    if dr > 0:
                        i[1][0] -= (s[3] * (i[0][0] - s[0][0]) / dr ** 3)
                        i[1][1] -= (s[3] * (i[0][1] - s[0][1]) / dr ** 3)

            i[0][0] += i[1][0]
            i[0][1] += i[1][1]

        if i[3] < 0:
            pygame.draw.circle(screen, i[2], (i[0][0], i[0][1]), abs(i[4]))
            pygame.draw.circle(screen, (0, 0, 0), (i[0][0], i[0][1]), abs(i[4]) - 1)
        else:
            pygame.draw.circle(screen, (0, 0, 0), (i[0][0], i[0][1]), i[4])
            pygame.draw.circle(screen, i[2], (i[0][0], i[0][1]), i[4] - 1)

        if not Paused:
            pygame.draw.aaline(background, i[2], (tempx, tempy), (i[0][0], i[0][1]))

    pygame.draw.circle(screen, (0, 0, 0), (w / 2, h / 2), 20)
    pygame.draw.circle(screen, (255, 255, 0), (w / 2, h / 2), 19)

    if Debug:
        timetext = font.render(f"Time: {str(t)}", True, (255, 255, 255))
        textrect = timetext.get_rect()
        textrect.topright = (w - 10, 10)
        screen.blit(timetext, textrect)

        planettext = font.render(f"Planets: {len(planets)}", True, (255, 255, 255))
        textrect = planettext.get_rect()
        textrect.topright = (w - 10, 30)
        screen.blit(planettext, textrect)

        fpstext = font.render(f"Fps: {round(clock.get_fps())}", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.topright = (w - 10, 50)
        screen.blit(fpstext, textrect)

    pygame.display.flip()

    if not Paused:
        clock.tick(60)

        t += 1
