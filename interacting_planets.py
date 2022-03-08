import pygame
import sys
import math
import random


pygame.init()


font = pygame.font.SysFont('Fira Code', 30)


screen = pygame.display.set_mode((0, 0), pygame.RESIZABLE)
size = w, h = screen.get_width(), screen.get_height()
#Alien.images = [load_image(im) for im in ("alien1.gif", "alien2.gif", "alien3.gif")]
#pygame.display.set_icon(surface)
#icon = pygame.transform.scale(Alien.images[0], (32, 32))
#pygame.display.set_icon(icon)
pygame.display.set_caption("Orbit Simulator")
print(screen.get_size())

# s = h / 2
g = 0
# red boi is [[w / 2 + 0, h / 2 + -180], [1, 0], [255, 0, 0], 0]

planets = []

for i in range(100):
    ang = random.uniform(math.radians(0), math.radians(360))
    dist = random.uniform(100, 300)

    speed_angle = random.uniform(math.radians(0), math.radians(360))
    #speed_angle = math.pi / 2 + ang
    speed = random.uniform(0, 0)

    planets.append([[w / 2 - math.cos(ang) * dist, h / 2 - math.sin(ang) * dist],
                    [math.cos(speed_angle) * speed, math.sin(speed_angle) * speed],
                    [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)],
                    random.uniform(-10, 10)])

t = 0
clock = pygame.time.Clock()


while 1:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                # prevents crash screen from appearing on mac
                screen.fill((20, 20, 45))
    screen.fill((20, 20, 45))
    a = 0
    for i in planets:
        d = math.sqrt((h / 2 - i[0][1]) ** 2 + (w / 2 - i[0][0]) ** 2)

        if d > 50:
            i[1][0] -= (g * (i[0][0] - w / 2) / d ** 3)
            i[1][1] -= (g * (i[0][1] - h / 2) / d ** 3)

        if d < 0:
            i[1][0] += (g * (i[0][0] - w / 2) / d ** 3)
            i[1][1] += (g * (i[0][1] - h / 2) / d ** 3)

        for s in planets:
            dr = math.sqrt((s[0][1] - i[0][1]) ** 2 + (s[0][0] - i[0][0]) ** 2)
            if dr > 50 and i[3] > 0:
                i[1][0] -= (s[3] * (i[0][0] - s[0][0]) / dr ** 3)
                i[1][1] -= (s[3] * (i[0][1] - s[0][1]) / dr ** 3)

            if dr > 50 and i[3] < 0:
                i[1][0] += (s[3] * (i[0][0] - s[0][0]) / dr ** 3)
                i[1][1] += (s[3] * (i[0][1] - s[0][1]) / dr ** 3)

        i[0][0] += i[1][0]
        i[0][1] += i[1][1]
        #                              color, position, size
        #pygame.draw.circle(screen, i[2], (i[0][0], i[0][1]), abs(i[3]) + 2)

        pygame.draw.circle(screen, (255 - 12.75 * (i[3] + 10), 0, 12.75 * (i[3] + 10)), (i[0][0], i[0][1]), 10)

        if a * 55 < screen.get_height():
            # text = font.render("Mass: (" + str(i[5]) + ")", True, i[2])
            # textRect = text.get_rect()
            # textRect.bottomleft = (i[0][0], i[0][1])
            # screen.blit(text, textRect)

            text = font.render(
                "Pos: (" + str(round((-(w / 2 - i[0][0])), 1)) + ", " + str(round((h / 2 - i[0][1]), 1)) + ")", True,
                i[2])
            textRect = text.get_rect()
            textRect.topleft = (10, a * screen.get_height() / (screen.get_height() // 55))
            screen.blit(text, textRect)

            text1 = font.render("Dist: " + str(round(d, 3)), True, i[2])
            textRect1 = text1.get_rect()
            textRect1.topleft = (10, 16 + a * screen.get_height() / (screen.get_height() // 55))
            screen.blit(text1, textRect1)

            text2 = font.render("Vel: " + str(round(math.sqrt(i[1][0] ** 2 + i[1][1] ** 2), 2)), True, i[2])
            textRect2 = text2.get_rect()
            textRect2.topleft = (10, 32 + a * screen.get_height() / (screen.get_height() // 55))
            screen.blit(text2, textRect2)

            a += 1
    #pygame.draw.circle(screen, (255, 255, 0), (w / 2, h / 2), 20)

    text3 = font.render("Time: " + str(t), True, (255, 128, 0))
    textRect3 = text3.get_rect()
    textRect3.topright = (w - 10, 10)
    screen.blit(text3, textRect3)

    text4 = font.render(f"Fps: {round(clock.get_fps())}", True, (255 - int(clock.get_fps() * 4), int(clock.get_fps() * 4), 0))
    textRect4 = text4.get_rect()
    textRect4.topright = (w - 10, 50)
    screen.blit(text4, textRect4)

    clock.tick(60)

    pygame.display.flip()
    t += 1
