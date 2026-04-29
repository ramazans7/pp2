import pygame
from datetime import datetime
from collections import deque

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint TSIS2")

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 28)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

colors = [BLACK, RED, GREEN, BLUE, YELLOW]
current_color = BLACK

tool = "pencil"
brush_size = 5

drawing = False
start_pos = None
last_pos = None

text_mode = False
text = ""
text_pos = None

clock = pygame.time.Clock()


def draw_ui():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 60))

    x = 10
    for c in colors:
        pygame.draw.rect(screen, c, (x, 10, 40, 40))
        if c == current_color:
            pygame.draw.rect(screen, BLACK, (x, 10, 40, 40), 3)
        x += 50

    info = f"Tool: {tool} | Size: {brush_size}"
    text_surface = font.render(info, True, BLACK)
    screen.blit(text_surface, (300, 15))


def draw_shape(surface, start, end):
    x1, y1 = start
    x2, y2 = end

    if tool == "line":
        pygame.draw.line(surface, current_color, start, end, brush_size)

    elif tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
        pygame.draw.rect(surface, current_color, rect, brush_size)

    elif tool == "circle":
        radius = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5)
        pygame.draw.circle(surface, current_color, start, radius, brush_size)

    elif tool == "square":
        side = min(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(x1, y1, side if x2 > x1 else -side, side if y2 > y1 else -side)
        rect.normalize()
        pygame.draw.rect(surface, current_color, rect, brush_size)

    elif tool == "right_triangle":
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, current_color, points, brush_size)

    elif tool == "equilateral_triangle":
        side = abs(x2 - x1)
        height = int(side * 0.866)
        points = [(x1, y2), (x2, y2), ((x1 + x2) // 2, y2 - height)]
        pygame.draw.polygon(surface, current_color, points, brush_size)

    elif tool == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(surface, current_color, points, brush_size)


def flood_fill(surface, pos, new_color):
    x, y = pos

    if x < 0 or x >= WIDTH or y < 60 or y >= HEIGHT:
        return

    old_color = surface.get_at((x, y))

    if old_color == new_color:
        return

    q = deque()
    q.append((x, y))

    while q:
        x, y = q.popleft()

        if x < 0 or x >= WIDTH or y < 60 or y >= HEIGHT:
            continue

        if surface.get_at((x, y)) != old_color:
            continue

        surface.set_at((x, y), new_color)

        q.append((x + 1, y))
        q.append((x - 1, y))
        q.append((x, y + 1))
        q.append((x, y - 1))


running = True
while running:
    pos = pygame.mouse.get_pos()

    screen.blit(canvas, (0, 0))

    if drawing and start_pos and tool not in ["pencil", "eraser", "fill", "text"]:
        temp = canvas.copy()
        draw_shape(temp, start_pos, pos)
        screen.blit(temp, (0, 0))

    draw_ui()

    if text_mode:
        txt = font.render(text, True, current_color)
        screen.blit(txt, text_pos)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if text_mode:
                if event.key == pygame.K_RETURN:
                    canvas.blit(font.render(text, True, current_color), text_pos)
                    text_mode = False
                    text = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    text = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]

                else:
                    text += event.unicode

            else:
                if event.key == pygame.K_p:
                    tool = "pencil"
                elif event.key == pygame.K_l:
                    tool = "line"
                elif event.key == pygame.K_r:
                    tool = "rect"
                elif event.key == pygame.K_c:
                    tool = "circle"
                elif event.key == pygame.K_e:
                    tool = "eraser"
                elif event.key == pygame.K_f:
                    tool = "fill"
                elif event.key == pygame.K_t:
                    tool = "text"
                elif event.key == pygame.K_s:
                    tool = "square"
                elif event.key == pygame.K_1:
                    brush_size = 2
                elif event.key == pygame.K_2:
                    brush_size = 5
                elif event.key == pygame.K_3:
                    brush_size = 10
                elif event.key == pygame.K_4:
                    tool = "right_triangle"
                elif event.key == pygame.K_5:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_6:
                    tool = "rhombus"

                if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    filename = "paint_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
                    pygame.image.save(canvas, filename)
                    print("Saved:", filename)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos

                if y <= 60:
                    for i, c in enumerate(colors):
                        if 10 + i * 50 <= x <= 50 + i * 50:
                            current_color = c
                else:
                    if tool == "fill":
                        flood_fill(canvas, event.pos, current_color)

                    elif tool == "text":
                        text_mode = True
                        text = ""
                        text_pos = event.pos

                    else:
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "pencil":
                    pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                    last_pos = event.pos

                elif tool == "eraser":
                    pygame.draw.line(canvas, WHITE, last_pos, event.pos, brush_size)
                    last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                if tool not in ["pencil", "eraser"]:
                    draw_shape(canvas, start_pos, event.pos)

                drawing = False
                start_pos = None
                last_pos = None

    clock.tick(60)

pygame.quit()
# P — карандаш
# L — линия
# R — прямоугольник
# C — круг
# E — ластик
# F — заливка
# T — текст
# S — квадрат
# 4 — прямоугольный треугольник
# 5 — равносторонний треугольник
# 6 — ромб
# 1 / 2 / 3 — размер кисти
# Cmd + S — сохранить картинку PNG