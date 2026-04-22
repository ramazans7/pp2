import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))

colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)

clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5

currX = 0
currY = 0
prevX = 0
prevY = 0

mode = "rect"
current_color = colorRED

def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def calculate_circle(x1, y1, x2, y2):
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) // 2)
    return center_x, center_y, radius

screen.blit(base_layer, (0, 0))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX = event.pos[0]
            prevY = event.pos[1]

        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX = event.pos[0]
                currY = event.pos[1]

                screen.blit(base_layer, (0, 0))

                if mode == "rect":
                    pygame.draw.rect(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)

                elif mode == "circle":
                    center_x, center_y, radius = calculate_circle(prevX, prevY, currX, currY)
                    if radius > 0:
                        pygame.draw.circle(screen, current_color, (center_x, center_y), radius, THICKNESS)

                elif mode == "line":
                    pygame.draw.line(screen, current_color, (prevX, prevY), (currX, currY), THICKNESS)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX = event.pos[0]
            currY = event.pos[1]

            if mode == "rect":
                pygame.draw.rect(screen, current_color, calculate_rect(prevX, prevY, currX, currY), THICKNESS)

            elif mode == "circle":
                center_x, center_y, radius = calculate_circle(prevX, prevY, currX, currY)
                if radius > 0:
                    pygame.draw.circle(screen, current_color, (center_x, center_y), radius, THICKNESS)

            elif mode == "line":
                pygame.draw.line(screen, current_color, (prevX, prevY), (currX, currY), THICKNESS)

            base_layer.blit(screen, (0, 0))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                THICKNESS += 1

            if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                if THICKNESS > 1:
                    THICKNESS -= 1

            if event.key == pygame.K_r:
                mode = "rect"

            if event.key == pygame.K_e:
                mode = "circle"

            if event.key == pygame.K_l:
                mode = "line"

            if event.key == pygame.K_1:
                current_color = colorRED

            if event.key == pygame.K_2:
                current_color = colorBLUE

            if event.key == pygame.K_3:
                current_color = colorBLACK

            if event.key == pygame.K_c:
                base_layer.fill(colorWHITE)
                screen.blit(base_layer, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()