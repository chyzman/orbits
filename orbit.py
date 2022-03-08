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

planets = []
def spawnsun():
    planets.append([[w / 2, h / 2], [0, 0], (255, 255, 0), 100, 20, True])

def start():
    for i in range(30):
        ang = random.uniform(math.radians(0), math.radians(360))
        dist = random.uniform(100, 300)

        speed_angle = random.uniform(math.radians(0), math.radians(360))
        speed = random.uniform(0, 0.1)
        mass = random.uniform(5, 10)
        planets.append([[w / 2 - math.cos(ang) * dist, h / 2 - math.sin(ang) * dist],
                        [math.cos(speed_angle) * speed, math.sin(speed_angle) * speed],
                        [random.randint(0, 255),
                         random.randint(0, 255),
                         random.randint(0, 255)],
                        mass, mass, False])

t = 0
spawnsun()
#start()
Running = True
Paused = False
Debug = True
Help = False
spawnvars = [5.0, 5.0]
choice = 0
clock = pygame.time.Clock()

background.fill((50, 50, 50))

while Running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Running = False
            if event.key == pygame.K_SPACE:
                Paused = not Paused
            if event.key == pygame.K_h:
                Help = not Help
            if event.key == pygame.K_F3:
                Debug = not Debug
            if event.key == pygame.K_c:
                background.fill((50, 50, 50))
            if event.key == pygame.K_x:
                planets.clear()
                spawnsun()
            if event.key == pygame.K_r:
                planets.clear()
                background.fill((50, 50, 50))
                spawnsun()
                start()
            if event.key == pygame.K_t:
                start()
            if event.key == pygame.K_TAB:
                if choice < len(spawnvars)-1:
                    choice += 1
                else:
                    choice = 0
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                firstx = pygame.mouse.get_pos()[0]
                firsty = pygame.mouse.get_pos()[1]
            if event.button == pygame.BUTTON_WHEELUP:
                modifier = 1
                if keys[pygame.K_LSHIFT]: modifier = 10
                if keys[pygame.K_LCTRL]: modifier = 0.1
                spawnvars[choice] += modifier
            if event.button == pygame.BUTTON_WHEELDOWN:
                modifier = 1
                if keys[pygame.K_LSHIFT]: modifier = 10
                if keys[pygame.K_LCTRL]: modifier = 0.1
                spawnvars[choice] -= modifier
            if event.button == pygame.BUTTON_MIDDLE:
                spawnvars[choice] = 5.0
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                xdist = 0.001 + pygame.mouse.get_pos()[0] - firstx
                ydist = 0.001 + pygame.mouse.get_pos()[1] - firsty
                angle = math.atan2(ydist, xdist)
                speed = math.sqrt(xdist**2+ydist**2)/250
                planets.append([[firstx, firsty],
                                [math.cos(angle) * speed, math.sin(angle) * speed],
                                [random.randint(0, 255),
                                 random.randint(0, 255),
                                 random.randint(0, 255)],
                                spawnvars[0], spawnvars[1], False])
            if event.button == pygame.BUTTON_RIGHT:
                for index, i in enumerate(planets):
                    if math.sqrt((pygame.mouse.get_pos()[1] - i[0][1]) ** 2 + (pygame.mouse.get_pos()[0] - i[0][0]) ** 2) < i[4]:
                        planets.pop(index)
    screen.blit(background, (0, 0))

    for index, i in enumerate(planets):
        if not Paused:

            if math.sqrt((h/2 - i[0][1]) ** 2 + (w/2 - i[0][0]) ** 2) > 20000:
                planets.pop(index)

            tempx = i[0][0]
            tempy = i[0][1]

            for s in planets:
                dr = math.sqrt((s[0][1] - i[0][1]) ** 2 + (s[0][0] - i[0][0]) ** 2)

                if not i[5] and dr > 0:
                    if i[3] < 0:
                        i[1][0] += (s[3] * (i[0][0] - s[0][0]) / dr ** 3)
                        i[1][1] += (s[3] * (i[0][1] - s[0][1]) / dr ** 3)
                    if i[3] > 0:
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

    if pygame.mouse.get_pressed()[0]:
        pygame.draw.aaline(screen, (255, 255, 255), (firstx, firsty), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))

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

    fpstext = font.render(f"Mass: {spawnvars[0]}", True, (255, 255, 255) if choice == 0 else (128, 128, 128))
    textrect = fpstext.get_rect()
    textrect.topleft = (10, 10)
    screen.blit(fpstext, textrect)

    fpstext = font.render(f"Size: {spawnvars[1]}", True, (255, 255, 255) if choice == 1 else (128, 128, 128))
    textrect = fpstext.get_rect()
    textrect.topleft = (10, 30)
    screen.blit(fpstext, textrect)

    if Help:
        text = font.render(f"Click and Drag To Spawn Planets", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 190)
        screen.blit(text, textrect)

        text = font.render(f"R to Reset Universe", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 170)
        screen.blit(text, textrect)

        text = font.render(f"T to spawn a random assortment of Planets", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 150)
        screen.blit(text, textrect)

        text = font.render(f"Space to Pause", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 130)
        screen.blit(text, textrect)

        text = font.render(f"Esc to Quit", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 110)
        screen.blit(text, textrect)

        text = font.render(f"X to clear Universe", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 90)
        screen.blit(text, textrect)

        text = font.render(f"Scroll to change properties", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 70)
        screen.blit(text, textrect)

        text = font.render(f"Tab to change selection", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 50)
        screen.blit(text, textrect)

        text = font.render(f"Rclick on Planet to delete", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 30)
        screen.blit(text, textrect)

        text = font.render(f"H to toggle This help Menu", True, (255, 255, 255))
        textrect = fpstext.get_rect()
        textrect.bottomright = (95, h - 10)
        screen.blit(text, textrect)

    pygame.display.flip()

    if not Paused:
        clock.tick(60)

        t += 1